from .models import product_card, categories
from django.forms import ModelForm, TextInput, EmailInput, FileInput, CheckboxInput, Select, ValidationError



# class CategoriesSelect(forms.Select):
#     def create_option(
#         self, name, value, label, selected, index, subindex=None, attrs=None 
#     ):
#         option = super().create_option(
#           self, name, value, label, selected, index, subindex, attrs 
#         )
#         if value:
#             option["attrs"]["category"] = value.instance.name
#         return option

# class ProductCardForm(forms.ModelForm):
#     class Meta:
#         model = product_card
#         fields = ['category']
#         widgets = {"category":CategoriesSelect}
   
        
class PublishCardForm(ModelForm):
    class Meta:
        model = product_card
        fields = {'card_image', 'comment', 'choice'}
        widgets = {
            'comment': TextInput(attrs={
                'class': "form-control m-2",
                'placeholder': "Name",
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
                'placeholder': "Name",
            }),
        }
