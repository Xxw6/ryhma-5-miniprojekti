*** Settings ***
Resource  resource.robot

*** Test Cases ***
Viitteen Poisto Avaimella Onnistuu
    Lisaa Kirja  ${EMPTY}  Tervo, Jari  Ukko  2022  Otava
    Poista Viite  Tervo2022
    Syota  3
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla  Viite Tervo2022 poistettu.
    Tulosteessa Pitaisi Olla  Ei tallennettuja teoksia.

Poisto Poistaa Vain Annetun Viitteen
    Lisaa Kirja  ${EMPTY}  Tervo, Jari  Ukko  2022  Otava
    Lisaa Kirja  ${EMPTY}  Linna, Väinö  Tuntematon sotilas  1954  WSOY
    Poista Viite  Tervo2022
    Syota  3
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla  [Linna1954] Linna, Väinö: Tuntematon sotilas (1954).
    Tulosteessa Ei Pitaisi Olla  [Tervo2022] Tervo, Jari: Ukko (2022).

Olemattoman Avaimen Poisto Antaa Virheen
    Poista Viite  EiOle2000
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla  Viiteavainta EiOle2000 ei löytynyt.
