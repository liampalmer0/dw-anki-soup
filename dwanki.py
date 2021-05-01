from bs4 import BeautifulSoup, SoupStrainer
import subprocess
import click
import sys
import unicodedata
import genanki

def create_deck():
    return genanki.Deck(2017993711, 'DW Vocabulary')

def create_model():
    return genanki.Model(
        1844773645,
        'dw-anki model',
        fields=[
            {'name': 'German'},
            {'name': 'English'}
        ],
        templates=[
            {'name': 'DE to E',
             'qfmt': '{{German}}',
             'afmt': '{{English}}'},
            {'name': 'E to DE',
             'qfmt': '{{English}}',
             'afmt': '{{German}}'}
        ]
    )

def validate_use_entry(choice):
    if choice != 'y' and choice != 'n' and choice != 'e' and choice != 'edit':
        click.echo(click.style(
            'Unrecognized option. Choice must be [y]es [n]o or [e]dit',
             fg='red'))
        return False
    else: 
        return True

def add_entries(entries, deck, model):
    for e in entries:
        deck.add_note(genanki.Note(
            model=model,
            fields=[e['front'], e['back']]
        ))

def edit(**args):
    choice = click.prompt('Edit [front/back/all]')
    while (choice != 'all' and choice != 'front'
            and choice != 'back' and choice != 'q'):
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
@click.option(
    '-i', is_flag=True,
    help='Interactively review and confirm vocabulary entries')
@click.argument('url')
def parse(url, i):
    click.secho(
        '\n%%%%%%%%    %%%%        %%%%            %%%%%%      %%%%%%   %'
        '%%%  %%%%   %%%%  %%%%%%\n'
        '%%%%  %%%%  %%%%   %%   %%%%           %%%%%%%%     %%%%%%%  %'
        '%%%  %%%% %%%%     %%%%\n'
        '%%%%  %%%%  %%%%  %%%%  %%%%   %&%    %%%%  %%%%    %%%%%%%% %'
        '%%%  %%%%%%%       %%%%\n'
        '%%%%  %%%%   %%%%%%%%%%%%%%          %%%%%%%%%%%%   %%%% %%%%%'
        '%%%  %%%% %%%%     %%%%\n'
        '%%%%%%%%      %%%%%  %%%%%          %%%%      %%%%  %%%%  %%%%'
        '%%%  %%%%   %%%%  %%%%%%\n',
        fg='blue', bold=True
    )
    only_vocab = SoupStrainer(
        'div', class_='section exercise-container vocabulary copy')
    soup = BeautifulSoup(
        subprocess.run(["curl", url], capture_output=True).stdout,
        'html.parser', parse_only=only_vocab)
    deck = create_deck()
    all_words = []
    add = []
    for entry in soup.select("div.row.vocabulary"):
        cols = entry.find_all('div', recursive=False)
        if len(cols) == 3:
            front = unicodedata.normalize(
                'NFKC',
                cols[0].get_text().strip()
                    .replace('\n', ' ', 1)
                    .replace('\n', ''))
            back = unicodedata.normalize(
                'NFKC',
                cols[2].get_text().strip()
                    .replace('\n', ' ', 1)
                    .replace('\n', ''))
            all_words.append({'front': front, 'back': back})
    if i:
        click.echo(
            '== Interactive Mode == \n'
            '> Review and choose which words to add\n'
        )
        for pair in all_words:
                click.echo(click.style(pair['front'], fg='green'))
                click.echo(click.style(pair['back'], fg='green'))
                valid = False
                choice = 'n'
                while not valid:
                    choice = click.prompt(
                        'Use this entry? [y]es/[n]o/[e]dit',
                        default='y').lower()
                    valid = validate_use_entry(choice) 
                if choice == 'y':
                   add.append({'front': pair['front'], 'back': pair['back']})
                elif choice == 'n':
                    pass
                elif choice == 'e':
                    add.append(edit(front=pair['front'], back=pair['back']))
        click.echo('Adding {} entries'.format(len(add)))
        add_entries(add, deck, create_model())
    else:
        click.echo("Adding all entries ({})".format(len(all_words)))
        add_entries(all_words, deck, create_model())
    genanki.Package(deck).write_to_file('dw-vocab.apkg')

if __name__ == '__main__':
    parse()
