"""
This file contains usefully functions that are used in many functions, such as blast or fasta parser.
"""

from Bio.Blast import NCBIWWW, NCBIXML

try:
    from .models import *
except:
    from models import *


# Usefull function and class are coded here.

def blastn(blast: BlastResult):
    """
    The blastn function takes a BlastResult object as an argument and returns the results of a blastn search
    of the NCBI database. It does this by using BioPython to query the NCBI website for 100 hits with an expect value
    less than 1e-10, and then parses through these results to find relevant information about each hit.

    :param blast:BlastResult: Get the blast result from the database
    :return: The result of the blast query
    """
    results = []
    result_handle = NCBIWWW.qblast("blastn", "nt", blast.sequence, hitlist_size=101)
    print(f'blasting : {blast.sequence}')
    blast_results = result_handle.read()
    with open('results.xml', 'w') as file:
        file.write(blast_results)
    record = NCBIXML.read(open('results.xml'), )
    i = 0
    for align in record.alignments:
        hit = BlastHit()
        hit.id = align.hit_id
        hit.accession = align.accession
        hit.definition = align.hit_def
        hit.len = align.length
        hit.num = i
        hit.blastResult = blast
        for hsp in align.hsps:
            hit.value = hsp.expect
            hit.identitie = (hsp.identities / hsp.align_length) * 100
            hit.align_length = hsp.align_length
            hit.score = hsp.score
            hit.query_end = hsp.query_end
            hit.query_start = hsp.query_start
            hit.query = hsp.query
            hit.subject = hsp.sbjct
            hit.gaps = hsp.gaps
            hit.match = hsp.match
            hit.subject_start = hsp.sbjct_start
            hit.subject_end = hsp.sbjct_end
        hit.save()
        i += 1
    blast.isFinished = True
    blast.save()

def blastp(blast: BlastResult):

    """
    The blastp function takes a sequence as input and returns the results of a blastp search of that sequence against
    the NCBI nr database. The function also saves the results to an xml file called 'results.xml'

    :param sequence:str: Input the sequence that is to be searched
    :return: The result of a blastp search
    """
    results = []
    result_handle = NCBIWWW.qblast("blastp", "nr", blast.sequence, hitlist_size=101)
    print(f'blasting : {blast.sequence}')
    blast_results = result_handle.read()
    with open('results.xml', 'w') as file:
        file.write(blast_results)
        record = NCBIXML.read(open('results.xml'), )
    i = 0
    for align in record.alignments:
        hit = BlastHit()
        hit.id = align.hit_id
        hit.accession = align.accession
        hit.definition = align.hit_def
        hit.len = align.length
        hit.num = i
        hit.blastResult = blast
        for hsp in align.hsps:
            hit.value = hsp.expect
            hit.identitie = (hsp.identities / hsp.align_length) * 100
            hit.align_length = hsp.align_length
            hit.score = hsp.score
            hit.query_end = hsp.query_end
            hit.query_start = hsp.query_start
            hit.query = hsp.query
            hit.subject = hsp.sbjct
            hit.gaps = hsp.gaps
            hit.match = hsp.match
            hit.subject_start = hsp.sbjct_start
            hit.subject_end = hsp.sbjct_end
        hit.save()
        i += 1
    blast.isFinished = True
    blast.save()
 
    
    
""" 
    with open('results.xml', 'w') as file:
        
    
    i = 0
    for align in record.alignments:
        hit = BlastHit()
        hit.id = align.hit_id
        hit.accession = align.accession
        hit.definition = align.hit_def
        hit.len = align.length
        hit.num = i
        hit.blastResult = blast
        for hsp in align.hsps:
            hit.value = hsp.expect
            hit.identitie = (hsp.identities / hsp.align_length) * 100
            hit.align_length = hsp.align_length
            hit.score = hsp.score
            hit.query_end = hsp.query_end
            hit.query_start = hsp.query_start
            hit.query = hsp.query
            hit.subject = hsp.sbjct
            hit.gaps = hsp.gaps
            hit.match = hsp.match
            hit.subject_start = hsp.sbjct_start
            hit.subject_end = hsp.sbjct_end
        hit.save()
        i += 1
    blast.isFinished = True
    blast.save()
"""
# Sequence compressor

def cds2compact(sequence: str) -> str:
    """
    Compress a DNA sequence from base 15 to base 15**4
    :param sequence:str: The full DNA sequence
    :return: The compressed DNA sequence.
    """
    letter2number = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'R': 4, 'Y': 5, 'S': 6, 'W': 7, 'K': 8, 'M': 9, 'B': 10, 'D': 11,
                     'H': 12, 'V': 13, 'N': 14}
    prefix = (4 - len(sequence) % 4) % 4
    sequence = 'A' * prefix + sequence
    result = chr(prefix)
    for i in range(len(sequence) // 4):
        s = 0
        for j in range(4):
            s += 15 ** j * letter2number[sequence[4 * i + j]]
        result = result + chr(s)
    return result


def compact2cds(sequence: str) -> str:
    """
    Uncompress a DNA sequence from base 15**4 to base 15
    :param sequence:str: The compressed DNA sequence
    :return: The full DNA sequence.
    """
    number2letter = {0: 'A', 1: 'C', 2: 'G', 3: 'T', 4: 'R', 5: 'Y', 6: 'S', 7: 'W', 8: 'K', 9: 'M', 10: 'B', 11: 'D',
                     12: 'H', 13: 'V', 14: 'N'}
    prefix = ord(sequence[0])
    result = ''
    for char in sequence[1:]:
        for i in range(4):
            result = result + number2letter[ord(char) // (15 ** i) % 15]
    return result[prefix:]


def pep2compact(sequence: str) -> str:
    """
    Compress a peptidic sequence from base 25 to base 25**3
    :param sequence:str: The full peptidic sequence
    :return: The compressed peptidic sequence.
    """
    letter2number = {'A': 0, 'R': 1, 'N': 2, 'D': 3, 'C': 4, 'Q': 5, 'E': 6, 'G': 7, 'H': 8, 'I': 9, 'L': 10, 'K': 11,
                     'M': 12, 'F': 13, 'P': 14, 'S': 15, 'T': 16, 'W': 17, 'Y': 18, 'V': 19, 'X': 20, 'B': 21, 'Z': 22,
                     'J': 23, 'U': 24}
    prefix = (3 - len(sequence) % 3) % 3
    sequence = 'A' * prefix + sequence
    result = chr(prefix)
    for i in range(len(sequence) // 3):
        s = 0
        for j in range(3):
            s += 24 ** j * letter2number[sequence[3 * i + j]]
        result = result + chr(s)
    return result


def compact2pep(sequence: str) -> str:
    """
    Uncompress a peptidic sequence from base 25**3 to base 25
    :param sequence:str: The compressed peptidic sequence
    :return: The full peptidic sequence.
    """
    number2letter = {0: 'A', 1: 'R', 2: 'N', 3: 'D', 4: 'C', 5: 'Q', 6: 'E', 7: 'G', 8: 'H', 9: 'I', 10: 'L', 11: 'K',
                     12: 'M', 13: 'F', 14: 'P', 15: 'S', 16: 'T', 17: 'W', 18: 'Y', 19: 'V', 20: 'X', 21: 'B', 22: 'Z',
                     23: 'J', 24: 'U'}
    prefix = ord(sequence[0])
    result = ''
    for char in sequence[1:]:
        for i in range(3):
            result = result + number2letter[ord(char) // (24 ** i) % 24]
    return result[prefix:]


# Sequence renversor

def reverseSequence(sequence: str) -> str:
    """
    Find the complementary DNA sequence
    :param sequence:str: The original sequence
    :return: The complementary sequence
    """
    dico = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'R': 'Y', 'Y': 'R', 'S': 'S', 'W': 'W', 'K': 'M', 'M': 'K',
            'B': 'V', 'D': 'H', 'H': 'D', 'V': 'B', 'N': 'N'}
    reverseSeq = ''
    for c in sequence[::-1]:
        reverseSeq = reverseSeq + dico[c]
    return reverseSeq


## Fasta parser (better than SeqIO)

def fastaParser(lines: list, genome: Genome, defaultAnnotator: User = None, defaultValidator: User = None):
    """
    The fastaParser function parses a fasta file to extract sequence and annotations. It is better than the biopython
    parser because it deals with the read direction.
    :param lines:list: The fasta file lines
    :param genome:Genome: The genome the fasta file is coding for
    :param defaultAnnotator:User: The annotator who annotated each annotation in this file
    :param defaultValidator:User: The validator who validated each annotation in this fil
    :return: Tuple of sequences, annotations
    """
    sequences = []
    annotations = []
    for line in lines:
        if line.startswith('>'):
            description = line[1:].split(' ')
            s = Sequence()
            s.sequence = ''
            s.genome = genome
            s.isCds = description[1] == 'cds'
            s.id = description[0] + ('_cds' if s.isCds else '_pep')
            splitDesc = description[2].split(':')
            s.position = int(splitDesc[3])
            try:
                s.direction = splitDesc[5] == '1'
            except:
                s.direction = True
            sequences.append(s)
            j = 3
            if len(description) > 3:
                sequences[-1].hasValid = True
                annotations.append(Annotation())
                annotations[-1].isValidate = True
                # annotations[-1].id = sequences[-1].id + '.0'
                annotations[-1].sequence = sequences[-1]  # Set the foreign key to link with the sequence
                if defaultAnnotator != None:
                    annotations[-1].annotator = defaultAnnotator
                if defaultValidator != None:
                    annotations[-1].validator = defaultValidator

                while len(description) > j:
                    if description[j].startswith('gene:'):
                        annotations[-1].gene = description[j].split(':')[1]
                        j += 1
                    elif description[j].startswith('gene_biotype:'):
                        annotations[-1].gene_biotype = description[j].split(':')[1]
                        j += 1
                    elif description[j].startswith('transcript_biotype:'):
                        annotations[-1].transcript_biotype = description[j].split(':')[1]
                        j += 1
                    elif description[j].startswith('gene_symbol:'):
                        annotations[-1].gene_symbol = description[j].split(':')[1]
                        j += 1
                    elif description[j].startswith('description:'):
                        annotations[-1].description = ' '.join(description[j:]).split(':')[1]
                        j += len(description)
                    elif description[j].startswith('transcript:'):
                        annotations[-1].transcript = description[j].split(':')[1]
                        j += 1
                    else:
                        print(description[j])
                        j += 1
                    annotations[-1].isValidate = True
        else:
            if line.endswith('\n'):
                line = line[:-1]
            sequences[-1].sequence = sequences[-1].sequence + line
    return sequences, annotations
