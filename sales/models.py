from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    # Informações do proprietário
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties", verbose_name="Proprietário")
    owner_name = models.CharField(max_length=255, verbose_name="Nome completo do proprietário", default="Não especificado")
    phone_number = models.CharField(max_length=15, verbose_name="Celular", default="(00) 00000-0000")
    email = models.EmailField(verbose_name="E-mail", default="default@example.com")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="properties", verbose_name="Proprietário", null=True, blank=True)


    # Endereço do imóvel
    street = models.CharField(max_length=255, verbose_name="Rua", default="Não especificada")
    street_number = models.CharField(max_length=10, verbose_name="Número", default="0")
    zip_code = models.CharField(max_length=10, verbose_name="CEP", default="00000-000")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro", default="Não especificado")
    city = models.CharField(max_length=100, verbose_name="Cidade", default="Não especificada")
    state = models.CharField(max_length=100, verbose_name="Estado", default="Não especificado")

    # Informações do imóvel
    property_type = models.CharField(
        max_length=50,
        choices=[('apartment', 'Apartamento'), ('house', 'Casa'), ('land', 'Lote'), ('farm', 'Fazenda'), ('wahehouse', 'Galpão'), ('commercial', 'Comercial')],
        verbose_name="Tipo de Imóvel",
        default='apartment'
    )
    property_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área útil do imóvel (m²)", default=0.0)

    # Características do imóvel
    bedrooms = models.IntegerField(verbose_name="Dormitórios (incluindo suítes)", default=1)
    suites = models.IntegerField(verbose_name="Suítes", default=0)
    bathrooms = models.IntegerField(verbose_name="Banheiros", default=1)

    # Adereços e características
    features = models.CharField(max_length=255, verbose_name="Adereços", default="Nenhum")  # Usando um CharField para valores separados por vírgula
    is_covered = models.CharField(
        max_length=3,
        choices=[('yes', 'Sim'), ('no', 'Não')],
        verbose_name="Cobertura",
        default='no'
    )
    private_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área privativa (m²)", default=0.0)

    # Vagas de garagem e portaria
    garage_spots = models.IntegerField(verbose_name="Vagas de garagem", default=0)
    garage_type = models.CharField(
        max_length=20,
        choices=[
            ('covered', 'Coberta'),
            ('free', 'Livre'),
            ('covered_and_free', 'Coberta e Livre'),
            ('none', 'Nem Coberta nem Livre')
        ],
        verbose_name="Tipo de Vaga",
        default='none'
    )
    has_pool = models.CharField(
        max_length=3,
        choices=[('yes', 'Sim'), ('no', 'Não')],
        verbose_name="Piscina",
        default='no'
    )
    has_gatehouse = models.CharField(
        max_length=20,
        choices=[
            ('24h', '24 h'),
            ('daytime', 'Diurna'),
            ('night', 'Noturna'),
            ('none', 'Sem portaria')
        ],
        verbose_name="Portaria",
        default='none'
    )

    # Condição do imóvel e acessibilidade
    is_occupied = models.CharField(
        max_length=20,
        choices=[
            ('vacant', 'Está vago'),
            ('owner', 'Proprietário mora'),
            ('tenant', 'Inquilino mora')
        ],
        verbose_name="Alguém mora no imóvel",
        default='vacant'
    )
    access = models.CharField(
        max_length=20,
        choices=[('Key', 'Chave'), ('Biometry', 'Biometria'), ('Password', 'Senha')],
        verbose_name="Acesso",
        default='Key'
    )
    accessibility = models.CharField(
        max_length=3,
        choices=[('yes', 'Sim'), ('no', 'Não')],
        verbose_name="Acessibilidade",
        default='no'
    )

    # Informações de disponibilidade e valores
    move_availability = models.CharField(
        max_length=20,
        choices=[('immediate', 'Imediata'), ('30_days', '30 dias'), ('60_days', '60 dias'), ('other', 'Outro')],
        verbose_name="Disponibilidade de mudança",
        default='immediate'
    )
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do aluguel", null=True, blank=True, default=0.0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor de venda", null=True, blank=True, default=0.0)
    iptu_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do IPTU", null=True, blank=True, default=0.0)
    condo_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do condomínio", null=True, blank=True, default=0.0)
    video_url = models.URLField(max_length=500, null=True, blank=True, help_text="URL do vídeo do imóvel (e.g., YouTube link)")

    # Descrição livre do imóvel
    free_description = models.TextField(verbose_name="Descrição livre", null=True, blank=True)

    def __str__(self):
        return f"{self.owner_name} - {self.street}, {self.city}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.street}"


# In models.py
class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('accepted', 'Aceito'),
        ('refused', 'Recusado'),
        ('counteroffer', 'Contra-Oferta')
    ]
    
    property = models.ForeignKey(Property, related_name="bids", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="bids", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    counteroffer = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # For counteroffers
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bid by {self.user.username} - R$ {self.amount}"




class Deal(models.Model):
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE, related_name='deal', verbose_name="Lance")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="Imóvel")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals', verbose_name="Comprador")
    date_closed = models.DateTimeField(auto_now_add=True, verbose_name="Data de Fechamento")
    status = models.CharField(max_length=50, choices=[('pending', 'Pendente'), ('closed', 'Fechado')], verbose_name="Status")

    def __str__(self):
        return f"Negócio para {self.property.title} - {self.status}"

