from bs4 import BeautifulSoup, SoupStrainer
import subprocess
import click
import sys

@click.command()
@click.option('-i', is_flag=True, help='Interactively review and confirm vocabulary entries')
@click.argument('url')
def parse(url, i):
    only_vocab = SoupStrainer('div', class_='section exercise-container vocabulary copy')
    soup = BeautifulSoup(subprocess.run(["curl", url], capture_output=True).stdout, 'html.parser', parse_only=only_vocab)
    if i:
        print('Interactive Mode')
        for entry in soup.select("div.row.vocabulary"):
            cols = entry.find_all('div', recursive=False)
            if len(cols) == 3:
                click.echo(cols[0].get_text().strip().replace('\n', ''))
                click.echo(cols[2].get_text().strip().replace('\n', ''))
                click.confirm('Use this entry?', abort=True)
    else:
        click.echo('TODO: setup auto anki add')

if __name__ == '__main__':
    parse()
