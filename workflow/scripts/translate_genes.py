from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys

def translate_fasta(input_file, output_file):
    translated_records = []
    for record in SeqIO.parse(input_file, "fasta"):
        translated_seq = record.seq.translate(to_stop=True)  # Translate to amino acids
        # Create a new SeqRecord with the same header
        translated_record = SeqRecord(translated_seq, id=record.id, description="")
        translated_records.append(translated_record)

    # Write translated sequences to the output file
    SeqIO.write(translated_records, output_file, "fasta")

if __name__ == "__main__":
    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
    translate_fasta(input_fasta, output_fasta)
