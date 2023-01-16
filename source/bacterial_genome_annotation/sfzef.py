from Bio.Blast import NCBIWWW, NCBIXML

sequence = 'ggtaagtcctctagtacaaacacccccaatattgtgatataattaaaattatattcatattctgttgccagaaaaaacacttttaggctatattagagccatcttctttgaagcgttgtc'.upper()
results = []
result_handle = NCBIWWW.qblast("blastn", "nt", sequence)
print(f'blasting : {sequence}')
blast_results = result_handle.read()
with open('results.xml', 'w') as file:
    file.write(blast_results)
record = NCBIXML.read(open('results.xml'))
for align in record.alignments: 
    print(dict(align))