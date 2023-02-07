from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Annotation, Assignation

@receiver(post_save, sender=Annotation)
def update_sequence_hasvalid(sender, instance: Annotation, **kwargs):
    assignations = Assignation.objects.filter(sequence=instance.sequence, annotator=instance.annotator)
    for a in assignations:
        a.isAnnotated=True
    if instance.isValidate:
        for a in assignations:
            a.isValidated = True
            a.validator = instance.validator
        assignationsDifferent = Assignation.objects.filter(sequence=instance.sequence).exclude(annotator=instance.annotator)
        for a in assignationsDifferent:
            a.isRevision = True
            a.save()
        if not instance.sequence.hasValid:
            instance.sequence.hasValid = True
            instance.sequence.save()
    for a in assignations:
        a.save()

@receiver(post_delete, sender=Annotation)
def update_sequence_hasvalid_on_delete(sender, instance: Annotation, **kwargs):
    annotations = Annotation.objects.filter(sequence=instance.sequence)
    assignations = Assignation.objects.filter(sequence=instance.sequence, annotator=instance.annotator)
    for a in assignations:
        a.isAnnotated = False
        a.isValidated = False
        a.save()
    if not any(ann.isValidate for ann in annotations):
        instance.sequence.hasValid = False
        instance.sequence.save()
        assignationsDifferent = Assignation.objects.filter(sequence=instance.sequence).exclude(annotator=instance.annotator)
        for a in assignationsDifferent:
            a.isRevision = False
            a.save()