=================
django-ubiquitous_contactform
=================

A contact form for Django designed to be placed on every page
of the site.  Includes IP blocklist and honeypot spam prevention.

Installation
============

Install from PyPI with ``easy_install`` or ``pip``::

    pip3 install django-ubiquitous-contactform

or get the in-development version:

    pip3 install http://github.com/st8st8/django-ubiquitous-contactform


Dependencies
------------

``django-adminfiles`` requires `Django`_ 2.0 or later,


Usage
=====

To use django-adminfiles in your Django project:

    1. Add ``'ubiquitous_contactform'`` to your ``INSTALLED_APPS`` setting.
    
    2. Add ``'ubiquitous_contactform.middleware.UbiquitousContactOneErrorMiddleware'`` to your MIDDLEWARE
    
    3. Include the form defined by UBIQUITOUS_CONTACT_FORM_CONTEXT_KEY in your templates
    
    4. Optionally add the urls file to your urls.py:
        ``from ubiquitous_contactform import urls as enquiry_urls``
        ``url(r'^enquiries/', include(enquiry_urls, namespace="ubiquitous_contactform"))``


Settings
========

UBIQUITOUS_CONTACT_FORM_THANKS_URL
--------------------

The URL to be displayed upon successful completion of the contact form

UBIQUITOUS_CONTACT_FORM_CONTEXT_KEY
--------------------

The key in the template context in which to find the contact form

UBIQUITOUS_CONTACT_FORM_STAGING_EMAIL_ADDRESS
-------------------
The email address to send test emails to. 

UBIQUITOUS_CONTACT_FORM_RECIPIENTS
----------------------

A list of names and email addresses, in the same form as the ADMINS
setting.  These are the people who recieve the enquiry


UBIQUITOUS_CONTACT_FORM_CHECK_BLOCKLIST
---------------------------

A boolean setting: If set to True, ubiquitous_contactform will check the 
blocklist.de service to see if the IPaddress sending the enquiry
is known for sending spam messages.
