""" does a first pass inspection of pdf inventory, including
    how many pages per pdf and pdf type
"""

import csv
from pathlib import Path
import pdfplumber

from house_findisc.filer import (
    COLLATED_PDF_INVENTORY_PATH,
    archive_header_map,
    archive_headers,
    gather_archive_records,
    make_pdf_path,
    make_pdf_error_path,
    make_pdf_url,
)

def analyze_pdf(srcpath):
    d = {}
    pdf = pdfplumber.open(srcpath)
    d['page_count'] = len(pdf.pages)
    txt = pdf.pages[0].extract_text()
    if txt:
        d['pdf_type'] = 'text'
    else:
        d['pdf_type'] = 'image'
    return d


def collate():
    HEADER_MAP = archive_header_map()

    for _i, row in enumerate(gather_archive_records()):
        d = {}
        for oname in row.keys():
            _h = next((h for h in HEADER_MAP if h['original_name'] == oname), False)
            if _h:
                cname = _h['canonical_name']
                d[cname] =row[oname]

        d['pdf_path'] = make_pdf_path(row)
        d['pdf_url'] = make_pdf_url(row)
        err_path = make_pdf_error_path(row)
        if d['pdf_path'].exists():
            d['pdf_status'] = 'stashed'
            d['pdf_bytes'] = d['pdf_path'].stat().st_size
            meta = analyze_pdf(d['pdf_path'])
            d.update(meta)

        elif err_path.exists():
            d['pdf_status'] = 'error'
        else:
            d['pdf_status'] = 'n/a'

        yield d



def main():
    DEST_PATH = COLLATED_PDF_INVENTORY_PATH
    DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
    HEADERS = archive_headers()
    with open(DEST_PATH, 'w') as w:
        outs = csv.DictWriter(w, fieldnames=HEADERS,)
        outs.writeheader()
        for _i, row in enumerate(collate()):
            outs.writerow(row)
            if _i % 100 == 0:
                print(_i)



if __name__ == '__main__':
    main()

