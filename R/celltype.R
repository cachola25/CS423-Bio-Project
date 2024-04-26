# Load the Seurat package
library(Seurat)

# Read in the RDS File from the research paper
seurat_object <- readRDS("CD3_and_HLADR_integrated_clean_HARMONY_NEW.RDS")

# Extract the metadata
metadata <- seurat_object@meta.data

# Write the metadata to a CSV file
write.csv(metadata, file = "metadata.csv")
