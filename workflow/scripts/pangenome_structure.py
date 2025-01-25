import sys
import pandas as pd

def main():
    cdb = sys.argv[1]
    contig_lengths = sys.argv[2]
    output_file = sys.argv[3]

    # Read all input tables
    cdb_df = pd.read_csv(cdb)
    contig_lengths_df = pd.read_csv(contig_lengths)

    # Extract genome from the contig names in all_clusters.tsv
    contig_lengths_df["genome"] = contig_lengths_df["Contig"].str.split("@").str[0]
    contig_lengths_df["genome"] = contig_lengths_df["genome"].str.replace(":", "_")
    cdb_df["genome"] = cdb_df["genome"].str.replace(".fna", "")
    cdb_df['primary_cluster'] = 'cluster' + cdb_df['primary_cluster'].astype(str)

    # Merge Cdb.csv with all_clusters.tsv on genome
    merged_df = pd.merge(
        contig_lengths_df,
        cdb_df[["genome", "primary_cluster"]],
        left_on="genome",
        right_on="genome",
        how="left"
    )

    #Rename headers
    merged_df = merged_df.rename(columns={"primary_cluster": "cluster", "Length": "length", "Contig": "gene"})


    # Select the required columns and save
    final_df = merged_df[["cluster", "genome", "gene", "length"]]
    final_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
