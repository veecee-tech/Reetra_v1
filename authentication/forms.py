import re
from django import forms
from .models import UserAccount, UserProfile
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Your Username","required":"required"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required":"required"}))

    fields = ['username', 'password']
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args,**kwargs)
        

        for field in self.fields:
            # self.fields[field].widget.attrs['class'] = 'a7 a3l a3m dark:a3w[#242B51] a13 a33 dark:a1n a1i az a1S aH a3x a3o focus-visible:aE focus:a3p'
            self.fields[field].widget.attrs['required'] = 'required'
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        ':type':"show ? 'password' : 'text'", 'class': 'a7 a3l a3m dark:a3w[#242B51] a13 a33 dark:a1n a1i az a1S aH a3x a3o focus-visible:aE focus:a3p', 'placeholder': 'Password'
    }))
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        ':type':"show ? 'password' : 'text'", 'class': 'a7 a3l a3m dark:a3w[#242B51] a13 a33 dark:a1n a1i az a1S aH a3x a3o focus-visible:aE focus:a3p', 'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = UserAccount
        fields = ['username','email', 'password','password_2', 'phone']

    def clean_email(self):

        email = self.cleaned_data.get('email')
        qs = UserAccount.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("Email already exists")
            
        return email
    def clean_username(self):
    
        username = self.cleaned_data.get('username')
        qs = UserAccount.objects.filter(username=username)

        if(" " in username):
            raise forms.ValidationError("Username can not contain whitespaces")
        if qs.exists():
            raise forms.ValidationError("Username already exists")
            
        return username
    
    def clean_phone(self):
        
        phone = self.cleaned_data.get('phone')
    
        if not re.match(r'^([0]){1}([897]){1}([01]){1}[0-9]{8}$', phone):
            raise forms.ValidationError("Invalid Phone Number format")
        
        return phone

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if password is not None and password != password_2:
            self.add_error("password_2", "Your password must match")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = "Choose a Username"
        self.fields['email'].widget.attrs['placeholder'] = "Enter Your Email"
        self.fields['phone'].widget.attrs['placeholder'] = "eg. 08143344333 or 8134223332"

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'a7 a3l a3m dark:a3w[#242B51] a13 a33 dark:a1n a1i az a1S aH a3x a3o focus-visible:aE focus:a3p'
            self.fields[field].widget.attrs['required'] = 'required'

    def save(self,commit=True):
        user = super().save(commit=False)
        
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'phone', 'is_admin', 'is_staff', 'is_active']

    def clean_username(self):

        username = self.cleaned_data.get('username')
        qs = UserAccount.objects.filter(username=username)

        if qs.exists():
            raise forms.ValidationError("account number already exists")
        return username

    def clean_email(self):

        email = self.cleaned_data.get('email')
        qs = UserAccount.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("email already exists")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def clean_phone(self):
        
        phone = self.cleaned_data.get('phone')
    
        if not re.match(r'^([0]){1}([897]){1}([01]){1}[0-9]{8}$', phone) or re.match(r'^(([897]){1}([01]){1}[0-9]{8}$', phone):
            raise forms.ValidationError("Invalid Phone Number format")
        
        return phone

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
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
        model = UserAccount
        fields = ['username','email', 'password', 'phone', 'is_admin', 'is_active', 'is_staff']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserProfileForm(forms.ModelForm):
    
    class Meta:

        model = UserProfile
        # busines_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Account Number"}))
        # business_address = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Account Number"}))

        exclude = ['user']
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
