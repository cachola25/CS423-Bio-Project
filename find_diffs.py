import os
import pandas as pd

# Index positions for the bio_files.csv file
# Comment
GSMID_INDEX = 0
FILENAME_INDEX = 1
PRIORITY_INDEX = 2

if __name__ == "__main__":
    # Create tuples of GSM files that contain priority and are
    # apart of the same inflamed-cancerous pair (priority, inflamed, cancerous)
    bio_file = pd.read_csv("./bio_files.csv")
    pairs = []
    for file in bio_file.values:
        for other_file in bio_file.values:
            if (
                file[FILENAME_INDEX].split()[0] == other_file[FILENAME_INDEX].split()[0]
                and file[FILENAME_INDEX].split()[-1] == other_file[FILENAME_INDEX].split()[-1]
                and file[0] != other_file[0]
            ):
                if (file[PRIORITY_INDEX],file[GSMID_INDEX],other_file[GSMID_INDEX],) not in pairs and \
                    (file[PRIORITY_INDEX],other_file[GSMID_INDEX],file[GSMID_INDEX],) not in pairs:
                    pairs.append((file[PRIORITY_INDEX],file[GSMID_INDEX],other_file[GSMID_INDEX]))

    # Get the priority number from the user
    priority = int(input("Enter the priority number: "))
    while priority < 1 or priority > 4:
        priority = int(input("Enter the priority number: "))
    directory = "data_files/priority_" + str(priority)

    # Get all the csv files in all the subdirectories
    # Must have run process_data.py before running this script
    # or the program will error
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))

    # Remove all the pairs that do not have the priority number
    while not all(pair[0] == priority for pair in pairs):
        pairs.remove([pair for pair in pairs if pair[0] != priority][0])

    # Compare each pair of inflamed and cancerous tissue
    for pair in pairs:
        # Get the gene counts for each sample
        file1 = f"{directory}/{pair[1]}/{pair[1]}_gene_count.csv"
        file2 = f"{directory}/{pair[2]}/{pair[2]}_gene_count.csv"
        inflamed = pd.read_csv(file1)
        cancerous = pd.read_csv(file2)
        print(f"Comparing {pair[1]} and {pair[2]}")
        print("-" * 50)
        len_inflamed = len(inflamed)
        len_cancerous = len(cancerous)

        if len_inflamed > len_cancerous:
            print(
                f"{pair[1]} has {len_inflamed - len_cancerous} more genes than {pair[2]}"
            )
        elif len_cancerous > len_inflamed:
            print(
                f"{pair[2]} has {len_cancerous - len_inflamed} more genes than {pair[1]}"
            )
        else:
            print("Both files have the same number of genes")

        # Normalize the data by taking out the genes that are not in both files
        inflamed_genes = inflamed["Gene Name"].values
        cancerous_genes = cancerous["Gene Name"].values
        i_skip = []
        c_skip = []
        for i_gene in inflamed_genes:
            if i_gene not in cancerous_genes:
                i_skip.append(i_gene)

        for c_gene in cancerous_genes:
            if c_gene not in inflamed_genes:
                c_skip.append(c_gene)
                
        # Only process the genes that are not in the skip lists and then sort
        # the data by gene name to make it easier to compare
        inflamed = inflamed[~inflamed["Gene Name"].isin(i_skip)].sort_values(
            by="Gene Name"
        )
        cancerous = cancerous[~cancerous["Gene Name"].isin(c_skip)].sort_values(
            by="Gene Name"
        )

        # Create output directory and file
        output_dir = f"{directory}/diff_files/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = f"{output_dir}{pair[1]}_{pair[2]}_diff.csv"

        # A positive difference indicates that the gene is more expressed
        # in the inflamed tissue than in the cancerous tissue and a negative
        # difference indicates that the gene is more expressed in the cancerous
        with open(output_file, "w") as f:
            f.write("Gene name, Inflamed count, Cancerous count, Difference\n")
            for i_gene, c_gene in zip(inflamed.values, cancerous.values):
                if i_gene[0] != c_gene[0]:
                    raise ValueError(
                        f"Gene names do not match: {i_gene[0]} and {c_gene[0]}"
                    )
                f.write(
                    f"{i_gene[0]}, {i_gene[1]}, {c_gene[1]}, {i_gene[1] - c_gene[1]}"
                )
                f.write("\n")
        print(f"Finished writing to {output_file}")
