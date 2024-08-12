
"""TOP 100 SOMALI YOUTUBERS



Original file is located at
    https://colab.research.google.com/drive/1AifQGihFzdkBIij1RHYBhk9fRmEXRj0P
"""

!pip install beautifulsoup4 requests pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://us.youtubers.me/somalia/all/top-1000-most-subscribed-youtube-channels-dentro-somalia'
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

data = []
table = soup.find('table', class_='top-charts')  # Use the correct class name
if table:
    for row in table.find_all('tr')[1:]:  # Start from the second row to skip headers
        columns = row.find_all('td')
        if len(columns) >= 6:  # Ensure we have enough columns
            rank = columns[0].text.strip()
            youtuber = columns[1].text.strip()
            subscribers = columns[2].text.strip()
            video_views = columns[3].text.strip()
            category = columns[5].text.strip()  # Adjust index for category
            data.append([rank, youtuber, subscribers, video_views, category])

    df = pd.DataFrame(data, columns=['Rank', 'Youtuber', 'Subscribers', 'Video Views', 'Category'])
    print(df)
else:
    print("Table not found. Double-check the website structure and class names.")

import pandas as pd
import os

# Load the dataset
file_path = 'Top 100 somalia_youtube_channels.csv'
df = pd.read_csv('Top 100 somalia_youtube_channels.csv')

# Display the first few rows of the dataset
print("Original Data:")
print(df.head())

# Get basic information about the dataset
print("\nDataset Info:")
df.info()

# Get summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Convert 'subscribers', 'video views', and 'video count' to integers
df['subscribers'] = df['subscribers'].str.replace(',', '').astype(int)
df['video views'] = df['video views'].str.replace(',', '').astype(int)
df['video count'] = df['video count'].str.replace(',', '').astype(int)

# Handle missing values in 'category' by filling them with 'Unknown'
df['category'] = df['category'].fillna('Unknown')

# Remove duplicate rows
df = df.drop_duplicates()

# Strip leading/trailing whitespace from string columns
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Save the cleaned dataset to a new CSV file
cleaned_file_path = '/mnt/data/cleaned_youtube_channels.csv'

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(cleaned_file_path), exist_ok=True)

df.to_csv(cleaned_file_path, index=False)

# Display the first few rows of the cleaned dataset
print("\nCleaned Data:")
print(df.head())

# Get basic information about the cleaned dataset
print("\nCleaned Dataset Info:")
df.info()

# Get summary statistics of the cleaned dataset
print("\nCleaned Summary Statistics:")
print(df.describe())

# Check for missing values in the cleaned dataset
print("\nCleaned Missing Values:")
print(df.isnull().sum())

import matplotlib.pyplot as plt

# Get top 10 YouTubers by subscribers
top_youtubers = df.nlargest(10, 'subscribers')

plt.figure(figsize=(10, 6))
plt.bar(top_youtubers['Youtuber'], top_youtubers['subscribers'], color='skyblue')
plt.xlabel('Youtuber')
plt.ylabel('Subscribers')
plt.title('Top 10 YouTubers by Subscribers')
plt.xticks(rotation=45)
plt.show()

category_views = df.groupby('category')['video views'].sum().sort_values()

plt.figure(figsize=(10, 6))
category_views.plot(kind='bar', stacked=True, color='skyblue')
plt.xlabel('Category')
plt.ylabel('Total Video Views')
plt.title('Total Video Views by Category')
plt.show()

channels_per_year = df['started'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.plot(channels_per_year.index, channels_per_year.values, marker='o', linestyle='-', color='skyblue')
plt.xlabel('Year')
plt.ylabel('Number of Channels Started')
plt.title('Growth of YouTube Channels Over Time')
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(df['subscribers'], df['video views'], color='skyblue')
plt.xlabel('Subscribers')
plt.ylabel('Video Views')
plt.title('Subscribers vs. Video Views')
plt.show()

category_counts = df['category'].value_counts()

plt.figure(figsize=(10, 6))
category_counts.plot(kind='pie', autopct='%1.1f%%', colors=plt.cm.Paired.colors)
plt.ylabel('')
plt.title('Distribution of Categories')
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(df['video count'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Video Count')
plt.ylabel('Frequency')
plt.title('Distribution of Video Counts')
plt.show()

import seaborn as sns

correlation_matrix = df[['subscribers', 'video views', 'video count', 'started']].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

import plotly.express as px

fig = px.treemap(df, path=['category'], values='subscribers', title='Subscribers by Category')
fig.show()
