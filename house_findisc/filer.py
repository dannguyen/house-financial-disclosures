import csv
from pathlib import Path
from urllib.parse import urljoin

BASE_SRC_URL = 'http://clerk.house.gov/public_disc/'


ARCHIVES_DIR =  Path('data', 'stashed', 'year_archives')
COLLATED_PDF_INVENTORY_PATH = Path('data', 'collated', 'pdf_inventory.csv')
PDFS_DIR = Path('data', 'stashed', 'pdfs')
PDF_ERRORS_DIR = PDFS_DIR.joinpath('metadata', 'fetch-errors')

def archive_headers():
    return [a['canonical_name'] for a in archive_header_map()]

def archive_header_map():
    p = Path('lookups', 'year_archive_header_map.csv')
    return list(csv.DictReader(p.open()))


def make_pdf_path(record):
    destdir = PDFS_DIR.joinpath(record['Year'])
    destpath = destdir.joinpath(f"{record['DocID']}.pdf")
    return destpath

def make_pdf_error_path(record):
    destdir = PDF_ERRORS_DIR.joinpath(record['Year'])
    destpath = destdir.joinpath(f"{record['DocID']}.txt")
    return destpath

def make_pdf_url(record):
    if record['FilingType'] == 'P':
        subdir = 'ptr-pdfs'
    else:
        subdir = 'financial-pdfs'
    subpath = f"{subdir}/{record['Year']}/{record['DocID']}.pdf"
    url = urljoin(BASE_SRC_URL, subpath, )
    return url



def gather_archives():
    return sorted(ARCHIVES_DIR.glob('*.txt'), reverse=True)

def gather_archive_records():
    return [row for fpath in gather_archives() for row in parse_year_archive(fpath)]


def parse_year_archive(srcpath):
    with open(srcpath) as o:
        data = list(csv.DictReader(o, delimiter="\t"))
        return data

