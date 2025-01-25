import sys
import pandas as pd

def main():
    # Input file and output files from command-line arguments
    input_file = sys.argv[1]
    output_read_counts = sys.argv[2]
    output_covered_bases = sys.argv[3]

    # Read the input TSV file
    df = pd.read_csv(input_file, sep="\t")

    # Separate columns by their names
    contig_column = "Contig"
    read_count_columns = [col for col in df.columns if "Read Count" in col]
    covered_bases_columns = [col for col in df.columns if "Covered Bases" in col]

    # Create DataFrames for read counts and covered bases
    read_counts_df = df[[contig_column] + read_count_columns]
    covered_bases_df = df[[contig_column] + covered_bases_columns]

    # Renamge contig to gene
    read_counts_df = read_counts_df.rename(columns={"Contig": "gene"})
    covered_bases_df = covered_bases_df.rename(columns={"Contig": "gene"})

    # Remove " Read Count" and " Covered Bases" from column names
    read_counts_df.columns = [col.replace(" Read Count", "") for col in read_counts_df.columns]
    covered_bases_df.columns = [col.replace(" Covered Bases", "") for col in covered_bases_df.columns]

    # Write the resulting DataFrames to separate files
    read_counts_df.to_csv(output_read_counts, index=False, sep="\t")
    covered_bases_df.to_csv(output_covered_bases, index=False, sep="\t")

if __name__ == "__main__":
    main()
