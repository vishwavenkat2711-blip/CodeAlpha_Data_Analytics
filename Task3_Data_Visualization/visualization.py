"""
CodeAlpha - Data Analytics Internship
Task 3: Data Visualization

This script reads the data generated in Task 2 (books_data.csv and
quotes_sentiment.csv) and creates clear, well-labeled visualizations
using Matplotlib and Seaborn to reveal insights and trends.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ---- Load data from Task 2 ----
books_df = pd.read_csv("../Task2_Data_Analytics/books_data.csv")
quotes_df = pd.read_csv("../Task2_Data_Analytics/quotes_sentiment.csv")

# =========================================================
# Chart 1: Price Distribution (Histogram + KDE)
# =========================================================
plt.figure(figsize=(8, 5))
sns.histplot(books_df["price"], bins=15, kde=True, color="steelblue")
plt.title("Distribution of Book Prices", fontsize=14, fontweight="bold")
plt.xlabel("Price (£)")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig("price_histogram.png", dpi=150)
plt.close()
print("Saved: price_histogram.png")

# =========================================================
# Chart 2: Rating vs Average Price (Bar chart)
# =========================================================
avg_price_by_rating = books_df.groupby("rating")["price"].mean().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(x="rating", y="price", data=avg_price_by_rating, hue="rating",
            palette="viridis", legend=False)
plt.title("Average Book Price by Rating", fontsize=14, fontweight="bold")
plt.xlabel("Rating (Stars)")
plt.ylabel("Average Price (£)")
plt.tight_layout()
plt.savefig("avg_price_by_rating.png", dpi=150)
plt.close()
print("Saved: avg_price_by_rating.png")

# =========================================================
# Chart 3: Rating Distribution (Pie chart)
# =========================================================
rating_counts = books_df["rating"].value_counts().sort_index()

plt.figure(figsize=(7, 7))
plt.pie(
    rating_counts,
    labels=[f"{r} Star" for r in rating_counts.index],
    autopct="%1.1f%%",
    startangle=90,
    colors=sns.color_palette("pastel"),
)
plt.title("Proportion of Books by Rating", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("rating_pie_chart.png", dpi=150)
plt.close()
print("Saved: rating_pie_chart.png")

# =========================================================
# Chart 4: Sentiment Breakdown (Bar chart)
# =========================================================
plt.figure(figsize=(8, 5))
sentiment_order = ["Positive", "Neutral", "Negative"]
sns.countplot(x="sentiment", data=quotes_df, order=sentiment_order,
              hue="sentiment", palette="coolwarm", legend=False)
plt.title("Sentiment Breakdown of Quotes", fontsize=14, fontweight="bold")
plt.xlabel("Sentiment")
plt.ylabel("Number of Quotes")
plt.tight_layout()
plt.savefig("sentiment_breakdown.png", dpi=150)
plt.close()
print("Saved: sentiment_breakdown.png")

# =========================================================
# Chart 5: Sentiment Score Distribution (Histogram)
# =========================================================
plt.figure(figsize=(8, 5))
sns.histplot(quotes_df["sentiment_score"], bins=15, kde=True, color="darkorange")
plt.title("Distribution of Sentiment Scores", fontsize=14, fontweight="bold")
plt.xlabel("Sentiment Score (-1 = Negative, +1 = Positive)")
plt.ylabel("Number of Quotes")
plt.tight_layout()
plt.savefig("sentiment_score_distribution.png", dpi=150)
plt.close()
print("Saved: sentiment_score_distribution.png")

print("\nAll Task 3 visualizations created successfully!")