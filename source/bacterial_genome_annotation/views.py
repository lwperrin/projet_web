from django.shortcuts import render
from .forms import SearchForm
from .models import *

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
    return render(request, 'bacterial_genome_annotation/annoter.html')

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
            print(isCds)
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
                sequences = sequences.filter(sequence__contains=seq)
    return render(request, 'bacterial_genome_annotation/search.html', {"form": form, "description": description, "sequences": sequences[:50]})