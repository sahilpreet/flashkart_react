from .models import Customer,Cart
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#can also use decorator for this
#@receiver(post_save,sender=User)
def customer_profile(sender,instance,created,**kwargs):
    if created:
        customer_created=Customer.objects.create(user=instance)
        Cart.objects.create(customer=customer_created)
        Token.objects.create(user=instance)
        print('profile created!')

post_save.connect(customer_profile,sender=User)
