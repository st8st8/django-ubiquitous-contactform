# Create your views here.
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import render, redirect
from . import forms, settings


class ContactView(generic.FormView):
    template_name = 'ubiquitous_contactform/contact.html'
    context = dict()
    form_class = forms.EnquiryForm
    context["hide_footer_contact"] = True
    
    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['contact_form'] = context["form"]
        return context
        
    def form_valid(self, form):
        form.send_enquiry(self.request)
        return redirect(settings.UBIQUITOUS_CONTACT_FORM_THANKS_URL)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())


class ThanksView(generic.TemplateView):
    template_name = 'ubiquitous_contactform/thanks.html'
