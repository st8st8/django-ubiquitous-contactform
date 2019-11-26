from __future__ import absolute_import
from __future__ import unicode_literals

from django.urls import reverse
from django.shortcuts import redirect
from ubiquitous_contactform import forms as enquiry_forms
from ubiquitous_contactform import settings


class UbiquitousContactFormOneErrorMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.POST.get("action") == "ubiquitous_contact_submit":
            form = enquiry_forms.EnquiryForm(request.POST)
            if form.is_valid():
                form.send_enquiry(request)
                return redirect(settings.UBIQUITOUS_CONTACT_FORM_THANKS_URL)

        response = self.get_response(request)
        return response


class UbiquitousContactFormHoneypotOneErrorMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.POST.get("action") == "ubiquitous_contact_submit":
            form = enquiry_forms.HeavyHoneypotEnquiryForm(request.POST)
            if form.is_valid():
                form.send_enquiry(request)
                return redirect(settings.UBIQUITOUS_CONTACT_FORM_THANKS_URL)

        response = self.get_response(request)
        return response
