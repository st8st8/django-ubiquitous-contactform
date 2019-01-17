from __future__ import absolute_import
from __future__ import unicode_literals
from myenquiries import forms as enquiry_forms
from . import settings


def get_form_error(form):
    errors = form.errors
    if len(errors) != 0:
        ekey = errors.keys()[0]
        err = "'{0}': {1}".format(form.fields[ekey].label, errors[ekey].as_text()[2:])
        return err  # the slice strips the star and space off the front
    else:
        return ""


def ubiquitous_contact(request):
    context = dict()
    if request.method == 'POST':
        form = enquiry_forms.EnquiryForm(request.POST)
        if not form.is_valid():
            context['myenquiries_one_error'] = get_form_error(form)
    else:
        form = enquiry_forms.EnquiryForm()

    k = settings.MYENQUIRIES_CONTEXT_KEY
    context[k] = form
    return context
