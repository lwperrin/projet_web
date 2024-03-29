"""
This file contains tests, mainly to know if signals work fine.
"""

from django.test import TestCase

# Create your tests here.

from bacterial_genome_annotation.models import *

class AnnotationSignalTestCase(TestCase):
    """Test the signals"""
    def setUp(self):
        g = Genome.objects.create(id='g1')
        s = Sequence.objects.create(id='s1', genome=g)
        u1 = User.objects.create_user('test1@gmail.com', 'bonjour')
        u2 = User.objects.create_user('test2@gmail.com', 'bonjour')
        Annotation.objects.create(sequence=s)
        Annotation.objects.create(sequence=s)
        Assignation.objects.create(annotator=u1, validator=u2, sequence=s)


    def test_sequence_is_updated(self):
        """sequence.hasValid should be automatically updated"""
        s = Sequence.objects.get(id='s1')
        ass = Assignation.objects.get(sequence=s)
        self.assertTrue((not s.hasValid) and (not ass.isRevision))
        a = Annotation.objects.filter(sequence=s).first()
        a.isValidate=True
        a.save()
        s = Sequence.objects.get(id='s1')
        ass = Assignation.objects.get(sequence=s)
        self.assertTrue(s.hasValid and ass.isRevision)
        a.delete()
        s = Sequence.objects.get(id='s1')
        ass = Assignation.objects.get(sequence=s)
        self.assertTrue((not s.hasValid ) and (not ass.isRevision))
        a2 = Annotation.objects.create(sequence=s, isValidate=True)
        s = Sequence.objects.get(id='s1')
        ass = Assignation.objects.get(sequence=s)
        self.assertTrue(s.hasValid and ass.isRevision)