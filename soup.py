from bs4 import BeautifulSoup

with open('./page-example.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

for x in soup.select("div.row .vocabulary-entry .richtext-content-container"):
    for s in x.stripped_strings:
        print(s)
