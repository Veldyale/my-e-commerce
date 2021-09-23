from PIL import Image

from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe("""<span style="color: red; font-size: 14px;">Разрешение изображения будет изменено до {}px * {}px</span>""".format(*Product.MAX_RESOLUTION))


    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     min_height, min_width = Product.MIN_RESOLUTION
    #     max_height, max_width = Product.MAX_RESOLUTION
    #     if img.width != img.height:
    #         raise ValidationError('Изображение должно быть квадратным')
    #     if img.width > max_width or img.height > max_height:
    #         raise ValidationError('Разрешение изображения больше максимального')
    #     if img.width < min_width or img.height < min_height:
    #         raise ValidationError('Разрешение изображения меньше минимального')
    #     return image

User = get_user_model()


class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug__icontains="notebooks"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug__icontains="smartphones"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
