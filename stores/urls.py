from django.conf.urls import url
from .views import store_list_view , StoreDetailSlugView ,add_store_view
  


urlpatterns = [
	url(r'^$', store_list_view, name='list'),
	url(r'^add_store/$', add_store_view, name='add_store'),

	url(r'^(?P<id>[\w-]+)/$', StoreDetailSlugView, name='detail'),
]
app_name = 'stores'