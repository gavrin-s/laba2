import requests
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}


def get_email(url, headers=None):
    """
    :param url: url
    :param headers: headers for requests
    :return: list of emails
    """
    response = requests.get(url, headers=headers)
    result = re.findall(pattern=r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}', string=response.text)
    return list(set(result))


def get_urls(url, netloc, urls=set(), headers=None):
    """
    :param url: url
    :param netloc: domain name site
    :param urls: set of urls was collected
    :param headers: headers for requests
    :return: list of urls
    """
    # If count of url > 100 break
    if len(urls) > 100:
        return None

    try:
        response = requests.get(url, headers=headers)
    except:
        return None

    links = []

    dec = [] # list of urls at the url
    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.find_all('a', href=True):
        links.append(a['href'])

    for path in links:
        link = urljoin(url, path)
        # cleaning url from params, query, fragment and ect.
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


def parse_emails(urls, headers=None):
    """
    :param urls: list of urls
    :param headers: headers for requests
    :return: list of emails from all urls
    """
    emails = set()

    for url in urls:
        em = set(get_email(url, headers))
        emails.update(em)

    return list(emails)


if __name__ == "__main__":
    url = "http://kdv-group.com/ru/"
    print('Start to get urls')
    urls = get_urls(url, urlparse(url)[1], headers=headers)
    print('end to get urls, readed {} urls'.format(len(urls)) )
    print('start to get emails')
    emails = parse_emails(urls, headers=headers)
    print('end to get emails, readed {} emails'.format(len(emails)))
    print(emails)

