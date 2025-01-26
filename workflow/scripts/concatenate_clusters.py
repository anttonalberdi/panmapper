import sys
import os
import pandas as pd

def main(input_files, output_file):
    merged_rows = []

    for file_path in input_files:
        # Infer cluster name from the file name
        cluster_name = os.path.basename(file_path).replace(".tsv", "")

        # Read the .tsv file into a DataFrame
        df = pd.read_csv(file_path, sep="\t", header=None, names=["reference", "all"])

        # Add the cluster column
        df["cluster"] = cluster_name

        # Append to the merged rows
        merged_rows.append(df)

    # Concatenate all DataFrames
    merged_df = pd.concat(merged_rows, ignore_index=True)

    # Save the merged DataFrame to the output file
    merged_df.to_csv(output_file, sep="\t", index=False)

if __name__ == "__main__":
    input_files = sys.argv[1:-1]  # All input files passed as space-separated arguments
    output_file = sys.argv[-1]   # The last argument is the output file
    main(input_files, output_file)
