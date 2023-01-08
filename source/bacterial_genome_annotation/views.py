from django.shortcuts import render
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