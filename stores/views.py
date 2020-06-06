from django.views.generic import ListView, DetailView
from .models import Store
from django.shortcuts import render, get_object_or_404

from .models import Store
from .forms import AddStoreForm 



def store_list_view(request):
    store = Store.objects.all()
    print (store)
    context = {
        'obj': store,
    }
    return render(request, "stores/list.html", context)




def StoreDetailSlugView(request, id):
    print(request.GET)

    queryset = Store.objects.get(id=id)
    context = {
        'object': queryset
    }
    return render(request, "stores/detail.html", context)
    

def add_store_view(request):
    form = AddStoreForm(request.POST or None) 
    context = {
        "form": form
    }
    print(request.POST)
    # next_ = request.GET.get('next')
    # next_post = request.POST.get('next')
    # redirect_path = next_ or next_post or None
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()

        #print(form.cleaned_data)

        # model.attr = form.cleaned_data['attr']
        # model.attr2 = form.cleaned_data['attr2']
        # model.save()

       # instance = form.save(commit=False)

    
    return render(request, "stores/add_store.html", context)   

# def add_product_view(request):
#     form = AddProductForm(request.POST or None)
#     context = {
#         "form": form
#     }
#     if form.is_valid(): # All validation rules pass
#             # Process the data in form.cleaned_data
#             # ...
#             title         = request.POST.get('title')
#             description   = request.POST.get('description')
#             price         = request.POST.get('price')
#             image         = request.POST.get('image')
#             featured      = request.POST.get('featured')
#             queryset = Store.objects.filter(user=request.user)
#             print (queryset)
#             queryset.product.add(title=title,
#                 description=description,
#                 price=price ,
#                 image=image,
#                 featured=featured)



#     return render(request, "stores/add_product.html", context)   
