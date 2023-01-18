from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, primary_key=True, default='')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_no = models.CharField(max_length = 10, blank=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    role = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

"""class User(AbstractUser):
    username = models.EmailField(_('email address'), unique = True, primary_key=True)
    native_name = models.CharField(max_length = 5)
    phone_no = models.CharField(max_length = 10)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    role = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    def __str__(self):
        return "{}".format(self.email)

class User(models.Model):
    
    mail = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phoneNumber = PhoneField(blank=True, help_text='Contact phone number')
    role = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    # 0: viewer | 1: annotator | 2: validator | 3: administrator"""

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
    transcript = models.CharField(max_length=200, default='')
    isValidate = models.BooleanField(default=False)
    
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='annotationForSequence', related_query_name='annotationQueryName')
    annotator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="annotationForAnnotator")
    validator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="annotationForValidator")

class BlastResult(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    isCds = models.BooleanField(default=True)
    numberOfResults = models.IntegerField(default=0)
    isFinished = models.BooleanField(default=False)
    sequence = models.CharField(max_length=300)

class BlastHit(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    num = models.IntegerField()
    definition = models.CharField(max_length=100)
    accession = models.CharField(max_length=50)
    len = models.IntegerField()

    blastResult = models.ForeignKey(BlastResult, on_delete=models.CASCADE)