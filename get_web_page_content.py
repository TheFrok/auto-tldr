from bs4 import BeautifulSoup
import requests


def get_html(url):
    return requests.get(url).text


def extract_content(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.get_text(html)


if __name__ == '__main__':
    url = "http://www.fisheye.co.il/maktoob/"
    html = get_html(url)
    text = extract_content(html)
    with open("html_data.txt", "wb") as f:
        f.write(bytes(text, "utf8"))