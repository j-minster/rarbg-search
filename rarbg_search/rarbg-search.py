#!/usr/bin/env python3

import os
import sqlite3
import click
from pick import pick
from hurry.filesize import size

def to_magnet(row: tuple) -> str:
    magstring = "magnet:?xt=urn:btih:"
    infohash = row[1]
    title = row[2]

    magnet_link = f"{magstring}{infohash}&dn={title}&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopentor.org%3A2710&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Ftracker.blackunicorn.xyz%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969"

    return magnet_link

@click.command()
@click.argument("title", required=True)
@click.argument("dbpath", required=False, default=r"./rarbg_db.sqlite")
@click.option("--noxxx", "-nx",
              default=True,
              type=bool,
              required=False,
              help="Filter out adult content")
def search(title: str, dbpath: str, noxxx: bool) -> None:
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    print('db connected')

    title_pattern = '%' + title.replace(' ', '%') + '%'
    query = f"SELECT * FROM items WHERE title LIKE '{title_pattern}'"

    if noxxx:
        query += " AND cat <> 'xxx'"

    cursor.execute(query)
    rows = cursor.fetchall()

    prompt = 'Please choose a torrent to open: '
    movie_titles = [(row[2], size(row[5])) for row in rows]
    option, index = pick(movie_titles, prompt)

    if index:
        os.system(f"open '{to_magnet(rows[index])}'")
    else:
        print('no selection - connection aborted')

    conn.close()
