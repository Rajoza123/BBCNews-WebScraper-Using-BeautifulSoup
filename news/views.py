# scraper/views.py
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import News
def scrape_sports(request):
    url = 'https://www.bbc.com/sport'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    index=0
    headlines = []
    links = []
    imagelink=[]
    for item in soup.find_all('div', class_="ssrcss-1f3bvyz-Stack e1y4nx260"):  
        headline_tag = item.find('p', class_="ssrcss-1b1mki6-PromoHeadline exn3ah96")
        if headline_tag:
            headline_text = headline_tag.text.strip()
        
        
            if index == 0:
                index += 1
                continue  # Skip the first iteration
        
            headlines.append(headline_text)

        link_tag = item.find('a', class_='ssrcss-zmz0hi-PromoLink exn3ah91', href=True)
        if link_tag:
            href_value = link_tag['href']
            links.append(f'http://bbc.com{href_value}')        
    image_divs = soup.find_all('div', class_='ssrcss-fec6qv-ImageWrapper en81kx33')
    image_sources = []
    for index, image_div in enumerate(image_divs):
        if index == 0:
            continue  
        img_tag = image_div.find('img')  # Find the <img> tag
        if img_tag and 'src' in img_tag.attrs:
            img_src = img_tag['src']  # Get the src value
            image_sources.append(img_src)  # Add to the list
    news = zip(headlines, links , image_sources)
    search_query = request.GET.get('q', '')
    if search_query:
        news = filter(lambda x: search_query.lower() in x[0].lower(), news)
    return render(request, 'sports.html',{'context':news,'search_query': search_query})


def scrape_entertainment(request):
    url = 'https://www.bbc.com/culture'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    image_sources = []
    headlines = []

# Counter to skip the first 8 links and images
    skip_count = 0

# Scraping links and images
    for item in soup.find_all('a', {"data-testid": "internal-link", 'class': "sc-2e6baa30-0 gILusN"}):  
        if skip_count < 8:
            skip_count += 1
            continue  # Skip first 8 links and images

    # Get the link (href)
        link_tag = item['href']
        if link_tag:
            links.append(f'https://www.bbc.com{link_tag}')

    # Get the image src from <img> tag inside <div>
        img_tag = item.find('img', class_="sc-a34861b-0 efFcac")
        if img_tag and 'src' in img_tag.attrs:
            img_src = img_tag['src']
            if img_src not in image_sources:  # Check to avoid duplicate images
                image_sources.append(img_src)

# Scraping headlines
    for headline in soup.find_all("h2", {"data-testid": "card-headline", "class": "sc-4fedabc7-3 zTZri"}):
        headline_text = headline.text.strip()  # Extract and clean the text
        if headline_text:  # Check if there's text content
            headlines.append(headline_text)  # Append the headline to the list

# Combine the headlines, links, and image sources into a zipped list
    news = zip(headlines, links, image_sources)
    print(headlines)
# Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        news = filter(lambda x: search_query.lower() in x[0].lower(), news)

# Pass the zipped news object to the template
    return render(request, 'entertainment.html', {'context': news, 'search_query': search_query})


def scrape_business(request):
    url = 'https://www.bbc.com/business'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    image_sources = []
    headlines =[] 
    skip_count = 0
    # Scraping links and images
    for item in soup.find_all('a', {"data-testid": "internal-link", 'class':"sc-2e6baa30-0 gILusN"}):  
        if skip_count < 5:
            skip_count += 1
            continue 
        link_tag = item['href']
        if link_tag:
            links.append(f'https://www.bbc.com{link_tag}')

        # Get the image src from <img> tag inside <div>
        img_tag = item.find('img', class_="sc-a34861b-0 efFcac")
        if img_tag and 'src' in img_tag.attrs:
            img_src = img_tag['src']
            image_sources.append(img_src)
    first_headline = soup.find("h2", {"data-testid": "card-headline", "class": "sc-4fedabc7-3 dsoipF"})
    if first_headline:
        first_headline_text = first_headline.text.strip()
        print(f"First headline: {first_headline_text}")
        headlines.append(first_headline_text)

    for headline in soup.find_all("h2", {"data-testid": "card-headline", "class": "sc-4fedabc7-3 zTZri"}):
        headline_text = headline.text.strip()  # Extract and clean the text
        if headline_text:  # Check if there's text content
            headlines.append(headline_text)  # Append the headline to the list

    # Combine the links and image sources into a zipped list
    news = zip(headlines,links, image_sources)
    # print(headlines)
    
    search_query = request.GET.get('q', '')
    if search_query:
        news = filter(lambda x: search_query.lower() in x[0].lower(), news)
    
    return render (request,'business.html',{'context': news, 'search_query': search_query})


def scrape_sports_top():
    url = 'https://www.bbc.com/sport'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = []
    links = []
    image_sources = []
    index = 0

    for item in soup.find_all('div', class_="ssrcss-1f3bvyz-Stack e1y4nx260"):  
        headline_tag = item.find('p', class_="ssrcss-1b1mki6-PromoHeadline exn3ah96")
        if headline_tag:
            headline_text = headline_tag.text.strip()
            if index == 0:
                index += 1
                continue  # Skip the first iteration
            headlines.append(headline_text)

        link_tag = item.find('a', class_='ssrcss-zmz0hi-PromoLink exn3ah91', href=True)
        if link_tag:
            href_value = link_tag['href']
            links.append(f'http://bbc.com{href_value}')

    image_divs = soup.find_all('div', class_='ssrcss-fec6qv-ImageWrapper en81kx33')
    for index, image_div in enumerate(image_divs):
        if index == 0:
            continue  
        img_tag = image_div.find('img')  
        if img_tag and 'src' in img_tag.attrs:
            img_src = img_tag['src']
            image_sources.append(img_src)

    news = zip(headlines[:3], links[:3], image_sources[:3])  # Top 3 news
    return list(news)

def scrape_entertainment_top():
    url = 'https://www.bbc.com/culture'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    image_sources = []
    headlines = []

    skip_count = 0
    for item in soup.find_all('a', {"data-testid": "internal-link", 'class': "sc-2e6baa30-0 gILusN"}):  
        if skip_count < 8:
            skip_count += 1
            continue

        link_tag = item['href']
        if link_tag:
            links.append(f'https://www.bbc.com{link_tag}')

        img_tag = item.find('img', class_="sc-a34861b-0 efFcac")
        if img_tag and 'src' in img_tag.attrs:
            img_src = img_tag['src']
            if img_src not in image_sources:
                image_sources.append(img_src)

    for headline in soup.find_all("h2", {"data-testid": "card-headline", "class": "sc-4fedabc7-3 zTZri"}):
        headline_text = headline.text.strip()
        if headline_text:
            headlines.append(headline_text)

    news = zip(headlines[:3], links[:3], image_sources[:3])  # Top 3 news
    return list(news)

def scrape_business_top():
    url = 'https://www.bbc.com/business'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headlines = []
    links = []
    image_sources = []
    skip_count = 0

    for item in soup.find_all('a', {"data-testid": "internal-link", 'class': "sc-2e6baa30-0 gILusN"}):  
        if skip_count < 5:
            skip_count += 1
            continue
        link_tag = item['href']
        if link_tag:
            links.append(f'https://www.bbc.com{link_tag}')

        img_tag = item.find('img', class_="sc-a34861b-0 efFcac")
        if img_tag and 'src' in img_tag.attrs:
            img_src = img_tag['src']
            image_sources.append(img_src)

    for headline in soup.find_all("h2", {"data-testid": "card-headline", "class": "sc-4fedabc7-3 zTZri"}):
        headline_text = headline.text.strip()
        if headline_text:
            headlines.append(headline_text)

    news = zip(headlines[:3], links[:3], image_sources[:3])  # Top 3 news
    return list(news)

def homepage(request):
    # Get top news from each section
    sports_news = scrape_sports_top()
    entertainment_news = scrape_entertainment_top()
    business_news = scrape_business_top()

    # Combine all top news
    top_news = {
        'sports': sports_news,
        'entertainment': entertainment_news,
        'business': business_news
    }

    weather = get_weather_data()
    # Render the top news on the homepage template
    return render(request, 'home.html', {'top_news': top_news,'weather': weather})

def get_weather_data():
    API_KEY = ''  # Replace with your OpenWeather API key
    CITY = 'Rajkot'  # Change this to your preferred city
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = {
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
            return weather
        else:
            return None
    except Exception as e:
        return None
