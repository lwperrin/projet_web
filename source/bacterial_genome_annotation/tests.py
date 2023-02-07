from django.test import TestCase

# Create your tests here.
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
#from .models import BlastHit, BlastResult

# Usefull function and class are coded here.

#def blastn(blast: BlastResult):
    #results = []
    #result_handle = NCBIWWW.qblast("blastn", "nt", blast.sequence, hitlist_size=101)
    #blast_results = result_handle.read()
#with open('results.xml', 'w') as file:
     #   file.write(blast_results)     
record = NCBIXML.read(open('results.xml'), )
i=0
#print(dir(record.alignments.hsps))
for align in record.alignments:
    #print(dir(align.hsps))
    #print(align.hsps.score)
    for hsp in align.hsps:
        #print(dir(hsp))
        #
        #['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', 
        # '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__',
        #  '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
        #  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__'
        # , 'align_length', 'bits', 'expect', 'frame', 'gaps', 'identities', 'match', 'num_alignments'
        # , 'positives', 'query', 'query_end', 'query_start', 'sbjct', 'sbjct_end', 'sbjct_start', 'score', 'strand']
        #
        print(hsp.match)
        #print(hsp.bits)  1683.83 PAS LUI
        #print(hsp.subclasshook) ERROR
        #print(hsp.expect) 0.0  evalue
        #print(hsp.frame) CADRE DE LECTURE
        #print(hsp.match) Match 
        #print(hsp.strand) PLUS MINUS 
        #print(hsp.identities) 933 Nombre de nucléotide identiques
        
        #print(hsp.align_length) # taille de l'alignement
        #print(dir(hsp))
        #
        # for test in hsp.bits:

        #print(hsp.score) see the value of list score
        #print(dir(hsp.score))
        #for value in hsp.identities:
         #   print(dir(value))
          #  i=1
        #hit = BlastHit()
        #hit.id=align.hit_id
        #hit.accession=align.accession
        #hit.definition=align.hit_def
        #hit.len=align.length
        #hit.num=i
        #hit.blastResult = blast
        #hit.save()