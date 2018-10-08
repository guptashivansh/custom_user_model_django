from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserLoginForm(forms.Form):
    email = forms.CharField(label ="Username or email:")
    # username = forms.CharField(max_length=25)
    password = forms.CharField(widget = forms.PasswordInput)

    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
        
    #     # user_qs = User.objects.filter(username=username)
    #     # if user_qs.count() == 1:
    #     #   user = user_qs.first()
    #     if email and password:
    #         user = authenticate(email=email,password=password)
    #         if not user:
    #             raise forms.ValidationError("This user does not exist")

    #         if not user.check_password(password):
    #             raise forms.ValidationError("Incorrect Password")

    #         if not user.is_active:
    #             raise forms.ValidationError("This user is no longer active.")
    #     return super(UserLoginForm, self).clean(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=25)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','username','active', 'admin')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_username(self):
        # Check that the two password entries match
        username = self.cleaned_data.get("username")
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username already exist")
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]