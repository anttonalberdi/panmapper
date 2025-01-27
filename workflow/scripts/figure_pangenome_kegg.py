import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def main():
    # Input and output file paths
    genomes = sys.argv[1]  # Genome table
    cluster_info_path = sys.argv[2]  # Cluster info (contains KEGG IDs for reference genes)
    genes_tables = sys.argv[3:-1]  # Multiple genes tables
    output_pdf = sys.argv[-1]  # Output PDF file

    # Load the genomes table
    genomes_df = pd.read_csv(genomes)

    # Load the cluster info table
    cluster_info_df = pd.read_csv(cluster_info_path)

    # Inspect column names
    print("Genome Table Columns:", genomes_df.columns)
    print("Cluster Info Columns:", cluster_info_df.columns)

    # Merge cluster info into genomes_df to expand KEGG IDs for all genes
    expanded_kegg_df = pd.merge(
        genomes_df,
        cluster_info_df[["cluster", "gene", "length", "ko_id", "ko_e"]],
        left_on="gene",  # Match genomes_df 'gene' column
        right_on="gene",  # Match cluster_info 'gene' column
        how="left"
    )

    # Ensure all genes have KEGG IDs propagated from their reference gene
    expanded_kegg_df["ko_id"] = expanded_kegg_df["ko_id"].fillna(expanded_kegg_df["gene"])

    # Create a binary matrix for the heatmap
    binary_matrix = expanded_kegg_df.pivot_table(
        index="ko_id",
        columns="genome",
        aggfunc=lambda x: 1,
        fill_value=0
    )

    # Generate heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(binary_matrix, cmap="viridis", cbar_kws={'label': 'Presence (1) / Absence (0)'})
    plt.title("KEGG ID Presence Across Genomes")
    plt.xlabel("Genomes")
    plt.ylabel("KEGG IDs")

    # Save the heatmap to the PDF
    with PdfPages(output_pdf) as pdf:
        pdf.savefig()  # Save the heatmap
        plt.close()

        # Generate barplots for each gene table
        for genes in genes_tables:
            # Load the genes table
            genes_df = pd.read_csv(genes, sep="\t", header=None, names=["reference", "all"])

            # Extract the file name without the extension
            plot_name = os.path.splitext(os.path.basename(genes))[0]

            # Merge genes_df with expanded_kegg_df to include KEGG IDs
            merged_table = pd.merge(
                genes_df,
                expanded_kegg_df,
                left_on="reference",  # Match genes_df 'reference' column
                right_on="gene",     # Match expanded_kegg_df 'gene' column
                how="left"
            )

            # Replace genes with KEGG IDs for the plot
            merged_table["x_label"] = merged_table["ko_id"].fillna(merged_table["gene"])

            print(merged_table)

            # Plot using seaborn
            plt.figure(figsize=(10, 6))
            sns.barplot(
                x="x_label",
                y="reference",
                data=merged_table,
                order=merged_table.sort_values("reference")["x_label"]
            )
            plt.title(plot_name)
            plt.xlabel("KEGG ID (or Gene if unavailable)")
            plt.ylabel("Reference")
            plt.xticks(rotation=90)

            # Save the current figure to the PDF
            pdf.savefig()
            plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python figure_pangenome_reference.py <genome_gene.csv> <cluster_info.csv> <cluster_*.tsv> <output.pdf>")
        sys.exit(1)

    main()
