from django.contrib import admin
from .models import Identifikation, Position, ACLTyp, ACL

class DefaultNotEmptyFieldListFilter(admin.EmptyFieldListFilter):
    def __init__(self, *args, **kwargs):
        super(DefaultNotEmptyFieldListFilter, self).__init__(*args, **kwargs)
        # disable All, default to Not Empty!
        if self.lookup_val not in ("0", "1"):
            self.lookup_val = "0"
            self.used_parameters = {'user__isempty', '0'}


class ACLInline(admin.TabularInline):
    model = ACL
    extra = 1

@admin.register(Identifikation)
class IdentifikationAdmin(admin.ModelAdmin):
    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.short_description = 'ID Karte Eigentümer'
    sortable_str.admin_order_field = 'user__last_name'

    list_filter = (('user', DefaultNotEmptyFieldListFilter),)

    search_fields = ('slug',)
    list_display = ('sortable_str', 'position', )
    inlines = [
        ACLInline,
    ]
    fieldsets = (
        (None, {
            'fields': ('user', 'position', 'bild')
        }),
        ('Slug Info', {
            'classes': ('collapse',),
            'fields': ('slug', 'id_url')
        }),
    )
    readonly_fields = ('slug','id_url')

    def id_url(self, obj):
        return 'https://id.bootshaus.tv/%s' % (obj.slug)

admin.site.register(Position)
admin.site.register(ACLTyp)
#admin.site.register(ACL)
