from django import forms

from .models import Store
 

class AddStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'title',
            'location',
            'store_open',
            'store_closed',
            'city',
            'country',
            'state',
           
        ]


# class AddProductForm (forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             'title',
#             'description',
#             'price',
#             'image',
#             'featured',

#         ]
