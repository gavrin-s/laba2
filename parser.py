import requests
import re

headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}


def get_email(url, headers):
    response = requests.get(url, headers=headers)

    result = re.findall(pattern=r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}', string=response.text)

    return result

def get_urls(domain, depth=5, n=5):
    pass

if __name__ == "__main__":
    print(get_email('https://www.mosigra.ru/', headers=headers))
