import os
import pandas as pd

# Create a csv file that only contains the genes
# we want to look at
if __name__ == "__main__":
    cells = open("../genes_of_interest.txt").read().splitlines()
    
    # Get the priority number from the user
    priority = int(input("Enter the priority number: "))
    while priority < 1 or priority > 4:
        priority = int(input("Enter the priority number: "))
    directory = "../data_files/priority_" + str(priority)
    
    gene_count_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_gene_count.csv"):
                gene_count_files.append(os.path.join(root, file))
    
    for count in gene_count_files:
        curr_file = pd.read_csv(count)
        curr_file = curr_file[curr_file["Gene Name"].isin(cells)]
        output_file = directory + '/' + count.split("/")[3] + "/" + count.split("/")[-1].split("_")[0] + "_GOI.csv"
        with open(output_file, "w") as f:
            f.write("Gene Name,Barcode,Count\n")
            for index, element in curr_file.iterrows():
                f.write(f"{element[0]},{element[1]},{element[2]}\n")
        print(f"Created {output_file}")

    
