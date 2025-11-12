import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('movies.csv')
print("Dataset loaded successfully!\n")

# Show first few rows
print(df.head(), "\n")

# Average rating per movie
avg_ratings = df.groupby('Title')['Rating'].mean().sort_values(ascending=False)
print("Average Rating per Movie:\n", avg_ratings, "\n")

# Average rating per genre
genre_avg = df.groupby('Genre')['Rating'].mean().sort_values(ascending=False)
print("Average Rating per Genre:\n", genre_avg, "\n")

# Count of ratings per genre
genre_count = df['Genre'].value_counts()
print("Number of Ratings per Genre:\n", genre_count, "\n")

# Plot 1: Average rating by genre
genre_avg.plot(kind='bar', color='skyblue', title='Average Rating by Genre')
plt.ylabel('Average Rating')
plt.tight_layout()
plt.savefig('avg_rating_by_genre.png')
plt.close()

# Plot 2: Number of ratings by genre
genre_count.plot(kind='bar', color='lightgreen', title='Ratings Count by Genre')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('ratings_count_by_genre.png')
plt.close()

print("✅ Analysis complete! Charts saved in your folder.")
