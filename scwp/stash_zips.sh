#!/bin/sh
BASE_URL=http://clerk.house.gov/public_disc/financial-pdfs
DEST_DIR=data/stashed/report_zips
mkdir -p ${DEST_DIR}

for year in $(seq 2008 2018); do
    url=${BASE_URL}/${year}FD.ZIP
    dest=${DEST_DIR}/fd-${year}.zip
    curl -o ${dest} ${url}
    unzip ${dest} -d ${DEST_DIR}
done
