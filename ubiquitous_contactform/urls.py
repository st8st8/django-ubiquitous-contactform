from django.urls import re_path
from ubiquitous_contactform import views as enquiry_views

app_name = "ubiquitous_contactform"
urlpatterns = [
    re_path(r'^contact/?$', enquiry_views.ContactView.as_view(), name='url_contact'),
    re_path(r'^thanks/?$', enquiry_views.ThanksView.as_view(), name='url_thanks'),
]

