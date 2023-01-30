
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail


class EnquiriesTests(TestCase):
    @override_settings(UBIQUITOUS_CONTACT_FORM_CHECK_BLOCKLIST=False)
    @override_settings(UBIQUITOUS_CONTACT_FORM_RECIPIENTS=[("Admin Istrator", "admin@admin.com"),
                                               ("Admin Istrator 2", "admin2@admin.com")])
    def test_enquiry_middleware(self):
            response = self.client.get(reverse("ubiquitous_contact:url_thanks"), {})
            self.assertIsNone(response.context.get("ubiquitous_contact_one_error"))

            response = self.client.post(reverse("ubiquitous_contact:url_thanks"), {})
            self.assertEqual(response.context.get("ubiquitous_contact_one_error"), "'Enquiry': This field is required.")

            data = {"text": "Test Testshaw"}
            response = self.client.post(reverse("ubiquitous_contact:url_thanks"), data)
            self.assertEqual(response.context.get("ubiquitous_contact_one_error"), "'Your name': This field is required.")

            data = {
                "name": "Test Testshaw",
                "text": "Test Testshaw"
            }
            response = self.client.post(reverse("ubiquitous_contact:url_thanks"), data)
            self.assertEqual(response.context.get("ubiquitous_contact_one_error"), "'Email': This field is required.")

            data = {
                "name": "Test Testshaw",
                "email": "test@testshaw.org",
                "text": "Test Testshaw"
            }
            self.assertEqual(len(mail.outbox), 0)
            response = self.client.post(reverse("ubiquitous_contact:url_thanks"), data)
            self.assertIsNone(response.context.get("ubiquitous_contact_one_error"))
            self.assertEqual(len(mail.outbox), 2)
            self.assertEqual(mail.outbox[0].to, ["admin@admin.com"])
            self.assertEqual(mail.outbox[1].to, ["admin2@admin.com"])
