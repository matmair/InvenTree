"""Admin functionality for the 'order' app."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from order import models


# region general classes
class ExtraLineAdmin(admin.ModelAdmin):
    """Admin class template for the 'ExtraLineItem' models."""

    list_display = ('order', 'quantity', 'reference')

    search_fields = ['order__reference', 'order__customer__name', 'reference']

    autocomplete_fields = ('order',)


# endregion


class PurchaseOrderLineItemInlineAdmin(admin.StackedInline):
    """Inline admin class for the PurchaseOrderLineItem model."""

    model = models.PurchaseOrderLineItem
    extra = 0


class PurchaseOrderAdmin(admin.ModelAdmin):
    """Admin class for the PurchaseOrder model."""

    exclude = ['reference_int']

    list_display = ('reference', 'supplier', 'status', 'description', 'creation_date')

    search_fields = ['reference', 'supplier__name', 'description']

    inlines = [PurchaseOrderLineItemInlineAdmin]

    autocomplete_fields = ('supplier',)


class SalesOrderAdmin(admin.ModelAdmin):
    """Admin class for the SalesOrder model."""

    exclude = ['reference_int']

    list_display = ('reference', 'customer', 'status', 'description', 'creation_date')

    search_fields = ['reference', 'customer__name', 'description']

    autocomplete_fields = ('customer',)


class PurchaseOrderLineItemAdmin(admin.ModelAdmin):
    """Admin class for the PurchaseOrderLine model."""

    list_display = ('order', 'part', 'quantity', 'reference')

    search_fields = ('reference',)

    autocomplete_fields = ('order', 'part', 'destination')


class SalesOrderLineItemAdmin(admin.ModelAdmin):
    """Admin class for the SalesOrderLine model."""

    list_display = ('order', 'part', 'quantity', 'reference')

    search_fields = [
        'part__name',
        'order__reference',
        'order__customer__name',
        'reference',
    ]

    autocomplete_fields = ('order', 'part')


class SalesOrderShipmentAdmin(admin.ModelAdmin):
    """Admin class for the SalesOrderShipment model."""

    list_display = ['order', 'shipment_date', 'reference']

    search_fields = ['reference', 'order__reference', 'order__customer__name']

    autocomplete_fields = ('order',)


class SalesOrderAllocationAdmin(admin.ModelAdmin):
    """Admin class for the SalesOrderAllocation model."""

    list_display = ('line', 'item', 'quantity')

    autocomplete_fields = ('line', 'shipment', 'item')


class ReturnOrderAdmin(admin.ModelAdmin):
    """Admin class for the ReturnOrder model."""

    exclude = ['reference_int']

    list_display = ['reference', 'customer', 'status']

    search_fields = ['reference', 'customer__name', 'description']

    autocomplete_fields = ['customer']


class ReturnOrderLineItemAdmin(admin.ModelAdmin):
    """Admin class for ReturnOrderLine model."""

    list_display = ['order', 'item', 'reference']


# Purchase Order models
admin.site.register(models.PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(models.PurchaseOrderLineItem, PurchaseOrderLineItemAdmin)
admin.site.register(models.PurchaseOrderExtraLine, ExtraLineAdmin)

# Sales Order models
admin.site.register(models.SalesOrder, SalesOrderAdmin)
admin.site.register(models.SalesOrderLineItem, SalesOrderLineItemAdmin)
admin.site.register(models.SalesOrderExtraLine, ExtraLineAdmin)
admin.site.register(models.SalesOrderShipment, SalesOrderShipmentAdmin)
admin.site.register(models.SalesOrderAllocation, SalesOrderAllocationAdmin)

# Return Order models
admin.site.register(models.ReturnOrder, ReturnOrderAdmin)
admin.site.register(models.ReturnOrderLineItem, ReturnOrderLineItemAdmin)
admin.site.register(models.ReturnOrderExtraLine, ExtraLineAdmin)
