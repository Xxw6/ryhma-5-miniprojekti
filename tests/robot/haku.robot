*** Settings ***
Resource    resource.robot

*** Test Cases ***
Haku Loytaa Tekijan Perusteella
    Lisaa Kirja    Tervo, Jari    Ukko    2022    Otava
    Syota    6
    Syota    Tervo
    Syota    ${EMPTY}
    Syota    ${EMPTY}
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla    [Tervo2022] Tervo, Jari: Ukko (2022). Otava

Haku Loytaa Vuoden Perusteella
    Lisaa Kirja    Tervo, Jari    Ukko    2022    Otava
    Syota    6
    Syota    ${EMPTY}
    Syota    2022
    Syota    ${EMPTY}
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla    [Tervo2022] Tervo, Jari: Ukko (2022). Otava

Haku Loytaa Kustantajan Perusteella
    Lisaa Kirja    Tervo, Jari    Ukko    2022    Otava
    Syota    6
    Syota    ${EMPTY}
    Syota    ${EMPTY}
    Syota    Ota
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla    [Tervo2022] Tervo, Jari: Ukko (2022). Otava

Haku Loytaa Artikkelin Julkaisun Perusteella
    Syota    2
    Syota    Tervo2022
    Syota    Tervo, Jari
    Syota    Testiartikkeli
    Syota    Julkaisu X
    Syota    2022
    Syota    ${EMPTY}
    Syota    ${EMPTY}
    Syota    6
    Syota    ${EMPTY}
    Syota    ${EMPTY}
    Syota    Julkaisu
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla    [Tervo2022] Tervo, Jari: Testiartikkeli (2022). Julkaisu X

Haku Ilmoittaa Tyhjasta Tuloksesta
    Lisaa Kirja    Tervo, Jari    Ukko    2022    Otava
    Syota    6
    Syota    EiLoydy
    Syota    ${EMPTY}
    Syota    ${EMPTY}
    Kaynnista Sovellus
    Tulosteessa Pitaisi Olla    Ei hakutuloksia.