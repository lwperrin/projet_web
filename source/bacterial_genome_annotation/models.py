from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_no = models.CharField(max_length=10, default='0000000000')
    first_name = models.CharField(_("first name"), max_length=32, default='anonymous')
    last_name = models.CharField(_("last name"), max_length=32, default='anonymous')
    role = models.IntegerField(default=0, validators=[
                               MinValueValidator(0), MaxValueValidator(3)])
    picture = models.ImageField(upload_to='profile_pic',
                                default='profile_pic/default.png')
    friends = models.ManyToManyField('self')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Genome(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    fullSequence = models.TextField()


class Sequence(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    sequence = models.TextField()
    position = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    isCds = models.BooleanField(default=True)  # True: cds | False: peptidic
    direction = models.BooleanField(default=True)
    hasValid = models.BooleanField(default=False)

    genome = models.ForeignKey(Genome, on_delete=models.CASCADE)


class Annotation(models.Model):
    gene = models.CharField(max_length=10, default='')
    gene_biotype = models.CharField(max_length=50, default='')
    transcript_biotype = models.CharField(max_length=50, default='')
    gene_symbol = models.CharField(max_length=10, default='')
    description = models.CharField(max_length=200, default='')
    transcript = models.CharField(max_length=200, default='')
    isValidate = models.BooleanField(default=False)

    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE,
                                 related_name='annotationForSequence', related_query_name='annotationQueryName')
    annotator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="annotationForAnnotator")

    validator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="annotationForValidator")

    validator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="annotationForValidator")


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

    value = models.IntegerField(null=True)
    identitie = models.IntegerField(null=True)
    # ident = models.IntegerField(null=True)
    # lenn = models.IntegerField(null=True)

    blastResult = models.ForeignKey(BlastResult, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=500, blank=False)
    date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False)

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=False)
