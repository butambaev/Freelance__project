from django import forms
from .models import JobPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'price', 'image']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Название должно быть не короче 5 символов')
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 100:
            raise forms.ValidationError('Минимальная цена — 100')
        return price
