from django.conf.urls import url
from django.urls import path

from .views import (
        ProductListView, 
        ProductDetailSlugView,
        ProductDownloadView,
        remove_single_item_from_cart,
        add_to_cart 
        )

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
	path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
]

app_name = 'products'