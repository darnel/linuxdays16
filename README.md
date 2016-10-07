# Level 1 - extrakce dat z dopředu staženého HTML

## Import části knihovny *lxml*

```
from lxml import html
```

## Načtení souboru

```
with open('knihovna.html', 'rt') as file:
        text = file.read()
```

## Zpracování textu do struktury

```
dom = html.fromstring(text)
```

## Výběr pomocí XPath dotazu

Stažené HTML je potřeba zanalyzovat např. pomocí Firebugu a stanovit vhodné XPath dotazy.

* `/element/element` - traverzování v DOM stromu
* `//element` - hledání kdekoliv v DOM stromu
* `@atribut`
* `element[podmínka]`
* `contains(@atribut, "text")` - zda atribut obsahuje text

```
books = dom.xpath('//div[contains(@class, "libListText")]')
```

## Iterace množiny elementů

```
for book in books:
    title = book.xpath('a[@class="titul"]/@title')[0]
```

## Úprava pro získání obrázku knihy

Pomocná funkce - vrátí buď vnitřek (text) HTML elementu nebo hodnotu (např. atributu)

```
def resolve(node):
    if len(node):
        # element inner text
        if isinstance(node[0], html.HtmlElement):
            return node[0].text
        # return node (e.g. html attribute)
        else:
            return node[0]
    return None
```

Obrázek je mimo element s třídou `libListText`, proto změníme XPath dotaz pro `books`

> mezera za `libList ` zabrání konfliktu s `libListText` (zde contains také platí), naštestí je class v HTML včetně mezery :)

```
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
```
# Level 2 - živá extrakce dat včetně přihlášení

## Stažení úvodní stránky pro získání cookies

```
base_url = 'http://www.ereading.cz'
response = requests.get(base_url)
cookies = response.cookies
```

## Přihlášení

Podíváme se (opět pomocí Firebugu), jak vlastně přihlašování probíhá :) Zejména jaká data a kam je potřeba poslat.

Sestavíme hlavičky požadavku:

```
headers = {
    'Cookie': '; '.join(k + '=' + v for k, v in cookies.items())
}
```

a data:

```
login_data = {
    'login': 'user@example.com',
    'heslo': '*****',
    'log_in': u'P\xc5ihl\xc3sit se' # tlacitko pro odeslani formulare - je zde nutne ;)
}
```

a provedeme HTTP POST:

```
response = requests.post(login_url, headers=headers, data=login_data)
```

Po přihlášení si znovu uložíme cookies.

```
cookies = response.cookies
```

## Načtení knihovničky

Opět pošleme v hlavičkách cookies získané po přihlášení.

```
response = requests.get(library_url, headers=headers)
text = response.text
```

## ... Profit

viz výše :)
