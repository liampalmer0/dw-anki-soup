# dwanki: Turn DW Course Vocab Lists into Anki Decks

Take vocabulary words from Deutsche Welle online German courses with Beautiful Soup and add them to an Anki deck. This program is meant to be a companion/expansion for these courses to help with word recall & recognition.

*This tool and its author are not affiliated with Deutsche Welle in any way.*

## Usage

`dwanki.py [OPTIONS] <url>`

### Parameters

`<url>`: The url of the vocabulary list

### Options:

`-i`: Interactively review and confirm vocabulary entries


## Tools Used
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [genanki](https://github.com/kerrickstaley/genanki)
- [Click](https://click.palletsprojects.com)
