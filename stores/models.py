from django.db import models
from ecommerce.utils import unique_slug_generator
# Create your models here.
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save , pre_save
from django.urls import reverse

from products.models import Product

User = get_user_model()


# class StoreManager(models.Manager):
#      def new_or_get(self, request):
#         qs = self.get_queryset().filter(id=id)
#         if qs.count() == 1:
#             new_obj = False
#             store_obj = qs.first()
#             if request.user.is_authenticated() and store_obj.user is None:
#                 store_obj.user = request.user
#                 store_obj.save()
#         else:
#             cart_obj = Cart.objects.new(user=request.user)
#             new_obj = True
#             request.session['cart_id'] = cart_obj.id
#         return cart_obj, new_obj

#     def new(self, user=None):
#         user_obj = None
#         if user is not None:
#             if user.is_authenticated():
#                 user_obj = user
#         return self.model.objects.create(user=user_obj)

class Store(models.Model):
        title           = models.CharField(max_length=120,unique=True)
        slug            = models.SlugField(blank=True, unique=True)
        user            = models.OneToOneField(User,blank=True, null=True,on_delete=models.CASCADE)
        timestamp       = models.DateTimeField(auto_now_add=True)
        location        = models.CharField(max_length=120 , blank=True ,null= True)
        store_open      = models.DateField(default=True)
        store_closed    = models.DateField(default=True)
        active          = models.BooleanField(default=True)
        products        = models.ManyToManyField(Product ,blank=True)
        city            = models.CharField(max_length=120, default='damascuse')
        country         = models.CharField(max_length=120, default='syria')
        state           = models.CharField(max_length=120, null=True, blank= True)



        def get_store(self):
            return "{title}\n{user}\n{location}\n{city}, {country}\n{state}".format(
                    title = self.title,
                    user = self.user or "",
                    location = self.location,
                    city = self.city,
                    country= self.country,
                    state = self.state
                )





        def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        	return reverse("store:detail", kwargs={"id": self.id})


        #objects = StoreManager()


        def __str__(self):
            return self.title


def store_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(store_pre_save_receiver, sender=Store)
