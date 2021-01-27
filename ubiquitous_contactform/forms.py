from __future__ import unicode_literals

import copy
import json

import requests
import six
from django import forms
from django.forms import widgets
from django.utils import timezone

from django.contrib.sites.models import Site
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


class AbstractEnquiryForm(StyledErrorForm):
    def form_to_model(self, request):
        raise NotImplementedError

    def send_enquiry(self, request):
        enquiry = self.form_to_model(request)
        self.is_blocklist(request, enquiry)
        enquiry.save()
        if not enquiry.ip_blocklist:
            utils.send_enquiry_emails(enquiry, request=request)
                
        return enquiry

    @staticmethod
    def is_blocklist(request, enquiry):
        if settings.UBIQUITOUS_CONTACT_FORM_CHECK_BLOCKLIST is True:
            if request.META.get("REMOTE_ADDR"):
                ip = request.META.get("REMOTE_ADDR")
                resp = requests.get("http://api.blocklist.de/api.php?ip={0}".format(ip))
                enquiry.ip_blocklist_response = resp.content
                if "attacks: " in resp.text:
                    if "attacks: 0" in resp.text:
                        enquiry.ip_blocklist = False
                    else:
                        enquiry.ip_blocklist = True


class EnquiryForm(AbstractEnquiryForm):
    action = forms.CharField(
        max_length="31",
        widget=forms.HiddenInput(),
        initial="ubiquitous_contact_submit")
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
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=widgets.EmailInput(attrs={"id": "id_email", "placeholder": "email"}))
    confirm_email = forms.EmailField(
        max_length=30, required=False,
        label="Confirm email",
        widget=widgets.EmailInput(attrs={"id": "id_confirm_email", "placeholder": "email"}),
        validators=[validators.validate_empty],
        help_text="This is a honeypot, and shouldn't be filled in by humans"
    )
    text = forms.CharField(
        required=True,
        label="Enquiry",
        widget=widgets.Textarea(attrs={"id": "id_enquiry", "placeholder": "enquiry:"})
    )
    
    def form_to_model(self, request):
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
        post = "\n".join(["{0} = {1}".format(x, request.POST[x]) for x in request.POST.keys()])
        enquiry.request_meta = post
        
        return enquiry


class HeavyHoneypotEnquiryForm(AbstractEnquiryForm):
    action = forms.CharField(
        max_length="31",
        widget=forms.HiddenInput(),
        initial="ubiquitous_contact_submit")
    xelpud = forms.CharField(
        max_length=255, required=True,
        label="Your name",
        widget=widgets.TextInput(attrs={"placeholder": "your name"})
        )
    shorn = forms.CharField(
        max_length=255, required=False,
        label="Company",
        widget=widgets.TextInput(attrs={"placeholder": "company"})
    )
    lumisa = forms.CharField(
        max_length=30, required=False,
        label="Phone number",
        widget=widgets.TextInput(attrs={"placeholder": "phone"})
    )
    lemeza = forms.EmailField(
        required=True,
        label="Email",
        widget=widgets.EmailInput(attrs={"id": "id_lemeza", "placeholder": "email"}))
    email = forms.EmailField(
        max_length=30, required=False,
        label="Email",
        widget=widgets.EmailInput(attrs={"id": "id_email", "placeholder": "email"}),
        validators=[validators.validate_empty],
        help_text="This is a honeypot, and shouldn't be filled in by humans"
    )
    mulbruk = forms.CharField(
        required=True,
        label="Enquiry",
        widget=widgets.Textarea(attrs={"id": "id_enquiry", "placeholder": "enquiry:"})
    )
    
    def form_to_model(self, request):
        enquiry = models.Enquiry()
        names = self.cleaned_data['xelpud'].rsplit(' ', 1)
        enquiry.first_name = names[0]
        if len(names) > 1:
            enquiry.last_name = names[1]
        else:
            enquiry.last_name = ""  # this stops it becoming 'None'
        enquiry.tel = self.cleaned_data['lumisa']
        enquiry.email = self.cleaned_data['lemeza']
        enquiry.company = self.cleaned_data['shorn']
        enquiry.text = self.cleaned_data['mulbruk']
        enquiry.datemade = timezone.now()
        enquiry.frompage = request.path
        enquiry.user_agent = request.META.get("HTTP_USER_AGENT")
        post = "\n".join(["{0} = {1}".format(x, request.POST[x]) for x in request.POST.keys()])
        enquiry.request_meta = post
        
        return enquiry
