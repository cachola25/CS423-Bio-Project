
import pandas as pd

if __name__ == '__main__':
    # Read in CSV file
    data = pd.read_csv('metadata.csv')
    
    # Get unique cell types
    track = []
    with open("celltypes.txt", "w") as f:
        # Loop through the data and write to file if a cell type is not already in the list 
        for i in range(0, len(data)):
            if data['labels'][i] not in track:
                f.write(data['labels'][i] + '\n')
                track.append(data['labels'][i])
