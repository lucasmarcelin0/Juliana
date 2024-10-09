# views.py
from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from .models import Property, PropertyImage
from django.contrib.auth.decorators import login_required




# View index que mostra todos os imóveis
@login_required
def index(request):
    imos = Property.objects.prefetch_related('images').all()
    return render(request, 'sales/index.html', {'imos': imos})


def filter_properties(request):
    # Extract filter parameters from the GET request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    location = request.GET.get('location')
    property_type = request.GET.get('property_type')
    property_area_min = request.GET.get('property_area_min')
    property_area_max = request.GET.get('property_area_max')
    private_area_min = request.GET.get('private_area_min')
    private_area_max = request.GET.get('private_area_max')
    bedrooms = request.GET.get('bedrooms')
    suites = request.GET.get('suites')
    bathrooms = request.GET.get('bathrooms')
    garage_spots = request.GET.get('garage_spots')
    features = request.GET.get('features')
    is_covered = request.GET.get('is_covered')
    garage_type = request.GET.get('garage_type')
    has_pool = request.GET.get('has_pool')
    has_gatehouse = request.GET.get('has_gatehouse')
    is_occupied = request.GET.get('is_occupied')
    access = request.GET.get('access')
    accessibility = request.GET.get('accessibility')
    move_availability = request.GET.get('move_availability')
    min_sale_price = request.GET.get('min_sale_price')
    max_sale_price = request.GET.get('max_sale_price')
    min_iptu_value = request.GET.get('min_iptu_value')
    max_iptu_value = request.GET.get('max_iptu_value')
    min_condo_fee = request.GET.get('min_condo_fee')
    max_condo_fee = request.GET.get('max_condo_fee')

    # Filter the queryset based on the provided parameters
    properties = Property.objects.all()

    if min_price:
        properties = properties.filter(rent_price__gte=min_price)
    if max_price:
        properties = properties.filter(rent_price__lte=max_price)
    if location:
        properties = properties.filter(Q(city__icontains=location) | Q(neighborhood__icontains=location))
    if property_type:
        properties = properties.filter(property_type=property_type)
    if property_area_min:
        properties = properties.filter(property_area__gte=property_area_min)
    if property_area_max:
        properties = properties.filter(property_area__lte=property_area_max)
    if private_area_min:
        properties = properties.filter(private_area__gte=private_area_min)
    if private_area_max:
        properties = properties.filter(private_area__lte=private_area_max)
    if bedrooms:
        properties = properties.filter(bedrooms__gte=bedrooms)
    if suites:
        properties = properties.filter(suites__gte=suites)
    if bathrooms:
        properties = properties.filter(bathrooms__gte=bathrooms)
    if garage_spots:
        properties = properties.filter(garage_spots__gte=garage_spots)
    if features:
        feature_list = features.split(',')
        for feature in feature_list:
            properties = properties.filter(features__icontains=feature.strip())
    if is_covered:
        properties = properties.filter(is_covered=is_covered)
    if garage_type:
        properties = properties.filter(garage_type=garage_type)
    if has_pool:
        properties = properties.filter(has_pool=has_pool)
    if has_gatehouse:
        properties = properties.filter(has_gatehouse=has_gatehouse)
    if is_occupied:
        properties = properties.filter(is_occupied=is_occupied)
    if access:
        properties = properties.filter(access=access)
    if accessibility:
        properties = properties.filter(accessibility=accessibility)
    if move_availability:
        properties = properties.filter(move_availability=move_availability)
    if min_sale_price:
        properties = properties.filter(sale_price__gte=min_sale_price)
    if max_sale_price:
        properties = properties.filter(sale_price__lte=max_sale_price)
    if min_iptu_value:
        properties = properties.filter(iptu_value__gte=min_iptu_value)
    if max_iptu_value:
        properties = properties.filter(iptu_value__lte=max_iptu_value)
    if min_condo_fee:
        properties = properties.filter(condo_fee__gte=min_condo_fee)
    if max_condo_fee:
        properties = properties.filter(condo_fee__lte=max_condo_fee)

    # Convert properties to a list of dictionaries to return as JSON
    properties_data = list(properties.values(
        'id', 'owner_name', 'street', 'city', 'state', 'neighborhood',
        'property_type', 'rent_price', 'sale_price', 'bedrooms', 'bathrooms', 'suites',
        'property_area', 'private_area', 'garage_spots', 'features', 'is_covered',
        'garage_type', 'has_pool', 'has_gatehouse', 'is_occupied', 'access',
        'accessibility', 'move_availability', 'iptu_value', 'images', 'video_url', 'condo_fee',
    ))
    
    
    return JsonResponse({'properties': properties_data})



# View index que mostra todos os imóveis
@login_required
def index(request):
    imos = Property.objects.prefetch_related('images').all()
    return render(request, 'sales/index.html', {'imos': imos})


def perfil(request):
    # Aqui você pode adicionar lógica para obter dados do usuário, se necessário.
    return render(request, 'sales/perfil.html')



def render_property(request):
    form = PropertyForm()  # Initialize the form
    return render(request, 'sales/render.html', {'form': form})
