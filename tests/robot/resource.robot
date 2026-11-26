*** Settings ***
Library  AppLibrary.py

*** Keywords ***
Lisaa Kirja
    [Arguments]  ${viiteavain}  ${tekijat}  ${otsikko}  ${vuosi}  ${kustantaja}
    Syota  1
    Syota  ${viiteavain}
    Syota  ${tekijat}
    Syota  ${otsikko}
    Syota  ${vuosi}
    Syota  ${kustantaja}
