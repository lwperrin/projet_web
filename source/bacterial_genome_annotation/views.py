"""
This is the views file. It contains all the views used by the website. You can find here the interface between front
and back.
"""

from .forms import *
from .models import *
from .models import Sequence
from .utils import blastn, blastp, reverseSequence, fastaParser
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
from django.shortcuts import resolve_url, redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from Bio import SeqIO
import io


# Create your views here.


def home(request: HttpRequest):
    """
    The home function renders the home page of the LADN website.
    
    
    :param request: HttpRequest: Pass the request from the server to the function
    :return: The home
    """
    return render(request, 'bacterial_genome_annotation/home.html')


def help(request: HttpRequest):
    """
    The help function renders the help page.
    
    
    :param request: HttpRequest: Pass the request to the view
    :return: A rendered version of the help page
    """
    return render(request, 'bacterial_genome_annotation/Help.html')


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_validate'))
def AddGenome(request: HttpRequest):
    """
    The AddGenome function is used to add a new genome to the database.
    It takes in a request and returns an HttpResponse object.
    
    :param request: HttpRequest: Get the data from the form
    :return: A page that has a form for adding a new genome
    """
    if request.method == 'POST':
        form = AddGenomeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                fileCds = io.TextIOWrapper(request.FILES['cds_file'])
                filePep = io.TextIOWrapper(request.FILES['pep_file'])
                fileGen = io.TextIOWrapper(request.FILES['fasta_file'])
                genome = Genome()
                for record in SeqIO.parse(fileGen, "fasta"):
                    genome.id = request.POST['ID']
                    genome.fullSequence = record.seq
                    genome.save()
                    break
                sequences, annotations = fastaParser(fileCds.readlines(), genome)
                s, a = fastaParser(filePep.readlines(), genome)
                sequences.extend(s)
                annotations.extend(a)
                for i in range(len(annotations)):
                    annotations[i].annotator = request.user
                    annotations[i].validator = request.user
                genome.save()
                Sequence.objects.bulk_create(sequences, ignore_conflicts=True)
                Annotation.objects.bulk_create(annotations, ignore_conflicts=True)
            except:
                messages.error(request, 'At least one file is not a fasta file !')
    else:
        form = AddGenomeForm()
    return render(request, 'bacterial_genome_annotation/AddGenome.html', {'form':form})


@login_required
def AccountView(request: HttpRequest, id: str):
    """
    The AccountView function is used to display the account of a user.
    It displays all the annotations and/or validations done by this user, and all the ones that he has to do.
    Another role of this function is to show if a user is friend with another one, or if it's his own account.

    :param request:HttpRequest: Get the user who is logged in
    :param id:str: Identify the user
    :return: The account of the user
    """
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
    validations = Assignation.objects.filter(validator=user, isValidated=False, isAnnotated=True).order_by('date')
    validationsDone = Assignation.objects.filter(validator=user, isValidated=True).order_by('date')
    assignationsNew = Assignation.objects.filter(annotator=user, isRevision=False, isValidated=False,
                                                 isAnnotated=False).order_by('date')
    assignationsRevision = Assignation.objects.filter(annotator=user, isRevision=True, isValidated=False,
                                                      isAnnotated=False).order_by('date')
    assignationsDone = Assignation.objects.filter(annotator=user, isAnnotated=True, isValidated=False).order_by('date')
    assignationsValidated = Assignation.objects.filter(annotator=user, isAnnotated=True, isValidated=True).order_by(
        'date')
    params = {
        'user': user,
        'role': role,
        'own': request.user.id == int(id),
        'isFriend': request.user.friends.filter(id=id).exists(),
        'assignationsNew': assignationsNew,
        'assignationsRevision': assignationsRevision,
        'assignationsDone': assignationsDone,
        'validations': validations,
        'validationsDone': validationsDone,
        'assignationsValidated': assignationsValidated,
        }
    return render(request, 'bacterial_genome_annotation/Account.html', params)


@login_required
def AddToFavorites(request: HttpRequest, id: str):
    """
    The AddToFavorites function is called when the user click on 'Add to favorites' button. It simply adds the account
    to his favorites.

    :param request:HttpRequest: Get the user who is logged in
    :param id:str: Identify the user
    :return: The account of the user
    """
    user = request.user
    user.friends.add(User.objects.get(id=id))
    user.save()
    return redirect('account', id=id)


@login_required
def RemoveFromFavorites(request: HttpRequest, id: str):
    """
    The RemoveFromFavorites function is called when the user click on 'Remove from favorites' button. It simply removes
    the account from his favorites.

    :param request:HttpRequest: Get the user who is logged in
    :param id:str: Identify the user
    :return: The account of the user
    """
    user = request.user
    user.friends.remove(User.objects.get(id=id))
    user.save()
    return redirect('account', id=id)


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_promote_annotator'))
def PromoteToAnnotator(request: HttpRequest, id: str):
    """
    The PromoteToAnnotator function is used to promote a user to the annotator group.
    It takes in an id and checks if the user is already an annotator, if not it promotes them.
    
    :param request: HttpRequest: Get the current user
    :param id: str: Get the user id from the url
    :return: Redirect to the account view
    """
    futureAnnotator = User.objects.get(id=id)
    if futureAnnotator.groups.filter(name='annotator').exists():
        messages.info(request, 'This user is already an annotator !')
    else:
        g = Group.objects.get(name='annotator')
        futureAnnotator.groups.add(g)
        futureAnnotator.save()
        g.save()
    return redirect('account', id=id)


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_promote_validator'))
def PromoteToValidator(request: HttpRequest, id: str):
    """
    The PromoteToAdmin function is used to promote a user to validator.
    It takes in an id and checks if the user is already a validator, if not it adds them to the group of validators.
    
    :param request: HttpRequest: Get the user's id
    :param id: str: Get the id of the user we want to promote
    :return: Redirect to the account view
    :doc-author: Trelent
    """
    futureValidator = User.objects.get(id=id)
    if futureValidator.groups.filter(name='validator').exists():
        messages.info(request, 'This user is already a validator !')
    else:
        g = Group.objects.get(name='validator')
        futureValidator.groups.add(g)
        futureValidator.save()
        g.save()
    return redirect('account', id=id)


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_promote_admin'))
def PromoteToAdmin(request: HttpRequest, id: str):
    """
    The PromoteToAdmin function is used to promote a user to admin.
    It takes in an id and checks if the user is already an admin, if not it adds them to the group of admins.
    
    :param request: HttpRequest: Get the user's id
    :param id: str: Get the id of the user we want to promote
    :return: Redirect to the account view
    """
    futureAdmin = User.objects.get(id=id)
    if futureAdmin.groups.filter(name='admin').exists():
        messages.info(request, 'This user is already an admin !')
    else:
        g = Group.objects.get(name='admin')
        futureAdmin.groups.add(g)
        futureAdmin.save()
        g.save()
    return redirect('account', id=id)


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_downgrade'))
def Downgrade(request: HttpRequest, id: str):
    """
    The Downgrade function is used to downgrade a user of one group.
    It takes in an id and removes their highest group.

    :param request: HttpRequest: Get the user's id
    :param id: str: Get the id of the user we want to promote
    :return: Redirect to the account view
    """
    futureNoob = User.objects.get(id=id)
    if futureNoob.groups.filter(name='admin').exists():
        g = Group.objects.get(name='admin')
        futureNoob.groups.remove(g)
        futureNoob.save()
        g.save()
        return redirect('account', id=id)
    if futureNoob.groups.filter(name='validator').exists():
        g = Group.objects.get(name='validator')
        futureNoob.groups.remove(g)
        futureNoob.save()
        g.save()
        return redirect('account', id=id)
    if futureNoob.groups.filter(name='annotator').exists():
        g = Group.objects.get(name='annotator')
        futureNoob.groups.remove(g)
        futureNoob.save()
        g.save()
        return redirect('account', id=id)
    return redirect('account', id=id)


@login_required
def AccountModificationView(request: HttpRequest):
    """
    The AccountModificationView function is used to modify the user's account information.
    It takes a request as an argument and returns a render of the AccountModification.html template with parameters
    containing the user, and form.

    :param request:HttpRequest: Pass the request from the view to the template
    :return: A page that allows the user to change their information
    """
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
    """
    The MembersView function is used to display the members of the website.
    It takes in a request and returns a render function that will be loaded with
    the appropriate parameters for the MembersView page. The form is also passed in
    as well as all users from User model, paginator object and page object.

    :param request:HttpRequest: Get the user object from the request
    :return: A list of all the users in the database
    """
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


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_annotate'))
def ANNOT(request: HttpRequest, id):
    """
    The ANNOT function is used to annotate a sequence. It takes in the id of the sequence and returns
    the annotation form for that sequence. The user can then fill out the form and submit it, which will
    save their annotations to the database.

    :param request:HttpRequest: Get the user's request
    :param id:str: Get the sequence object from the database
    :return: The annotation page
    """
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
            annotation.annotator = request.user
            annotation.save()
            return redirect('sequence', id=id)

    # , "sequences": sequences})
    return render(request, 'bacterial_genome_annotation/annoter.html', {"form": form})


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_validate'))
def Valid_Annotation(request: HttpRequest, id: str):
    """
    The Valid_Annotation function is usefully for validators to validate an annotation.

    :param request:HttpRequest: Get the user who is logged in
    :param id:str: Identify the annotation
    :return: The sequence view
    """
    annotation = Annotation.objects.get(id=id)
    annotation.isValidate = True
    annotation.validator = request.user
    annotation.save()
    return redirect('sequence', id=annotation.sequence.id)


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_validate'))
def Delete_Annotation(request: HttpRequest, id: str):
    """
    The Delete_Annotation function is usefully for validators to delete an annotation.

    :param request:HttpRequest: The request
    :param id:str: Identify the annotation
    :return: The sequence view
    """
    annotation = Annotation.objects.get(id=id)
    sequence = annotation.sequence
    annotation.delete()
    return redirect('sequence', id=sequence.id)


@login_required
@user_passes_test(lambda u: u.has_perm('bacterial_genome_annotation.can_assign'))
def Assign(request: HttpRequest, id: str):
    """
    The Assign function is used to assign a sequence to an annotator.
    It takes in a request and the sequence id and returns a render function that will show the user's favorites members
    list. Note that only members who are at least annotators are shown.

    :param request:HttpRequest: Get the user object from the request
    :param id:str: The sequence id
    :return: The assignation page
    """
    sequence = Sequence.objects.get(id=id)
    if request.method == "POST":
        annotator = User.objects.get(id=request.POST['Annotator'])
        assignation = Assignation(annotator=annotator, validator=request.user, sequence=sequence)
        assignation.save()
        return redirect('sequence', id=id)
    perm = Permission.objects.get(codename='can_annotate')
    favorites = request.user.friends.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
    if favorites.exists():
        choices = [(u.id, u.email) for u in favorites]
        print(choices)
        form = AssignateForm(choices)
    else:
        form = AssignateForm([('empty', 'No favorite')])
    return render(request, 'bacterial_genome_annotation/Assign.html', {"form": form})


@login_required
def Parser(request: HttpRequest, id):
    """
    The Parser function is used to parse the BLAST results and display them in a table.
    It takes as input an id, which is the primary key of a Sequence object.
    If no such sequence exists, it returns an error message. Otherwise, if the sequence has not been parsed yet
    (i.e., there is no corresponding BlastResult object),
    it creates one with that id and starts parsing its corresponding BLAST result file (either blastn or blastp
    depending on whether it's a CDS or not). Then shows the results.
    Otherwise, if the sequence has already been parsed before (i.e., there already exists a BlastResult), it just shows
    the results
    
    :param request: HttpRequest: Get the request made by the user to access a specific page
    :param id: Get the id of the sequence we want to annotate
    :return: A page with the results of the blast
    """
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
                params['isDone'] = False
            else:
                params['progression'] = 'Finished !'
                params['results'] = list
                params['isDone'] = True
    return render(request, 'bacterial_genome_annotation/Parser.html', params)


def Search(request: HttpRequest):
    """
    The Search function is used to search for a specific gene, transcript or genome.
    It takes in the following parameters:
        request - The HttpRequest object that contains metadata about the request made to this view.
        type - A string representing what kind of search it is (cds, genome or transcript)
    
    :param request: HttpRequest: Construct the httpresponse
    :return: The page with the search results
    :doc-author: Trelent
    """
    page = int(request.GET.get('page', '1'))
    description = 'empty'
    sequences = []
    genomes = []
    typeForm = SearchTypeForm(request.GET)
    type = request.GET.get('type', 'cds')
    if type == 'gen':
        searchForm = GenomeSearchForm(request.POST)
        if searchForm.is_valid():
            bacterial_name = searchForm.cleaned_data['bacterial_name']
            seq = searchForm.cleaned_data['sequence']
            genomes = Genome.objects.all()
            if bacterial_name != '':
                genomes = genomes.filter(id__icontains=bacterial_name)
            if seq != '':
                seq = seq.upper()
                splitSearch = seq.split('%')
                for s in splitSearch:
                    genomes = genomes.filter(fullSequence__contains=s)
                genomes = genomes.filter(
                    fullSequence__regex='.*' + '.*'.join(splitSearch) + '.*')
        paginator = Paginator(genomes, 50)
        pageObj = paginator.get_page(page)
        params = {
            "typeForm": typeForm,
            "form": searchForm,
            "description": description,
            "genomes": genomes,
            "page_obj_genomes": pageObj,
            }
        return render(request, 'bacterial_genome_annotation/search.html', params)

    searchForm = SequenceSearchForm(request.POST)
    if request.method == "POST":
        if searchForm.is_valid():
            bacterial_name = searchForm.cleaned_data['bacterial_name']
            isCds = type == 'cds'
            gene_name = searchForm.cleaned_data['gene_name']
            transcript_name = searchForm.cleaned_data['transcript_name']
            description = searchForm.cleaned_data['description']
            seq = searchForm.cleaned_data['sequence']
            # Query
            sequences = Sequence.objects.filter(isCds=isCds)
            if bacterial_name != '':
                sequences = sequences.filter(genome__id__icontains=bacterial_name)
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
                    sequence__regex='.*' + '.*'.join(splitSearch) + '.*')
    paginator = Paginator(sequences, 50)
    pageObj = paginator.get_page(page)
    params = {
        "typeForm": typeForm,
        "form": searchForm,
        "description": description,
        "sequences": sequences,
        "page_obj_sequences": pageObj,
        }

    return render(request, 'bacterial_genome_annotation/search.html', params)


def alignment(request: HttpRequest, id: str):
    """
    The alignment function takes a blast hit id and renders the alignment template with the query, match, and subject
    sequences.
    The alignment is done by taking three strings: query, match, and subject. The function iterates over each string
    to create a multiline string that contains all the characters in order from start to finish.
    
    :param request: HttpRequest: Get the request from the user
    :param id: str: Get the blast hit with the given id
    :return: The alignment of the query, match and subject sequences
    """
    blast = BlastHit.objects.get(id=id)
    multiline = []
    vide = ' '
    for i in range(min([len(blast.query), len(blast.match), len(blast.subject)])):
        if blast.match[0] != 'M':
            multiline.append(f'{blast.query[i]}{blast.match[i]}{blast.subject[i]}')
        else:
            multiline.append(f'{blast.query[i]}{blast.subject[i]}')    
    params = {
        "blast": blast,
        "multiline": multiline
        }
    return render(request, 'bacterial_genome_annotation/alignment.html', params)


def FAQ(request: HttpRequest):
    """
    The FAQ function renders the FAQ.html template, which contains a list of frequently asked questions about the
    project.
    
    :param request: HttpRequest: Get the information about the user's request
    :return: The faq page
    """
    return render(request, 'bacterial_genome_annotation/FAQ.html')


def SequenceView(request: HttpRequest, id: str):
    """
    The SequenceView function is used to display the information of a specific sequence.
    It also displays all the annotations that have been made for this particular sequence, and it allows 
    the user to comment on this particular annotation. It also has links for assigning and validating an 
    annotation.
    
    :param request: HttpRequest: Get the request from the user
    :param id: str: Get the id of the sequence to be displayed
    :return: The sequence page
    """
    sequence: Sequence = Sequence.objects.get(id=id)
    annotationsValidated = Annotation.objects.filter(sequence=sequence, isValidate=True)
    annotations = Annotation.objects.filter(sequence=sequence, isValidate=False)
    form = CommentForm()
    can_assign = False
    can_valid = False
    if request.user.is_authenticated:
        can_assign = request.user.has_perm('bacterial_genome_annotation.can_assign')
        can_valid = request.user.has_perm('bacterial_genome_annotation.can_valid')
    params = {
        "seq": sequence,
        "annotationsValidated": annotationsValidated,
        "annotations": annotations,
        "form": form,
        "can_assign": can_assign,
        "can_valid": can_valid,
        }
    return render(request, 'bacterial_genome_annotation/sequence.html', params)


def GenomeView(request: HttpRequest, id: str):
    """
    The GenomeView function is used to display the genome of a given bacterial species.
    It takes in an id as a parameter and returns the html page with all the relevant information.
    The function also uses pagination to allow for viewing of large genomes.

    :param request:HttpRequest: Get the user's request
    :param id:str: Get the id of the genome to be displayed
    :return: A page containing the selected genome with its cds highlighted
    """
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
                annotationQuery = Annotation.objects.filter(sequence=seq, isValidate=True)
                if annotationQuery.exists():
                    annotation = annotationQuery.first()
                    suffix = f"\nGene : {annotation.gene}\nGene biotype : {annotation.gene_biotype}\nGene symbol : {annotation.gene_symbol}\nTranscript : {annotation.transcript}\nTranscript biotype : {annotation.transcript_biotype}"
                else:
                    suffix = ""

                self.title = f"ID : {seq.id}\nPosition : {seq.position}"+suffix

    seqList = []
    fullSeq = genome.fullSequence
    i = (page - 1) * 10000
    j = i + 10000
    sequences = Sequence.objects.filter(
        genome=genome, isCds=True, position__gt=i, position__lt=j).order_by('position')
    for s in sequences:
        if i < s.position:
            seqList.append(sequenceAugmented(fullSeq[i:s.position - 1]))
            i = s.position - 1
        newS = Sequence()
        newS.id = s.id
        newS.position = s.position
        b = i + 1 - s.position
        e = j - s.position - 1
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
            self.previous = self.page - 1
            self.next = self.page + 1

    params = {
        'seqList': seqList,
        'genome': genome,
        'fullSequence': genome.fullSequence[(page - 1) * 10000:j],
        'page': pageObj(page=page, first=1, last=len(genome.fullSequence) // 10000 + 1),
        }

    return render(request, 'bacterial_genome_annotation/genome.html', params)


class SignUpView(generic.CreateView):
    template_name = 'bacterial_genome_annotation/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        The form_valid function is called when the form is valid.
        It should return an HttpResponse.
        If it returns None, then a redirect will be issued automatically; this does not happen in our case.

        :param self: Access the attributes and methods of the class in python
        :param form: Create a new user
        :return: The result of calling the form_valid method on the parent class
        """
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        """
        The get_success_url function is used to redirect the user back to the page they were on before making a change. 
        It's important that this function returns a URL, not an HttpResponse object. The reverse() function will be
        called on whatever string is returned.
        
        :param self: Access the attributes and methods of the class
        :return: The url to redirect to after a successful submission
        """
        list(messages.get_messages(self.request))
        if 'next' in self.request.GET:
            return self.request.GET['next']
        return '/'

    def get_initial(self):
        """
        The get_initial function is used to populate the initial data of a form. 
        It takes in self as an argument, and returns a dictionary that will be passed into the form's __init__
        function.
        This allows us to pass in some information from outside our model into our form.
        
        :param self: Access the attributes and methods of the class in python
        :return: The initial data of the form
        """
        if 'next' in self.request.GET:
            if self.request.user.is_authenticated:
                messages.warning(self.request,
                                 'You don\'t have the authorization to do that !.')
            else:
                messages.warning(self.request,
                                 'You must be connected to do that !.')

        return self.initial.copy()


class LogoutView(auth_views.LogoutView):
    template_name = 'accounts/logout.html'


def validate_email(request: HttpRequest):
    """
    The validate_email function checks if the email is empty, taken or valid.
    If it is empty, it returns true for the first condition. If it is taken, 
    it returns true for the second condition. If not then false will be returned.
    
    :param request: HttpRequest: Get the data from the form
    :return: A jsonresponse object
    """
    email = request.POST.get('email', '')
    response = {
        'is_empty': email == '',
        'is_taken': User.objects.filter(email__iexact=email).exists(),
        'is_valid': bool(re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email))
        }
    return JsonResponse(response)


def validate_password(request: HttpRequest):
    """
    The validate_password function is used to validate the password entered by the user. 
    It uses django's built in validator v_p to check if the password is strong enough. 
    If it isn't, then a ValidationError will be raised and an appropriate message will be returned.
    
    :param request: HttpRequest: Get the post data from the frontend
    :return: A json response with the following keys:
    """
    password = request.POST.get('password1', None)
    try:
        v_p(password)
        return JsonResponse({'is_valid': True, 'message': 'Password is valid', 'is_empty': password == ''})
    except ValidationError as e:
        return JsonResponse({'is_valid': False, 'message': ' '.join(e.messages), 'is_empty': password == ''})


def contact(request):
    """
    The contact function is used to send an email from the contact page. It takes a request and returns a redirect to
    the contact page.
    
    :param request: Get the data from the form
    :return: A render of the contact
    """

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
    """
    The AboutUs function shows the About Us view

    :param request:HttpRequest: The request
    :return: The About Us view
    """
    return render(request, 'bacterial_genome_annotation/AboutUs.html')
