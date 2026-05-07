import requests
from bs4 import BeautifulSoup
import tkinter as tk
import csv
import os
import time #prevent rate limits

from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="ozanba/news_sentiment_stock"
)

# Allowed sites
# https://www.bbc.com/business
# https://www.cnn.com/business
# https://www.npr.org/sections/business/

# Requesting website
# URL_web = input("Enter URL: ")

# This is Ryan


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
                for h in headlines:
                    text = h.text.strip()

                    #refactor for model
                    result = sentiment_model(text)[0]
                    raw_label = result["label"] # pulling from huggingface LM
                    label = convert_label(raw_label) # converting
                    score = result["score"]
                    result = sentiment_model(text)[0]

                    headlines_list.append((url, text, label, score))
                    
                output.insert(tk.END, text + "\n\n")
                
            time.sleep(2)

        except Exception as e:
            output.insert(tk.END, f"Error with {url}: {e}\n\n")
        
def export_csv():
    try:
        file_path = os.path.abspath("headlines.csv")

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Headline", "Sentiment", "Confidence"])

            for url, text, label, score in headlines_list:
                writer.writerow([url, text, label, score])

        status_label.config(
            text=f"Export successful! Saved to:\n{file_path}",
            fg="green"
        )

    except Exception as e:
        status_label.config(
            text=f"Export failed: {e}",
            fg="red"
        )
        
def show_results():
    output.delete("1.0", tk.END)

    for url, text, label, score in headlines_list:

        # choose color
        if label.lower() == "positive":
            color = "green"
        elif label.lower() == "negative":
            color = "red"
        else:
            color = "orange"

        output.insert(tk.END, f"{url}\n{text}\n{label} ({score:.2f})\n\n")

        # apply color to last inserted block
        start_index = output.index("end-3l linestart")
        end_index = output.index("end-1l lineend")

        output.tag_add(color, start_index, end_index)
        output.tag_config(color, foreground=color)
        
def convert_label(label): #Mapping labels for the huggingface LM
    # refactor this code to account for new LM
    mapping = {
        "LABEL_0": "negative",
        "LABEL_1": "neutral",
        "LABEL_2": "positive"
    }
    return mapping.get(label, label)

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

show_button = tk.Button(root, text="Show Results", command=show_results)
show_button.pack()

button = tk.Button(root, text="Scrape", command=scrape)
button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()

