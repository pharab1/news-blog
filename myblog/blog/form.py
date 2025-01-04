from django import forms
from .models import Comments

class CommentsForm(forms.ModelForm):              #Связываем модель с полями
    class Meta:
        model = Comments
        fields = ('name', 'email', 'text_comments')