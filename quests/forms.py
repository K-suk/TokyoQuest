from django import forms
from .models import Review

class TagSearchForm(forms.Form):
    keyword = forms.CharField(label='Tag Keyword', max_length=50, required=False)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
