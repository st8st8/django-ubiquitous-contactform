from __future__ import unicode_literals
import json
import ubiquitous_contactform.models as enq
from django.contrib import admin


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
                       

    def get_queryset(self, request):
        qs = super(EnquiryAdmin, self).get_queryset(request)
        return qs.order_by('datemade')
    
admin.site.register(enq.Enquiry, EnquiryAdmin)
