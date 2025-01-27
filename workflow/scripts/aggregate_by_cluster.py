import pandas as pd
import sys

def merge_and_summarize(cluster_file, counts_file, output_file):
    # Load the cluster information
    cluster_info = pd.read_csv(cluster_file)

    # Load the counts file and split columns based on tabs
    counts = pd.read_csv(counts_file)

    # Merge the tables on the 'gene' column
    merged = pd.merge(cluster_info, counts, on='gene', how='inner')

    # Sum counts for each cluster
    count_columns = counts.columns[1:]
    summary = merged.groupby('cluster')[count_columns].sum().reset_index()

    # Save the summary to a TSV file
    summary.to_csv(output_file, index=False)

def main():
    if len(sys.argv) != 4:
        print("Usage: python merge_clusters_counts.py <cluster_info.csv> <counts.csv> <output.tsv>")
        sys.exit(1)

    cluster_file = sys.argv[1]
    counts_file = sys.argv[2]
    output_file = sys.argv[3]

    merge_and_summarize(cluster_file, counts_file, output_file)

if __name__ == "__main__":
    main()
