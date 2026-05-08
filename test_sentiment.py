from transformers import pipeline

pipe = pipeline(
    "text-classification",
    model="shashanksrinath/News_Sentiment_Analysis"
)

text = "GameStop shares surge after announcing major expansion plans"

#"GameStop shares surge after announcing major expansion plans"

result = pipe(text)
print(result)