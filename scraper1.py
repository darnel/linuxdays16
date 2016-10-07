from lxml import html
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

with open('knihovna.html', 'rt') as file:
    text = file.read()

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
