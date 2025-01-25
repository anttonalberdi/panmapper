import sys
import pandas as pd

def main():
    clusters = sys.argv[1]
    lengths = sys.argv[2]
    kofams = sys.argv[3]
    output_file = sys.argv[4]

    # Read all input tables
    clusters_df = pd.read_csv(clusters)
    lengths_df = pd.read_csv(lengths)
    kofams_df = pd.read_csv(kofams)

    # Modify inputs
    clusters_df["genome"] = clusters_df["genome"].str.replace(".fna", "")
    clusters_df['primary_cluster'] = 'cluster' + clusters_df['primary_cluster'].astype(str)

    lengths_df["genome"] = lengths_df["Contig"].str.split("@").str[0]
    lengths_df["genome"] = lengths_df["genome"].str.replace(":", "_")

    # Merge Cdb.csv with all_clusters.tsv on genome
    merged_df1 = pd.merge(
        lengths_df,
        clusters_df[["genome", "primary_cluster"]],
        left_on="genome",
        right_on="genome",
        how="left"
    )

    #Rename headers
    merged_df1 = merged_df1.rename(columns={"primary_cluster": "cluster", "Length": "length", "Contig": "gene"})

    merged_df2 = pd.merge(
        merged_df1,
        kofams_df,
        left_on="gene",
        right_on="gene",
        how="left"
    )

    # Select the required columns and save
    final_df = merged_df[["cluster", "genome", "gene", "length","ko_id","ko_e"]]
    final_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
