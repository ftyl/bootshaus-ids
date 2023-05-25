from django.contrib import admin
from .models import Identifikation, Position, ACLTyp, ACL, IDLog
from import_export.admin import ExportActionModelAdmin
from django.utils.html import format_html
from django_admin_relation_links import AdminChangeLinksMixin

admin.site.site_header = "Bootshaus ID Admin"

class DefaultNotEmptyFieldListFilter(admin.EmptyFieldListFilter):
    def __init__(self, *args, **kwargs):
        super(DefaultNotEmptyFieldListFilter, self).__init__(*args, **kwargs)
        # disable All, default to Not Empty!
        if self.lookup_val not in ("0", "1"):
            self.lookup_val = "0"
            self.used_parameters = {'user__isempty', '0'}


class ACLInline(admin.TabularInline):
    model = ACL
    extra = 0

@admin.register(Identifikation)
class IdentifikationAdmin(AdminChangeLinksMixin, ExportActionModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(IdentifikationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "user":
            field.label_from_instance = lambda u: "%s %s (%s)" % (u.first_name, u.last_name, u.username)
        return field

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.short_description = 'ID Karten Halter'
    sortable_str.admin_order_field = 'user__last_name'

    list_filter = (('user', DefaultNotEmptyFieldListFilter),)

    search_fields = ('slug', 'position__name', 'user__last_name', 'user__first_name', 'user__username', 'user__email',)
    list_display = ('sortable_str', 'active', 'user_link', 'position', 'aaa', )
    inlines = [
        ACLInline,
    ]
    fieldsets = (
        (None, {
            'fields': ('user', 'position', 'bild', 'aaa', 'active', 'id_logs')
        }),
        ('Slug Info', {
            'classes': ('collapse',),
            'fields': ('slug', 'id_url')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug','id_url','id_logs')
        else:
            return ('id_url','id_logs')

    change_links = ['user']

    def id_logs(self, obj):
        return format_html('<a href="/admin/ids/idlog/?identifikation__slug={id}">{c} Entries</a>', id=obj.slug, c=obj.idlogs.count())


    def id_url(self, obj):
        return format_html('<a href="https://id.bootshaus.tv/{url}/" target="_blank">https://id.bootshaus.tv/{url}/</a>', url=obj.slug)

@admin.register(IDLog)
class IDLogAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    def sortable_str(self, obj):
        return  obj.identifikation.__str__()

    sortable_str.short_description = "ID Karte"
    sortable_str.admin_order_field = "logged_at"

    list_display = ['sortable_str', "logged_at", "match_success", "matched_type", "matched_acl"]

    readonly_fields = ('identifikation', 'logged_at', 'match_success', 'matched_type', 'matched_acl')

admin.site.register(Position)
admin.site.register(ACLTyp)
#admin.site.register(ACL)

