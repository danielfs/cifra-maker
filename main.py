import os, pdfkit, requests, shutil, uuid
from pypdf import PdfMerger
from parsers import Cifraclub, MusicasParaMissa

urls = [
    ('https://www.cifraclub.com.br/paulo-roberto/a-biblia-a-palavra-de-deus/', 0),
    ('https://www.cifraclub.com.br/paulo-roberto/a-biblia-a-palavra-de-deus/', 2),
    ('https://www.cifraclub.com.br/paulo-roberto/a-biblia-a-palavra-de-deus/', 5),
    ('https://www.cifraclub.com.br/paulo-roberto/a-biblia-a-palavra-de-deus/', 7),
    ('https://www.cifraclub.com.br/paulo-roberto/a-biblia-a-palavra-de-deus/', 10),
    ('https://musicasparamissa.com.br/musica/muito-perdoais/', 0),
    ('https://musicasparamissa.com.br/musica/muito-perdoais/', 2),
    ('https://musicasparamissa.com.br/musica/muito-perdoais/', 5),
    ('https://musicasparamissa.com.br/musica/muito-perdoais/', 7),
    ('https://musicasparamissa.com.br/musica/muito-perdoais/', 10),
    ('https://www.cifraclub.com.br/eliana-ribeiro/gloria-deus-nas-alturas/', 10),
    ('https://musicasparamissa.com.br/musica/minha-vida-tem-sentido/', 0),
    ('https://musicasparamissa.com.br/musica/minha-vida-tem-sentido/', 2),
    ('https://musicasparamissa.com.br/musica/minha-vida-tem-sentido/', 5),
    ('https://musicasparamissa.com.br/musica/minha-vida-tem-sentido/', 7),
    ('https://musicasparamissa.com.br/musica/minha-vida-tem-sentido/', 10),
    ('https://www.cifraclub.com.br/catolicas/a-forca-da-eucaristia/', 0),
    ('https://www.cifraclub.com.br/catolicas/a-forca-da-eucaristia/', 2),
    ('https://www.cifraclub.com.br/catolicas/a-forca-da-eucaristia/', 5),
    ('https://www.cifraclub.com.br/catolicas/a-forca-da-eucaristia/', 7),
    ('https://www.cifraclub.com.br/catolicas/a-forca-da-eucaristia/', 9),
    ('https://www.cifraclub.com.br/celina-borges/fica-senhor-comigo/', 0),
    ('https://www.cifraclub.com.br/anjos-de-resgate-musicas/manda-teus-anjos/', 10),
]

def get_parser(url):
    print(f'Parsing {url}')

    if 'musicasparamissa' in url:
        return MusicasParaMissa()
    elif 'cifraclub' in url:
        return Cifraclub()
    
    raise Exception('Parser desconhecido: ' + url)

def get_content(url, parser, amount):
    response = requests.get(url)
    parser.parse(response.text, amount)
    
    content = "<h2>" + parser.titulo + "</h2>"
    content += parser.cifra

    return content

folder = uuid.uuid4().hex

os.mkdir(folder)

for i, data in enumerate(urls):
    url = data[0]
    amount = data[1]

    parser = get_parser(url)

    cifra = "<html lang=\"pt-BR\"><head><title>CIFRAS</title><meta charset=\"UTF-8\">"
    cifra += "<style>"
    cifra += "#letra, h2 { font-size: 20px; background: white; display: block; padding-right: 85px; } pre { font-size: 18px; background: white; font-family: monospace; display: block; padding-right: 85px; column-count: 2; column-gap: 20px; } pre b { color: #FF0000; font-weight: bold; } h2 { padding-right: 85px; }</style>"
    cifra += "</head><body>"

    content = get_content(url, parser, amount)
    cifra += content

    cifra += "</body></html>"

    with open(f'{folder}/cifra{i}.html', 'w', encoding=parser.get_encoding()) as f:
        f.write(cifra)

htmls = os.listdir(folder)
htmls = [f"{folder}/{h}" for h in htmls]

options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None
}

for i, html in enumerate(htmls):
    pdfkit.from_file(html, f'{folder}/cifras{i}.pdf', options=options)

pdfs = filter(lambda f: ('.pdf' in f), os.listdir(folder))
pdfs = [f"{folder}/{h}" for h in pdfs]

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("cifras.pdf")
merger.close()

shutil.rmtree(folder)
