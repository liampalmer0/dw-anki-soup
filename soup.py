from bs4 import BeautifulSoup, SoupStrainer
import subprocess
import click
import sys
import unicodedata
import genanki

def validate_use_entry(choice):
    if choice != 'y' and choice != 'n' and choice != 'e' and choice != 'edit':
        click.echo(click.style('Unrecognized option. Choice must be [y]es [n]o or [e]dit', fg='red'))
        return False
    else: 
        return True

def add_entries(entries, deck):
    # TODO: Add all to anki deck
    click.echo('adding {} to the {} deck'.format(len(entries), deck))

def edit(**args):
    choice = click.prompt('Edit [front/back/all]')
    while choice != 'all' and choice != 'front' and choice != 'back' and choice != 'q':
        click.echo(click.style('Invalid input! ([q] to quit editing)'))
        choice = click.prompt('Edit [front/back/all]')
    if choice == 'q':
        return {'front':args['front'], 'back': args['back']}
    elif choice == 'all':
        click.echo('Editing All Fields')
        new_front = click.prompt('Enter new front')
        new_back = click.prompt('Enter new back')
        new_words = {'front': new_front, 'back': new_back}
    else:
        new_words = {'front': args['front'], 'back': args['back']}
        click.echo('Editing:\n{}'.format(args[choice]))
        new_words[choice] = click.prompt('Enter new value')
    return new_words

@click.command()
@click.option('-i', is_flag=True, help='Interactively review and confirm vocabulary entries')
@click.argument('url')
def parse(url, i):
    only_vocab = SoupStrainer('div', class_='section exercise-container vocabulary copy')
    soup = BeautifulSoup(subprocess.run(["curl", url], capture_output=True).stdout, 'html.parser', parse_only=only_vocab)
    if i:
        add = []
        for entry in soup.select("div.row.vocabulary"):
            cols = entry.find_all('div', recursive=False)
            if len(cols) == 3:
                front = unicodedata.normalize('NFKC', cols[0].get_text().strip().replace('\n', ' ', 1).replace('\n', ''))
                back = unicodedata.normalize('NFKC', cols[2].get_text().strip().replace('\n', ' ', 1).replace('\n', ''))
                click.echo(click.style(front, fg='green'))
                click.echo(click.style(back, fg='green'))
                valid = False
                choice = 'n'
                while not valid:
                    choice = click.prompt('Use this entry? [y]es/[n]o/[e]dit', default='y').lower()
                    valid = validate_use_entry(choice) 
                if choice == 'y':
                   add.append({'front': front, 'back': back})
                elif choice == 'n':
                    pass
                elif choice == 'e':
                    add.append(edit(front=front, back=back))
        click.echo(add)
        add_entries(add, 'default')
                    
    else:
        # TODO: set up automatic add
        click.echo('adding all to deck')

if __name__ == '__main__':
    parse()
