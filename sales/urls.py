from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'sales'  # This sets the namespace for the app

urlpatterns = [

    path("", views.index, name="index"),
    path("perfil/", views.perfil, name="perfil"),
    path('filter_properties/', views.filter_properties, name='filter_properties'),
    path("cadastrar_imovel/", views.cadastrar_imovel, name="cadastrar_imovel"),
    path("editar_imovel/<int:property_id>/", views.editar_imovel, name="editar_imovel"),
    path('painel_juridico/', views.painel_juridico, name='painel_juridico'),
    path("acordo/<int:acordo_id>/", views.acordo_detalhes, name="acordo_detalhes"),
    path("etapa/<int:step_id>/atualizar/", views.atualizar_etapa, name="atualizar_etapa"),
    path("etapa/<int:step_id>/deletar/", views.deletar_etapa, name="deletar_etapa"),
    path("like/<int:property_id>/", views.toggle_like, name="like_property"),
    path("dislike/<int:property_id>/", views.toggle_dislike, name="dislike_property"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
