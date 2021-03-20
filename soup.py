from bs4 import BeautifulSoup
import subprocess
import sys

soup = BeautifulSoup(subprocess.run(["curl", sys.argv[1]], capture_output=True).stdout, 'html.parser')

for entry in soup.select("div.row .vocabulary-entry .richtext-content-container"):
    for s in entry.stripped_strings:
        print(s)
