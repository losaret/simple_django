from django import forms
from .models import product_card

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
        
class PublishForm(forms.ModelForm):
    class Meta:
        model = product_card
        fields = {'card_image', 'comment', 'choice', 'category'}