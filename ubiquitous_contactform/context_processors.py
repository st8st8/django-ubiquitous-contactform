from __future__ import absolute_import
from __future__ import unicode_literals
from ubiquitous_contactform import forms as enquiry_forms
from . import settings


def get_form_error(form):
    errors = form.errors
    if len(errors) != 0:
        ekey = next(iter(errors.keys()))
        err = "'{0}': {1}".format(form.fields[ekey].label, errors[ekey].as_text()[2:])
        return err  # the slice strips the star and space off the front
    else:
        return ""


def ubiquitous_contact(request):
    context = dict()
    if request.method == 'POST' and request.POST.get("action") == "ubiquitous_contact_submit":
        form = enquiry_forms.EnquiryForm(request.POST)
        if not form.is_valid():
            context['ubiquitous_contact_one_error'] = get_form_error(form)
    else:
        form = enquiry_forms.EnquiryForm()

    k = settings.UBIQUITOUS_CONTACT_FORM_CONTEXT_KEY
    context[k] = form
    return context
