from django.test import TestCase

from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO


#def blastn(blast: BlastResult):
    #results = []
    #result_handle = NCBIWWW.qblast("blastn", "nt", blast.sequence, hitlist_size=101)
    #blast_results = result_handle.read()
#with open('results.xml', 'w') as file:
     #   file.write(blast_results)     
record = NCBIXML.read(open('results.xml'), )
i=0
#print(dir(record))
#print(dir(record.alignments))


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
       
       
        #['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
        # '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
        # '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', 
        # '__str__', '__subclasshook__', '__weakref__', 'align_length', 'bits', 'expect', 'frame', 'gaps', 'identities', 'match',
        #  'num_alignments', 'positives', 'query', 'query_end', 'query_start', 'sbjct', 'sbjct_end', 'sbjct_start', 'score', 'strand']
        #print(hsp.match) For peptidique is not good
       # print(hsp.bits) # 1683.83 PAS LUI
        #print(hsp.subclasshook) ERROR
        #print(hsp.expect) #0.0  evalue
        #print(hsp.frame) CADRE DE LECTURE
        #print(hsp.match) #Match 
        #print(hsp.strand) PLUS MINUS 
        #print(hsp.gaps)
        #print(hsp.num_alignments) none
        #print(hsp.positives)
        #print(hsp.strand)
        #print(hsp.identities) #933 Nombre de nucléotide identiques

        #print(hsp.align_length) # taille de l'alignement
        #print(dir(hsp))
        #
        # for test in hsp.bits:

    