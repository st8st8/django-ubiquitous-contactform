# Create your views here.
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import render, redirect
from . import forms, settings


class ContactView(generic.FormView):
    template_name = 'ubiquitous_contactform/contact.html'
    context = dict()
    context["hide_footer_contact"] = True
    
    def get_context_data(self, **kwargs):
        context = dict()
        form = forms.EnquiryForm(self.request.POST)  # An unbound form
        context['contact_form'] = form
        return context
        
    def post(self, request, *args, **kwargs):
        form = forms.EnquiryForm(self.request.POST)

        if form.is_valid():
            form.send_enquiry(self.request)
            return redirect(settings.UBIQUITOUS_CONTACT_FORM_THANKS_URL)


class ThanksView(generic.TemplateView):
    template_name = 'ubiquitous_contactform/thanks.html'
