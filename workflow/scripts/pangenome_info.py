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
    clusters_df["genome"] = clusters_df["genome"].str.replace(".fna", "")
    clusters_df['secondary_cluster'] = 'cluster' + clusters_df['secondary_cluster'].astype(str)


    merged_df1 = pd.merge(
        genomes_df,
        clusters_df[["genome", "secondary_cluster"]],
        left_on="genome",
        right_on="genome",
        how="left"
    )

    merged_df2 = pd.merge(
        merged_df1,
        lengths_df,
        left_on="contig",
        right_on="contig",
        how="left"
    )

    merged_df2 = merged_df2.rename(columns={"secondary_cluster": "cluster"})

    print(merged_df2)

    print(kofams_df)

    merged_df3 = pd.merge(
        merged_df2,
        kofams_df,
        left_on="gene",
        right_on="gene",
        how="left"
    )

    # Select the required columns and save
    final_df = merged_df3[["cluster", "genome", "gene", "length", "ko_id", "ko_e"]]
    final_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()
