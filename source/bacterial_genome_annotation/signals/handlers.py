from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Annotation

@receiver(post_save, sender=Annotation)
def update_sequence_hasvalid(sender, instance, **kwargs):
    if instance.isValidate and not instance.sequence.hasValid:
        instance.sequence.hasValid = True
        instance.sequence.save()

@receiver(post_delete, sender=Annotation)
def update_sequence_hasvalid_on_delete(sender, instance, **kwargs):
    annotations = Annotation.objects.filter(sequence=instance.sequence)
    if not any(ann.isValidate for ann in annotations):
        instance.sequence.hasValid = False
        instance.sequence.save()