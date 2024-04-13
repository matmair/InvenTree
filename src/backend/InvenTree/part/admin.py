"""Admin class definitions for the 'part' app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from part import models


class PartParameterInline(admin.TabularInline):
    """Inline for part parameter data."""

    model = models.PartParameter


class PartAdmin(admin.ModelAdmin):
    """Admin class for the Part model."""

    list_display = ('full_name', 'description', 'total_stock', 'category')

    list_filter = ('active', 'assembly', 'is_template', 'virtual')

    search_fields = (
        'name',
        'description',
        'category__name',
        'category__description',
        'IPN',
    )

    autocomplete_fields = [
        'variant_of',
        'category',
        'default_location',
        'default_supplier',
    ]

    inlines = [PartParameterInline]


class PartPricingAdmin(admin.ModelAdmin):
    """Admin class for PartPricing model."""

    list_display = ('part', 'overall_min', 'overall_max')

    autcomplete_fields = ['part']


class PartStocktakeAdmin(admin.ModelAdmin):
    """Admin class for PartStocktake model."""

    list_display = ['part', 'date', 'quantity', 'user']


class PartStocktakeReportAdmin(admin.ModelAdmin):
    """Admin class for PartStocktakeReport model."""

    list_display = ['date', 'user']


class PartCategoryAdmin(admin.ModelAdmin):
    """Admin class for the PartCategory model."""

    list_display = ('name', 'pathstring', 'description')

    search_fields = ('name', 'description')

    autocomplete_fields = ('parent', 'default_location')


class PartRelatedAdmin(admin.ModelAdmin):
    """Class to manage PartRelated objects."""

    autocomplete_fields = ('part_1', 'part_2')


class PartAttachmentAdmin(admin.ModelAdmin):
    """Admin class for the PartAttachment model."""

    list_display = ('part', 'attachment', 'comment')

    autocomplete_fields = ('part',)


class PartTestTemplateAdmin(admin.ModelAdmin):
    """Admin class for the PartTestTemplate model."""

    list_display = ('part', 'test_name', 'required')
    readonly_fields = ['key']

    autocomplete_fields = ('part',)


class BomItemAdmin(admin.ModelAdmin):
    """Admin class for the BomItem model."""

    list_display = ('part', 'sub_part', 'quantity')

    search_fields = (
        'part__name',
        'part__description',
        'sub_part__name',
        'sub_part__description',
    )

    autocomplete_fields = ('part', 'sub_part')


class ParameterTemplateAdmin(admin.ModelAdmin):
    """Admin class for the PartParameterTemplate model."""

    list_display = ('name', 'units')

    search_fields = ('name', 'units')


class ParameterAdmin(admin.ModelAdmin):
    """Admin class for the PartParameter model."""

    list_display = ('part', 'template', 'data')

    autocomplete_fields = ('part', 'template')


class PartCategoryParameterAdmin(admin.ModelAdmin):
    """Admin class for the PartCategoryParameterTemplate model."""

    autocomplete_fields = ('category', 'parameter_template')


class PartSellPriceBreakAdmin(admin.ModelAdmin):
    """Admin class for the PartSellPriceBreak model."""

    class Meta:
        """Metaclass options."""

        model = models.PartSellPriceBreak

    list_display = ('part', 'quantity', 'price')


class PartInternalPriceBreakAdmin(admin.ModelAdmin):
    """Admin class for the PartInternalPriceBreak model."""

    class Meta:
        """Metaclass options."""

        model = models.PartInternalPriceBreak

    list_display = ('part', 'quantity', 'price')

    autocomplete_fields = ('part',)


admin.site.register(models.Part, PartAdmin)
admin.site.register(models.PartCategory, PartCategoryAdmin)
admin.site.register(models.PartRelated, PartRelatedAdmin)
admin.site.register(models.PartAttachment, PartAttachmentAdmin)
admin.site.register(models.BomItem, BomItemAdmin)
admin.site.register(models.PartParameterTemplate, ParameterTemplateAdmin)
admin.site.register(models.PartParameter, ParameterAdmin)
admin.site.register(models.PartCategoryParameterTemplate, PartCategoryParameterAdmin)
admin.site.register(models.PartTestTemplate, PartTestTemplateAdmin)
admin.site.register(models.PartSellPriceBreak, PartSellPriceBreakAdmin)
admin.site.register(models.PartInternalPriceBreak, PartInternalPriceBreakAdmin)
admin.site.register(models.PartPricing, PartPricingAdmin)
admin.site.register(models.PartStocktake, PartStocktakeAdmin)
admin.site.register(models.PartStocktakeReport, PartStocktakeReportAdmin)
