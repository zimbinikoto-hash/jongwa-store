from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, Store, Product, Review


class UserRegistrationForm(UserCreationForm):
    """Form for registering vendors and buyers."""

    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        """Save the user and assign their selected role."""

        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            profile = UserProfile.objects.get(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()

        return user


class StoreForm(forms.ModelForm):
    """Form for creating and updating a store."""

    class Meta:
        model = Store
        fields = ['name', 'description']


class ProductForm(forms.ModelForm):
    """Form for creating and updating products."""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']


class ReviewForm(forms.ModelForm):
    """Form for submitting a product review."""

    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your product review here...'
            }),
        }
