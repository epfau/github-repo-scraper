#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

topics_url = 'https://github.com/topics'

response = requests.get(topics_url)

response.status_code

len(response.text)

page_contents = response.text

page_contents[:1000]

with open('webpage.html', 'w', encoding='utf-8') as f:
    f.write(page_contents)

# Use Beautiful Soup to parse and extract information
# - Parse and explore the structure of downloaded web pages using Beautiful soup.
# - Use the right properties and methods to extract the required information.
# - Create functions to extract from the page into lists and dictionaries.
# - (Optional) Use a REST API to acquire additional information if required.

doc = BeautifulSoup(page_contents, 'html.parser')

selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
topic_title_tags = doc.find_all('p', {'class': selection_class})

len(topic_title_tags)

topic_title_tags[:5]

desc_selector = 'f5 color-fg-muted mb-0 mt-1'
topic_desc_tags = doc.find_all('p', {'class': desc_selector})

# c_desc_tags[:5]

topic_title_tag0 = topic_title_tags[0]

div_tag = topic_title_tag0.parent

topic_link_tags = doc.find_all('a', {'no-underline flex-1 d-flex flex-column'})

len(topic_link_tags)

topic0_url = "https://www.github.com" + topic_link_tags[0]['href']
print(topic0_url)

topic_titles = []
for tag in topic_title_tags:
    topic_titles.append(tag.text)
print(topic_titles)

topic_descs = []
for tag in topic_desc_tags:
    topic_descs.append(tag.text.strip())
topic_descs[:5]

topic_urls = []
base_url = "https://github.com"
for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])
topic_urls

topics_dict = {'Title': topic_titles,
               'Decription': topic_descs,
               'URL': topic_urls,
}

topics_df = pd.DataFrame(topics_dict)

topics_df

# Create CSV file(s) with the extracted information
# - Create functions for the end-to-end process of downloading, parsing, and saving CSVs.
# - Execute the function with different inputs to create a dataset of CSV files.
# - Verify the information in the CSV files by reading them back using Pandas.

topics_df.to_csv('topics.csv', index=None)

# Getting Information Out of a Topic Page

topic_page_url = topic_urls[0]

topic_page_url

response = requests.get(topic_page_url)

response.status_code

len(response.text)

topic_doc = BeautifulSoup(response.text, 'html.parser')

h3_selection_class = "f3 color-fg-muted text-normal lh-condensed"
repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})

len(repo_tags)

a_tags = repo_tags[0].find_all('a')

a_tags[0].text.strip()

a_tags[1].text.strip()

repo_url = base_url + a_tags[1]['href']
print(repo_url)

star_tags = topic_doc.find_all('span', {'class': 'Counter js-social-count'})

len(star_tags)

star_tags[0].text

def parse_star_count(stars_str):
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    return int(stars_str)

parse_star_count(star_tags[0].text)

repo_tags[0]

def get_repo_info(h3_tag, star_tag):
    # returns all the required information about a repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username, repo_name, stars, repo_url

get_repo_info(repo_tags[0], star_tags[0])

topic_repos_dict = {
    'username': [],
    'repo_name': [],
    'stars': [],
    'repo_url': []
}

for i in range (len(repo_tags)):
    repo_info = get_repo_info(repo_tags[i], star_tags[i])
    topic_repos_dict['username'].append(repo_info[0])
    topic_repos_dict['repo_name'].append(repo_info[1])
    topic_repos_dict['stars'].append(repo_info[2])
    topic_repos_dict['repo_url'].append(repo_info[3])

def get_topic_page(topic_url):
    # Download the page
    response = requests.get(topic_url)
    # Check successful response
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    # Parse using BeautifulSoup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def get_repo_info(h3_tag, star_tag):
    # returns all the required information about a repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username, repo_name, stars, repo_url

def get_topic_repos(topic_doc):
    # Get the h3 tags containing repo title, repo URL, and username
    h3_selection_class = "f3 color-fg-muted text-normal lh-condensed"
    repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})
    # Get star tags
    star_tags = topic_doc.find_all('span', {'class': 'Counter js-social-count'})
    # Creating a topic dictionary
    topic_repos_dict = {
        'username': [],
        'repo_name': [],
        'stars': [],
        'repo_url': []
    }
    # Get repo info
    for i in range (len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])

    return pd.DataFrame(topic_repos_dict)

def scrape_topic(topic_url, path):
    if os.path.exists(path):
        print("The file {} already exists. Skipping...".format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path, index = None)

# Write a single function to:
# 1. Get the list of topics from the topics page
# 2. Get the list of top repos from the individual topic pages
# 3. For each topic, create a CSV of the top repos for the topic

def get_topic_titles(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class': selection_class})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles

def get_topic_descs(doc):
    desc_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class': desc_selector})
    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())
    return topic_descs

def get_topic_urls(doc):
    topic_link_tags = doc.find_all('a', {'no-underline flex-1 d-flex flex-column'})
    topic_urls = []
    base_url = "https://github.com"
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])
    return topic_urls

def scrape_topics():
    topics_url = "https://github.com/topics"
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    topics_dict = {
        'Title': get_topic_titles(doc),
        'Description': get_topic_descs(doc),
        'URL': get_topic_urls(doc)
    }
    return pd.DataFrame(topics_dict)

help(os.makedirs)

def scrape_topics_repos():
    print('Scraping list of topics...')
    topics_df = scrape_topics()

    os.makedirs('data', exist_ok=True)
    for index, row in topics_df.iterrows():
        print('Scraping top repositories for "{}"'.format(row['Title']))
        scrape_topic(row['URL'], 'data/{}.csv'.format(row['Title']))

scrape_topics_repos()
