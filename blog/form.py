from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


class LoginForm(forms.Form):
    username = forms.CharField(label="Enter first name", max_length=50)
    password = forms.CharField(label="Enter your Password", max_length=50, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label=" confirm Your Password ", widget=forms.PasswordInput)

    def clean_password(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('confirm_password')

        if pass1 != pass2:
            return forms.ValidationError("passsword donot match")
        return self.confirm_password
