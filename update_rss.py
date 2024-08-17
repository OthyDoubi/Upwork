import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import pytz

def fetch_upwork_jobs():
    url = "https://www.upwork.com/nx/search/jobs/?client_hires=1-9,10-&nbs=1&payment_verified=1&q=graphic%20designer&sort=recency"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []
    for job in soup.find_all('section', class_='up-card-section'):
        title = job.find('h4', class_='job-title').text.strip()
        link = "https://www.upwork.com" + job.find('a', class_='job-title-link')['href']
        description = job.find('span', class_='job-description').text.strip()
        jobs.append({
            'title': title,
            'link': link,
            'description': description
        })
    return jobs

def update_rss_feed(jobs):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = 'Offres Upwork pour Graphic Designer'
    ET.SubElement(channel, 'link').text = 'https://www.upwork.com/nx/search/jobs/?client_hires=1-9,10-&nbs=1&payment_verified=1&q=graphic%20designer&sort=recency'
    ET.SubElement(channel, 'description').text = 'Les dernières offres pour les designers graphiques sur Upwork'
    ET.SubElement(channel, 'language').text = 'fr'

    for job in jobs:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = job['title']
        ET.SubElement(item, 'link').text = job['link']
        ET.SubElement(item, 'description').text = job['description']
        ET.SubElement(item, 'pubDate').text = datetime.now(pytz.UTC).strftime('%a, %d %b %Y %H:%M:%S %z')

    tree = ET.ElementTree(rss)
    tree.write('upwork_graphic_designer_feed.xml', encoding='UTF-8', xml_declaration=True)
    print(f"Nombre d'offres récupérées : {len(jobs)}")

def main():
    jobs = fetch_upwork_jobs()
    update_rss_feed(jobs)
    print("Flux RSS mis à jour avec succès.")

if __name__ == "__main__":
    main()
