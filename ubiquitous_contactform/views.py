# Create your views here.
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from . import forms, settings


def contact(request):
    is_admin = request.user.is_staff
    context = dict()
    context["hide_footer_contact"] = True

    if request.method == 'POST':  # If the form has been submitted...
        form = forms.EnquiryForm(request.POST)

        if form.is_valid():
            form.send_enquiry(request)
            return redirect(settings.UBIQUITOUS_CONTACT_FORM_THANKS_URL)
        else:
            context['contact_form'] = form
    else:
        form = forms.EnquiryForm()  # An unbound form
        context['contact_form'] = form

    return render(request, 'ubiquitous_contact/contact.html', context)


def thanks(request):
    is_admin = request.user.is_staff
    context = dict()
    return render(request, 'ubiquitous_contact/thanks.html', context)
