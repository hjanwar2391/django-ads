from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Ad
from django import forms
from .models import Withdrawal

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'zip_code', 'country', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class ReferenceForm(forms.Form):
    reference_id = forms.CharField(
        max_length=5,
        label="Reference ID",
        widget=forms.TextInput(attrs={'placeholder': 'Enter 5 Digit Reference ID'}),
        required=True
    )




class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['amount', 'withdrawal_method', 'phone_number']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 440:
            raise forms.ValidationError('Minimum withdrawal amount is 440 points.')
        return amount



# admin area

class VideoForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'video']
