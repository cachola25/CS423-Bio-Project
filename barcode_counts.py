import os
from time import sleep
import pandas as pd
from rich.progress import track

if __name__ == "__main__":
    
    # Get the data from the RDS file
    metadata = pd.read_csv("./get_celltypes/metadata.csv")
        
    # Get the barcode files and gene count files for all of the samples
    barcode_files = []
    gene_count_files = []
    for i in range(1,5):
        directory = "data_files/priority_" + str(i)
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith("_barcodes.tsv"):
                    barcode_files.append(os.path.join(root, file))
                if file.endswith("_GOI.csv"):
                    gene_count_files.append(os.path.join(root, file))
    
    
    gene_count_files.sort()
    barcode_files.sort()
    
    # The barcode files for each sample is different so
    # use a dictionary with the GSM ID and the line number
    # as the keys to store the barcodes
    barcode_dict = dict()
    counts_dict = dict()
    for barcode in barcode_files:
        index = 1
        with open(barcode, 'r') as f:
            gsm = barcode.split('/')[-1].split('_')[0]
            for line in f:
                line = line.strip().split()
                if (gsm,index) not in barcode_dict:
                    barcode_dict[(gsm,index)] = line[0]
                index += 1
                
            curr_csv = pd.read_csv(gene_count_files[barcode_files.index(barcode)])
            for i, row in curr_csv.iterrows():
                barcode_str = barcode_dict[(gsm,row['Barcode'])]
                counts_dict[(gsm,barcode_str)] = (row['Count'], row['Gene Name'])
    
    # Use GSMID and barcode from gene name to get the the gene count for that cell
    output_file = "./barcode_counts.csv"
    output_lines = []
    with open(output_file, 'w') as f:
        
        # Print top of the csv
        header = "Celltype,Barcode"
        genes = open("genes_of_interest.txt", 'r').read().strip().split('\n')
        for gene in genes:
            header += "," + gene
        f.write(header + "\n")
        
        # loop through all of the rows of the metadata
        for i,row in track(metadata.iterrows(),total= metadata.shape[0],description="Processing metadata..."):
            
            # Get the barcode for the current row
            curr_code = row['cell_name'].split('_')[-1]
            
            # Check if the barcode is in the dictionary
            if (row["GSMID"], curr_code) in counts_dict:
                # Get cell type and barcode
                line = row["labels.fine"] + "," + curr_code
                # Get the counts for each gene, if the gene is not in the dictionary, set the count to 0
                for gene in genes:
                    if gene in counts_dict[(row["GSMID"], curr_code)][1]:
                        line += "," + str(counts_dict[(row["GSMID"], curr_code)][0])
                    else:
                        line += ",0"
                output_lines.append(line + "\n")
        
        # Sort the output lines and write them to the file
        output_lines.sort()
        for line in output_lines:
            f.write(line)
    
    
    