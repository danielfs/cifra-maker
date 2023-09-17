import re
from bs4 import BeautifulSoup


class Parser:
    titulo: str = None
    cifra: str = None
    amount: int = 0

    def set_content(self, soup):
        pass

    def get_encoding(self):
        return ''

    def parse(self, text, amount):
        soup = BeautifulSoup(text, 'html.parser')
        self.amount = amount
        self.set_content(soup)

    def transpose(self, text: str):
        text = text.strip()

        chord_before = text[0]

        if text[0] in ('#', 'b'):
            chord_before = f"{chord_before}{text[0]}"

        scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        normalizeMap = {"Cb":"B", "Db":"C#", "Eb":"D#", "Fb":"E", "Gb":"F#", "Ab":"G#", "Bb":"A#",  "E#":"F", "B#":"C"}

        chord = ''
        if chord_before in normalizeMap:
            chord = normalizeMap[chord_before]
        else:
            chord = chord_before
        
        i = (scale.index(chord) + self.amount) % len(scale)

        if i < 0:
            i = i + len(scale)

        chord_next = scale[i]

        return text.replace(chord_before, chord_next)
    
    def fix_cifra(self, cifra_content):

        for b in cifra_content.find_all('b'):
            b.string = self.transpose(b.get_text())

        text = str(cifra_content)
        return re.sub(r'(\n\s*)+\n+', '\n\n', text)


class MusicasParaMissa(Parser):
    def set_content(self, soup):
        cifra_content = soup.find(id="div-cifra")
        self.cifra = self.fix_cifra(cifra_content)
        self.titulo = soup.find(id='titulo-musica').get_text()
    
    def get_encoding(self):
        return 'iso-8859-1'

class Cifraclub(Parser):
    def set_content(self, soup):
        for tab in soup.find_all("span", {'class':'tablatura'}): 
            tab.decompose()
        cifra_content = soup.find('pre')

        self.cifra = self.fix_cifra(cifra_content)
        self.titulo = soup.find('h1', {'class': 't1'}).get_text()

    def get_encoding(self):
        return 'utf-8'
