from .models import ProductCard, Category
from django.forms import (
    ModelForm,
    TextInput,
    FileInput,
    Select,
)


class PublishCardForm(ModelForm):
    class Meta:
        model = ProductCard
        fields = {"card_image", "comment", "choice"}
        widgets = {
            "comment": TextInput(
                attrs={
                    "class": "form-control m-2",
                    "placeholder": "Название",
                }
            ),
            "card_image": FileInput(
                attrs={
                    "class": "form-control m-2",
                }
            ),
            "choice": Select(attrs={"class": "form-select m-2"}),
        }


class PublishCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = {"name"}
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control m-2",
                    "placeholder": "Название",
                }
            ),
        }
