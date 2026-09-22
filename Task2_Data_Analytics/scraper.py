import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Step 1: Scrape the site ----
titles = []
prices = []
ratings = []

for page in range(1, 6):  # scrape first 5 pages
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]
        titles.append(title)
        prices.append(price)
        ratings.append(rating)

print(f"Scraped {len(titles)} books")

# ---- Step 2: Clean and save data ----
df = pd.DataFrame({"title": titles, "price": prices, "rating": ratings})
df["price"] = df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
df["rating"] = df["rating"].map(rating_map)

df.to_csv("books_data.csv", index=False)
print(df.head())

# ---- Step 3: Explore the data (EDA) ----
print(df.info())
print(df.describe())
print("Missing values:\n", df.isnull().sum())

# ---- Step 4: Visualize ----
plt.figure(figsize=(8,5))
sns.histplot(df["price"], bins=15, kde=True)
plt.title("Distribution of Book Prices")
plt.xlabel("Price (£)")
plt.savefig("price_distribution.png")
plt.show()

plt.figure(figsize=(6,4))
sns.countplot(x="rating", data=df, palette="viridis")
plt.title("Book Ratings Count")
plt.xlabel("Rating (stars)")
plt.savefig("ratings_count.png")
plt.show()