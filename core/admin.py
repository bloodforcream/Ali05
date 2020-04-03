from django.contrib import admin
from core.models import Organization, PhoneNumber, Address, Category, Subcategory, Profile, Tag

admin.site.register(Category)


class AddressInline(admin.StackedInline):
    model = Address


class PhoneNumberInline(admin.StackedInline):
    model = PhoneNumber


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
        PhoneNumberInline,
    ]


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Address)
admin.site.register(PhoneNumber)
admin.site.register(Subcategory)
admin.site.register(Profile)
admin.site.register(Tag)
