
import csv
from pathlib import Path
import requests
from urllib.parse import urljoin

SRC_DIR =  Path('data', 'stashed', 'year_archives')
BASE_SRC_URL = 'http://clerk.house.gov/public_disc/'
DEST_DIR = Path('data', 'stashed', 'pdfs')

def parse_year_file(srcpath):
    with open(srcpath) as o:
        data = list(csv.DictReader(o, delimiter="\t"))
        return data

def make_pdf_url(record):
    if record['FilingType'] == 'P':
        subdir = 'ptr-pdfs'
    else:
        subdir = 'financial-pdfs'
    subpath = f"{subdir}/{record['Year']}/{record['DocID']}.pdf"
    url = urljoin(BASE_SRC_URL, subpath, )
    return url


def gather_files(srcdir=SRC_DIR):
    return sorted(SRC_DIR.glob('*.txt'))


def main():
    for src in gather_files():
        for row in (parse_year_file(src)):
            url = make_pdf_url(row)
            print(f"{row['Year']}: {row['StateDst']} {row['Last']}, {row['First']}")
            print("\tDownloading", url)
            resp = requests.get(url)
            if resp.status_code == 200:
                destdir = DEST_DIR.joinpath(row['Year'])
                destdir.mkdir(parents=True, exist_ok=True)
                destpath = destdir.joinpath(f"{row['DocID']}.pdf")
                destpath.write_bytes(resp.content)
                print('\tWrote', len(resp.content), 'bytes to:', destpath)
            else:
                print(f"\tError: got status code {resp.status_code}")


if __name__ == '__main__':
    main()
