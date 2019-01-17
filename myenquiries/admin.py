from __future__ import unicode_literals
import json
import myenquiries.models as enq
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
                        ('sent_to_salesforce'),
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
                        'datemade', 'utctime', 'company', ('email', 'tel'), 'frompage', 'user_agent', 'format_request_meta'
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
                       'utctime', 'email', 'tel', 'frompage', 'format_request_meta']

    def format_request_meta(self, instance):
        ret = u"<table>\n"
        meta = json.loads(instance.request_meta)
        for x in sorted(meta.keys()):
            ret += u"<tr><td>{0}</td><td>{1}</td></tr>".format(x, meta[x])
        ret += u"</table>"
        return ret

    format_request_meta.allow_tags = True

    def get_queryset(self, request):
        qs = super(EnquiryAdmin, self).get_queryset(request)
        return qs.order_by('datemade')
    
admin.site.register(enq.Enquiry, EnquiryAdmin)