from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps  # Use apps to get model reference dynamically

@receiver(post_save, sender='ads_app.User')
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet = apps.get_model('ads_app', 'Wallet')  # Get the Wallet model dynamically
        Wallet.objects.create(user=instance, points=15)

@receiver(post_save, sender='ads_app.User')
def save_user_wallet(sender, instance, **kwargs):
    instance.wallet.save()
