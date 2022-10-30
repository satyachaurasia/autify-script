import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import re


def add_meta_data_in_soup(soup):
    tags = ['num_links', 'images', 'last_fetch']
    for tag in tags:
        meta_tag = soup.new_tag('meta')
        meta_tag.attrs['name'] = tag
        if tag == 'num_links':
            meta_tag.attrs['content'] = len(soup.findAll('a'))
        elif tag == 'images':
            meta_tag.attrs['content'] = len(soup.findAll('img'))
        else:
            meta_tag.attrs['content'] = datetime.utcnow().ctime()
        soup.head.append(meta_tag)

def print_meta_data_from_soup(soup):
    tags = ['num_links', 'images', 'last_fetch']
    for tag in tags:
        meta_tag = soup.find("meta", attrs={'name': tag})
        if not meta_tag:
            continue
        print(f"{tag}: {meta_tag['content']}")


def get_soup(contents, parser = 'lxml'):
    return BeautifulSoup(contents, parser)


def get_file_name(domain_name, path):
    filename = f'{domain_name}{path}'
    filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]+')
    sub='_'
    new_file_name = str(filename_ascii_strip_re.sub(sub, '_'.join(filename.split()))).strip('._')
    return f'{new_file_name}.html'



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('urls', metavar='urls', type=str, nargs='+', help='urls to fetch')
    parser.add_argument('-m', '--metadata',
                    action='store_true')
    args = parser.parse_args()
    session = requests.Session()

    for url in args.urls:
        parse_result = urlparse(url)
        file_name = get_file_name(parse_result.netloc, parse_result.path)
        if args.metadata:
            try:
                with open(file_name) as file:
                    contents = file.read()
                    print(f'site: {url}')
                    soup = get_soup(contents)
                    print_meta_data_from_soup(soup)
                    print('\n')
            except Exception as e:
                print(f"Error in getting metadata for url: {e} ")
                continue
        else:
            try:
                response = session.get(url)
                response.raise_for_status() 
            except Exception as e:
                print(f'Error for url {url}: {e}')
                continue
                
            soup = get_soup(response.text)
            add_meta_data_in_soup(soup)
            with open(file_name, 'wb') as file:
                file.write(soup.prettify('utf-8'))
            print(f"URL {url} fetched successfully\n")
   
