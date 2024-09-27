# Appmenu/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Carrito
from .services import generar_enlace_whatsapp

@receiver(post_save, sender=Carrito)
def enviar_whatsapp_despues_de_guardar(sender, instance, **kwargs):
    if instance.completo:
        enlace = generar_enlace_whatsapp(instance)
        # Aquí puedes enviar el enlace a WhatsApp o realizar alguna otra acción
        print(f"Enlace generado: {enlace}")
        # Ejemplo: enviar el enlace por email, o enviar un request a una API para enviar el mensaje por WhatsApp
