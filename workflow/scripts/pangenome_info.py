import sys
import pandas as pd

def main():
    clusters = sys.argv[1]
    genomes = sys.argv[2]
    lengths = sys.argv[3]
    kofams = sys.argv[4]
    output_file = sys.argv[5]

    # Read all input tables
    clusters_df = pd.read_csv(clusters)
    genomes_df = pd.read_csv(genomes)
    lengths_df = pd.read_csv(lengths)
    kofams_df = pd.read_csv(kofams)

    # Modify inputs
    clusters_df["genome"] = clusters_df["genome"].str.replace(".fna", "", regex=False)
    clusters_df['secondary_cluster'] = 'cluster' + clusters_df['secondary_cluster'].astype(str)


    clusters_df = clusters_df.rename(columns={"secondary_cluster": "cluster"})

    merged_df1 = pd.merge(
        genomes_df,
        clusters_df[["genome", "cluster"]],
        left_on="genome",
        right_on="genome",
        how="left"
    )

    merged_df2 = pd.merge(
        merged_df1,
        lengths_df,
        left_on="gene",
        right_on="gene",
        how="right"
    )

    merged_df3 = pd.merge(
        merged_df2,
        kofams_df,
        left_on="gene",
        right_on="gene",
        how="left"
    )

    print(merged_df3)

    # Select the required columns and save
    final_df = merged_df3[["cluster", "genome", "gene", "length", "ko_id", "ko_e"]]
    final_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
