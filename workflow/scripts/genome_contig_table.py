import sys
import os
from Bio import SeqIO
import pandas as pd

def main(input_files, output_file):
    rows = []

    for file_path in input_files:
        # Infer genome name from the file name
        genome_name = os.path.basename(file_path).replace(".fna", "")

        # Parse the FASTA file to extract contig names
        with open(file_path, "r") as fasta_file:
            for record in SeqIO.parse(fasta_file, "fasta"):
                contig_name = record.id  # Extract the header ID
                rows.append({"genome": genome_name, "contig": contig_name})

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # The input files are passed as space-separated arguments
    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]
    main(input_files, output_file)
