from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phone_field import PhoneField

class User(models.Model):
    mail = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phoneNumber = PhoneField(blank=True, help_text='Contact phone number')
    role = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    # 0: viewer | 1: annotator | 2: validator | 3: administrator

class Genome(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fullSequence = models.TextField()

class Sequence(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    sequence = models.TextField()
    position = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    isCds = models.BooleanField(default=True) # True: cds | False: peptidic

    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)


class Annotation(models.Model):
    id = models.CharField(max_length=50, primary_key=True) # The same than the sequence but with '.X' with X a number to allow multipple annotation.
    gene = models.CharField(max_length=10, default='')
    gene_biotype = models.CharField(max_length=50, default='')
    transcript_biotype = models.CharField(max_length=50, default='')
    gene_symbol = models.CharField(max_length=10, default='')
    description = models.CharField(max_length=200, default='')
    isValidate = models.BooleanField(default=False)
    
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="annotationForAnnotator")
    validator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="annotationForValidator")