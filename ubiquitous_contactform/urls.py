from __future__ import unicode_literals
from django.conf.urls import url
from ubiquitous_contactform import views as enquiry_views

urlpatterns = [
    url(r'^contact/?$', enquiry_views.contact, name='url_contact'),
    url(r'^thanks/?$', enquiry_views.thanks, name='url_thanks'),
]

