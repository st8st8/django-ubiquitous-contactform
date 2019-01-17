=================
django-myenquiries
=================

A contact form for Django designed to be placed on every page
of the site.  Includes IP blocklist and honeypot spam prevention.

Installation
============

Install from PyPI with ``easy_install`` or ``pip``::

    pip install django-myenquiries

or get the in-development version:

    pip install http://github.com/st8st8/django-myenquiries


Dependencies
------------

``django-adminfiles`` requires `Django`_ 1.11 or later,


Usage
=====

To use django-adminfiles in your Django project:

    1. Add ``'myenquiries'`` to your ``INSTALLED_APPS`` setting.
    
    2. Add ``'myenquiries.middleware.MyEnquiriesOneErrorMiddleware'`` to your MIDDLEWARE
    
    3. Include the form defined by MYENQUIRIES_CONTEXT_KEY in your templates
    
    4. Optionally add the urls file to your urls.py:
        ``from myenquiries import urls as enquiry_urls``
        ``url(r'^enquiries/', include(enquiry_urls, namespace="myenquiries"))``


Settings
========

MYENQUIRIES_THANKS_URL
--------------------

The URL to be displayed upon successful completion of the contact form

MYENQUIRIES_CONTEXT_KEY
--------------------

The key in the template context in which to find the contact form


MYENQUIRIES_RECIPIENTS
----------------------

A list of names and email addresses, in the same form as the ADMINS
setting.  These are the people who recieve the enquiry


MYENQUIRIES_CHECK_BLOCKLIST
---------------------------

A boolean setting: If set to True, myenquiries will check the 
blocklist.de service to see if the IPaddress sending the enquiry
is known for sending spam messages.
