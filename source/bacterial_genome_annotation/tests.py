from django.test import TestCase

# Create your tests here.
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO

from bacterial_genome_annotation.models import *

class AnnotationSignalTestCase(TestCase):
    def setUp(self):
        g = Genome(id='g1')
        s = Sequence.objects.create(id='s1', genome=g)
        a1 = Annotation.objects.create(sequence=s)
        a2 = Annotation.objects.create(sequence=s)

    def test_sequence_is_updated(self):
        """sequence.hasValid should be automatically updated"""
        s = Sequence.objects.get(id='s1')
        self.assertTrue(not s.hasValid, msg='At first, hasValid=False')
        a = Annotation.objects.filter(sequence=s).first()
        a.isValidate=True
        a.save()
        self.assertTrue(s.hasValid, msg='with an annotation saved as validate it is true')
        a.delete()
        self.assertTrue(not s.hasValid, msg='it is false now')
        a2 = Annotation.objects.create(sequence=s, isValidate=True)
        self.assertTrue(s.hasValid, msg='it is true now')
