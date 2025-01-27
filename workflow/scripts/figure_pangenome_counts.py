import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec
import fastcluster

def main():
    # Input and output file paths
    clusters = sys.argv[1]  # Cluster table
    counts = sys.argv[2]  # Count table
    output_pdf = sys.argv[3]  # Output PDF file

    # Load the genomes table
    clusters_df = pd.read_csv(clusters)
    counts_df = pd.read_csv(counts)

    # List clusters
    clusters = clusters_df['cluster'].unique()

    # Create a PDF object to save multiple pages
    with PdfPages(output_pdf) as pdf:
        for cluster in clusters:
            # List genes from cluster
            genes = clusters_df[clusters_df['cluster'] == cluster]['gene']

            # Filter counts_df for the genes in the current cluster
            counts_cluster = counts_df[counts_df['gene'].isin(genes)]

            # Split table into gene names and count data
            counts_cluster_genes = counts_cluster["gene"]
            counts_cluster_counts = counts_cluster.drop(columns=["gene"])

            # Remove columns with all zero values
            counts_cluster_counts = counts_cluster_counts.loc[:, (counts_cluster_counts != 0).any(axis=0)]

            # Transform to counts per million (CPM)
            counts_cluster_cpm = counts_cluster_counts.div(counts_cluster_counts.sum(axis=0), axis=1) * 1e6

            # Fill NaN (resulting from all-zero columns) with zeros
            counts_cluster_cpm = counts_cluster_cpm.fillna(0)

            # Transpose the data and set the gene names explicitly
            heatmap_data = counts_cluster_cpm.T  # Transpose for genes on x-axis
            column_sums = heatmap_data.sum(axis=0)
            sorted_columns = column_sums.sort_values(ascending=False).index

            # Reorder the DataFrame's columns
            heatmap_data_sorted = heatmap_data[sorted_columns]

            # Calculate the total counts for the genes (for the bar plot)
            total_counts_per_gene = column_sums.sort_values(ascending=False)

            # Reset index to ensure proper sorting in barplot
            total_counts_per_gene.index = range(len(total_counts_per_gene))

            heatmap_data.index.name = "Samples"  # Optional, set index name for rows
            heatmap_data.columns.name = "Genes"  # Set column names for genes

            # Create a combined plot
            fig = plt.figure(figsize=(12, 10))
            gs = GridSpec(2, 1, height_ratios=[1, 8])  # GridSpec for bar plot and heatmap

            # Bar plot for total counts per gene
            ax_bar = fig.add_subplot(gs[0])
            ax_bar.bar(total_counts_per_gene.index, total_counts_per_gene.values, color='gray')
            ax_bar.set_xticks([])
            ax_bar.set_ylabel("Total Counts")
            ax_bar.set_title(f"Cluster: {cluster}")

            # Heatmap for CPM values
            ax_heatmap = fig.add_subplot(gs[1])
            sns.heatmap(
                heatmap_data_sorted,
                ax=ax_heatmap,
                cmap="Greens",
                cbar_kws={'label': 'CPM'},
                xticklabels=False,  # Disable x-axis labels for the heatmap
                yticklabels=True
            )
            ax_heatmap.set_xlabel("Genes")
            ax_heatmap.set_ylabel("Samples")

            # Adjust layout
            plt.tight_layout()

            # Save the figure to the PDF
            pdf.savefig(fig)
            plt.close(fig)  # Close the figure to free memory

if __name__ == "__main__":
    main()
