from __future__ import unicode_literals

import copy
import json

import requests
import six
from django import forms
from django.forms import widgets
from django.utils import timezone

from ubiquitous_contactform import utils
from . import models, validators, settings
from django.conf import settings as django_settings


class StyledErrorForm(forms.Form):
    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            if not f in self.fields:
                continue
            if 'class' in self.fields[f].widget.attrs:
                self.fields[f].widget.attrs['class'] += ' error'
            else:
                self.fields[f].widget.attrs.update({'class': 'error'})

        return ret


class EnquiryForm(StyledErrorForm):
    name = forms.CharField(
        max_length=255, required=True,
        label="Your name",
        widget=widgets.TextInput(attrs={"placeholder": "your name"})
        )
    company = forms.CharField(
        max_length=255, required=False,
        label="Company",
        widget=widgets.TextInput(attrs={"placeholder": "company"})
    )
    tel = forms.CharField(
        max_length=30, required=False,
        label="Phone number",
        widget=widgets.TextInput(attrs={"placeholder": "phone"})
    )
    confirm_email = forms.URLField(
        max_length=30, required=False,
        label="Confirm email",
        widget=widgets.EmailInput(attrs={"id": "id_email", "name": "email", "placeholder": "email"}),
        validators=[validators.validate_empty],
        help_text="This is a honeypot, and shouldn't be filled in by humans"
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=widgets.EmailInput(attrs={"id": "id_url", "name": "url", "placeholder": "email"}))
    text = forms.CharField(
        required=True,
        label="Enquiry",
        widget=widgets.Textarea(attrs={"id": "id_beans", "name": "beans", "placeholder": "enquiry:"})
    )

    def send_enquiry(self, request):
        enquiry = models.Enquiry()
        names = self.cleaned_data['name'].rsplit(' ', 1)
        enquiry.first_name = names[0]
        if len(names) > 1:
            enquiry.last_name = names[1]
        else:
            enquiry.last_name = ""  # this stops it becoming 'None'
        enquiry.tel = self.cleaned_data['tel']
        enquiry.email = self.cleaned_data['email']
        enquiry.company = self.cleaned_data['company']
        enquiry.text = self.cleaned_data['text']
        enquiry.datemade = timezone.now()
        enquiry.frompage = request.path
        enquiry.user_agent = request.META.get("HTTP_USER_AGENT")
        meta = copy.copy(request.META)

        for x in meta.keys():
            if not isinstance(meta[x], six.string_types):
                del meta[x]

        enquiry.request_meta = json.dumps(meta)
        blocklist = "http://api.blocklist.de/api.php?ip={0}"
        self.is_blocklist(request, enquiry)
        if not enquiry.ip_blocklist:
            for a in settings.UBIQUITOUS_CONTACT_FORM_RECIPIENTS:
                context = {}
                context["e"] = self.cleaned_data
                html_message, text_message = utils.ubiquitous_contact_get_html_email_template(
                    "myenquiry",
                    a[1],
                    context
                )
                utils.ubiquitous_contact_send_mail(
                    "Coracle Inside enquiry",
                    text_message,
                    django_settings.SERVER_EMAIL,
                    a[1],
                    html_message=html_message
                )
        enquiry.save()
        return enquiry

    @staticmethod
    def is_blocklist(request, enquiry):
        if settings.UBIQUITOUS_CONTACT_FORM_CHECK_BLOCKLIST is True:
            if request.META.get("REMOTE_ADDR"):
                ip = request.META.get("REMOTE_ADDR")
                resp = requests.get("http://api.blocklist.de/api.php?ip={0}".format(ip))
                enquiry.ip_blocklist_response = resp.content
                if "attacks: " in resp.content:
                    if "attacks: 0" in resp.content:
                        enquiry.ip_blocklist = False
                    else:
                        enquiry.ip_blocklist = True