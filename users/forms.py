from allauth.account.forms import SignupForm
from django import forms
from sales.models import PropertyOwner  # Import PropertyOwner from the sales app

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="Nome", required=True)
    last_name = forms.CharField(max_length=30, label="Sobrenome", required=True)
    phone_number = forms.CharField(max_length=15, label="Celular", required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # Save first_name and last_name to the User model
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        # Create the PropertyOwner entry with the phone number
        PropertyOwner.objects.create(
            user=user,
            phone_number=self.cleaned_data.get('phone_number')
        )
        return user
