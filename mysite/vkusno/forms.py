from .models import product_card, categories
from django.forms import ModelForm, TextInput, EmailInput, FileInput, CheckboxInput, Select, ValidationError

        
class PublishCardForm(ModelForm):
    class Meta:
        model = product_card
        fields = {'card_image', 'comment', 'choice'}
        widgets = {
            'comment': TextInput(attrs={
                'class': "form-control m-2",
                'placeholder': "Название",
            }),
            'card_image': FileInput(attrs={
                'class': "form-control m-2",
            }), 
            'choice': Select(attrs={
                'class': "form-select m-2"
            }),
        }
        
class PublishCategoryForm(ModelForm):         
    class Meta:
        model = categories
        fields = {'name'}
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control m-2",
                'placeholder': "Название",
            }),
        }
