*** Settings ***
Resource  resource.robot

*** Test Cases ***
Kirjan Lisays Muodostaa Viiteavaimen Automaattisesti
    Lisaa Kirja  Tervo, Jari  Ukko  2022  Otava
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla  Teos tallennettu viiteavaimella Tervo2022.

Kirja Ilman Pakollista Kenttaa Antaa Virheen
    Lisaa Kirja  Tervo, Jari  ${EMPTY}  2022  Otava
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla  Täytä kaikki pakolliset kentät.

Lisatty Kirja Nakyy Listauksessa
    Lisaa Kirja  Tervo, Jari  Ukko  2022  Otava
    Syota  3
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla  [Tervo2022] Tervo, Jari: Ukko (2022).
