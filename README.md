# Top 100 Somali YouTubers Analysis

This project involves web scraping, data cleaning, and visualization of the top 100 Somali YouTubers. The data is scraped from a website, cleaned for analysis, and visualized using various libraries in Python.

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
Code
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

Data Cleaning
Objective
Clean the scraped data to ensure it is in a usable format.
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

Data Visualization
Objective
Visualize the cleaned data to gain insights.
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

Conclusion
This notebook demonstrates the complete workflow from web scraping to data visualization. Each section is modular and can be expanded or modified based on specific needs. You can upload this notebook to GitHub for sharing and collaboration.
text

### Instructions for Use

1. **Copy the Markdown**: Copy the entire markdown content above into a new Jupyter Notebook cell or a README file in your project.

2. **Run the Code Cells**: Execute each code cell sequentially to perform web scraping, data cleaning, and visualization.

3. **Modify File Paths**: Adjust any file paths as necessary based on your local environment.

This format provides a clear and organized presentation of your project, making it easier for others to understand and replicate your work.
