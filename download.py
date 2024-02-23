from urllib.parse import urlparse, unquote # to process a URL and get the filename
from bs4 import BeautifulSoup # to parse the HTML
from tqdm import tqdm # to create the progress bar
import pandas as pd # to read in the spreadsheet
import requests # to make the request to the website
import os # to get directory information
import subprocess # to run shell commands

# A python script to download the barcode, genes, and matrix files from the GEO database
# Will download everything specified in the bio_files.csv file
# Takes ~20 minutes to download everything


if __name__ == "__main__":
    # Read in spreadsheet to get the GSM links and create the website URL for each link
    bio_files = pd.read_csv("bio_files.csv")
    links = []
    for link in bio_files["link"]:
        links.append("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=" + link)
    
    # Loop through each download link and try to download the barcode, genes, and matrix files
    for link in links:
        
        # Try to make a request and report if there was an error
        try:
            
            # Load the webpage and parse the HTML
            page = requests.get(link)
            soup = BeautifulSoup(page.content, "html.parser")
            
            # Find all hyperlinks
            a_link = soup.find_all("a")
            
            # Find all the (http) download links
            http_links = []
            for link in a_link:
                checking = link.get('href', '')
                if checking.startswith("/geo/download"):
                    http_links.append(checking)
            
            # Format each download link to be used in the requests.get() function
            download_links = []
            for http_link in http_links:
                download_links.append("https://www.ncbi.nlm.nih.gov" + http_link)
                
            # Try to download each file
            for download in download_links:
                response = requests.get(download, stream=True)
                if response.status_code == 200:
                    # query is the attribute of the URL that contains the filename
                    url_query = urlparse(unquote(download)).query
                    
                    # Isolate the only part of the query that contains the filename
                    filename = url_query[url_query.find("&file=")+6:]
                    
                    # Get the current working directory and create a new directory for the files
                    directory = subprocess.run(["pwd"],capture_output=True, text=True).stdout.strip()
                    
                    # Isolate only the GSM number from the filename
                    lookup = [filename[:filename.find("_")]]
                    
                    # Navigate to the right priority folder and create a new directory for the files
                    priority = bio_files.loc[bio_files["link"] == lookup[0], "priority"].values[0]
                    directory += "/data_files/priority_" + str(priority) + "/" + filename[:filename.find("_")]
                    
                    # Make directory if it doesn't exist
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                        
                    # Create the file path and download the file
                    filepath = os.path.join(directory, filename)
                    
                    # Create a progress bar so that we can see the progress and tell if the program hangs
                    total_size = int(response.headers.get('Content-Length', 0))
                    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc="Downloading " + filename)
                    
                    # Get the file and the file contents
                    with open(filepath, "wb") as f:
                        for data in response.iter_content(chunk_size=1024):
                            f.write(data)
                            progress_bar.update(len(data))
                    
                    # Close the progress bar and unzip the file
                    subprocess.run(["gunzip", filepath])
            progress_bar.close()
        except requests.exceptions.Timeout:
            print("Timeout occurred")

        except requests.exceptions.TooManyRedirects:
            print("Too many redirects")

        except requests.exceptions.RequestException as e:
            print("There was an ambiguous exception that occurred while handling your request.", e)