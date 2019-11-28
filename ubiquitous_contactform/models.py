from __future__ import unicode_literals

import django.utils.timezone as djangotz
from django.db import models


class Enquiry(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First Name(s)', null=True)
    last_name = models.CharField(max_length=255, verbose_name='Last Name', null=True)
    company = models.CharField(max_length=255, verbose_name='Company', blank=True)
    tel = models.CharField(max_length=30, verbose_name='Telephone', blank=True)
    email = models.EmailField(verbose_name='Email', null=True)
    text = models.TextField(verbose_name='Enquiry text', null=True)
    datemade = models.DateTimeField(default=djangotz.now, blank=True, verbose_name='Enquiry Date')
    frompage = models.CharField(max_length=50, verbose_name='Made on page', blank=True)
    request_meta = models.TextField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    ip_blocklist_response = models.TextField(null=True, blank=True)
    ip_blocklist = models.BooleanField(null=False, default=False)
    
    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name).strip()

    def utctime(self):
        return self.datemade

    utctime.short_description ='UTC Date and Time'
    
    class Meta:
        verbose_name_plural = "Enquiries"

    def __unicode__(self):
            return "Enquiry from {0} {1}".format(self.first_name, self.last_name)

    def __str__(self):
            return "Enquiry from {0} {1}".format(self.first_name, self.last_name)



