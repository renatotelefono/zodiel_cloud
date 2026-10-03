# -*- coding: utf-8 -*-
"""
Genera le pagine dei 22 Arcani Maggiori (arcani/<slug>.html) e l'indice (arcani/index.html)
partendo dai testi in asset/descrizione_it/*.md.
Uso (dalla cartella del sito):  python strumenti/genera_arcani.py
"""
import html, json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOM = "https://zodiel.cloud"

ARCANI = [
 ("00_il_matto","Il Matto","0","libertà, nuovi inizi, spontaneità, fiducia nella vita","imprudenza, distrazione, rischi inutili"),
 ("01_il_mago","Il Mago","I","volontà, abilità, iniziativa, comunicazione","manipolazione, insicurezza, talenti sprecati"),
 ("02_la_papessa","La Papessa","II","intuizione, saggezza interiore, mistero, silenzio","segreti, chiusura, intuizione ignorata"),
 ("03_l_imperatrice","L'Imperatrice","III","abbondanza, creatività, fertilità, cura","blocco creativo, dipendenza, trascuratezza"),
 ("04_l_imperatore","L'Imperatore","IV","autorità, struttura, stabilità, protezione","rigidità, controllo eccessivo, autoritarismo"),
 ("05_il_papa","Il Papa","V","tradizione, insegnamento, valori, guida spirituale","ribellione, dogmatismo, scelte fuori dagli schemi"),
 ("06_gli_amanti","Gli Amanti","VI","amore, scelta, armonia, unione","indecisione, disarmonia, scelte affrettate"),
 ("07_il_carro","Il Carro","VII","determinazione, vittoria, controllo, movimento","perdita di controllo, ostacoli, mancanza di direzione"),
 ("08_la_forza","La Forza","VIII","coraggio, pazienza, dominio di sé, compassione","insicurezza, debolezza, impulsività"),
 ("09_l_eremita","L'Eremita","IX","introspezione, ricerca interiore, saggezza, solitudine","isolamento, chiusura, rifiuto dei consigli"),
 ("10_la_ruota_della_fortuna","La Ruota della Fortuna","X","cambiamento, destino, cicli, opportunità","battute d'arresto, resistenza al cambiamento, sfortuna"),
 ("11_la_giustizia","La Giustizia","XI","equilibrio, verità, responsabilità, decisioni","ingiustizia, squilibrio, disonestà"),
 ("12_l_appeso","L'Appeso","XII","pausa, sacrificio, nuova prospettiva, attesa","stallo, resistenza, sacrifici inutili"),
 ("13_la_morte","La Morte","XIII","trasformazione, fine di un ciclo, rinascita","paura del cambiamento, stagnazione, attaccamento al passato"),
 ("14_la_temperanza","La Temperanza","XIV","equilibrio, moderazione, pazienza, armonia","eccessi, squilibrio, impazienza"),
 ("15_il_diavolo","Il Diavolo","XV","tentazione, attaccamento, desiderio, materialismo","liberazione, presa di coscienza, rottura delle catene"),
 ("16_la_torre","La Torre","XVI","cambiamento improvviso, crollo, rivelazione","crisi rimandata, paura del cambiamento, resistenza"),
 ("17_la_stella","La Stella","XVII","speranza, ispirazione, rinnovamento, serenità","sfiducia, scoraggiamento, speranze deluse"),
 ("18_la_luna","La Luna","XVIII","illusione, inconscio, paure, intuizione","chiarezza ritrovata, paure che si dissolvono, confusione"),
 ("19_il_sole","Il Sole","XIX","gioia, successo, vitalità, chiarezza","entusiasmo offuscato, ritardi, ottimismo eccessivo"),
 ("20_il_giudizio","Il Giudizio","XX","risveglio, rinascita, chiamata interiore, bilancio","autocritica, dubbi, occasioni mancate"),
 ("21_il_mondo","Il Mondo","XXI","compimento, realizzazione, viaggio, integrazione","incompletezza, ritardi, obiettivi non raggiunti"),
]

NOTE = {
 "13_la_morte": "Nonostante il nome, la Morte nei tarocchi non annuncia una morte fisica: rappresenta la chiusura di una fase e l'inizio di qualcosa di nuovo.",
 "16_la_torre": "La Torre è una delle carte più temute, ma il crollo che annuncia libera spazio per costruire su basi più solide.",
 "15_il_diavolo": "Il Diavolo non va letto come una carta \"malvagia\": parla dei legami e delle abitudini che ci tengono prigionieri.",
}

POSIZIONI = ["Passato", "Presente", "Futuro"]

FEMMINILI = {"02_la_papessa","03_l_imperatrice","08_la_forza","10_la_ruota_della_fortuna","11_la_giustizia",
             "13_la_morte","14_la_temperanza","16_la_torre","17_la_stella","18_la_luna"}
PLURALI = {"06_gli_amanti"}

def accorda(fid, parola):
    """dritto/rovesciato concordati con il nome della carta."""
    radice = parola[:-1]
    if fid in PLURALI: return radice + "i"
    if fid in FEMMINILI: return radice + "a"
    return parola

def slug(file_id):
    return file_id[3:].replace("_", "-")

def leggi(file_id, rov, pos):
    nome = f"{file_id}{'_r' if rov else ''}_{pos}.md"
    with open(os.path.join(BASE, "asset", "descrizione_it", nome), encoding="utf-8-sig") as f:
        testo = f.read()
    paragrafi = [p.strip() for p in re.split(r"\r?\n", testo) if p.strip()]
    return "\n".join(f"        <p>{html.escape(p, quote=False)}</p>" for p in paragrafi)

def pagina(i):
    fid, nome, num, kw_d, kw_r = ARCANI[i]
    s = slug(fid)
    url = f"{DOM}/arcani/{s}"
    prev_ = ARCANI[i-1] if i > 0 else None
    next_ = ARCANI[i+1] if i < len(ARCANI)-1 else None
    titolo = f"{nome}: significato nei Tarocchi, dritto e rovesciato | Zodiel"
    desc = (f"Significato di {nome} (Arcano {num}) nei tarocchi, dritto e rovesciato, "
            f"nel passato, nel presente e nel futuro. Interpretazione completa e lettura gratuita online.")
    img = f"/asset/img_it/{fid}.jpeg"
    nota = f'\n      <p class="nota">{html.escape(NOTE[fid], quote=False)}</p>' if fid in NOTE else ""

    def sezione(rov):
        blocchi = []
        for pos in POSIZIONI:
            blocchi.append(
                f'      <h3>{nome}{" " + accorda(fid, "rovesciato") if rov else ""} nel {pos.lower()}</h3>\n'
                f'{leggi(fid, rov, pos)}')
        return "\n".join(blocchi)

    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Zodiel", "item": DOM + "/"},
            {"@type": "ListItem", "position": 2, "name": "Arcani Maggiori", "item": DOM + "/arcani/"},
            {"@type": "ListItem", "position": 3, "name": nome, "item": url},
        ]}

    nav = '    <nav class="prevnext">\n'
    nav += (f'      <a href="/arcani/{slug(prev_[0])}">&larr; {prev_[1]}</a>\n' if prev_ else '      <span></span>\n')
    nav += '      <a href="/arcani/">Tutti gli Arcani</a>\n'
    nav += (f'      <a href="/arcani/{slug(next_[0])}">{next_[1]} &rarr;</a>\n' if next_ else '      <span></span>\n')
    nav += '    </nav>'

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <script src="/analytics.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titolo)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(titolo)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOM}{img}">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/arcani/arcani.css">
  <script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
</head>
<body>
  <header class="testata">
    <a class="logo" href="/">Zodiel</a>
    <nav><a href="/arcani/">Arcani Maggiori</a> <a class="pill" href="/master">Fai una lettura</a></nav>
  </header>

  <main class="arcano">
    <p class="briciole"><a href="/">Home</a> &rsaquo; <a href="/arcani/">Arcani Maggiori</a> &rsaquo; {nome}</p>
    <h1>{nome}: significato nei Tarocchi</h1>

    <section class="intro">
      <img src="{img}" alt="Carta dei tarocchi {nome}, Arcano Maggiore {num}" width="240" height="403">
      <div>
        <p><strong>{nome}</strong> {'sono' if fid in PLURALI else 'è'} l'Arcano Maggiore numero <strong>{num}</strong> dei tarocchi. Il suo significato cambia a seconda che la carta esca <strong>dritta</strong> o <strong>rovesciata</strong> e della posizione che occupa nella stesa: passato, presente o futuro.</p>
        <p><span class="etichetta">Dritto:</span> {kw_d}.</p>
        <p><span class="etichetta">Rovesciato:</span> {kw_r}.</p>{nota}
        <a class="cta" href="/master">Scopri cosa dicono le carte per te</a>
      </div>
    </section>

    <section>
      <h2>{nome} {accorda(fid, "dritto")}</h2>
{sezione(False)}
    </section>

    <section>
      <h2>{nome} {accorda(fid, "rovesciato")}</h2>
      <img class="rovesciata" src="{img}" alt="{nome} {accorda(fid, 'rovesciato')}" width="120" height="201" loading="lazy">
{sezione(True)}
    </section>

    <section class="finale">
      <h2>Fai la tua lettura gratuita</h2>
      <p>Mescola il mazzo, scegli tre carte e scopri cosa raccontano del tuo passato, presente e futuro. È gratuita e non serve registrarsi.</p>
      <a class="cta" href="/master">Inizia la lettura</a>
    </section>

{nav}
  </main>

  <footer class="piede"><a href="/">zodiel.cloud</a> · <a href="/arcani/">Arcani Maggiori</a> · <a href="/privacy">Privacy e cookie</a></footer>
</body>
</html>
"""

def indice():
    voci = "\n".join(
        f'      <li><a href="/arcani/{slug(fid)}"><img src="/asset/img_it/{fid}.jpeg" alt="{nome}" width="120" height="201" loading="lazy">'
        f'<span class="num">{num}</span><span class="nome">{nome}</span></a></li>'
        for fid, nome, num, _, _ in ARCANI)
    desc = "Il significato dei 22 Arcani Maggiori dei tarocchi, dritti e rovesciati, nel passato, nel presente e nel futuro. Scegli una carta e leggi l'interpretazione completa."
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <script src="/analytics.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Significato dei 22 Arcani Maggiori dei Tarocchi | Zodiel</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{DOM}/arcani/">
  <meta property="og:title" content="Significato dei 22 Arcani Maggiori dei Tarocchi">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{DOM}/arcani/">
  <meta property="og:image" content="{DOM}/asset/tarot_corona.jpg">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/arcani/arcani.css">
</head>
<body>
  <header class="testata">
    <a class="logo" href="/">Zodiel</a>
    <nav><a href="/arcani/">Arcani Maggiori</a> <a class="pill" href="/master">Fai una lettura</a></nav>
  </header>

  <main class="arcano">
    <p class="briciole"><a href="/">Home</a> &rsaquo; Arcani Maggiori</p>
    <h1>Il significato dei 22 Arcani Maggiori</h1>
    <p class="lead">Gli Arcani Maggiori sono le 22 carte principali dei tarocchi, dal Matto (0) al Mondo (XXI). Ognuna ha un significato diverso se esce dritta o rovesciata, e se si trova nella posizione del passato, del presente o del futuro. Scegli una carta per leggere tutte le sue interpretazioni.</p>
    <ul class="griglia">
{voci}
    </ul>
    <section class="finale">
      <h2>Fai la tua lettura gratuita</h2>
      <p>Mescola il mazzo e scegli tre carte: scoprirai cosa raccontano del tuo passato, presente e futuro.</p>
      <a class="cta" href="/master">Inizia la lettura</a>
    </section>
  </main>

  <footer class="piede"><a href="/">zodiel.cloud</a> · <a href="/privacy">Privacy e cookie</a></footer>
</body>
</html>
"""

def scrivi(nome_file, testo):
    with open(os.path.join(BASE, "arcani", nome_file), "w", encoding="utf-8", newline="\r\n") as f:
        f.write(testo)

if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "arcani"), exist_ok=True)
    for i in range(len(ARCANI)):
        scrivi(slug(ARCANI[i][0]) + ".html", pagina(i))
    scrivi("index.html", indice())
    print("Create", len(ARCANI), "pagine + indice")
