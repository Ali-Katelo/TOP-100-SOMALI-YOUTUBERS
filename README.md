# Top 100 Somali YouTubers Analysis

**What is the key pain point?**
The Head of Marketing wants to find out who the top YouTubers are in 2024 to decide on which YouTubers would be best to run marketing campaigns throughout the rest of the year.

**What is the ideal solution?**
To create a dashboard that provides insights into the top UK YouTubers in 2024 that includes their

subscriber count
total views
total videos, and
engagement metrics
This will help the marketing team make informed decisions about which YouTubers to collaborate with for their marketing campaigns.

# User story
As the Head of Marketing, I want to use a dashboard that analyses YouTube channel data in the UK .

This dashboard should allow me to identify the top performing channels based on metrics like subscriber base and average views.

With this information, I can make more informed decisions about which Youtubers are right to collaborate with, and therefore maximize how effective each marketing campaign is.

# Data source
URL= 'https://us.youtubers.me/somalia/all/top-1000-most-subscribed-youtube-channels-dentro-somalia' 
What data is needed to achieve our objective?
We need data on the Top 100 Somali YouTubers in 2024 that includes their

1. **Rank**
2. **Youtuber**
3. **Subscriber**
4. **Video-Views**
5. **Video-Counts**
6. **Category**
7. **Started**


Where is the data coming from? The data is sourced from Kaggle (an Excel extract)

## Table of Contents

1. [Installation](#installation)
2. [Web Scraping](#web-scraping)
3. [Data Cleaning](#data-cleaning)
4. [Data Visualization](#data-visualization)
5. [Conclusion](#conclusion)

## Installation

Before running the notebook, ensure you have the required libraries installed. You can install them using pip:

```bash
!pip install beautifulsoup4 requests pandas matplotlib seaborn plotly
```

# Web Scraping
**Objective**
The goal is to extract data about the top YouTubers from a specified URL.
**Code**
```bash
python
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
url = 'https://us.youtubers.me/somalia/all/top-1000-most-subscribed-youtube-channels-dentro-somalia'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Initialize a list to store the data
data = []

# Find the table containing the YouTuber data
table = soup.find('table', class_='top-charts')  # Use the correct class name

if table:
    # Iterate through each row in the table
    for row in table.find_all('tr')[1:]:  # Start from the second row to skip headers
        columns = row.find_all('td')
        if len(columns) >= 6:  # Ensure we have enough columns
            rank = columns.text.strip()
            youtuber = columns[1].text.strip()
            subscribers = columns[2].text.strip()
            video_views = columns.text.strip()
            category = columns.text.strip()  # Adjust index for category
            data.append([rank, youtuber, subscribers, video_views, category])

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(data, columns=['Rank', 'Youtuber', 'Subscribers', 'Video Views', 'Category'])
    print(df)
else:
    print("Table not found. Double-check the website structure and class names.")
```

##  Data Cleaning
# Objective
**Clean the scraped data to ensure it is in a usable format.**
```bash
Code
python
import os

# Load the dataset
file_path = 'Top 100 somalia_youtube_channels.csv'
df = pd.read_csv(file_path)

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
df['Subscribers'] = df['Subscribers'].str.replace(',', '').astype(int)
df['Video Views'] = df['Video Views'].str.replace(',', '').astype(int)
df['Video Count'] = df['Video Count'].str.replace(',', '').astype(int)

# Handle missing values in 'Category' by filling them with 'Unknown'
df['Category'] = df['Category'].fillna('Unknown')

# Remove duplicate rows
df = df.drop_duplicates()

# Strip leading/trailing whitespace from string columns
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Save the cleaned dataset to a new CSV file
cleaned_file_path = 'cleaned_youtube_channels.csv'
df.to_csv(cleaned_file_path, index=False)

# Display the first few rows of the cleaned dataset
print("\nCleaned Data:")
print(df.head())
```

## Data Visualization
# Objective
**Visualize the cleaned data to gain insights.**
```bash
Code
python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Top 10 YouTubers by subscribers
top_youtubers = df.nlargest(10, 'Subscribers')
plt.figure(figsize=(10, 6))
plt.bar(top_youtubers['Youtuber'], top_youtubers['Subscribers'], color='skyblue')
plt.xlabel('Youtuber')
plt.ylabel('Subscribers')
plt.title('Top 10 YouTubers by Subscribers')
plt.xticks(rotation=45)
plt.show()


# Total Video Views by Category
category_views = df.groupby('Category')['Video Views'].sum().sort_values()
plt.figure(figsize=(10, 6))
category_views.plot(kind='bar', stacked=True, color='skyblue')
plt.xlabel('Category')
plt.ylabel('Total Video Views')
plt.title('Total Video Views by Category')
plt.show()

# Growth of YouTube Channels Over Time
channels_per_year = df['Started'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
plt.plot(channels_per_year.index, channels_per_year.values, marker='o', linestyle='-', color='skyblue')
plt.xlabel('Year')
plt.ylabel('Number of Channels Started')
plt.title('Growth of YouTube Channels Over Time')
plt.show()

# Subscribers vs. Video Views
plt.figure(figsize=(10, 6))
plt.scatter(df['Subscribers'], df['Video Views'], color='skyblue')
plt.xlabel('Subscribers')
plt.ylabel('Video Views')
plt.title('Subscribers vs. Video Views')
plt.show()

# Distribution of Categories
category_counts = df['Category'].value_counts()
plt.figure(figsize=(10, 6))
category_counts.plot(kind='pie', autopct='%1.1f%%', colors=plt.cm.Paired.colors)
plt.ylabel('')
plt.title('Distribution of Categories')
plt.show()

# Distribution of Video Counts
plt.figure(figsize=(10, 6))
plt.hist(df['Video Count'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Video Count')
plt.ylabel('Frequency')
plt.title('Distribution of Video Counts')
plt.show()

# Correlation Matrix
correlation_matrix = df[['Subscribers', 'Video Views', 'Video Count']].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Treemap of Subscribers by Category
fig = px.treemap(df, path=['Category'], values='Subscribers', title='Subscribers by Category')
fig.show()
```

## Conclusion
The project on analyzing the top 100 Somali YouTubers has successfully demonstrated a comprehensive workflow that encompasses web scraping, data cleaning, and visualization. Through the process of web scraping, we were able to gather valuable data regarding the most subscribed Somali YouTubers from a specified online source. This data included key metrics such as subscriber counts, video views, and content categories, which are essential for understanding the landscape of Somali content creators on YouTube.
After collecting the data, we undertook a rigorous cleaning process to ensure its accuracy and usability. This included handling missing values, converting data types for numerical analysis, and removing duplicates. The cleaned dataset provides a solid foundation for further analysis and insights.
The visualization phase highlighted key trends and patterns within the data. We created various plots, including bar charts for the top YouTubers, pie charts for category distributions, and scatter plots to explore the relationship between subscribers and video views. These visualizations not only made the data more accessible but also revealed significant insights into the popularity and reach of different content categories.
Overall, this project not only sheds light on the current state of Somali YouTubers but also serves as a valuable resource for anyone interested in digital content creation in Somalia. The methodologies applied can be adapted for similar analyses in different contexts, making this work a versatile reference for future projects.
Future work could involve a deeper analysis of trends over time, exploring factors that contribute to the success of these YouTubers, and potentially expanding the dataset to include more channels or additional metrics. This analysis has laid the groundwork for understanding the dynamics of YouTube as a platform for Somali creators, and it opens the door for further exploration in this vibrant digital space.



