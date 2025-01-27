import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def main():
    # Input and output file paths
    genomes = sys.argv[1]  # Genome table
    genes_tables = sys.argv[2:-1]  # Multiple genes tables
    output_pdf = sys.argv[-1]  # Output PDF file

    # Load the genomes table
    genomes_df = pd.read_csv(genomes)

    # Create a PDF object to save multiple pages
    with PdfPages(output_pdf) as pdf:
        for genes in genes_tables:
            # Load the genes table
            genes_df = pd.read_csv(genes, sep="\t", header=None, names=["reference", "all"])

            # Extract the file name without the extension
            plot_name = os.path.splitext(os.path.basename(genes))[0]

            # Merge tables on 'redundant' column
            merged_table = pd.merge(
                genes_df,
                genomes_df,
                left_on="all",
                right_on="gene",
                how="left"
            )

            # Create a pivot table for the heatmap
            binary_matrix = (
                merged_table
                .assign(match=1)  # Add a column with value 1 for existing associations
                .pivot_table(index='genome', columns='reference', values='match', fill_value=0)  # Pivot to create binary matrix
            )

            # Compute prevalence (sum of each column)
            prevalence = binary_matrix.sum(axis=0)

            # Sort columns and rows
            sorted_columns = prevalence.sort_values(ascending=False).index
            binary_matrix = binary_matrix[sorted_columns]
            binary_matrix = binary_matrix.sort_index()

            # Create a figure with two subplots: bar plot and heatmap
            fig, (ax_bar, ax_heatmap) = plt.subplots(
                nrows=2,
                ncols=1,
                figsize=(12, 10),
                gridspec_kw={"height_ratios": [1, 4]}  # Allocate more space to the heatmap
            )

            # Plot the bar plot (prevalence of genes across genomes)
            ax_bar.bar(
                x=range(len(prevalence)),
                height=prevalence[sorted_columns],
                color="grey",
                edgecolor="black"
            )
            ax_bar.set_title("Number of Genomes per Gene", fontsize=12)
            ax_bar.set_ylabel("Genome Count", fontsize=10)
            ax_bar.set_xticks([])  # Remove x-ticks for clarity
            ax_bar.set_xlim(-0.5, len(prevalence) - 0.5)

            # Plot the heatmap
            sns.heatmap(
                binary_matrix,
                cmap="YlGnBu",
                cbar=False,
                ax=ax_heatmap,
                xticklabels=False,
                vmin=0,
                vmax=1
            )
            ax_heatmap.set_title(plot_name, fontsize=12)
            ax_heatmap.set_xlabel("")
            ax_heatmap.set_ylabel("Original Genomes", fontsize=10)

            plt.tight_layout()

            # Save the current figure to the PDF
            pdf.savefig(fig)
            plt.close(fig)  # Close the current figure to avoid overlaps

    print(f"All heatmaps saved in {output_pdf}")

if __name__ == "__main__":
    main()
