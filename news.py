import requests
from bs4 import BeautifulSoup
import tkinter as tk
import csv
import os

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
titleURL_label = tk.Label(root, text="Enter News URL (USE BBC, CNN, NPR links)")
titleURL_label.pack()
url_entry = tk.Entry(root, width=50,)
url_entry.pack(pady=10)

#output box
output = tk.Text(root, height=10, width=90)
output.pack(pady=10)

headlines_list = [] #headline list to store from websites

def scrape():
    global headlines_list
    headlines_list = []
    url = url_entry.get().strip()

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all('h1')

        output.delete("1.0", tk.END)
        

        for h in headlines:
            text = h.text.strip()
            headlines_list.append(text)
            output.insert(tk.END, h.text.strip() + "\n\n")

    except Exception as e:
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"Error: {e}")
        
def export_csv():
    try:
        file_path = os.path.abspath("headlines.csv")

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Headline"])

            for item in headlines_list:
                writer.writerow([item])

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
    