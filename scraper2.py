from lxml import html
import requests
from pprint import pprint

def resolve(node):
    if len(node):
        # element inner text
        if isinstance(node[0], html.HtmlElement):
            return node[0].text
        # return node (e.g. html attribute)
        else:
            return node[0]
    return None


# ziskani cookies
base_url = 'http://www.ereading.cz'
response = requests.get(base_url)
cookies = response.cookies

# prihlaseni
login_url = 'https://www.ereading.cz/cs/prihlaseni'
headers = {
    'Cookie': '; '.join(k + '=' + v for k, v in cookies.items())
}
login_data = {
    'login': 'user@example.com',
    'heslo': '*****',
    'log_in': u'P\xc5ihl\xc3sit se' # tlacitko pro odeslani formulare - je zde nutne ;)
}
response = requests.post(login_url, headers=headers, data=login_data)
cookies = response.cookies

# precteni elektronicke knihovnicky
library_url = 'https://www.ereading.cz/cs/moje-eknihovna'
headers = {
    'Cookie': '; '.join(k + '=' + v for k, v in cookies.items())
}

response = requests.get(library_url, headers=headers)
text = response.text

# ... profit
dom = html.fromstring(text)

result = []

books = dom.xpath('//div[contains(@class, "libList ")]')

for book in books:
    texts = book.xpath('div[contains(@class, "libListText")]')[0]
    result.append({
        'title': resolve(texts.xpath('a[@class="titul"]/@title')),
        'author': resolve(texts.xpath('a[@class="author"]/@title')),
        'image': 'https://ereading.cz/' + resolve(book.xpath('div[@class="imgSpace"]/a/img/@src')),
        'detail_url': resolve(texts.xpath('a[@class="titul"]/@href'))
    })

pprint(result)
