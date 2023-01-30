from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
from .models import BlastHit, BlastResult

# Usefull function and class are coded here.

def blastn(blast: BlastResult):
    results = []
    result_handle = NCBIWWW.qblast("blastn", "nt", blast.sequence, hitlist_size=101)
    print(f'blasting : {blast.sequence}')
    blast_results = result_handle.read()
    with open('results.xml', 'w') as file:
        file.write(blast_results)
    record = NCBIXML.read(open('results.xml'), )
    i=0
    for align in record.alignments:
        hit = BlastHit()
        hit.id=align.hit_id
        hit.accession=align.accession
        hit.definition=align.hit_def
        hit.len=align.length
        hit.num=i
        hit.blastResult = blast
        for hsp in align.hsps:
            hit.value = hsp.expect
            hit.identitie = ( hsp.identities / hsp.align_length ) *100
        hit.save()
        i+=1
    blast.isFinished=True
    blast.save()

def blastp(sequence: str):
    result_handle = NCBIWWW.qblast("blastp", "nr", sequence)
    with open('results.xml', 'w') as save_file: 
        blast_results = result_handle.read() 
        save_file.write(blast_results)

## Sequence compressor

def cds2compact(sequence: str)->str:
    """Compress a sequence

    Args:
        sequence (str): the sequence

    Returns:
        str: the compression, but letters other than ACGT are nor correctly saved
    """
    letter2number = {'A':0,'C':1,'G':2,'T':3,'R':4,'Y':5,'S':6,'W':7,'K':8,'M':9,'B':10,'D':11,'H':12,'V':13,'N':14}
    prefix = (4-len(sequence)%4)%4
    sequence = 'A'*prefix+sequence
    result = chr(prefix)
    for i in range(len(sequence)//4):
        s = 0
        for j in range(4):
            s+=15**j*letter2number[sequence[4*i+j]]
        result = result + chr(s)
    return result

def compact2cds(sequence: str)->str:
    """uncompress the sequence

    Args:
        sequence (str): the compressed sequence

    Returns:
        str: the final sequence
    """
    number2letter = {0:'A',1:'C',2:'G',3:'T',4:'R',5:'Y',6:'S',7:'W',8:'K',9:'M',10:'B',11:'D',12:'H',13:'V',14:'N'}
    prefix = ord(sequence[0])
    result = ''
    for char in sequence[1:]:
        for i in range(4):
            result = result + number2letter[ord(char)//(15**i)%15]
    return result[prefix:]

def pep2compact(sequence: str)->str:
    letter2number = {'A':0,'R':1,'N':2,'D':3,'C':4,'Q':5,'E':6,'G':7,'H':8,'I':9,'L':10,'K':11,'M':12,'F':13,'P':14,'S':15,'T':16,'W':17,'Y':18,'V':19,'X':20,'B':21,'Z':22,'J':23,'U':24}
    prefix = (3-len(sequence)%3)%3
    sequence = 'A'*prefix+sequence
    result = chr(prefix)
    for i in range(len(sequence)//3):
        s = 0
        for j in range(3):
            s+=24**j*letter2number[sequence[3*i+j]]
        result = result + chr(s)
    return result

def compact2pep(sequence: str)->str:
    number2letter = {0:'A',1:'R',2:'N',3:'D',4:'C',5:'Q',6:'E',7:'G',8:'H',9:'I',10:'L',11:'K',12:'M',13:'F',14:'P',15:'S',16:'T',17:'W',18:'Y',19:'V',20:'X',21:'B',22:'Z',23:'J',24:'U'}
    prefix = ord(sequence[0])
    result = ''
    for char in sequence[1:]:
        for i in range(3):
            result = result + number2letter[ord(char)//(24**i)%24]
    return result[prefix:]