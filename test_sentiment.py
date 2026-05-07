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

print(sentiment_model.model.config.id2label)

print(sentiment_model("I love this")[0])
print(sentiment_model("I hate this")[0])
print(sentiment_model("This is okay")[0])