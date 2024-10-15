from django import forms
from .models import Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite as condições de pagamento'}),
        }
