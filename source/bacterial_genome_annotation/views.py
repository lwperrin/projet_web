from django.shortcuts import render
# Create your views here.
def Base(request):
    return render(request, 'bacterial_genome_annotation/home.html')