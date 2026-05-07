import requests
from bs4 import BeautifulSoup
import tkinter as tk
import csv
import os
import time #prevent rate limits

# Allowed sites
# https://www.bbc.com/business
# https://www.cnn.com/business
# https://www.npr.org/sections/business/

# Requesting website
# URL_web = input("Enter URL: ")


#creating window for scraper
root = tk.Tk()
root.title("News Sentiment")
root.geometry("800x800")

#input box
titleURL_label = tk.Label(root, text="Enter News URL (USE BBC, CNN, NPR links). Make sure you have https://")
titleURL_label.pack()
#url_entry = tk.Entry(root, width=50,)
#url_entry.pack(pady=10)

#trying multiple links

url_entry= tk.Text(root, height=5, width=70)
url_entry.pack(pady=10)

#output box
output = tk.Text(root, height=10, width=90)
output.pack(pady=10)

headlines_list = [] #headline list to store from websites

def scrape():
    global headlines_list
    headlines_list = []

    raw_urls = url_entry.get("1.0", tk.END).strip()
    urls = raw_urls.splitlines()

    headers = {"User-Agent": "Mozilla/5.0"}

    output.delete("1.0", tk.END)

    for url in urls:
        url = url.strip()

        try:
            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = soup.find_all('h1')

            for h in headlines:
                text = h.text.strip()
                headlines_list.append((url, text))
                output.insert(tk.END, text + "\n\n")
                
            time.sleep(2)

        except Exception as e:
            output.insert(tk.END, f"Error with {url}: {e}\n\n")
        
def export_csv():
    try:
        file_path = os.path.abspath("headlines.csv")

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Headline"])

            for url, item in headlines_list:
                writer.writerow([url, item])

        status_label.config(
            text=f"Export successful! Saved to:\n{file_path}",
            fg="green"
        )

    except Exception as e:
        status_label.config(
            text=f"Export failed: {e}",
            fg="red"
        )

#headers = {"User-Agent": "Mozilla/5.0"}
#response = requests.get(URL_web, headers=headers)
#print("The response code is : ", response)

#Parsing HTML Document
#soup=BeautifulSoup(response.content,'html.parser')

#Extract headline
#headlines=soup.find_all('h1')
#for headline in headlines:
#    print(headline.text, "\n")
    
export_button = tk.Button(root, text="Export CSV", command=export_csv)
export_button.pack()

button = tk.Button(root, text="Scrape", command=scrape)
button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
    