import requests
import random
import string
import os
import time
import threading
import queue
from plugins.log import log
from colorama import Fore
import colorama

colorama.init()

MAX_RETRIES = 2
DELAY = 3
NUM_WORKERS = 10

file_count = 0
total_size = 0
proxies = None  


def ask_for_proxies():

    """Function to ask the user if they want to use proxies and whether they want to use a file with proxies"""
    global proxies
    use_proxies = input("Do you want to use proxies? (y/n): ").lower()
    
    if use_proxies == "y":
        proxy_type = input("Enter proxy type (http/https/socks5): ").lower()
        proxy_mode = input("Do you want to use a single proxy or load proxies from a file? (single/file): ").lower()
        
        if proxy_mode == "single":
            proxy_address = input(f"Enter {proxy_type} proxy (IP:Port): ").strip()
            proxies = [{proxy_type: f"http://{proxy_address}"}]
            log("proxy_set", f"Using single proxy: {proxy_address}")
        
        elif proxy_mode == "file":
            proxy_file = input("Enter the path to the proxy file: ").strip()
            try:
                with open(proxy_file, "r") as file:
                    proxy_addresses = file.readlines()
                    proxy_addresses = [proxy.strip() for proxy in proxy_addresses] 
                    proxies = [{proxy_type: f"http://{proxy}"} for proxy in proxy_addresses]
                log("proxy_set", f"Loaded {len(proxies)} proxies from file.")
            except FileNotFoundError:
                print("Error: The specified proxy file was not found.")
                proxies = None
        
        else:
            print("Invalid option. Not using proxies.")
            proxies = None

    else:
        log("no_proxy", "Not using proxies.")
        proxies = None


def retry_request(url, max_retries=MAX_RETRIES, delay=DELAY):
    update_count()
    for attempt in range(max_retries):
        try:
            update_count()
            if proxies:
                proxy = random.choice(proxies) 
                response = requests.get(url, stream=True, proxies=proxy)
            else:
                response = requests.get(url, stream=True)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            log("error_request", f"Attempt {attempt + 1} failed: {str(e)}")
            time.sleep(delay)
            update_count()
    return None

def download_file(url, folder_path):
    update_count()
    global file_count, total_size
    log("downloading", f"{url}")
    filename = os.path.basename(url)
    ext = os.path.splitext(filename)[1].lstrip('.')
    ext_folder = os.path.join(folder_path, ext if ext else "other")
    os.makedirs(ext_folder, exist_ok=True)
    file_path = os.path.join(ext_folder, filename)
    update_count()
    response = retry_request(url)
    if not response:
        archive_url = f"https://web.archive.org/web/10190205175555if_/{url}"
        response = retry_request(archive_url)
        update_count()
        if not response:
            log("error_download", f"Failed to download {url} from both sources.")
            update_count()
            return False
    
    try:
        update_count()
     
        file_size = 0
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                file_size += len(chunk)
        
     
        file_count += 1
        total_size += file_size

  
        size_mb = file_size / (1024 * 1024)
        log("download_success", f"Downloaded {filename} to {file_path}, Size: {size_mb:.2f} MB")
        
     
        update_count()

        return True
    except Exception as e:
        log("error_saving_file", f"Error saving {filename}: {str(e)}")
        return False


def update_count():
    """Function to update the download count and size in the console"""
    print(Fore.YELLOW + f"Downloaded: {file_count} files, Size: {total_size / (1024 * 1024):.2f} MB", end='\r')

def worker(queue, folder_path):
    while True:
        url = queue.get()
        if url is None:
            break
        download_file(url, folder_path)
        queue.task_done()

def grab_links(domain):
    global proxies
  
    ask_for_proxies()
    
    url = f"https://web.archive.org/cdx/search/cdx?url=*.[{domain}]/*&collapse=urlkey&output=text&fl=original"
    log("get_links", domain)
    
    response = retry_request(url)
    if not response:
        log("error_grabbing_links", "Failed to retrieve links after multiple attempts.")
        return
    
    links = response.text.splitlines()
    log("links_grabbed", len(links))
    
    save_or_continue = input("Do you want to save the links in a file? (y/n): ").lower()
    
    if save_or_continue == "y":
        filename = f"links-{random.randint(1000, 9999)}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write('\n'.join(links))
        log("file_saved", filename)
    elif save_or_continue == "n":
        log("continue_with_extensions")
        extensions = []
        while True:
            print("Choose file extensions to grab:")
            print("1: .php, .html, .htm")
            print("2: .pdf, .xls, .xlsx")
            print("3: .txt, .doc, .docx")
            print("4: Add custom extensions")
            print("5: All important files")
            choice = input("Select an option or type 'done': ").strip()
            
            if choice == "1":
                extensions += [".php", ".html", ".htm"]
            elif choice == "2":
                extensions += [".pdf", ".xls", ".xlsx"]
            elif choice == "3":
                extensions += [".txt", ".doc", ".docx"]
            elif choice == "4":
                custom_ext = input("Enter your extensions (comma separated): ").split(",")
                extensions.extend([ext.strip() for ext in custom_ext])
            elif choice == "5":
                extensions = [
                    ".php", ".html", ".htm", ".pdf", ".xls", ".xlsx", ".txt", ".doc", ".docx", 
                    ".log", ".db", ".js", ".css", ".xml", ".json", ".csv", ".yaml", ".md", 
                    ".rtf", ".ppt", ".pptx", ".odt", ".ods", ".iso", ".tar", ".zip", ".gz", 
                    ".7z", ".bak", ".swp", ".img", ".bin", ".exe", ".dll", ".tar.gz", 
                    ".sqlite", ".dbf", ".mdb", ".jsonld", ".xsd", ".xsl", ".apk", ".ipa", 
                    ".jar", ".dmg", ".psd", ".ai", ".eps", ".cdr", ".indd", ".epub"
                ]
                break
            elif choice.lower() == "done":
                if not extensions:
                    print("No extensions selected. Please select at least one extension.")
                else:
                    break
            else:
                print("Invalid choice, try again.")
        
        log("extensions_selected", ", ".join(extensions))
        filtered_links = [link for link in links if any(link.endswith(ext) for ext in extensions)]
        if filtered_links:
            folder_path = f"results/{random.randint(1000, 9999)}"
            os.makedirs(folder_path, exist_ok=True)
            
            q = queue.Queue()
            threads = []
            for _ in range(NUM_WORKERS):
                t = threading.Thread(target=worker, args=(q, folder_path))
                t.start()
                threads.append(t)
            
            for link in filtered_links:
                q.put(link)
            
            q.join()
            for _ in range(NUM_WORKERS):
                q.put(None)
            for t in threads:
                t.join()
            
            log("filtered_links_saved", folder_path)
        else:
            log("no_filtered_links", "No matching links found.")
    else:
        log("invalid_choice", "Invalid input. Please choose 'y' or 'n'.")

