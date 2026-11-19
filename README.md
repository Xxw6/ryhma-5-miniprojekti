# ryhma-5-miniprojekti

Miniprojekti
Ohjelmistotuotanto-kurssin ryhmätyö, syksy 2026.
Ryhmä: Teemu, Elli, Samu, Tomas, Essi

# Lähdeviitehallinta

[![CI](https://github.com/Xxw6/ryhma-5-miniprojekti/actions/workflows/main.yml/badge.svg)](https://github.com/Xxw6/ryhma-5-miniprojekti/actions)

Sovellus LaTeX-lähdeviitteiden hallintaan. Sen avulla kandidaatintutkielman kirjoittaja voi tallentaa käyttämänsä lähteet yhteen paikkaan ja tuottaa niistä BibTeX-tiedoston, jonka voi liittää suoraan LaTeX-dokumenttiin tai Overleafiin.

Ohjelmisto toteutetaan Ohjelmistotuotanto-kurssin miniprojektina Scrumia noudattaen.

## Mitä sovellus tekee

- **Viitteiden lisääminen** helppolukuisessa muodossa: käyttäjä syöttää kentät (tekijä, otsikko, vuosi…) ohjatusti, eikä hänen tarvitse kirjoittaa BibTeX-syntaksia itse.
- **BibTeX-tiedoston generointi**, jonka voi viedä suoraan LaTeX-dokumenttiin (`\bibliography{references}`).
- **Viitteiden listaus** ihmiselle luettavassa muodossa.
- **Haku ja rajaus** esimerkiksi kirjoittajan, vuoden tai julkaisun perusteella.
# Viitehallinta

Toteutettavat viitetyypit ovat aluksi `book`, `article` ja `inproceedings`.

Suunniteltuja jatko-ominaisuuksia ovat tagit, tietojen haku DOI-tunnisteella tai ACM Digital Libraryn linkistä sekä viitteiden synkronointi koneiden välillä. Tarkempi sisältö ja järjestys sovitaan asiakkaan kanssa sprinteittäin, ja ne näkyvät product backlogissa.

## Projektinhallinta
Linkit
- [Product backlog ja sprint backlogit](LINKKI_BACKLOGIIN)
- Product backlog: https://docs.google.com/spreadsheets/d/e/2PACX-1vSlPoHyTmr196f-UAnsxHPRqRhlnpJWYg5FNymdESZPKoTW9kiiol37jiW0-AugFU2qdXrfeuzbMuZk/pubhtml  (pelkkä lukuoikeus)
- Sprint backlog ja burndown: Samassa tiedostossa backlogin kanssa
- [CI (GitHub Actions)](https://github.com/Xxw6/ryhma-5-miniprojekti/actions)
- Hyväksymistestit: TODO
- [Definition of Done](DOD.md)
Definition of Done
Alustavasti homma on valmis, kun:
- Storyn hyväksymiskriteerit täyttyvät.
- Tarvittavat testit on tehty ja ne menevät läpi.
- CI ja sovitut Pylint-tarkistukset menevät läpi.
- Koodi on selkeää ja tarvittavat ohjeet on päivitetty.
Testaus
    uv run pytest                               # testit
    uv run coverage run --branch -m pytest      # testit ja kattavuuden mittaus
    uv run coverage report                      # kattavuusraportti
    uv run pylint .                             # koodityylin tarkistus

## Asennus ja käyttö

Tarvitset [uv](https://docs.astral.sh/uv/)-työkalun. uv asentaa oikean Python-version (3.14) ja riippuvuudet automaattisesti.

Asenna riippuvuudet projektin kansiossa:

    uv sync

Käynnistä ohjelma:

- PowerShell: `uv run python main.py`
- Git Bash: `winpty uv run python main.py`


## Toiminnot

- `1`: lisää teos
- `2`: listaa tallennetut teokset.
- `0`: lopeta ohjelma.

## Tietokanta

ohjelma luo `references.db` tietokannan automaattisesti ensimmäisellä
käynnistyksellä ja tiedot säilyvät myös ohjelman sulkemisen jälkeen.

Huom! Tätä tietokantaa ei tarvitse tallentaa versionhallintaan.

## Lisenssi

[MIT](LICENSE)

