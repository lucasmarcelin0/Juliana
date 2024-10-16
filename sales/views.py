from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Property, PropertyImage, Bid, PropertyOwner
from django.contrib.auth.decorators import login_required
from .forms import BidForm




from django.db.models import Q
from django.http import JsonResponse
from .models import Property

def filter_properties(request):
    # Start with all properties
    properties = Property.objects.all()

    # Apply filters only if parameters are present
    if request.GET.get('min_price'):
        min_price = request.GET.get('min_price')
        properties = properties.filter(rent_price__gte=min_price)
    
    if request.GET.get('max_price'):
        max_price = request.GET.get('max_price')
        properties = properties.filter(rent_price__lte=max_price)
    
    if request.GET.get('location'):
        location = request.GET.get('location')
        properties = properties.filter(Q(city__icontains=location) | Q(neighborhood__icontains=location))
    
    if request.GET.get('property_type'):
        property_type = request.GET.get('property_type')
        properties = properties.filter(property_type=property_type)
    
    if request.GET.get('property_area_min'):
        property_area_min = request.GET.get('property_area_min')
        properties = properties.filter(property_area__gte=property_area_min)
    
    if request.GET.get('property_area_max'):
        property_area_max = request.GET.get('property_area_max')
        properties = properties.filter(property_area__lte=property_area_max)
    
    if request.GET.get('private_area_min'):
        private_area_min = request.GET.get('private_area_min')
        properties = properties.filter(private_area__gte=private_area_min)
    
    if request.GET.get('private_area_max'):
        private_area_max = request.GET.get('private_area_max')
        properties = properties.filter(private_area__lte=private_area_max)
    
    if request.GET.get('bedrooms'):
        bedrooms = request.GET.get('bedrooms')
        properties = properties.filter(bedrooms__gte=bedrooms)
    
    if request.GET.get('suites'):
        suites = request.GET.get('suites')
        properties = properties.filter(suites__gte=suites)
    
    if request.GET.get('bathrooms'):
        bathrooms = request.GET.get('bathrooms')
        properties = properties.filter(bathrooms__gte=bathrooms)
    
    if request.GET.get('garage_spots'):
        garage_spots = request.GET.get('garage_spots')
        properties = properties.filter(garage_spots__gte=garage_spots)
    
    if request.GET.get('features'):
        feature_list = request.GET.get('features').split(',')
        for feature in feature_list:
            properties = properties.filter(features__icontains=feature.strip())
    
    if request.GET.get('is_covered'):
        is_covered = request.GET.get('is_covered')
        properties = properties.filter(is_covered=is_covered)
    
    if request.GET.get('garage_type'):
        garage_type = request.GET.get('garage_type')
        properties = properties.filter(garage_type=garage_type)
    
    if request.GET.get('has_pool'):
        has_pool = request.GET.get('has_pool')
        properties = properties.filter(has_pool=has_pool)
    
    if request.GET.get('has_gatehouse'):
        has_gatehouse = request.GET.get('has_gatehouse')
        properties = properties.filter(has_gatehouse=has_gatehouse)
    
    if request.GET.get('is_occupied'):
        is_occupied = request.GET.get('is_occupied')
        properties = properties.filter(is_occupied=is_occupied)
    
    if request.GET.get('access'):
        access = request.GET.get('access')
        properties = properties.filter(access=access)
    
    if request.GET.get('accessibility'):
        accessibility = request.GET.get('accessibility')
        properties = properties.filter(accessibility=accessibility)
    
    if request.GET.get('move_availability'):
        move_availability = request.GET.get('move_availability')
        properties = properties.filter(move_availability=move_availability)
    
    if request.GET.get('min_sale_price'):
        min_sale_price = request.GET.get('min_sale_price')
        properties = properties.filter(sale_price__gte=min_sale_price)
    
    if request.GET.get('max_sale_price'):
        max_sale_price = request.GET.get('max_sale_price')
        properties = properties.filter(sale_price__lte=max_sale_price)
    
    if request.GET.get('min_iptu_value'):
        min_iptu_value = request.GET.get('min_iptu_value')
        properties = properties.filter(iptu_value__gte=min_iptu_value)
    
    if request.GET.get('max_iptu_value'):
        max_iptu_value = request.GET.get('max_iptu_value')
        properties = properties.filter(iptu_value__lte=max_iptu_value)
    
    if request.GET.get('min_condo_fee'):
        min_condo_fee = request.GET.get('min_condo_fee')
        properties = properties.filter(condo_fee__gte=min_condo_fee)
    
    if request.GET.get('max_condo_fee'):
        max_condo_fee = request.GET.get('max_condo_fee')
        properties = properties.filter(condo_fee__lte=max_condo_fee)

    # Convert properties to a list of dictionaries to return as JSON (without related fields like 'images')
    properties_data = []
    for property in properties:
        properties_data.append({
            'id': property.id,
            'street': property.street,
            'street_number': property.street_number,
            'city': property.city,
            'state': property.state,
            'neighborhood': property.neighborhood,
            'rent_price': property.rent_price,
            'sale_price': property.sale_price,
            'bedrooms': property.bedrooms,
            'bathrooms': property.bathrooms,
            'suites': property.suites,
            'property_area': property.property_area,
            'private_area': property.private_area,
            'garage_spots': property.garage_spots,
            'features': property.features,
            'garage_type': property.garage_type,
            'has_pool': property.has_pool,
            'has_gatehouse': property.has_gatehouse,
            'is_occupied': property.is_occupied,
            'accessibility': property.accessibility,
            'move_availability': property.move_availability,
            'iptu_value': property.iptu_value,
            'condo_fee': property.condo_fee,
            'video_url': property.video_url,
            'images': [{'url': image.image.url} for image in property.images.all()]  # Include images
        })

    return JsonResponse({'properties': properties_data})





@login_required
def index(request):
    imos = Property.objects.prefetch_related('images', 'bids').all()
    
    if request.method == 'POST':
        # Handle bid submission
        if 'amount' in request.POST:
            bid_form = BidForm(request.POST)
            property_id = request.POST.get('property_id')
            property_instance = get_object_or_404(Property, id=property_id)
            
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                bid.user = request.user
                bid.property = property_instance
                bid.save()
                return redirect('sales:index')
        
        # Handle owner's decision on bids (accept, refuse, counteroffer)
        elif 'bid_action' in request.POST:
            bid_id = request.POST.get('bid_id')
            action = request.POST.get('bid_action')
            bid = get_object_or_404(Bid, id=bid_id)
            
            if action == 'accept':
                bid.status = 'accepted'
            elif action == 'refuse':
                bid.status = 'refused'
            elif action == 'counteroffer':
                counter_amount = request.POST.get('counteroffer')
                bid.status = 'counteroffer'
                bid.counteroffer = counter_amount
            bid.save()
            return redirect('sales:index')

    bid_form = BidForm()

    context = {
        'imos': imos,
        'bid_form': bid_form,
    }

    return render(request, 'sales/index.html', context)





def perfil(request):
    # Fetch the PropertyOwner for the logged-in user
    property_owner = PropertyOwner.objects.get(user=request.user)
    
    # Fetch all properties associated with this PropertyOwner
    user_properties = property_owner.properties.all()
    
    return render(request, 'sales/perfil.html', {
        'user': request.user,
        'user_properties': user_properties
    })


# Renderização da propriedade
def render_property(request):
    form = PropertyForm()  # Inicializa o formulário
    return render(request, 'sales/render.html', {'form': form})

