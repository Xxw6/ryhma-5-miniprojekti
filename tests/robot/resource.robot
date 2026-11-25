*** Settings ***
Library  AppLibrary.py

*** Keywords ***
Lisaa Kirja
    [Arguments]  ${tekijat}  ${otsikko}  ${vuosi}  ${kustantaja}
    Syota  1
    Syota  ${tekijat}
    Syota  ${otsikko}
    Syota  ${vuosi}
    Syota  ${kustantaja}
