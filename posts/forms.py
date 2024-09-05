from django import forms
from allauth.account.forms import SignupForm
from .models import Interest, Post

class CustomSignupForm(SignupForm):
    #interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        #user.interests.set(self.cleaned_data['interests'])
        user.save()
        return user
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption', 'tags']