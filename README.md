# house-financial-disclosures

Scraping House representative financial disclosures. See my similar scraper for the Senate: https://github.com/dannguyen/scrape-senate-financial-disclosures

Reference pages:

- House search: http://clerk.house.gov/public_disc/financial-search.aspx
- Year compilings: http://clerk.house.gov/public_disc/financial.aspx

The individual reports as PDFs (they are **all** pdfs) can be found in [data/stashed/pdfs](data/stashed/pdfs). The indices (i.e. which document id matches to which candidate) are, for now, in [data/stashed/year_archives](data/stashed/year_archives)

A few labeled samples can be found in [data/stashed/samples/pdfs](data/stashed/samples/pdfs)


-------------

## scwu and todos

(scwu stands for: stash, collate, wrangle, unify)

- stash
    - yearly archives
    - individual pdfs
    - year index pages
    - get FEC candidacy data?
    - match reps with congress/unitedstates? 
- collate
    - take inventory of image and text based pdfs (use pdfplumber)
    - extract text-based pdfs    
    
- wrangle

- unify


- [X] fetched yearly archives, 2008 to 2018
- [X] fetched PDFs as enumerated in yearly archives
- [ ] Finish pushing collected files for 2008 thru 2018 (as collected above)
- [ ] Write scraper for search page (to get 2019): http://clerk.house.gov/public_disc/financial-search.aspx
