from __future__ import unicode_literals
from django.conf import settings

MYENQUIRIES_RECIPIENTS = getattr(settings, "MYENQUIRIES_RECIPIENTS", [])
MYENQUIRIES_STAGING_EMAIL_ADDRESS = getattr(settings, "MYENQUIRIES_STAGING_EMAIL_ADDRESS", [])    
MYENQUIRIES_CHECK_BLOCKLIST = getattr(settings, "MYENQUIRIES_CHECK_BLOCKLIST", False)
MYENQUIRIES_CONTEXT_KEY = getattr(settings, "MYENQUIRIES_CONTEXT_KEY", "footer_contact_form")
MYENQUIRIES_THANKS_URL = getattr(settings, "MYENQUIRIES_THANKS_URL", "/myenquiries/thanks")
