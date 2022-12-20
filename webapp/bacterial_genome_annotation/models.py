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

class Annotator(User):
    argumentForAnnotators = models.CharField(max_length=100)

class Validator(Annotator):
    argumentForValidators = models.CharField(max_length=100)

class Administrator(Validator):
    argumentForAdministrators = models.CharField(max_length=100)

class Genome(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fullSequence = models.TextField()
    isAnnoted = models.BooleanField(default=False)

class Sequence(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    sequence = models.TextField()
    position = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    isAnnoted = models.BooleanField(default=False)
    isCds = models.BooleanField(default=True) # True: cds | False: peptidic

    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)


class Annotation(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    gene = models.CharField(max_length=10, default='')
    gene_biotype = models.CharField(max_length=50, default='')
    transcript_biotype = models.CharField(max_length=50, default='')
    gene_symbol = models.CharField(max_length=10, default='')
    description = models.CharField(max_length=200, default='')
    isValidate = models.BooleanField(default=False)
    
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    annotator = models.ForeignKey(Annotator, on_delete=models.SET_NULL, null=True, related_name="annotationForAnnotator")
    validator = models.ForeignKey(Validator, on_delete=models.SET_NULL, null=True, related_name="annotationForValidator")