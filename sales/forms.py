from django import forms
from .models import Bid, Property, PropertyImage, DealStep
from django.forms.models import inlineformset_factory

class DealStepForm(forms.ModelForm):
    class Meta:
        model = DealStep
        fields = ['description', 'status', 'attachment']


PropertyImageFormSet = inlineformset_factory(
    Property,
    PropertyImage,
    fields=('image',),
    extra=3,  # Número inicial de campos
    can_delete=True
)

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite as condições de pagamento'}),
        }


class PropertyForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Fotos do Imóvel"
    )

    class Meta:
        model = Property
        exclude = ['likes', 'dislikes', 'owner']
        widgets = {
            'features': forms.Textarea(attrs={'rows': 2}),
            'free_description': forms.Textarea(attrs={'rows': 4}),
        }
