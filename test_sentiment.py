from transformers import pipeline

pipe = pipeline(
    "text-classification",
    model="shashanksrinath/News_Sentiment_Analysis"
)

text = "The company released its quarterly earnings report on Monday." 

#"GameStop shares surge after announcing major expansion plans"

result = pipe(text, top_k=None)
print(result)