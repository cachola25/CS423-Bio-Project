## To get the metadata information from the Mair et al research:
    1.  Navigate to https://zenodo.org/records/6556290#.YoOCXGBBwrk and download the RDS file inside the CS423_Bio Project/R directory
    2.  Then, in the CS423_Bio Project/R directory, run the celltype.R script and wait for it to complete. You should end up with a metadata.csv file.
    3.  Then, navigate to the Python directory and run 'python add_gsm.py' to assign each cell to a GSMID
    4.  The information is now properly preprocessed


## To get the CSV data files:
  ### Prerequisites:
    1.	Python and access to a terminal: Download Python from the Python website
    2.	Navigate to the Python directory
  ### Instructions:
    1.	You must first run 'python download.py' to get the necessary files
    2.	You must then run 'python process_data.py' to create the initial gene count files
            a. You will be prompted to input which priority directory you would like to process [1 - 4]. To proceed with a 
               processing a priority directory, you must run this script on that priority first
    3.	Then run 'python get_GOI_info.py' to filter the gene count files for the specific genes we're looking for
            a. You will once again be prompted to enter a priority directory and you must run this to proceed with getting the final gene
               counts for that directory.
    4.	You can then run 'python [overall,sample]_barcode_counts.py' to get the final gene counts for each cell
  ### Troubleshooting:
    Missing Packages: If you encounter any errors related to missing packages during the installation or runtime process, follow the instructions to install the missing packages.


## For the HeatMap Generator:
 ### Prerequisites:
    1.	R and RStudio: Download R and RStudio from the RStudio website.
  ### Installation Instructions:
    1.	Download the Code: Download the provided R code and files from the Github repository.
    2.	Open RStudio: Launch Rstudio on your system.
    3.	Open the R Project: In RStudio, navigate to the location where you saved the repository. Open the R project file (usually ends with ‘.Rproj’).
    4.	Install Required Packages: If prompted, install any missing R packages that are required for the application to run. RStudio will display a message in the console indicating which packages are           missing. You can install these packages by clicking the “Install” button that appears in the console. 
  ### Running the Application:
    1.	Run the App: In RStudio, open the main R script file (heatmap_generator.R). 
    2.	Click “Run App”: Once the script is open, you will find a button labeled “Run App” at the top of the script editor window. Click this button to launch the application.
    3.	Using the Application: After clicking “Run App”, a new window should open displaying the application interface. Here you can upload your CSV file and generate its heatmap.
    4.	Open in Browser (Optional): For a smoother experience, you can click the “Open in Browser” button within the application window. This will open the application in your default web browser.
  ### Troubleshooting:
    Missing Packages: If you encounter any errors related to missing packages during the installation or runtime process, follow the instructions to install the missing packages as described above. 
