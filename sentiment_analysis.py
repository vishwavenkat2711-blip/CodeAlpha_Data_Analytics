import requests
from bs4 import BeautifulSoup
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Step 1: Scrape quotes ----
quotes = []
authors = []

for page in range(1, 6):  # first 5 pages
    url = f"http://quotes.toscrape.com/page/{page}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quote_blocks = soup.find_all("div", class_="quote")

    for block in quote_blocks:
        text = block.find("span", class_="text").text
        author = block.find("small", class_="author").text
        quotes.append(text)
        authors.append(author)

print(f"Scraped {len(quotes)} quotes")

# ---- Step 2: Sentiment analysis ----
analyzer = SentimentIntensityAnalyzer()

sentiments = []
scores = []

for quote in quotes:
    score = analyzer.polarity_scores(quote)
    compound = score["compound"]
    scores.append(compound)

    if compound >= 0.05:
        sentiments.append("Positive")
    elif compound <= -0.05:
        sentiments.append("Negative")
    else:
        sentiments.append("Neutral")

# ---- Step 3: Save results ----
df = pd.DataFrame({
    "quote": quotes,
    "author": authors,
    "sentiment_score": scores,
    "sentiment": sentiments
})

df.to_csv("quotes_sentiment.csv", index=False)
print(df.head())
print("\nSentiment counts:")
print(df["sentiment"].value_counts())

# ---- Step 4: Visualize ----
plt.figure(figsize=(6,4))
sns.countplot(x="sentiment", data=df, hue="sentiment", palette="coolwarm", legend=False)
plt.title("Quote Sentiment Distribution")
plt.savefig("sentiment_distribution.png")
plt.show()