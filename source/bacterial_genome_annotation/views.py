from django.shortcuts import render
from .forms import *
from .models import *
from .utils import blastn, blastp, reverseSequence
from django.http import HttpRequest, JsonResponse
import threading
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, views as auth_views
from django.contrib.auth.password_validation import validate_password as v_p
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import resolve_url, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import ContactForm

# Create your views here.


def home(request: HttpRequest):
    return render(request, 'bacterial_genome_annotation/home.html')


def AddGenome(request: HttpRequest):
    return render(request, 'bacterial_genome_annotation/AddGenome.html')


@login_required
def AccountView(request: HttpRequest, id: str):
    if id == '0':
        return redirect('account', id=request.user.id)
    user = User.objects.get(id=id)
    if user.groups.filter(name='admin').exists():
        role = 'admin'
    elif user.groups.filter(name='validator').exists():
        role = 'validator'
    elif user.groups.filter(name='annotator').exists():
        role = 'annotator'
    elif user.groups.filter(name='reader').exists():
        role = 'reader'
    else:
        role = 'no'
    params = {
        'user': user,
        'role': role,
        'own': request.user.id == int(id),
        'isFriend': request.user.friends.filter(id=id).exists(),
    }
    return render(request, 'bacterial_genome_annotation/Account.html', params)


@login_required
def AddToFavorites(request: HttpRequest, id: str):
    user = request.user
    user.friends.add(User.objects.get(id=id))
    user.save()
    print('a')
    return redirect('account', id=id)


@login_required
def RemoveFromFavorites(request: HttpRequest, id: str):
    user = request.user
    user.friends.remove(User.objects.get(id=id))
    user.save()
    return redirect('account', id=id)


@login_required
def AccountModificationView(request: HttpRequest):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=user)
        form.save()
        return redirect('account', id=user.id)
    else:
        form = UserChangeForm(instance=request.user)
    params = {
        'user': user,
        'form': form,
    }
    return render(request, 'bacterial_genome_annotation/AccountModification.html', params)


@login_required
def MembersView(request: HttpRequest):
    page = int(request.GET.get('page', '1'))
    form = UserSearchForm(request.GET)
    users = User.objects.all()
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        email = form.cleaned_data['email']
        last_name = form.cleaned_data['last_name']
        phone_number = form.cleaned_data['phone_number']
        show_only_favorites = form.cleaned_data['show_only_favorites']
        # Querry
        if show_only_favorites:
            users = request.user.friends.all()
        if first_name != '':
            users = users.filter(first_name__icontains=first_name)
        if last_name != '':
            users = users.filter(last_name__icontains=last_name)
        if phone_number != '':
            users = users.filter(phone_no__icontains=phone_number)
        if email != '':
            users = users.filter(email__icontains=email)
    paginator = Paginator(users, 50)
    pageObj = paginator.get_page(page)
    params = {
        "form": form,
        "users": users,
        "page_obj": pageObj,
    }
    return render(request, 'bacterial_genome_annotation/Members.html', params)

#
#### ANNOT via la page sequence ref BLAST #####
#


@login_required
@user_passes_test(lambda u: u.is_staff)
def ANNOT(request: HttpRequest, id):
    sequence = Sequence.objects.get(id=id)
    form = AnnotationFormBySearch
    description = 'empty'
    # sequences = []
    if request.method == "POST":
        form = AnnotationFormBySearch(request.POST)
        if form.is_valid():
            gene = form.cleaned_data['gene']
            gene_biotype = form.cleaned_data['gene_biotype']
            transcript_biotype = form.cleaned_data['transcript_biotype']
            gene_symbol = form.cleaned_data['gene_symbol']
            description = form.cleaned_data['description']
            transcript = form.cleaned_data['transcript']
            annotation = Annotation()
            annotation.gene = gene
            annotation.gene_biotype = gene_biotype
            annotation.transcript_biotype = transcript_biotype
            annotation.gene_symbol = gene_symbol
            annotation.description = description
            annotation.transcript = transcript
            annotation.sequence = sequence
            annotation.save()
            return redirect('sequence', id=id)

    # , "sequences": sequences})
    return render(request, 'bacterial_genome_annotation/annoter.html', {"form": form})


@login_required
def Parser(request: HttpRequest, id):
    params = {"progression": "", "results": []}
    if id != '0':
        query = BlastResult.objects.filter(id=id)
        if not query:
            sequence = Sequence.objects.get(id=id)
            blast = BlastResult()
            blast.id = id
            blast.isCds = sequence.isCds
            blast.sequence = sequence.sequence
            blast.save()
            if sequence.isCds:
                thread = threading.Thread(target=blastn, args=(blast,))
                thread.start()
            else:
                thread = threading.Thread(target=blastp, args=(blast,))
                thread.start()
        else:
            list = BlastHit.objects.filter(blastResult__id=id)
            if not list:
                if not BlastResult.objects.get(id=id):
                    params['progression'] = 'Something went wrong'
                else:
                    params['progression'] = 'Still in progress'
            else:
                params['progression'] = 'Finished !'
                params['results'] = list
    return render(request, 'bacterial_genome_annotation/Parser.html', params)


def Search(request: HttpRequest):
    page = int(request.GET.get('page', '1'))
    description = 'empty'
    sequences = []
    form = SearchForm(request.GET)

    if request.method == "GET":
        if form.is_valid():
            bacterial_name = form.cleaned_data['bacterial_name']
            isCds = form.cleaned_data['nucleic_or_peptidic']
            gene_name = form.cleaned_data['gene_name']
            transcript_name = form.cleaned_data['transcript_name']
            description = form.cleaned_data['description']
            seq = form.cleaned_data['sequence']
            # Querry
            sequences = Sequence.objects.all()
            if bacterial_name != '':
                sequences = sequences.filter(genome__id__icontains=bacterial_name)
            if isCds:
                sequences = sequences.filter(isCds=isCds)
            if gene_name != '':
                sequences = sequences.filter(
                    annotationQueryName__isValidate=True, annotationQueryName__gene__icontains=gene_name)
            if transcript_name != '':
                sequences = sequences.filter(
                    annotationQueryName__isValidate=True, annotationQueryName__transcript__icontains=transcript_name)
            if description != '':
                sequences = sequences.filter(
                    annotationQueryName__isValidate=True, annotationQueryName__description__icontains=description)
            if seq != '':
                seq = seq.upper()
                splitSearch = seq.split('%')
                for s in splitSearch:
                    sequences = sequences.filter(sequence__contains=s)
                sequences = sequences.filter(
                    sequence__regex='.*'+'.*'.join(splitSearch)+'.*')
    paginator = Paginator(sequences, 50)
    pageObj = paginator.get_page(page)
    params = {
        "form": form,
        "description": description,
        "sequences": sequences,
        "page_obj": pageObj,
    }

    return render(request, 'bacterial_genome_annotation/search.html', params)


def SequenceView(request: HttpRequest, id: str):

    sequence = Sequence.objects.get(id=id)
    annotationsValidated = Annotation.objects.filter(sequence=sequence, isValidate=True)
    annotations = Annotation.objects.filter(sequence=sequence, isValidate=False)
    form = CommentForm()
    """
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            newComment = Comment()
            newComment.annotation = annotationsValidated.first()
            newComment.user = request.user
            newComment.content = form.cleaned_data['comment']
            newComment.save()
    class annotForTheme:
        def __init__(self, ann: Annotation, com: list):
            self.annotation=ann
            self.comments = com
            
    class commentForTheme:
        def __init__(self, com: Comment, ans: list):
            self.comment = com
            self.answers = ans
    
    annotationsValidatedBetter = []
    for a in annotationsValidated:
        comments = Comment.objects.filter(annotation=a)
        answers = comments.filter(isAnswer=True)
        base = comments.filter(isAnswer = False).order_by('-likes')
        commentsPretty = []
        for c in base:
            alist = []
            current = c
            nextAnswer = answers.filter(question=current).order_by('date')
            while not (not nextAnswer):
                alist.append(nextAnswer.first())
                current = nextAnswer
                nextAnswer = answers.filter(question=current)
            commentsPretty.append(commentForTheme(c, alist))
        annotationsValidatedBetter.append(annotForTheme(a, commentsPretty))
        
    annotationsBetter = []
    for a in annotations:
        comments = Comment.objects.filter(annotation=a)
        answers = comments.filter(isAnswer=True)
        base = comments.filter(isAnswer = False).order_by('-likes')
        commentsPretty = []
        for c in base:
            alist = []
            current = c
            nextAnswer = answers.filter(question=current).order_by('date')
            while not (not nextAnswer):
                alist.append(nextAnswer.first())
                current = nextAnswer
                nextAnswer = answers.filter(question=current)
            commentsPretty.append(commentForTheme(c, alist))
        annotationsBetter.append(annotForTheme(a, commentsPretty))"""

    params = {
        "seq": sequence,
        "annotationsValidated": annotationsValidated,
        "annotations": annotations,
        "form": form
    }
    return render(request, 'bacterial_genome_annotation/sequence.html', params)


def GenomeView(request: HttpRequest, id: str):
    page = int(request.GET.get('page', '1'))
    genome = Genome.objects.get(id=id)

    class sequenceAugmented:
        def __init__(self, seq: Sequence):
            self.seq = seq
            if isinstance(self.seq, str):
                self.isSeq = False
                self.title = ''
            else:
                self.isSeq = True
                self.title = ''
                self.title = f"ID : {seq.id}\nPosition : {seq.position}"
    seqList = []
    fullSeq = genome.fullSequence
    i = (page-1)*10000
    j = i+10000
    sequences = Sequence.objects.filter(
        genome=genome, isCds=True, position__gt=i, position__lt=j).order_by('position')
    for s in sequences:
        if i < s.position:
            seqList.append(sequenceAugmented(fullSeq[i:s.position-1]))
            i = s.position-1
        newS = Sequence()
        newS.id = s.id
        newS.position = s.position
        b = i+1-s.position
        e = j-s.position-1
        if s.direction:
            tmp = s.sequence
        else:
            tmp = reverseSequence(s.sequence)
        newS.sequence = tmp[b:e]
        if e > b:
            seqList.append(sequenceAugmented(newS))
        i += len(newS.sequence)
        if i >= j:
            break
    if i < j:
        seqList.append(sequenceAugmented(fullSeq[i:j]))

    class pageObj:
        def __init__(self, page, first, last):
            self.page = page
            self.first = first
            self.last = last
            self.hasPrevious = self.page != self.first
            self.hasNext = self.page != self.last
            self.previous = self.page-1
            self.next = self.page+1

    params = {
        'seqList': seqList,
        'genome': genome,
        'fullSequence': genome.fullSequence[(page-1)*10000:j],
        'page': pageObj(page=page, first=1, last=len(genome.fullSequence)//10000+1),
    }

    return render(request, 'bacterial_genome_annotation/genome.html', params)


class SignUpView(generic.CreateView):
    template_name = 'bacterial_genome_annotation/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class LoginView(auth_views.LoginView):

    template_name = 'registration/login.html'

    def get_success_url(self):
        if 'next' in self.request.GET:
            messages.add_message(self.request, messages.INFO,
                                 'You must be connected to do that !.')
        return '/'

    def get_initial(self):
        if 'next' in self.request.GET:
            messages.add_message(self.request, messages.INFO,
                                 'You must be connected to do that !.')
        return self.initial.copy()


class LogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'


def validate_email(request: HttpRequest):
    """Check email availability"""
    email = request.POST.get('email', '')
    response = {
        'is_empty': email == '',
        'is_taken': User.objects.filter(email__iexact=email).exists(),
        'is_valid': bool(re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email))
    }
    return JsonResponse(response)


def validate_password(request: HttpRequest):
    password = request.POST.get('password1', None)
    try:
        v_p(password)
        return JsonResponse({'is_valid': True, 'message': 'Password is valid', 'is_empty': password == ''})
    except ValidationError as e:
        return JsonResponse({'is_valid': False, 'message': ' '.join(e.messages), 'is_empty': password == ''})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            html = render_to_string('bacterial_genome_annotation/contactForm.html', {
                'name': name,
                'email': email,
                'content': content
            })

            send_mail('The contact form subject', 'This is the message',
                      '', ['codewithtestein@gmail.com'], html_message=html)

            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'bacterial_genome_annotation/contact.html', {
        'form': form
    })


def AboutUs(request: HttpRequest):
    return render(request, 'bacterial_genome_annotation/AboutUs.html')


def alignement(request: HttpRequest):
    return render(request, 'bacterial_genome_annotation/alignement.html')
