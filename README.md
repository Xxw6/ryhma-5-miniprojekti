# Lähdeviitehallinta

[![CI](https://github.com/Xxw6/ryhma-5-miniprojekti/actions/workflows/main.yml/badge.svg)](https://github.com/Xxw6/ryhma-5-miniprojekti/actions) [![codecov](https://codecov.io/gh/Xxw6/ryhma-5-miniprojekti/graph/badge.svg)](https://codecov.io/gh/Xxw6/ryhma-5-miniprojekti)

Sovellus LaTeX-lähdeviitteiden hallintaan. Sen avulla kandidaatintutkielman kirjoittaja voi tallentaa käyttämänsä lähteet yhteen paikkaan ja tuottaa niistä BibTeX-tiedoston, jonka voi liittää suoraan LaTeX-dokumenttiin tai Overleafiin.

Ohjelmistotuotanto-kurssin miniprojekti, syksy 2026. Ryhmä 5: Teemu, Elli, Samu, Tomas, Essi, Kasper.

## Projektinhallinta

- [Product backlog, sprint backlogit ja burndown](https://docs.google.com/spreadsheets/d/e/2PACX-1vSlPoHyTmr196f-UAnsxHPRqRhlnpJWYg5FNymdESZPKoTW9kiiol37jiW0-AugFU2qdXrfeuzbMuZk/pubhtml)
- [CI (GitHub Actions)](https://github.com/Xxw6/ryhma-5-miniprojekti/actions)
- [Testikattavuus (Codecov)](https://codecov.io/gh/Xxw6/ryhma-5-miniprojekti)
- [Hyväksymistestit (Robot Framework)](tests/robot)
- [Definition of Done](DOD.md)

## Asennus ja käyttö

Tarvitset [uv](https://docs.astral.sh/uv/)-työkalun. uv asentaa oikean Python-version (3.14) ja riippuvuudet automaattisesti.

Asenna riippuvuudet projektin kansiossa:

    uv sync

Käynnistä ohjelma:

- PowerShell: `uv run python main.py`
- Git Bash: `winpty uv run python main.py`

Ohjelma luo tietokannan `references.db` automaattisesti ensimmäisellä käynnistyksellä, ja viitteet säilyvät ohjelman sulkemisen jälkeen.

## Toiminnot

- `1` lisää kirjaviite (viiteavain muodostetaan automaattisesti)
- `2` lisää artikkeliviite
- `3` listaa tallennetut viitteet
- `4` tallenna BibTeX-tiedostoksi
- `5` poista viite viiteavaimen perusteella
- `6` hae viitteitä kirjoittajan, vuoden tai julkaisijan perusteella
- `0` lopeta

## Testaus

    uv run pytest                               # yksikkötestit
    uv run robot --pythonpath . tests/robot     # hyväksymistestit
    uv run coverage run --branch -m pytest      # testit ja kattavuuden mittaus
    uv run coverage report                      # kattavuusraportti
    uv run pylint .                             # koodityylin tarkistus

## Työnkulku

1. Ennen uutta taskia: `git switch main` ja `git pull`
2. Yksi haara per taski, esim. `git switch -c viitteen-poisto`
3. Muutos `main`iin pull requestilla, kun CI on vihreä ja toinen tiimiläinen on hyväksynyt sen
4. Haara poistetaan yhdistämisen jälkeen

## Lisenssi

[MIT](LICENSE)
