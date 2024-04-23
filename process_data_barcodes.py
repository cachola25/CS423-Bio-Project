import os
import pandas as pd
if __name__ == "__main__":
    
    
    metadata = pd.read_csv("./get_celltypes/metadata.csv")
            
    
    # Get the necessary matrix and gene files
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
        # print("Processing", barcode)
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
                counts_dict[(gsm,barcode_str)] = row['Count']
    
    for elem in counts_dict:
        if elem[0] == 'GSM4983128':
            print(elem, counts_dict[elem])
        break
    # Use GSMID and barcode from gene name to get the the gene count for that cell
    for i,row in metadata.iterrows():
        curr_code = row['cell_name'].split('_')[-1]
        print(row["GSMID"], curr_code)
        # print(row["GSMID"], curr_code, counts_dict[(row["GSMID"],curr_code)])
    #     if i > 10:
        break
        
    
    
    