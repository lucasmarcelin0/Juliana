from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Property, PropertyImage, Bid, PropertyOwner, UserProfile, Deal, DealStep
from django.contrib.auth.decorators import login_required
from .forms import BidForm, PropertyForm, PropertyImageFormSet, DealStepForm


from django.core.exceptions import ValidationError
from django.contrib import messages


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.views.decorators.http import require_POST

from django.utils import timezone



@login_required
def toggle_like(request, property_id):
    property_obj = Property.objects.get(id=property_id)

    if request.user in property_obj.likes.all():
        property_obj.likes.remove(request.user)
        liked = False
    else:
        property_obj.likes.add(request.user)
        property_obj.dislikes.remove(request.user)  # remove dislike se curtir
        liked = True

    return JsonResponse({'liked': liked})


@login_required
def toggle_dislike(request, property_id):
    property_obj = Property.objects.get(id=property_id)

    if request.user in property_obj.dislikes.all():
        property_obj.dislikes.remove(request.user)
        disliked = False
    else:
        property_obj.dislikes.add(request.user)
        property_obj.likes.remove(request.user)  # remove like se rejeitar
        disliked = True

    return JsonResponse({'disliked': disliked})







@require_POST
@login_required
def deletar_etapa(request, step_id):
    step = get_object_or_404(DealStep, id=step_id)
    if request.user.userprofile.role != 'advogada':
        return redirect('sales:perfil')

    acordo_id = step.deal.id
    step.delete()
    return redirect('sales:acordo_detalhes', acordo_id=acordo_id)


@require_POST
@login_required
def atualizar_etapa(request, step_id):
    step = get_object_or_404(DealStep, id=step_id)
    if request.user.userprofile.role != 'advogada':
        return redirect('sales:perfil')

    novo_status = request.POST.get('status')
    if novo_status in ['todo', 'in_progress', 'done']:
        step.status = novo_status
        step.save()

    return redirect('sales:acordo_detalhes', acordo_id=step.deal.id)



from django.utils import timezone
from django.contrib import messages

@login_required
def acordo_detalhes(request, acordo_id):
    acordo = get_object_or_404(Deal, id=acordo_id)

    if request.user.userprofile.role != 'advogada':
        return redirect('sales:perfil')

    steps = acordo.steps.all()
    total = steps.count()
    concluídos = steps.filter(status='done').count()
    progresso = int((concluídos / total) * 100) if total > 0 else 0

    # Verifica se foi enviado um pedido para concluir o acordo
    if request.method == 'POST' and request.POST.get('fechar_acordo') == '1':
        if progresso == 100:
            acordo.status = 'closed'
            acordo.closed_at = timezone.now()  # ✅ Salva a data/hora da conclusão
            acordo.save()
            messages.success(request, "Acordo marcado como concluído com sucesso!")
            return redirect('sales:acordo_detalhes', acordo_id=acordo.id)

    # Criar nova etapa
    elif request.method == 'POST':
        form = DealStepForm(request.POST, request.FILES)
        if form.is_valid():
            step = form.save(commit=False)
            step.deal = acordo
            step.save()
            messages.success(request, "Nova etapa adicionada com sucesso.")
            return redirect('sales:acordo_detalhes', acordo_id=acordo.id)
    else:
        form = DealStepForm()

    return render(request, 'sales/acordo_detalhes.html', {
        'acordo': acordo,
        'steps': steps,
        'form': form,
        'progresso': progresso
    })





@login_required
def painel_juridico(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'advogada':
        return redirect('sales:perfil')

    acordos = Deal.objects.select_related('property', 'bid', 'buyer').order_by('-date_closed')

    return render(request, 'sales/painel_juridico.html', {
        'acordos': acordos
    })



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@login_required
def editar_imovel(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)

    # Verifica se o usuário é dono do imóvel
    property_owner = PropertyOwner.objects.filter(user=request.user).first()
    if property_owner not in property_instance.owner.all():
        messages.error(request, "Você não tem permissão para editar este imóvel.")
        return redirect('sales:perfil')

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_instance)
        formset = PropertyImageFormSet(request.POST, request.FILES, instance=property_instance)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Imóvel atualizado com sucesso!")
            return redirect('sales:perfil')
    else:
        form = PropertyForm(instance=property_instance)
        formset = PropertyImageFormSet(instance=property_instance)

    return render(request, 'sales/editar_imovel.html', {
        'form': form,
        'formset': formset,
        'property': property_instance
    })


@login_required
def cadastrar_imovel(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            new_property = form.save(commit=False)
            # Associa o corretor automaticamente como dono
            property_owner, _ = PropertyOwner.objects.get_or_create(user=request.user)
            new_property.save()
            new_property.owner.add(property_owner)

            # Salva imagens enviadas
            for image in request.FILES.getlist('images'):
                PropertyImage.objects.create(property=new_property, image=image)

            return redirect('sales:perfil')
    else:
        form = PropertyForm()

    return render(request, 'sales/cadastrar_imovel.html', {'form': form})



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





# In your views.py, verify the queries
def index(request):
    user = request.user
    print(f"Total properties: {Property.objects.count()}")  # Debug count

    # Anonymous users do not have id for ManyToMany lookups
    if user.is_authenticated:
        liked_ids = list(Property.objects.filter(likes=user).values_list('id', flat=True))
        disliked_ids = list(Property.objects.filter(dislikes=user).values_list('id', flat=True))
    else:
        liked_ids = []
        disliked_ids = []

    print(f"Liked IDs: {liked_ids}")  # Debug liked
    print(f"Disliked IDs: {disliked_ids}")  # Debug disliked

    imos_liked = Property.objects.filter(id__in=liked_ids).prefetch_related('images')
    imos_disliked = Property.objects.filter(id__in=disliked_ids).prefetch_related('images')
    imos = Property.objects.exclude(id__in=liked_ids).exclude(id__in=disliked_ids).prefetch_related('images')

    print(f"New properties count: {imos.count()}")  # Debug counts
    print(f"Liked properties count: {imos_liked.count()}")
    print(f"Disliked properties count: {imos_disliked.count()}")

    return render(request, 'sales/index.html', {
        'imos': imos,
        'imos_liked': imos_liked,
        'imos_disliked': imos_disliked,
    })



def perfil(request):
    try:
        property_owner, created = PropertyOwner.objects.get_or_create(user=request.user)

        if created:
            try:
                # Salvar para forçar validação com clean()
                property_owner.save()
            except ValidationError as e:
                messages.warning(request, f"Perfil incompleto: {e}")
                # Opcional: redirecionar para edição de perfil
                return redirect('editar_perfil')  # Crie essa view depois, se quiser

        # Buscar imóveis do proprietário
        user_properties = property_owner.properties.all()

    except Exception as e:
        property_owner = None
        user_properties = []
        messages.error(request, f"Ocorreu um erro ao acessar seu perfil: {e}")

    return render(request, 'sales/perfil.html', {
        'user': request.user,
        'property_owner': property_owner,
        'user_properties': user_properties
    })


# Renderização da propriedade
def render_property(request):
    form = PropertyForm()  # Inicializa o formulário
    return render(request, 'sales/render.html', {'form': form})

