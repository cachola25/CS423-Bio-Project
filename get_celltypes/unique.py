import pandas as pd
from rich.progress import track

data = pd.read_csv('metadata.csv')
cell_names = data['cell_name']
arr = []
index = 0

for i in track(range(0, len(cell_names)), description="Finding duplicates"):
    if cell_names[i] in arr:
        print(f"Duplicate found at index {i}: {cell_names[i]}")
    else:
        arr.append(cell_names[i])
    
print("No duplicates found!")