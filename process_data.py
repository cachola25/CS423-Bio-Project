import os

if __name__ == "__main__":
    # Get a valid priority number from the user
    priority = int(input("Enter the priority number: "))
    while (priority < 1 or priority > 4):
        priority = int(input("Enter the priority number: "))
    directory = "data_files/priority_" + str(priority)
    
    # Get the necessary matrix and gene files
    matrix_files = []
    gene_file = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_genes.tsv"):
                gene_file = os.path.join(root, file)
            if file.endswith(".mtx"):
                matrix_files.append(os.path.join(root, file))
    
    # Create a dictionary to store the gene names and their line numbers
    gene_indexes = dict()
    index = 1
    with open(gene_file, 'r') as f:
        for line in f:
            line = line.strip().split()
            name = line[1]
            if index not in gene_indexes:
                gene_indexes[index] = name
            index += 1
    
    # Loop through all of the matrix files
    for matrix in matrix_files:  
        skip_header = 0
        count_dictionary = dict()
        with open(matrix, 'r') as f:
            for line in f:
                # Don't process the header lines
                if skip_header < 3:
                    skip_header += 1
                    continue
                
                # Split the line and get only the gene name and UMI count
                line = line.strip().split()
                del line[1]
                curr = gene_indexes[int(line[0])]
                
                # Sum the UMI counts for each gene
                if curr not in count_dictionary:
                    count_dictionary[curr] = int(line[1])
                else:
                    count_dictionary[curr] += int(line[1])
                    
        # Create a new file to store the gene names and their counts
        output_file = "/".join(matrix.split('/')[:3]) + "/" + matrix.split('/')[2] + "_gene_count.csv"
        
        # Write the gene names and their counts to the file
        with open(output_file, 'w') as f:
            f.write("Gene Name,Count\n")
            for element in count_dictionary:
                f.write(f"{element},{count_dictionary[element]}\n")
        print(F"Finished processing {matrix}")
                
    
        
        
                
        
        
    