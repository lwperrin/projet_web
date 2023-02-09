"""
This file contains the signals that are launched when some objects are saved or deleted, in order to keep the database
sense-full.
"""

from django.db.models.signals import post_save, post_delete, pre_save
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
    """
    The update_sequence_hasvalid_on_delete function is called when an annotation is deleted.
    It checks if there are any other valid annotations for the sequence, and if not, it sets the hasValid field of that sequence to False.

    :param sender: Identify the model that triggers this signal
    :param instance:Annotation: Get the annotation instance that is being deleted
    :param **kwargs: Catch extra keyword arguments that are passed to the function
    :return: The list of all the annotations in a sequence
    """
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

@receiver(pre_save, sender=Assignation)
def onsave(sender, instance: Assignation, **kwargs):
    if instance.sequence.hasValid:
        instance.isRevision = True
    else:
        instance.isRevision = False
