from django.core.management.base import BaseCommand
from Bio import SeqIO
from os import listdir
from ...models import *
from os.path import dirname
from ...utils import fastaParser

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset the database',
        )

    def handle(self, *args, **kwargs):
        # Import data from fasta files
        bacteriaNamesList = []
        relativePath = dirname(__file__) + '/../../../../data/'
        allSequences = []
        allAnnotations = []
        
        for fileName in listdir(relativePath):
            # Find bacteria names from file names
            if (not fileName.endswith('s.fa')) and (not fileName.endswith('p.fa')) and fileName.endswith('.fa'):
                bacteriaNamesList.append(fileName[:-3])

        for bacteriaName in bacteriaNamesList:
            self.stdout.write(self.style.SUCCESS("Creating sequences for"+bacteriaName+"..."), ending='')
            with open(relativePath+bacteriaName+".fa") as file:
                # Genome creation
                for record in SeqIO.parse(file, "fasta"):
                    genome = Genome()
                    genome.id=bacteriaName
                    genome.fullSequence = record.seq
                    genome.save()
                    break
            sequences, annotations = fastaParser(relativePath+bacteriaName+'_cds.fa', genome)
            allSequences.extend(sequences)
            allAnnotations.extend(annotations)
            #Sequence.objects.bulk_create(sequences, ignore_conflicts=True)
            #Annotation.objects.bulk_create(annotations, ignore_conflicts=True)
            sequences, annotations = fastaParser(relativePath+bacteriaName+'_pep.fa', genome)
            allSequences.extend(sequences)
            allAnnotations.extend(annotations)
            #Sequence.objects.bulk_create(sequences, ignore_conflicts=True)
            #Annotation.objects.bulk_create(annotations, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS("Done !"))
        self.stdout.write(self.style.SUCCESS("Saving to database..."), ending='') 
        Sequence.objects.bulk_create(allSequences, ignore_conflicts=True)
        Annotation.objects.bulk_create(allAnnotations, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("Done !"))
            
    def handleOld(self, *args, **kwargs):
        # Import data from fasta files
        bacteriaNamesList = []
        relativePath = dirname(__file__) + '/../../../../data/'
        for fileName in listdir(relativePath):
            # Find bacteria names from file names
            if (not fileName.endswith('s.fa')) and (not fileName.endswith('p.fa')) and fileName.endswith('.fa'):
                bacteriaNamesList.append(fileName[:-3])

        for bacteriaName in bacteriaNamesList:
            with open(relativePath+bacteriaName+".fa") as file:
                # Genome creation
                for record in SeqIO.parse(file, "fasta"):
                    genome = Genome()
                    genome.id=bacteriaName
                    genome.fullSequence = record.seq
                    genome.save()
                    break

            with open(relativePath+bacteriaName+"_cds.fa") as file:
                # Sequences creation 
                self.stdout.write(self.style.SUCCESS(bacteriaName+"_cds.fa"))
                sequences = []
                annotations = []
                for record in SeqIO.parse(file, "fasta"):
                    #self.stdout.write(self.style.SUCCESS(record.id))
                    #self.stdout.write(self.style.SUCCESS(str(record.description)))
                    sequences.append(Sequence())
                    sequences[-1].id = record.id+'_cds'
                    sequences[-1].sequence = record.seq
                    sequences[-1].position = 0
                    sequences[-1].genome = genome # Set the foreign key to link with the genome
                    sequences[-1].isCds = True

                    # Extracting data from description. Two description examples :
                    # ABG68043 cds chromosome:ASM1330v1:Chromosome:190:255
                    # AAN78515 cds chromosome:ASM744v1:Chromosome:10716:11282:-1 gene:c0015 gene_biotype:protein_coding transcript_biotype:protein_coding gene_symbol:yaaH description:Hypothetical protein yaaH
                    desc = record.description.split(' ')
                    sequences[-1].position = int(desc[2].split(':')[3])
                    if int(desc[2].split(':')[5]) == 1:
                        sequences[-1].direction = True
                    else:
                        sequences[-1].direction = False

                    # Try to find an annotation
                    j = 3
                    if len(desc)>3:
                        annotations.append(Annotation())
                        annotations[-1].id = sequences[-1].id + '.0'
                        annotations[-1].sequence = sequences[-1] # Set the foreign key to link with the sequence
                        while len(desc)>j:
                            if desc[j].startswith('gene:'):
                                annotations[-1].gene = desc[j].split(':')[1]
                                j+=1
                            elif desc[j].startswith('gene_biotype:'):
                                annotations[-1].gene_biotype = desc[j].split(':')[1]
                                j+=1
                            elif desc[j].startswith('transcript_biotype:'):
                                annotations[-1].transcript_biotype = desc[j].split(':')[1]
                                j+=1
                            elif desc[j].startswith('gene_symbol:'):
                                annotations[-1].gene_symbol = desc[j].split(':')[1]
                                j+=1
                            elif desc[j].startswith('description:'):
                                annotations[-1].description = ' '.join(desc[j:]).split(':')[1]
                                j+=len(desc)
                            elif desc[j].startswith('transcript:'):
                                annotations[-1].transcript = desc[j].split(':')[1]
                                j+=1
                            else:
                                self.stdout.write(desc[j])
                                j+=1
                            annotations[-1].isValidate = True
                
                self.stdout.write(self.style.SUCCESS("saving..."))
                Sequence.objects.bulk_create(sequences, ignore_conflicts=True)
                Annotation.objects.bulk_create(annotations, ignore_conflicts=True)
                
            with open(relativePath+bacteriaName+"_pep.fa") as file:
                # Sequences creation 
                self.stdout.write(self.style.SUCCESS(bacteriaName+"_pep.fa"))
                sequences = []
                annotations = []
                for record in SeqIO.parse(file, "fasta"):
                    sequences.append(Sequence())
                    sequences[-1].id = record.id+'_pep'
                    sequences[-1].sequence = record.seq
                    sequences[-1].position = 0
                    sequences[-1].genome = genome # Set the foreign key to link with the genome
                    sequences[-1].isCds = False

                    # Extracting data from description. Two description examples :
                    # ABG68043 cds chromosome:ASM1330v1:Chromosome:190:255
                    # AAN78515 cds chromosome:ASM744v1:Chromosome:10716:11282:-1 gene:c0015 gene_biotype:protein_coding transcript_biotype:protein_coding gene_symbol:yaaH description:Hypothetical protein yaaH
                    desc = record.description.split(' ')
                    sequences[-1].position = int(desc[2].split(':')[3])

                    # Try to find an annotation
                    j = 3
                    if len(desc)>3:
                        annotations.append(Annotation())
                        annotations[-1].id = sequences[-1].id + '.0'
                        annotations[-1].sequence = sequences[-1] # Set the foreign key to link with the sequence
                        while len(desc)>j:
                            if desc[j].startswith('gene:'):
                                annotations[-1].gene = desc[j].split(':')[1]
                                j+=1
                            elif desc[j].startswith('gene_biotype:'):
                                annotations[-1].gene_biotype = desc[j].split(':')[1]
                                j+=1
                            elif desc[j].startswith('transcript_biotype:'):
                                annotations[-1].transcript_biotype = desc[j].split(':')[1]
                                j+=1
                            elif desc[j].startswith('gene_symbol:'):
                                annotations[-1].gene_symbol = desc[j].split(':')[1]
                                j+=1
                            elif desc[j].startswith('description:'):
                                annotations[-1].description = ' '.join(desc[j:]).split(':')[1]
                                j+=len(desc)
                            elif desc[j].startswith('transcript:'):
                                annotations[-1].transcript = desc[j].split(':')[1]
                                j+=1
                            else:
                                self.stdout.write(self.style.SUCCESS(' '.join(desc)))
                                j+=1
                            annotations[-1].isValidate = True
                
                self.stdout.write(self.style.SUCCESS("saving..."))
                Sequence.objects.bulk_create(sequences, ignore_conflicts=True)
                Annotation.objects.bulk_create(annotations, ignore_conflicts=True)
                """sequenceFields = Sequence._meta.get_fields()
                sequenceFields = [field.name for field in sequenceFields if field.name != 'id']
                self.stdout.write(self.style.SUCCESS(str(sequenceFields)))
                Sequence.objects.bulk_create(sequences, update_conflicts=True, update_fields=['sequence', 'position', 'isCds', 'genome', 'annotation'], unique_fields=['id'])
                annotationFields = Annotation._meta.get_fields()
                self.stdout.write(self.style.SUCCESS("saving2"))
                annotationFields = [field.name for field in annotationFields if field.name != 'id']
                Annotation.objects.bulk_create(annotations, update_conflicts=True, update_fields=['gene'], unique_fields=['id'])"""