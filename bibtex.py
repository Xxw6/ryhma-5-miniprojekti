ERIKOISMERKIT = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_"}


def suojaa(teksti):
    return "".join(ERIKOISMERKIT.get(merkki, merkki) for merkki in str(teksti))



def muodosta_viite(teos):
    if teos.get("tyyppi") == "article":
        viitetyyppi = "article"
        kentat = {
            "author": teos["tekijat"],
            "title": teos["otsikko"],
            "journal": teos["journal"],
            "year": teos["vuosi"],
            "volume": teos.get("volume", ""),
            "pages": teos.get("pages", ""),
        }
    else:
        viitetyyppi = "book"
        kentat = {
            "author": teos["tekijat"],
            "title": teos["otsikko"],
            "year": teos["vuosi"],
            "publisher": teos.get("kustantaja", ""),
        }

    rivit = [f"@{viitetyyppi}{{{teos['viiteavain']},"]
    for nimi, arvo in kentat.items():
        if arvo != "":
            rivit.append(f"  {nimi} = {{{suojaa(arvo)}}},")
    rivit.append("}")
    return "\n".join(rivit)



def muodosta_bibtex(teokset):
    return "\n".join(muodosta_viite(teos) + "\n" for teos in teokset)
