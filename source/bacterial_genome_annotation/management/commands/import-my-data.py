"""
This is the command to import the data from the fasta files in data folder.
"""

from django.core.management.base import BaseCommand
from Bio import SeqIO
from os import listdir
from ...models import *
from os.path import dirname
from ...utils import fastaParser


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """
        The handle function is the main function of this management command.
        It imports data from fasta files and saves it to the database.

        :param self: Access the attributes and methods of the class in python
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Catch any additional keyword arguments that are passed to the function
        """
        # Import data from fasta files
        bacteriaNamesList = []
        relativePath = dirname(__file__) + '/../../../../data/'
        allSequences = []
        allAnnotations = []
        User.objects.create_user('default@default.com', 'default')
        u = User.objects.get(email='default@default.com')

        for fileName in listdir(relativePath):
            # Find bacteria names from file names
            if (not fileName.endswith('s.fa')) and (not fileName.endswith('p.fa')) and fileName.endswith('.fa'):
                bacteriaNamesList.append(fileName[:-3])

        for bacteriaName in bacteriaNamesList:
            self.stdout.write(self.style.SUCCESS("Creating sequences for" + bacteriaName + "..."), ending='')
            with open(relativePath + bacteriaName + ".fa") as file:
                # Genome creation
                for record in SeqIO.parse(file, "fasta"):
                    genome = Genome()
                    genome.id = bacteriaName
                    genome.fullSequence = record.seq
                    genome.save()
                    break
            with open(relativePath + bacteriaName + '_cds.fa', 'r') as file:
                lines = file.readlines()
            sequences, annotations = fastaParser(lines, genome)
            allSequences.extend(sequences)
            allAnnotations.extend(annotations)
            with open(relativePath + bacteriaName + '_pep.fa', 'r') as file:
                lines = file.readlines()
            sequences, annotations = fastaParser(lines, genome)
            allSequences.extend(sequences)
            allAnnotations.extend(annotations)
            self.stdout.write(self.style.SUCCESS("Done !"))
        self.stdout.write(self.style.SUCCESS("Saving to database..."), ending='')
        Sequence.objects.bulk_create(allSequences, ignore_conflicts=True)
        for i in range(len(allAnnotations)):
            allAnnotations[i].annotator = u
            allAnnotations[i].validator = u
        Annotation.objects.bulk_create(allAnnotations, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("Done !"))
