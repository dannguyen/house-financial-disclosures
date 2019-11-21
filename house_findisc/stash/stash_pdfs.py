import asyncio
import httpx
from datetime import datetime

from house_findisc.filer import (
    make_pdf_error_path,
    make_pdf_path,
    make_pdf_url,
    gather_archive_records
)


# https://chrisalbon.com/python/data_wrangling/break_list_into_chunks_of_equal_size/
def chunks(_list, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(_list), n):
        # Create an index range for l of n items:
        yield _list[i:i+n]


async def stash(url, client, destpath, errpath):
    print("\tDownloading", url)
    resp = await client.get(url)

    if resp.status_code == 200:
        destpath.parent.mkdir(parents=True, exist_ok=True)
        destpath.write_bytes(resp.content)
        print('\tWrote', len(resp.content), 'bytes to:', destpath)
    else:
        print(f"\tError: got status code {resp.status_code} for url: {url}")
        errpath.parent.mkdir(parents=True, exist_ok=True)
        errpath.write_text(f"url: {url}\nstatus_code:{resp.status_code}\ntime:{datetime.now()}\n")

async def stash_batch(batch, _i):
    tasks = []
    async with httpx.AsyncClient() as client:
        for _j, row in enumerate(batch):
            url = make_pdf_url(row)
            destpath = make_pdf_path(row)
            errpath = make_pdf_error_path(row)
            if not destpath.exists() and not errpath.exists():
                print(f"{_i}|{_j}\t{row['Year']}: {row['StateDst']} {row['Last']}, {row['First']};\t{row['DocID']}")
                t = asyncio.create_task(stash(url, client, destpath, errpath))
                tasks.append(t)

        await asyncio.gather(*tasks)

async def main():
    batches = chunks(gather_archive_records(), 9)
    for _i, batch in enumerate(batches):
        await stash_batch(batch, _i)

if __name__ == '__main__':
    asyncio.run(main())
