import sqlite3


class ViiteVarasto:
    def __init__(self, yhteys):
        self.yhteys = yhteys
        self.yhteys.row_factory = sqlite3.Row
        self.yhteys.execute("""
            CREATE TABLE IF NOT EXISTS "references" (
                id INTEGER PRIMARY KEY,
                citekey TEXT NOT NULL UNIQUE,
                entry_type TEXT NOT NULL,
                author TEXT NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                publisher TEXT,
                journal TEXT,
                volume TEXT,
                pages TEXT
            )
        """)
        self.yhteys.commit()

    def lisaa_teos(self, teos):
        try:
            with self.yhteys:
                self.yhteys.execute("""
                    INSERT INTO "references"
                        (citekey, entry_type, author, title, year, publisher)
                    VALUES (:viiteavain, 'book', :tekijat, :otsikko, :vuosi, :kustantaja)
                """, teos)
        except sqlite3.IntegrityError as virhe:
            raise ValueError("Viiteavain on jo käytössä.") from virhe

    def lisaa_artikkeli(self, artikkeli):
        try:
            with self.yhteys:
                self.yhteys.execute("""
                    INSERT INTO "references"
                        (citekey, entry_type, author, title, year,
                         journal, volume, pages)
                    VALUES (
                        :viiteavain, 'article', :tekijat, :otsikko,
                        :vuosi, :journal, :volume, :pages
                    )
                """, artikkeli)
        except sqlite3.IntegrityError as virhe:
            raise ValueError("Viiteavain on jo käytössä.") from virhe


    def listaa_teokset(self):
        rivit = self.yhteys.execute("""
            SELECT id, citekey AS viiteavain,
                   entry_type AS tyyppi,
                   author AS tekijat,
                   title AS otsikko,
                   year AS vuosi,
                   publisher AS kustantaja,
                   journal, volume, pages
            FROM "references"
            ORDER BY id
        """).fetchall()

        return [dict(rivi) for rivi in rivit]



    def listaa_artikkelit(self):
        rivit = self.yhteys.execute("""
            SELECT id, citekey AS viiteavain,
                   author AS tekijat,
                   title AS otsikko,
                   year AS vuosi,
                   journal, volume, pages
            FROM "references"
            WHERE entry_type = 'article'
            ORDER BY id
        """).fetchall()

        return [dict(rivi) for rivi in rivit]
