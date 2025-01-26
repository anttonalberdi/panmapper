import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    # Input and output file paths
    genomes = sys.argv[1]
    genes = sys.argv[2]
    output_file = sys.argv[3]

    # Load your tables
    genomes_df = pd.read_csv(genomes)
    genes_df = pd.read_csv(genes, sep="\t", header=None, names=["reference", "all"])

    # Extract the file name without the extension
    plot_name = os.path.splitext(os.path.basename(genes))[0]

    # Merge tables on 'redundant' column
    merged_table = pd.merge(
        genes_df,
        genomes_df,
        left_on="all",
        right_on="gene",
        how="left")

    # Create a pivot table for the heatmap
    binary_matrix = (
    merged_table
    .assign(match=1)  # Add a column with value 1 for existing associations
    .pivot_table(index='genome', columns='reference', values='match', fill_value=0)  # Pivot to create binary matrix
    )

    # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(binary_matrix, cmap="YlGnBu", cbar=False,xticklabels=False)
    plt.title(plot_name)
    plt.xlabel("")
    plt.ylabel("Original Genomes")
    plt.tight_layout()

    plt.savefig(output_file)

if __name__ == "__main__":
    main()
