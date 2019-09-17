from bs4 import BeautifulSoup
import pypandoc
import tempfile
import requests

import html2text
h_convert = html2text.HTML2Text()
h_convert.body_width = 0

URL = 'http://www.leedsbeer.com/beers-breweries/'

tmp = tempfile.NamedTemporaryFile()


def get_brewery_details(brewery_url):
    content = requests.get(brewery_url).content
    soup = BeautifulSoup(content, 'html.parser')

    main_body = soup.find('div', class_='singleBeerContent')

    text = main_body.text.replace(u'\xa0', '')
    text = text.replace('\n', '')
    if text:
        markdown = h_convert.handle(str(main_body))

        return markdown


def main():
    output = ['# Leeds Beer Fest']

    content = requests.get(URL).content
    soup = BeautifulSoup(content, 'html.parser')

    beers_div = soup.find('div', {'id': 'isotope'})
    links = beers_div.find_all('a', {'class': 'breweryLink'}, href=True)
    for link in links:
        brewery_name = link.find('div', class_='tooltip').text
        print('Processing {}'.format(brewery_name))
        output.append('## {}\n'.format(brewery_name))
        brewery_url = link['href']

        details = get_brewery_details(brewery_url)
        if details:
            output.append(details + '\n')
        else:
            output.append('No info!\n')

        output.append('----\n')

    output_string = '\n'.join(output)
    with open(tmp.name, 'w') as f:
        f.write(output_string)

    output = pypandoc.convert_file(
        tmp.name, format='md', to='pdf', outputfile='output.pdf',
        extra_args=['-V', 'geometry:left=1cm,right=1cm, top=1cm, bottom=2cm']
    )


if __name__ == '__main__':
    main()
