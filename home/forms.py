# from django import forms
# from home.models import ContactUs

# class ContactUsForm(forms.ModelForm):

#     class Meta:
#         model = ContactUs
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(ContactUsForm, self).__init__(*args,**kwargs)
        
#         self.fields['name'].widget.attrs['placeholder'] = "Choose a Username"
#         self.fields['email'].widget.attrs['placeholder'] = "Enter Your Email"
#         self.fields['message'].widget.attrs['placeholder'] = "Enter you phone Number"

#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'a7 a3l a3m dark:a3w[#242B51] a13 a33 dark:a1n a1i az a1S aH a3x a3o focus-visible:aE focus:a3p'
#             self.fields[field].widget.attrs['required'] = 'required'