import requests
import re
from urllib.parse import urlparse, urljoin
from collections import deque
from bs4 import BeautifulSoup


headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}


def get_email(url, headers=None):
    response = requests.get(url, headers=headers)

    result = re.findall(pattern=r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}', string=response.text)

    return set(result)


def get_urls(url, netloc, urls=set(), headers=None):
    if len(urls) > 100:
        return None

    try:
        response = requests.get(url, headers=headers)
    except:
        return None

    links = []
    dec = []
    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.find_all('a', href=True):
        links.append(a['href'])

    for path in links:
        link = urljoin(url, path)
        parsed = urlparse(link)
        link = '{}://{}{}'.format(parsed.scheme, parsed.netloc, parsed.path)
        if urlparse(link)[1] != netloc:
            continue
        if link in urls:
            continue
        if link not in urls:
            dec.append(link)
            urls.add(link)

    for link in dec:
        get_urls(link, netloc, urls=urls, headers=headers)

    return list(urls)


def get_emails(urls, headers=None):
    emails = set()

    for i, url in enumerate(urls):
        em = get_email(url)
        print(i, url, len(em))
        emails.update(em)
    print(emails)

    return list(emails)


if __name__ == "__main__":
    url = "https://www.mosigra.ru/"
    print('Start to get urls')
    urls = get_urls(url, urlparse(url)[1], headers=headers)
    print('end to get urls, readed {} urls'.format(len(urls)) )
    print('start to get emails')
    emails = get_emails(urls, headers=headers)
    print('end to get emails, readed {} emails'.format(len(emails)))
    print(emails)
    #get_urls(url, urlparse(url)[1])
    #print(len(get_email(url, headers=headers)))
