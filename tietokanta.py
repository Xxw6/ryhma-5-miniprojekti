import sqlite3


class ViiteVarasto:
    def __init__(self, yhteys):
        self.yhteys = yhteys
        self.yhteys.row_factory = sqlite3.Row
        self.yhteys.execute("""
            CREATE TABLE IF NOT EXISTS book_references (
                id INTEGER PRIMARY KEY,
                citekey TEXT NOT NULL UNIQUE,
                author TEXT NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                publisher TEXT NOT NULL
            )
        """)
        self.yhteys.commit()

    def lisaa_teos(self, teos):
        try:
            with self.yhteys:
                self.yhteys.execute("""
                    INSERT INTO book_references
                        (citekey, author, title, year, publisher)
                    VALUES (:viiteavain, :tekijat, :otsikko, :vuosi, '')
                """, teos)
        except sqlite3.IntegrityError as virhe:
            raise ValueError("Viiteavain on jo käytössä.") from virhe

    def listaa_teokset(self):
        rivit = self.yhteys.execute("""
            SELECT id, citekey AS viiteavain, author AS tekijat,
                   title AS otsikko, year AS vuosi, publisher AS kustantaja
            FROM book_references ORDER BY id
        """).fetchall()
        return [dict(rivi) for rivi in rivit]
