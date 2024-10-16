from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Property, PropertyImage, Bid, Deal, PropertyOwner

# Customizing how PropertyOwner is displayed in the admin panel
class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'phone_number', 'is_married')

    # Make the full name and email read-only, but display them in the form
    readonly_fields = ('get_full_name', 'get_email')

    # Organize the fields displayed in the form
    fieldsets = (
        (None, {
            'fields': ('user', 'phone_number', 'is_married'),
        }),
        ('Informações do Usuário', {
            'fields': ('get_full_name', 'get_email'),
        }),
    )

    # Display full name from the User model
    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else "-"
    get_full_name.short_description = 'Nome completo'

    # Display email from the User model
    def get_email(self, obj):
        return obj.user.email if obj.user else "-"
    get_email.short_description = 'Email'

    # Optional validation to ensure User has first name, last name, and email
    def save_model(self, request, obj, form, change):
        if not obj.user.first_name or not obj.user.last_name or not obj.user.email:
            raise ValidationError("O usuário deve ter nome completo e email preenchidos antes de salvar um proprietário.")
        super().save_model(request, obj, form, change)

admin.site.register(PropertyOwner, PropertyOwnerAdmin)

# Inline for adding images related to a Property
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Allows adding one or more images

# Admin customization for Property model
class PropertyAdmin(admin.ModelAdmin):
    # Include the PropertyImage inline
    inlines = [PropertyImageInline]

    # Group fields into sections to make the admin more organized
    fieldsets = (
        ('Endereço do Imóvel', {
            'fields': ('street', 'street_number', 'zip_code', 'neighborhood', 'city', 'state'),
        }),
        ('Informações do Imóvel', {
            'fields': ('property_type', 'property_area', 'bedrooms', 'suites', 'bathrooms'),
        }),
        ('Proprietários', {
            'fields': ('owner',),  # Add the Many-to-Many field here to allow owner selection
        }),
        ('Características do Imóvel', {
            'fields': ('features', 'is_covered', 'private_area'),
        }),
        ('Vagas de Garagem e Portaria', {
            'fields': ('garage_spots', 'garage_type', 'has_pool', 'has_gatehouse'),
        }),
        ('Condição do Imóvel e Acessibilidade', {
            'fields': ('is_occupied', 'access', 'accessibility'),
        }),
        ('Disponibilidade e Valores', {
            'fields': ('move_availability', 'rent_price', 'sale_price', 'iptu_value', 'condo_fee'),
        }),
        ('Descrição Livre', {
            'fields': ('free_description',),
        }),
        ('Vídeo do Imóvel', {
            'fields': ('video_url',),
        }),
    )

    # Custom method to display related owner
    def get_owner(self, obj):
        return ", ".join([owner.user.get_full_name() for owner in obj.owner.all()])
    get_owner.short_description = 'Proprietários'

    # Display fields in the admin list view
    list_display = ('street', 'city', 'state', 'property_type', 'get_owner')

    # Add search functionality for address, city, and owner name
    search_fields = ('street', 'city', 'state', 'owner__user__first_name', 'owner__user__last_name')

    # Filters for property type and city
    list_filter = ('property_type', 'city', 'state')

# Register the Property model with the custom PropertyAdmin
admin.site.register(Property, PropertyAdmin)

# Register the PropertyImage model if needed in admin panel
admin.site.register(PropertyImage)

# Admin configuration for the Bid model
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'amount', 'status', 'date')

    # Add custom CSS classes to rows based on bid status
    def get_row_css(self, obj):
        return f"row-status-{obj.status}"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        response = super().changelist_view(request, extra_context=extra_context)
        for obj in response.context_data['cl'].result_list:
            obj.row_class = self.get_row_css(obj)
        return response

# Register the Deal model in the admin panel
admin.site.register(Deal)
