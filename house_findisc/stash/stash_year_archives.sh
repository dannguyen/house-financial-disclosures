#!/bin/sh
BASE_URL=http://clerk.house.gov/public_disc/financial-pdfs
DEST_DIR=data/stashed/year_archives
DEST_ZIPS_DIR=${DEST_DIR}/zips
mkdir -p ${DEST_ZIPS_DIR}

for year in $(seq 2018 2020); do
    url=${BASE_URL}/${year}FD.ZIP
    destzip=${DEST_ZIPS_DIR}/fd-${year}.zip
    curl -o ${destzip} ${url}
    echo "Unzipping ${destzip} into: ${DEST_DIR}"
    unzip ${destzip} -d ${DEST_DIR}
done
