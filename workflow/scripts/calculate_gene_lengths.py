import sys
from Bio import SeqIO
import pandas as pd

def main():
    fna_file = sys.argv[1]
    output_file = sys.argv[2]

    contig_lengths = []
    for record in SeqIO.parse(fna_file, "fasta"):
        contig_lengths.append({"gene": record.id, "length": len(record.seq)})

    pd.DataFrame(contig_lengths).to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
