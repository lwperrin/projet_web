from django.shortcuts import render
from .forms import SearchForm
from .forms import AnnotForm
from .models import *
from .utils import blastn, blastp
import threading

# Create your views here.
def home(request):
    return render(request, 'bacterial_genome_annotation/home.html')

def Base(request):
    return render(request, 'bacterial_genome_annotation/Base.html')

def AddGenome(request):
    return render(request, 'bacterial_genome_annotation/AddGenome.html')

def Account(request):
    return render(request, 'bacterial_genome_annotation/Account.html')

def LoginPage(request):
    return render(request, 'bacterial_genome_annotation/LoginPage.html')

def annoter(request):
    form = AnnotForm()
    description = 'empty'
    #sequences = []
    if request.method == "POST":
        form = AnnotForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['ID']
            gene = form.cleaned_data['gene name']
            gene_biotype = form.cleaned_data['gene_biotype']
            transcript_biotype = form.cleaned_data['biotype transcript_name']
            gene_symbol = form.cleaned_data['gene symbol']
            description = form.cleaned_data['description']
            transcript = form.cleaned_data['transcript']
            isValidate = form.cleaned_data['isValidate']

            # Querry
            #sequences = Sequence.objects.all()
            #if bacterial_name!='':
            #    sequences = sequences.filter(genome__id__contains=bacterial_name)
            #if isCds:
            #    sequences = sequences.filter(isCds=isCds)
            #if gene_name!='':
            #    sequences = sequences.filter(annotationQueryName__isValidate=True, annotationQueryName__gene__contains=gene_name)
            #if transcript_name!='':
            #    sequences = sequences.filter(annotationQueryName__isValidate=True, annotationQueryName__transcript__contains=transcript_name)
            #if description!='':
            #    sequences = sequences.filter(annotationQueryName__isValidate=True, annotationQueryName__description__contains=description)
            #if seq!='':
            #    sequences = sequences.filter(sequence__regex='.*'+'.*'.join(seq.split('%'))+'.*')
    return render(request, 'bacterial_genome_annotation/annoter.html', {"form": form, "description": description})#, "sequences": sequences})

    #return render(request, 'bacterial_genome_annotation/annoter.html')

def Parser(request, id):
    params = {"progression": "", "results": []}
    if id!='0':
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

def Search(request):
    form = SearchForm()
    description = 'empty'
    sequences = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            bacterial_name = form.cleaned_data['bacterial_name']
            isCds = form.cleaned_data['nucleic_or_peptidic']
            gene_name = form.cleaned_data['gene_name']
            transcript_name = form.cleaned_data['transcript_name']
            description = form.cleaned_data['description']
            seq = form.cleaned_data['sequence']
            # Querry
            sequences = Sequence.objects.all()
            if bacterial_name!='':
                sequences = sequences.filter(genome__id__contains=bacterial_name)
            if isCds:
                sequences = sequences.filter(isCds=isCds)
            if gene_name!='':
                sequences = sequences.filter(annotationQueryName__isValidate=True, annotationQueryName__gene__contains=gene_name)
            if transcript_name!='':
                sequences = sequences.filter(annotationQueryName__isValidate=True, annotationQueryName__transcript__contains=transcript_name)
            if description!='':
                sequences = sequences.filter(annotationQueryName__isValidate=True, annotationQueryName__description__contains=description)
            if seq!='':
                sequences = sequences.filter(sequence__regex='.*'+'.*'.join(seq.split('%'))+'.*')
    return render(request, 'bacterial_genome_annotation/search.html', {"form": form, "description": description, "sequences": sequences})

def SequenceView(request, id):
    sequence = Sequence.objects.get(id=id)
    print(sequence.id)
    annotationsValidated = Annotation.objects.filter(sequence=sequence, isValidate=True)
    annotations = Annotation.objects.filter(sequence=sequence, isValidate=False)
    params = {
        "seq":sequence,
        "annotationsValidated":annotationsValidated,
        "annotations":annotations
    }
    return render(request, 'bacterial_genome_annotation/sequence.html', params)
