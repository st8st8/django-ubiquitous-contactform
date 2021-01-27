import logging
from . import settings
from django.conf import settings as django_settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.sites.models import Site


def send_enquiry_emails(enquiry, request=None):
    site = Site.objects.get_current(request)
    for a in settings.UBIQUITOUS_CONTACT_FORM_RECIPIENTS:
        context = {}
        context["e"] = enquiry
        context["site"] = site
        html_message, text_message = ubiquitous_contact_get_html_email_template(
            "myenquiry",
            a[1],
            context
        )
        ubiquitous_contact_send_mail(
            "Enquiry on {0}".format(site.name),
            text_message,
            django_settings.SERVER_EMAIL,
            a[1],
            html_message=html_message,
            reply_to=[enquiry.email]
        )
    if settings.UBIQUITOUS_CONTACT_FORM_SEND_RECEIPT:
        context = {}
        context["e"] = enquiry
        context["site"] = site
        html_message, text_message = ubiquitous_contact_get_html_email_template(
            "receipt",
            enquiry.email,
            context
        )
        ubiquitous_contact_send_mail(
            settings.UBIQUITOUS_CONTACT_FORM_RECEIPT_SUBJECT,
            text_message,
            django_settings.SERVER_EMAIL,
            enquiry.email,
            html_message=html_message
        )


def email_default_context(recipient, target_user=None):
    return {}


def ubiquitous_contact_get_html_email_template(template_name, recipient, context, target_user=None):
    context.update(email_default_context(recipient, target_user=target_user))
    html_ret = None
    text_ret = None
    try:
        html_template = get_template("ubiquitous_contactform/emails/html/{0}.html".format(template_name))
        html_ret = html_template.render(context)
    except TemplateDoesNotExist:
        pass

    try:
        text_template = get_template("ubiquitous_contactform/emails/text/{0}.txt".format(template_name))
        text_ret = text_template.render(context)
    except TemplateDoesNotExist:
        pass

    return html_ret, text_ret


def ubiquitous_contact_send_mail(subject, message, from_email, recipient_list,
                            fail_silently=False, auth_user=None, auth_password=None, reply_to=None,
                            connection=None, headers=None, attachments=None, html_message=None, test_mode=False):
    if isinstance(recipient_list, str):
        recipient_list = [recipient_list]

    islive = django_settings.DEBUG is False
    if islive and test_mode:
        islive = False

    connection = connection or get_connection(username=auth_user,
                                              password=auth_password,
                                              fail_silently=fail_silently)
    if not islive:
        msg = EmailMultiAlternatives(subject="Ubiquitous Contact Form Test: " + "{0}".format(subject),
                                     body="To: " + ", ".join(recipient_list) + "\n\n--\n{0}\n".format(message),
                                     from_email=from_email,
                                     to=[settings.UBIQUITOUS_CONTACT_FORM_STAGING_EMAIL_ADDRESS],
                                     headers=headers,
                                     attachments=attachments,
                                     connection=connection,
                                     reply_to=reply_to)
        if html_message:
            html_message = "<h3>To: " + ", ".join(recipient_list) + "</h3>" + html_message
            msg.attach_alternative(html_message, "text/html")
        msg.send()
    else:
        logging.getLogger().info("Sending mail to %s" % str(recipient_list))
        msg = EmailMultiAlternatives(subject,
                                     body=message,
                                     from_email=from_email,
                                     to=recipient_list,
                                     headers=headers,
                                     attachments=attachments,
                                     connection=connection,
                                     reply_to=reply_to)

        if html_message:
            msg.attach_alternative(html_message, "text/html")
        msg.send()
