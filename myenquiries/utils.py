import logging

import six
from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import get_template


def email_default_context(recipoient, target_user=None):
    return {}


def myenquiries_get_html_email_template(template_name, recipient, context, target_user=None):
    context.update(email_default_context(recipient, target_user=target_user))
    html_ret = None
    text_ret = None
    try:
        html_template = get_template("myenquiries/emails/html/{0}.html".format(template_name))
        html_ret = html_template.render(context)
    except TemplateDoesNotExist:
        pass

    try:
        text_template = get_template("myenquiries/emails/text/{0}.txt".format(template_name))
        text_ret = text_template.render(context)
    except TemplateDoesNotExist:
        pass

    return html_ret, text_ret


def myenquiries_send_mail(subject, message, from_email, recipient_list,
                            fail_silently=False, auth_user=None, auth_password=None,
                            connection=None, headers=None, attachments=None, html_message=None, test_mode=False):
    if isinstance(recipient_list, six.string_types):
        recipient_list = [recipient_list]

    islive = settings.DEBUG is False
    if islive and test_mode:
        islive = False

    connection = connection or get_connection(username=auth_user,
                                              password=auth_password,
                                              fail_silently=fail_silently)
    if not islive:
        msg = EmailMultiAlternatives(subject="MyEnq Test: " + "{0}".format(subject),
                                     body="To: " + ", ".join(recipient_list) + "\n\n--\n" + unicode(message),
                                     from_email=from_email,
                                     to=[settings.STAGING_EMAIL_ADDRESS],
                                     headers=headers,
                                     attachments=attachments,
                                     connection=connection)
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
                                     connection=connection)

        if html_message:
            msg.attach_alternative(html_message, "text/html")
        msg.send()