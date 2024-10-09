from django import forms
from django.contrib import admin
from .models import Property, PropertyImage

# Custom Widget for Horizontal RadioSelect (if you still want to use it for specific fields)
class HorizontalRadioSelect(forms.RadioSelect):
    template_name = 'admin/horizontal_select.html'

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
        ('Informações do Proprietário', {
            'fields': ('owner_name', 'phone_number', 'email'),
        }),
        ('Endereço do Imóvel', {
            'fields': ('street', 'street_number', 'zip_code', 'neighborhood', 'city', 'state'),
        }),
        ('Informações do Imóvel', {
            'fields': ('property_type', 'property_area', 'bedrooms', 'suites', 'bathrooms'),
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

    # Override the default form field widgets for better customization
    formfield_overrides = {
        Property._meta.get_field('garage_type'): {'widget': forms.Select(choices=[
            ('covered', 'Coberta'),
            ('free', 'Livre'),
            ('covered_and_free', 'Coberta e Livre'),
            ('none', 'Nem Coberta nem Livre')
        ])},
        Property._meta.get_field('has_pool'): {'widget': forms.Select(choices=[('yes', 'Sim'), ('no', 'Não')])},
        Property._meta.get_field('has_gatehouse'): {'widget': forms.Select(choices=[
            ('24h', '24 h'), 
            ('daytime', 'Diurna'), 
            ('night', 'Noturna'), 
            ('none', 'Sem portaria')
        ])},
        Property._meta.get_field('is_occupied'): {'widget': forms.Select(choices=[
            ('vacant', 'Está vago'), 
            ('owner', 'Proprietário mora'), 
            ('tenant', 'Inquilino mora')
        ])},
        Property._meta.get_field('accessibility'): {'widget': forms.Select(choices=[('yes', 'Sim'), ('no', 'Não')])}
    }

# Register the Property model with the custom PropertyAdmin
admin.site.register(Property, PropertyAdmin)

# Register the PropertyImage model if needed in admin panel
admin.site.register(PropertyImage)
