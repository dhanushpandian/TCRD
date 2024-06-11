import os
import requests

def download_file(url, save_dir, filename=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    local_filename = filename if filename else os.path.basename(url)
    local_path = os.path.join(save_dir, local_filename)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    
    print(f"File downloaded and saved to {local_path}")
    return local_path

if __name__ == "__main__":
    # Example usage
    url = "http://www.ebi.ac.uk/gwas/docs/file-downloads"
    save_dir = "./downloads"
    filename = "gwas_catalog.tsv"  # You can specify the file name or leave it None to use the name from the URL

    download_file(url, save_dir, filename)
