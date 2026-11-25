# Definition of Done

User story on valmis, kun kaikki seuraavat kohdat täyttyvät:

1. Storyn hyväksymiskriteerit on kirjattu product backlogiin ja ne täyttyvät.
2. Hyväksymiskriteereille on Robot Framework -testit (`tests/robot/`), ja ne menevät läpi (sprintistä 2 alkaen).
3. Uudelle koodille on yksikkötestit, ja kaikki testit menevät läpi.
4. Koko projektin testikattavuus (haarautumakattavuus) on vähintään 70 %.
5. Koodi noudattaa projektin pylint-sääntöjä (`.pylintrc`).
6. Muutos on tehty omassa haarassaan ja yhdistetty `main`iin pull requestilla, jonka CI on vihreä ja jonka vähintään yksi toinen tiimiläinen on hyväksynyt.
7. Nimeäminen on selkeää, ja ratkaisu sopii sovelluksen kerrosarkkitehtuuriin (käyttöliittymä, palvelu, varasto).
8. README on päivitetty, jos muutos vaikuttaa sovelluksen käyttöön tai asennukseen.

Asiakas näkee testien ja kattavuuden tilan README:n CI- ja Codecov-merkeistä.
