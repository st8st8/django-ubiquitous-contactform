from __future__ import unicode_literals
import json
import ubiquitous_contactform.models as enq
from . import utils
from django.contrib import admin


def resend_enquiry_emails(modeladmin, request, queryset):
    for x in queryset:
        utils.send_enquiry_emails(x, request=request)


class EnquiryAdmin(admin.ModelAdmin):
    ordering = ('-datemade',)

    fieldsets = [
        (
            'Enquiry',
            {
                'fields':
                    [
                        ('first_name', 'last_name'),
                        ('ip_blocklist', 'ip_blocklist_response'),
                        'text'
                    ]
            }
        ),
        (
            'Information',
            {
                'fields':
                    [
                        'datemade', 'utctime', 'company', ('email', 'tel'), 'frompage', 'user_agent', 'request_meta'
                    ]
            }
        ),
    ]
    list_display = ('__unicode__', 'ip_blocklist', 'utctime', 'email', 'frompage')
    # inlines = [MyInline]
    list_filter = ['ip_blocklist', 'datemade']
    # search_fields = ['']
    # date_hierarchy = 'datemade'
    readonly_fields = ['first_name', 'last_name', 'company', 'text', 'datemade', 'user_agent',
                       'utctime', 'email', 'tel', 'frompage', 'request_meta']
    actions = [resend_enquiry_emails]
                       

    def get_queryset(self, request):
        qs = super(EnquiryAdmin, self).get_queryset(request)
        return qs.order_by('datemade')
    
admin.site.register(enq.Enquiry, EnquiryAdmin)
