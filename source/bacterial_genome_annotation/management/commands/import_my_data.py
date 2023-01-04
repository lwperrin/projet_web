from django.core.management.base import BaseCommand
from Bio import SeqIO
from os import listdir
from ...models import *

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset the database',
        )

    def handle(self, *args, **kwargs):
        bacteriaNamesList = []
        for fileName in listdir('data'):
            if (not fileName.endswith('s.fa')) and (not fileName.endswith('p.fa')):
                bacteriaNamesList.append(fileName[:-3])
        for bacteriaName in bacteriaNamesList:
            with open("data/"+bacteriaName+".fa") as file:
                for record in SeqIO.parse(file, "fasta"):
                    genome = Genome()
                    genome.id=bacteriaName
                    genome.fullsequence = record.seq
                    genome.save()
                    break
            with open("data/"+bacteriaName+"_cds.fa") as file:
                for record in SeqIO.parse(file, "fasta"):
                    self.stdout.write(self.style.SUCCESS(str(dir(record))))
                    self.stdout.write(self.style.SUCCESS(str(record.description)))
                    sequence = Sequence()
                    sequence.id = record.id
                    sequence.sequence = record.seq
                    sequence.position = 0
                    sequence.genome = genome
                    sequence.isCds = True
                    

    

