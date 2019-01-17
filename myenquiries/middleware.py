from __future__ import absolute_import
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from myenquiries import forms as enquiry_forms
from myenquiries import settings


class MyEnquiriesOneErrorMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            form = enquiry_forms.EnquiryForm(request.POST)
            if form.is_valid():
                form.send_enquiry(request)
                return redirect(settings.MYENQUIRIES_THANKS_URL)

        response = self.get_response(request)
        return response
