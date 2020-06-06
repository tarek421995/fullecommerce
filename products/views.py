# from django.views import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect

from analytics.mixins import ObjectViewedMixin

from carts.models import Cart

from .models import Product, ProductFile


def remove_single_item_from_cart(request, slug):
    # product = Cart.products.(product, slug=slug)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    product_obj =  Product.objects.get(slug=slug)
    # print (product)
    # product_obj = Product.objects.get(id=product_id)

    product_obj.quantity -=1
    product_obj.quantity_price = product_obj.quantity*product_obj.price
    product_obj.save()
    print (product_obj.quantity_price)
    final_price = 0
    # cart_obj.subtotal = product.quantity_price
    for product in cart_obj.products.all():
        final_price += product.price * product.quantity

    cart_obj.subtotal = final_price

    cart_obj.save()

    return redirect("cart:home")

def add_to_cart(request, slug):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    product_obj =  Product.objects.get(slug=slug) 
   
    product_obj.quantity +=1
    product_obj.quantity_price = product_obj.quantity*product_obj.price
    product_obj.save()
    print (product_obj.quantity_price)
    final_price = 0
    for product in cart_obj.products.all():
        final_price += product.price * product.quantity

    cart_obj.subtotal = final_price


        # if product_obj.slug == product.slug:
        #     cart_obj.subtotal = cart_obj.subtotal + product_obj.quantity_price

    print (product_obj.price)
    cart_obj.save()
    
    print (cart_obj.products.all())
        


    # Cart.save()
    return redirect("cart:home")

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()


class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = "products/user-history.html"
    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
        return views



class ProductListView(ListView):
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)



class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance

import os
from wsgiref.util import FileWrapper # this used in django
from mimetypes import guess_type

from django.conf import settings
from orders.models import ProductPurchase

class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        download_obj = downloads_qs.first()
        # permission checks
        
        can_download = False
        user_ready  = True
        if download_obj.user_required:
            if not request.user.is_authenticated:
                user_ready = False

        purchased_products = Product.objects.none()
        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            # not free
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item")
            return redirect(download_obj.get_default_url())

        # aws_filepath = download_obj.generate_download_url()
        # print(aws_filepath)
        # return HttpResponseRedirect(aws_filepath)
        file_root = settings.PROTECTED_ROOT
        # print (file_root)
        filepath = download_obj.file.path # .url /media/
        # print (filepath)
        final_filepath = os.path.join(file_root, filepath) # where the file is stored
        # print (final_filepath)
        with open(final_filepath, 'rb') as f:
            wrapper = FileWrapper(f)
            # print (wrapper)
            mimetype = 'application/force-download'
            gussed_mimetype = guess_type(filepath)[0] # filename.mp4
            # print (gussed_mimetype)
            if gussed_mimetype:
                mimetype = gussed_mimetype
            response = HttpResponse(wrapper, content_type=mimetype)
            print (download_obj.display_name)

            response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.display_name)
            response["X-SendFile"] = str(download_obj.name)
            return response

        return redirect(download_obj.get_default_url())




class ProductDetailView(ObjectViewedMixin, DetailView):
    #queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)


def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk, featured=True) #id
    # instance = get_object_or_404(Product, pk=pk, featured=True)
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('no product here')
    #     raise Http404("Product doesn't exist")
    # except:
    #     print("huh?")

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")
    #print(instance)
    # qs  = Product.objects.filter(id=pk)

    # #print(qs)
    # if qs.exists() and qs.count() == 1: # len(qs)
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")

    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)
