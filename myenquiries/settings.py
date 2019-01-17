from __future__ import unicode_literals
from django.conf import settings

MYENQUIRIES_RECIPIENTS = getattr(settings, "MYENQUIRIES_RECIPIENTS", [])
MYENQUIRIES_CHECK_BLOCKLIST = getattr(settings, "MYENQUIRIES_CHECK_BLOCKLIST", False)
MYENQUIRIES_CONTEXT_KEY = getattr(settings, "MYENQUIRIES_CONTEXT_KEY", "footer_contact_form")