from django.test import TestCase

# Create your tests here.

from bacterial_genome_annotation.models import *

class AnnotationSignalTestCase(TestCase):
    """Test the automatic update of sequence.hasvalid on annotation change"""
    def setUp(self):
        g = Genome.objects.create(id='g1')
        s = Sequence.objects.create(id='s1', genome=g)
        Annotation.objects.create(sequence=s)
        Annotation.objects.create(sequence=s)

    def test_sequence_is_updated(self):
        """sequence.hasValid should be automatically updated"""
        s = Sequence.objects.get(id='s1')
        self.assertTrue(not s.hasValid)
        a = Annotation.objects.filter(sequence=s).first()
        a.isValidate=True
        a.save()
        s = Sequence.objects.get(id='s1')
        self.assertTrue(s.hasValid)
        a.delete()
        s = Sequence.objects.get(id='s1')
        self.assertTrue(not s.hasValid)
        a2 = Annotation.objects.create(sequence=s, isValidate=True)
        s = Sequence.objects.get(id='s1')
        self.assertTrue(s.hasValid)
