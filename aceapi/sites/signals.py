from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Site, Page

@receiver(post_save, sender=Site)
def post_save_config_site(sender, instance, created, **kwargs):
    print('sender', sender)
    print('instance', instance)

@receiver(post_save, sender=Page)
def post_save_config_page(sender, instance, created, **kwargs):
    print('sender', sender)
    print('instance', instance)
