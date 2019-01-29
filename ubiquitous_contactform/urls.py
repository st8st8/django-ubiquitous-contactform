from __future__ import unicode_literals
from django.conf.urls import url
from ubiquitous_contactform import views as enquiry_views

app_name = "ubiquitous_contactform"
urlpatterns = [
    url(r'^contact/?$', enquiry_views.ContactView.as_view(), name='url_contact'),
    url(r'^thanks/?$', enquiry_views.ThanksView.as_view(), name='url_thanks'),
]

