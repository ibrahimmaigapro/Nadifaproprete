# -*- coding: utf-8 -*-
import os, re, html, datetime, hashlib
OUT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://nadifaproprete.fr"
PHONE_H = "06 47 27 10 62"; PHONE_T = "+33647271062"; WA = "33647271062"
EMAIL = "nadifa.proprete@gmail.com"
GBP = "https://www.google.com/maps?cid=6909362966415409349"
# Médiateur de la consommation : à remplir après adhésion (nom, adresse postale, site). Tant que None, rien n'est affiché.
MEDIATEUR = None  # ex. {"nom": "...", "adresse": "...", "site": "https://..."}
YEAR = 2026
# Zone mise en avant : Toulouse + communes proches (concentration SEO locale).
ZONES = ["Toulouse (tous quartiers)","Blagnac","Colomiers","Tournefeuille","Cugnaux","Portet-sur-Garonne","Muret"]
ZONES_TXT = ", ".join(ZONES[1:-1]) + " et " + ZONES[-1]
# Règle de déplacement, reprise telle quelle partout où le site en parle (zone d'intervention et hors zone).
DEPLACEMENT = ("Le déplacement est gratuit dans cette zone et jusqu'à 10 km autour. De 10 à 20 km autour, "
               "il est facturé et annoncé dans le devis sur photo. Au-delà de 20 km, nous n'intervenons pas.")
DEPLACEMENT_COURT = ("Déplacement gratuit à Toulouse, dans les <a href=\"contact.html#zone\">communes proches</a> et jusqu'à 10 km autour ; "
                     "facturé de 10 à 20 km autour ; au-delà de 20 km, nous n'intervenons pas.")  # même règle, en une phrase
AREA_LD = ", ".join('{ "@type": "City", "name": "%s" }' % z.split(" (")[0] for z in ZONES)

def wa(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"

WA_DEVIS = wa("Bonjour Nadifa Propreté, je souhaite un devis pour : ")

def picture(name, alt, sizes="(max-width: 700px) 100vw, 50vw", cls="", eager=False, w=1400, h=1050):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/{name}-800.webp" '
            f'srcset="assets/img/{name}-480.webp 480w, assets/img/{name}-800.webp 800w, assets/img/{name}-1400.webp 1400w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(alt)}" {load}>')

ICON = {
 "car": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11m-14 0h14a2 2 0 0 1 2 2v4h-2a2 2 0 1 1-4 0H9a2 2 0 1 1-4 0H3v-4a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 "sofa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11V8a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v3M3 13a2 2 0 0 1 2-2h0a2 2 0 0 1 2 2v2h10v-2a2 2 0 0 1 4 0v5H3v-5zm2 5v1m14-1v1" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "bed": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 18V8m18 10v-6a2 2 0 0 0-2-2H3m0 4h18M6 10V7h5v3M3 16v2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "rug": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4v16M19 4v16M5 6h14M5 18h14M8 9h8M8 15h8M8 12h8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 "window": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16v16H4zM12 4v16M4 12h16" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
 "spark": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM5 17l.8 2.2L8 20l-2.2.8L5 23l-.8-2.2L2 20l2.2-.8z" fill="currentColor"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 "wind": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h8a2 2 0 1 1-2 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 "tag": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12V4h8l9 9-8 8-9-9z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="7.5" cy="8.5" r="1.5" fill="currentColor"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.5 8.5c.2-.6.7-.6 1-.6h.6c.2 0 .4.1.5.4l.7 1.7c.1.2 0 .4-.1.6l-.5.6c-.1.1-.1.3 0 .4a6 6 0 0 0 2.9 2.7c.2.1.3 0 .4-.1l.7-.8c.2-.2.4-.2.6-.1l1.6.8c.2.1.3.3.3.5 0 .7-.3 1.3-.9 1.6-.6.4-1.3.5-2 .3a8.5 8.5 0 0 1-5.5-5.3c-.3-.9-.2-1.8.3-2.7z" fill="currentColor"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v12H3zM3 7l9 6 9-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "prev": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "next": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z" fill="currentColor"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
}

MARK = '<svg class="brand-mark" viewBox="0 0 64 64" width="44" height="44" aria-hidden="true"><rect width="64" height="64" rx="16" fill="#0cc0df"/><path d="M18 46V18h7l14 18V18h7v28h-7L25 28v18z" fill="#fff"/><path d="M48 10l1.5 4 4 1.5-4 1.5-1.5 4-1.5-4-4-1.5 4-1.5z" fill="#fff" fill-opacity=".92"/></svg>'

LOGO_IMG = '<img class="brand-logo" src="assets/img/logo-nadifa-600.webp" srcset="assets/img/logo-nadifa-600.webp 600w, assets/img/logo-nadifa.webp 1426w" sizes="220px" width="600" height="180" alt="Nadifa Propreté">'

NAV = [("./","Accueil"),("services.html","Particuliers"),("nettoyage-professionnels-toulouse.html","Professionnels"),("reservation.html","Réserver"),("contact.html","Contact")]

def head(title, desc, path, og_type="website", extra=""):
    canonical = BASE + ("/" if path=="index.html" else "/"+path)
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google-site-verification" content="cj4is6xl51RC_bZMNwxS9jAQGViXITtwPbpSm2-YP9A">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0b1f33">
<meta property="og:locale" content="fr_FR">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Nadifa Propreté">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="assets/img/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="stylesheet" href="assets/css/style.css?v={ASSET_V}">
{extra}</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
'''

def header(active):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a></li>' for h,t in NAV)
    return f'''<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="./" aria-label="Nadifa Propreté, accueil">
      {LOGO_IMG}
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">
      <svg class="ico-burger" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
      <svg class="ico-close" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
    </button>
    <nav id="nav" class="nav">
      <ul>{links}</ul>
      <a class="btn btn-primary btn-nav" href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} Devis WhatsApp</a>
    </nav>
  </div>
</header>
<main id="main">
'''

def footer():
    return f'''</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="brand brand-plate" href="./">{LOGO_IMG}</a>
      <p class="muted">Nettoyage à domicile de canapés, matelas, tapis et intérieurs de voiture. Toulouse et communes proches.</p>
    </div>
    <div>
      <h2 class="footer-title">Navigation</h2>
      <ul class="footer-links">
        <li><a href="services.html">Services</a></li>
        <li><a href="nettoyage-canape-toulouse.html">Nettoyage canapé</a></li>
        <li><a href="nettoyage-matelas-toulouse.html">Nettoyage matelas</a></li>
        <li><a href="nettoyage-tapis-moquette-toulouse.html">Nettoyage tapis et moquette</a></li>
        <li><a href="nettoyage-interieur-voiture-toulouse.html">Nettoyage intérieur voiture</a></li>
        <li><a href="nettoyage-professionnels-toulouse.html">Professionnels</a></li>
        <li><a href="reservation.html">Réserver une intervention</a></li>
        <li><a href="contact.html">Contact et zone d'intervention</a></li>
        <li><a href="{GBP}" target="_blank" rel="noopener">Avis Google</a></li>
        <li><a href="mentions-legales.html">Mentions légales</a></li>
        <li><a href="politique-confidentialite.html">Politique de confidentialité</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-title">Contact</h2>
      <ul class="footer-links">
        <li><a href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a></li>
        <li><a href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp</a></li>
        <li><a href="mailto:{EMAIL}">{ICON["mail"]} {EMAIL}</a></li>
        <li>{ICON["clock"]} Tous les jours sauf le vendredi, 7 h – 22 h 30</li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>© {YEAR} Nadifa Propreté · SIRET 989 023 213 00014</p>
  </div>
</footer>
<div class="mobile-bar" aria-label="Actions rapides">
  <a href="tel:{PHONE_T}">{ICON["phone"]} Appeler</a>
  <a class="mobile-bar-wa" href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} Devis WhatsApp</a>
</div>
<script src="assets/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
'''

# ---------- Grille de prix ----------
# Une liste par catégorie : (prestation, détail, prix). Reprise telle quelle sur la page Services, sur la page
# de la catégorie et dans les informations lues par Google : un prix s'écrit ici, et dans la description Google de la page.
PRIX_CANAPE = [("Canapé 2 ou 3 places","Assise, dossier et accoudoirs. Tissu ou cuir.","69 €"),
               ("Canapé 4 ou 5 places ou d'angle","Méridienne comprise. Tissu ou cuir.","79 €"),
               ("Fauteuil","Fauteuil de salon, chaise en tissu, tête de lit.","25 €")]
PRIX_MATELAS = [("Matelas 1 place","Une face.","45 €"),
                ("Matelas 2 places","Une face.","55 €"),
                ("Matelas king size","180 × 200 cm et plus, une face.","65 €")]
PRIX_TAPIS = [("Petit tapis","Jusqu'à 2 × 2 m.","35 €"),
              ("Grand tapis","Jusqu'à 2 × 3 m.","45 €"),
              ("Tapis plus grand que 2 × 3 m","Prix selon les dimensions.","Sur devis"),
              ("Moquette","Chambre, salon, bureau, escalier.","8 €/m²")]
PRIX_VOITURE = [("Formule Basique","Aspiration complète de l'habitacle, dépoussiérage des plastiques, du tableau de bord et des aérateurs.","À partir de 50 €"),
                ("Formule Premium","Formule Basique + shampoing des sièges, tapis de sol et moquettes par injection-extraction.","À partir de 70 €")]

# ---------- Remise multi-prestations ----------
# Règle de la Finance : −15 % sur le total des prestations dès 2 prestations dans la même intervention, voiture comprise ;
# le total est arrondi à l'euro du dessous. Les exemples du site sont calculés ici à partir de la grille de prix et de ce
# pourcentage : ils ne peuvent pas s'en écarter si un prix ou la remise change.
REMISE_POURCENT = 15

def montant(prix):
    """« 69 € » ou « À partir de 70 € » -> 69 ou 70. Une ligne sans montant (« Sur devis », « 8 €/m² ») n'a pas de total."""
    m = re.fullmatch(r"(?:À partir de )?(\d+) €", prix)
    if not m:
        raise ValueError(f"Prix inutilisable pour un exemple de remise : « {prix} »")
    return int(m.group(1))

def ligne(grille, nom):
    """La ligne de la grille qui porte ce nom : le site ne se fabrique plus si elle change de nom."""
    for l in grille:
        if l[0] == nom:
            return l
    raise ValueError(f"Prestation absente de la grille : « {nom} »")

def remise_exemple(titre, lignes):
    """Une ligne de prix pour la page Services : le total sans remise, puis le total remisé (arrondi à l'euro du dessous).
    Si une ligne est un prix de départ (« À partir de »), le total l'est aussi."""
    montants = [montant(p) for _, _, p in lignes]
    depart = any(p.startswith("À partir de") for _, _, p in lignes)
    sans = sum(montants)
    avec = sans * (100 - REMISE_POURCENT) // 100  # calcul entier : pas d'erreur d'arrondi
    detail = " + ".join(f"{m} €" for m in montants) + f" = {sans} € sans remise{' (prix de départ)' if depart else ''}, avec la remise :"
    return price_row(titre, detail, ("À partir de " if depart else "") + f"{avec} €")

def ld_offers(prices, service_type):
    """Offres lues par Google, une par ligne de prix : « 69 € », ou « 8 €/m² » (prix au m²). Une ligne sans montant (sur devis) reste sans prix."""
    out = []
    for name, _, price in prices:
        m = re.fullmatch(r"(?P<euros>\d+) €(?P<m2>/m²)?", price)
        if m and m["m2"]:
            spec = f'"priceSpecification": {{ "@type": "UnitPriceSpecification", "price": "{m["euros"]}", "priceCurrency": "EUR", "unitText": "m²" }}, '
        elif m:
            spec = f'"price": "{m["euros"]}", "priceCurrency": "EUR", '
        elif price == "Sur devis":
            spec = ""
        else:  # un prix mal tapé donnerait en silence une offre sans prix
            raise ValueError(f"Prix illisible pour Google : « {price} » ({name})")
        out.append(f'{{ "@type": "Offer", {spec}"itemOffered": {{ "@type": "Service", "name": "{name}", "serviceType": "{service_type}" }} }}')
    return out

LD_GRILLE = ",\n      ".join(ld_offers(PRIX_CANAPE, "Nettoyage de textile d'ameublement")
                              + ld_offers(PRIX_MATELAS, "Nettoyage de literie")
                              + ld_offers(PRIX_TAPIS, "Nettoyage de tapis et moquettes"))

# ---------- JSON-LD ----------
LD_BUSINESS = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "{BASE}/#business",
  "name": "Nadifa Propreté",
  "alternateName": "Nadifa Propreté – Nettoyage à domicile Toulouse",
  "description": "Nettoyage à domicile par injection-extraction : canapés, fauteuils, matelas, tapis, moquettes et intérieurs de voiture. Toulouse et communes proches.",
  "url": "{BASE}/",
  "telephone": "{PHONE_T}",
  "email": "{EMAIL}",
  "image": "{BASE}/assets/img/og-image.jpg",
  "logo": "{BASE}/assets/img/icon-512.png",
  "priceRange": "€€",
  "currenciesAccepted": "EUR",
  "address": {{ "@type": "PostalAddress", "addressLocality": "Toulouse", "postalCode": "31100", "addressCountry": "FR" }},
  "areaServed": [ {AREA_LD} ],
  "openingHoursSpecification": [{{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Saturday","Sunday"], "opens": "07:00", "closes": "22:30" }}],
  "sameAs": ["{GBP}"],
  "founder": {{ "@type": "Person", "name": "Ibrahim Maiga" }},
  "hasOfferCatalog": {{
    "@type": "OfferCatalog", "name": "Prestations de nettoyage",
    "itemListElement": [
      {{ "@type": "Offer", "priceSpecification": {{ "@type": "PriceSpecification", "minPrice": "50", "priceCurrency": "EUR" }}, "itemOffered": {{ "@type": "Service", "name": "Nettoyage intérieur de voiture – Formule Basique", "serviceType": "Nettoyage automobile intérieur" }} }},
      {{ "@type": "Offer", "priceSpecification": {{ "@type": "PriceSpecification", "minPrice": "70", "priceCurrency": "EUR" }}, "itemOffered": {{ "@type": "Service", "name": "Nettoyage intérieur de voiture – Formule Premium", "serviceType": "Nettoyage automobile intérieur" }} }},
      {LD_GRILLE}
    ]
  }}
}}
</script>
'''

def breadcrumb(name, path):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Accueil","item":"{BASE}/"}},
{{"@type":"ListItem","position":2,"name":"{name}","item":"{BASE}/{path}"}}]}}
</script>
'''

# ---------- Reusable blocks ----------
def cta_band(titre="Envoyez une photo, on vous rappelle rapidement",
             texte="Envoyez une photo de votre canapé, matelas, tapis ou véhicule sur WhatsApp : vous recevez le tarif exact avant toute intervention.",
             wa_lien=None, bouton="Envoyer une photo"):
    wa_lien = wa_lien or WA_DEVIS
    return f'''<section class="cta-band">
  <div class="wrap cta-inner">
    <div>
      <h2>{titre}</h2>
      <p>{texte}</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-light" href="{wa_lien}" target="_blank" rel="noopener">{ICON["wa"]} {bouton}</a>
      <a class="btn btn-outline-light" href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a>
    </div>
  </div>
</section>
'''

SERVICES = [
 ("car","Intérieur de voiture","voiture-207","Aspiration complète, plastiques, sièges et tapis de sol. Formule Basique ou Premium selon l'état.","nettoyage-interieur-voiture-toulouse.html","Intérieur d'une Peugeot 207 après nettoyage par Nadifa Propreté : tableau de bord, siège et moquette"),
 ("sofa","Canapés & fauteuils",("canape-avant","canape-apres"),"Tissu, microfibre, velours ou cuir : taches, auréoles et odeurs traitées en profondeur, sans abîmer la matière.","nettoyage-canape-toulouse.html",("Accoudoir d'un canapé en tissu gris clair taché, avant nettoyage","Le même accoudoir après nettoyage par Nadifa Propreté : la tache a disparu")),
 ("bed","Matelas","matelas","Poussière, acariens et traces. Un matelas assaini, sec en quelques heures.","nettoyage-matelas-toulouse.html","Illustration : aspirateur sur un matelas blanc"),
 ("rug","Tapis & moquettes","tapis","Tapis nettoyé chez vous, sans l'emporter. Moquettes de chambre, salon ou bureau.","nettoyage-tapis-moquette-toulouse.html","Tapis de salon bleu à médaillon nettoyé à domicile par Nadifa Propreté"),
]

def compare(left, right, alt_left, alt_right, sizes="(max-width: 760px) 100vw, 50vw", w=1400, h=1400):
    """Voitures : deux images superposées, une poignée à glisser, à gauche `left` (avant), à droite `right` (après)."""
    def img(name, alt, cls):
        return (f'<img class="{cls}" src="assets/img/{name}-800.webp" '
                f'srcset="assets/img/{name}-480.webp 480w, assets/img/{name}-800.webp 800w, assets/img/{name}-1400.webp 1400w" '
                f'sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(alt)}" loading="lazy" decoding="async" draggable="false">')
    return f'''<div class="compare" style="--pos:50%" data-start="50">
        {img(right, alt_right, "cmp-right")}
        {img(left, alt_left, "cmp-left")}
        <span class="cmp-label cmp-label-l">Avant</span><span class="cmp-label cmp-label-r">Après</span>
        <div class="cmp-line" aria-hidden="true"><span class="cmp-handle"><svg viewBox="0 0 24 24"><path d="M9 6l-5 6 5 6M15 6l5 6-5 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span></div>
        <input class="cmp-range" type="range" min="0" max="100" value="50" aria-label="Faire glisser pour comparer : Avant / Après">
      </div>'''

def avant_apres(avant, apres, alt_avant, alt_apres, titre="", sizes="min(520px, 84vw)", eager=False, w=1400, h=933):
    """Canapés : deux photos superposées, deux boutons. Départ sur « Avant ». Marche même si les deux photos n'ont pas le même cadrage."""
    titre_html = f'<span class="ba-titre">{titre}</span>' if titre else ""
    return f'''<figure class="ba">
        <div class="ba-media">
          {picture(apres, alt_apres, sizes=sizes, cls="ba-img ba-apres", w=w, h=h)}
          {picture(avant, alt_avant, sizes=sizes, cls="ba-img ba-avant", eager=eager, w=w, h=h)}
          <span class="ba-tag">Avant</span>
        </div>
        <figcaption class="ba-bar">{titre_html}<span class="ba-btns" role="group" aria-label="Voir la photo avant ou après le nettoyage"><button type="button" class="ba-btn" data-ba="avant" aria-pressed="true">Avant</button><button type="button" class="ba-btn" data-ba="apres" aria-pressed="false">Après</button></span></figcaption>
      </figure>'''

# Résultats canapés, dans l'ordre des paramètres de avant_apres() : (photo avant, photo après, texte de la photo avant, texte de la photo après, intitulé).
# Une photo présentée ici est une vraie photo d'une intervention Nadifa, avec l'accord du client.
RESULTATS_CANAPE = [
 ("canape-velours-avant","canape-velours-apres","Canapé en velours côtelé beige avant nettoyage : traces sombres sur les assises, le dossier et le devant","Le même canapé en velours côtelé après nettoyage par Nadifa Propreté à Toulouse","Canapé velours côtelé · vue d'ensemble"),
 ("canape-velours-assise-avant","canape-velours-assise-apres","Assise d'un canapé en velours côtelé avant nettoyage : auréoles et traces sombres","Assise du même canapé après nettoyage par Nadifa Propreté","Canapé velours côtelé · assise"),
 ("canape-angle-meridienne-avant","canape-angle-meridienne-apres","Méridienne d'un canapé d'angle gris avant nettoyage : grandes auréoles sur le tissu","La même méridienne après nettoyage par Nadifa Propreté","Canapé d'angle gris · méridienne"),
 ("canape-angle-assise-avant","canape-angle-assise-apres","Assise d'un canapé d'angle gris avant nettoyage : auréoles sur le tissu","Assise du même canapé d'angle après nettoyage par Nadifa Propreté","Canapé d'angle gris · assise"),
 ("canape-boudins-avant","canape-boudins-apres","Canapé gris à boudins avant nettoyage : assises ternies et marquées","Le même canapé à boudins après nettoyage par Nadifa Propreté","Canapé gris à boudins · vue d'ensemble"),
 ("canape-avant","canape-apres","Accoudoir d'un canapé en tissu gris clair taché, avant nettoyage","Le même accoudoir après nettoyage par Nadifa Propreté : la tache a disparu","Canapé gris clair · tache sur l'accoudoir"),
]

def carrousel_canapes():
    cartes = "".join(avant_apres(*resultat) for resultat in RESULTATS_CANAPE)
    return f'''<div class="ba-carrousel">
      <div class="ba-fleches" hidden>
        <button type="button" class="ba-fleche ba-prev" aria-label="Résultat précédent">{ICON["prev"]}</button>
        <button type="button" class="ba-fleche ba-next" aria-label="Résultat suivant">{ICON["next"]}</button>
      </div>
      <div class="ba-bande" tabindex="0" role="region" aria-label="Résultats avant et après nettoyage de canapés">{cartes}</div>
    </div>'''

# ---------- INDEX ----------
def page_index():
    h = head("Nettoyage canapé, matelas, tapis et voiture à Toulouse | Nadifa Propreté",
             "Nettoyage à domicile de canapés, matelas, tapis et intérieurs de voiture à Toulouse, par injection-extraction. Devis sur photo, intervention sous 48 h.",
             "index.html", extra=LD_BUSINESS + '<link rel="preload" as="image" href="assets/img/canape-velours-avant-800.webp" imagesrcset="assets/img/canape-velours-avant-480.webp 480w, assets/img/canape-velours-avant-800.webp 800w, assets/img/canape-velours-avant-1400.webp 1400w" imagesizes="(max-width: 900px) 100vw, 45vw">\n')
    def card(ic, t, img, d, link, alt):
        body = f'''<span class="icon">{ICON[ic]}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <span class="link-more">Voir la prestation</span>'''
        if isinstance(img, tuple):
            # Avant / après à boutons : la photo reste hors du lien, sinon la toucher ouvrirait la page.
            return f'''<div class="card service-card">
      <div class="card-media">{avant_apres(img[0], img[1], alt[0], alt[1], sizes="(max-width: 700px) 100vw, 25vw", w=1400, h=1050)}</div>
      <a class="card-body" href="{link}">
        {body}
      </a>
    </div>'''
        return f'''<a class="card service-card" href="{link}">
      <div class="card-media">{picture(img, alt, sizes="(max-width: 700px) 100vw, 25vw", w=1024, h=1024)}</div>
      <div class="card-body">
        {body}
      </div>
    </a>'''
    cards = "".join(card(*s) for s in SERVICES)
    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <p class="eyebrow">Nettoyage à domicile · Toulouse et communes proches</p>
      <h1>Canapés, matelas, tapis et intérieurs de voiture&nbsp;: propres en profondeur, chez vous.</h1>
      <p class="lead">Nettoyage professionnel avec du matériel de pro et des produits adaptés à chaque textile, et un tarif annoncé avant de commencer. Intervention sous 48&nbsp;h à Toulouse et dans les communes proches.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} Devis gratuit sur WhatsApp</a>
        <a class="btn btn-ghost btn-lg" href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a>
      </div>
      <ul class="hero-proof">
        <li>{ICON["check"]} Intervention sous 48 h</li>
        <li>{ICON["check"]} Sec en quelques heures</li>
        <li>{ICON["check"]} Prix fixe, sans surprise</li>
        <li>{ICON["check"]} Avis Google 5/5</li>
      </ul>
    </div>
    <div class="hero-media">
      {avant_apres(*RESULTATS_CANAPE[0], sizes="(max-width: 900px) 100vw, 45vw", eager=True)}
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Nos prestations</p>
      <h2>Ce que nous nettoyons</h2>
      <p class="muted">Tout se fait chez vous ou sur votre place de parking. Il suffit d'une prise électrique.</p>
    </div>
    <div class="grid-4">{cards}</div>
    <p class="center"><a class="btn btn-secondary" href="services.html">Toutes les prestations et tarifs</a></p>
  </div>
</section>

<section class="section section-alt" id="comment">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Simple et rapide</p>
      <h2>Comment ça se passe</h2>
    </div>
    <ol class="steps">
      <li><span class="step-num">1</span><h3>Vous envoyez une photo</h3><p>Sur WhatsApp ou par téléphone, décrivez ce qu'il faut nettoyer. On vous rappelle rapidement avec un prix fixe.</p></li>
      <li><span class="step-num">2</span><h3>On fixe un créneau</h3><p>Généralement sous 48 h, tous les jours sauf le vendredi, de 7 h à 22 h 30, à l'heure qui vous arrange.</p></li>
      <li><span class="step-num">3</span><h3>Nettoyage à domicile</h3><p>Pré-traitement des taches, injection-extraction, finitions. Comptez 45 min à 2 h selon la prestation.</p></li>
      <li><span class="step-num">4</span><h3>Vous profitez</h3><p>Le textile est sec en quelques heures. Vous réglez après l'intervention.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="resultats">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Avant / après</p>
      <h2>Des résultats visibles, pas des promesses</h2>
    </div>
    {carrousel_canapes()}
    <div class="grid-2 results">
      <figure class="result">
        {compare("yaris-avant", "yaris-apres", "Toyota Yaris avant nettoyage : tableau de bord poussiéreux, tapis de sol pleins de débris", "Toyota Yaris après nettoyage par Nadifa Propreté : console, plastiques et moquettes propres")}
        <figcaption>Citadine de tous les jours : tableau de bord, console et tapis de sol. Faites glisser pour comparer.</figcaption>
      </figure>
      <figure class="result">
        {compare("207-avant", "207-apres", "Peugeot 207 avant nettoyage : miettes et poussière sur les tapis de sol et les sièges", "Peugeot 207 après nettoyage par Nadifa Propreté : sièges, moquettes et plastiques nets")}
        <figcaption>Berline compacte : sièges en tissu, moquettes et plastiques. Faites glisser pour comparer.</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="section section-dark" id="pourquoi">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Pourquoi Nadifa</p>
      <h2>Ce qui fait la différence</h2>
    </div>
    <div class="grid-2 features">
      <div class="feature"><span class="icon">{ICON["spark"]}</span><h3>Injection-extraction professionnelle</h3><p>Une machine professionnelle qui nettoie dans la fibre, pas seulement en surface. Les taches incrustées partent.</p></div>
      <div class="feature"><span class="icon">{ICON["tag"]}</span><h3>Prix fixe annoncé avant</h3><p>Le devis sur photo annonce le prix avant l'intervention. Pas de supplément découvert sur place.</p></div>
      <div class="feature"><span class="icon">{ICON["clock"]}</span><h3>Réactif</h3><p>On vous rappelle rapidement, intervention sous 48 h dans la plupart des cas.</p></div>
      <div class="feature"><span class="icon">{ICON["pin"]}</span><h3>Proche de chez vous</h3><p>Une entreprise née à Toulouse : nous connaissons la ville et nous intervenons chez vous, dans tous les quartiers et les communes proches.</p></div>
    </div>
  </div>
</section>

<section class="section" id="avis">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Avis clients</p>
      <h2>Ils nous ont fait confiance</h2>
      <p class="rating">{ICON["star"]*5} <span>5/5 sur Google</span></p>
    </div>
    <div class="reviews-carousel">
      <button type="button" class="reviews-arrow reviews-prev" aria-label="Avis précédent" hidden>{ICON["prev"]}</button>
      <div class="reviews-band" tabindex="0" role="region" aria-label="Avis clients">
        <div class="reviews-track">
          <blockquote class="review">
            <p>« J'ai fait nettoyer l'intérieur de ma voiture pro, une Sandero Stepway qui vit sur les chantiers. Les tapis étaient pleins de débris et j'avais des taches sur les sièges que je n'arrivais pas à faire partir. Tout est parti. Sièges nickel, moquettes comme neuves, même les aérateurs et les rainures autour du levier de vitesses sont propres. »</p>
            <footer>Abdul M. · Nettoyage intérieur voiture</footer>
          </blockquote>
          <blockquote class="review">
            <p>« La voiture était dans un état catastrophique, je ne la reconnais plus. »</p>
            <footer>Madison V. · Nettoyage intérieur voiture</footer>
          </blockquote>
          <blockquote class="review">
            <p>« Très satisfaite du nettoyage de mon canapé. Avec mon enfant, il était plein de taches, et depuis son passage il n'y en a plus aucune. Juste après, aucune odeur d'humidité ni de traces sur le tissu. La personne est très sérieuse dans son travail, le résultat est top. Je recommande vivement ! »</p>
            <footer>Aissetou C. · Nettoyage canapé</footer>
          </blockquote>
          <blockquote class="review">
            <p>« Très bon travail, le nettoyage est propre, rapide et sans oublier la politesse qui va avec, j’ai l’impression de de récupérer ma 207 neuve. Je recommande ! »</p>
            <footer>Sam K. · Nettoyage intérieur voiture</footer>
          </blockquote>
          <blockquote class="review">
            <p>« J’ai fais appel à Nadifa propreté pour le nettoyage de mon matelas, le résultat est très bien, impeccable ! »</p>
            <footer>Joyce D. · Nettoyage matelas</footer>
          </blockquote>
        </div>
      </div>
      <button type="button" class="reviews-arrow reviews-next" aria-label="Avis suivant" hidden>{ICON["next"]}</button>
    </div>
    <p class="center"><a class="btn btn-secondary" href="{GBP}" target="_blank" rel="noopener">Lire les avis sur Google</a></p>
  </div>
</section>

<section class="section section-alt" id="faq">
  <div class="wrap narrow">
    <div class="section-head">
      <p class="eyebrow">Questions fréquentes</p>
      <h2>Ce qu'on nous demande souvent</h2>
    </div>
    <details><summary>Combien de temps faut-il pour que ça sèche ?</summary><p>Quelques heures pour un canapé ou un matelas, grâce à l'extraction qui retire la majeure partie de l'eau. Une pièce aérée accélère encore le séchage.</p></details>
    <details><summary>Dois-je déplacer mon canapé ou mon matelas ?</summary><p>Non. Nous intervenons à domicile, dans la pièce où se trouve le meuble. Nous avons seulement besoin d'une prise électrique.</p></details>
    <details><summary>Les taches anciennes partent-elles ?</summary><p>La plupart, oui : traces de boisson, sueur, auréoles, poussière incrustée. Certaines teintures (encre, colorant) peuvent laisser une marque atténuée. Envoyez une photo, nous vous dirons franchement ce qu'il est possible d'obtenir.</p></details>
    <details><summary>Où intervenez-vous ?</summary><p>À Toulouse (tous quartiers) et dans les communes proches : {ZONES_TXT}. {DEPLACEMENT}</p></details>
    <details><summary>Comment se passe le paiement ?</summary><p>Vous réglez après l'intervention.</p></details>
  </div>
</section>
{cta_band()}
'''
    return h + header("./") + body + footer()

# ---------- SERVICES ----------
def price_row(name, detail, price, note=""):
    p = f'<span class="price">{price}</span>'
    return f'<li><div><strong>{name}</strong><span class="muted">{detail}</span></div>{p}{f"<em>{note}</em>" if note else ""}</li>'

def page_services():
    h = head("Services : voiture, canapé, matelas, tapis à Toulouse | Nadifa Propreté",
             "Nettoyage à domicile à Toulouse : intérieur de voiture dès 50 €, canapés, fauteuils, matelas, tapis et moquettes. Devis sur photo avant l'intervention.",
             "services.html", extra=breadcrumb("Services","services.html"))
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h1>Nos services de nettoyage à domicile à Toulouse</h1>
    <p class="lead">Envoyez une photo sur WhatsApp : on vous rappelle rapidement avec le tarif exact. {DEPLACEMENT_COURT}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} Obtenir mon tarif</a>
      <a class="btn btn-ghost" href="reservation.html">Réserver un créneau</a>
    </div>
  </div>
</section>

<section class="section" id="voiture">
  <div class="wrap service-block">
    <div class="service-media">{picture("voiture-207","Intérieur d'une Peugeot 207 après nettoyage par Nadifa Propreté : tableau de bord, siège et moquette", sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON["car"]}</span>
      <h2>Intérieur de voiture</h2>
      <p>Voiture personnelle, voiture pro qui tourne sur les chantiers, véhicule de famille : nous intervenons sur votre parking, chez vous ou au travail.</p>
      <ul class="pricelist">
        {"".join(price_row(*x) for x in PRIX_VOITURE)}
      </ul>
      <p class="small muted">Le tarif dépend de la taille du véhicule (citadine, berline, SUV, utilitaire) et de son état. Devis sur photo : le prix total vous est annoncé avant l'intervention.</p>
      <p><a class="link-more" href="nettoyage-interieur-voiture-toulouse.html">Tout savoir sur cette prestation</a></p>
    </div>
  </div>
</section>

<section class="section section-alt" id="canapes">
  <div class="wrap service-block reverse">
    <div class="service-media">{picture("canape-angle-large","Canapé d'angle gris après nettoyage à domicile par Nadifa Propreté", sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON["sofa"]}</span>
      <h2>Canapés et fauteuils</h2>
      <p>Tissu, microfibre, velours, lin : pré-traitement des taches, injection-extraction sur l'assise, le dossier et les accoudoirs, puis finition. Sec en quelques heures. Le cuir est aussi pris en charge, au même prix que le tissu.</p>
      <ul class="pricelist">
        {"".join(price_row(*x) for x in PRIX_CANAPE)}
      </ul>
      <p><a class="link-more" href="nettoyage-canape-toulouse.html">Tout savoir sur cette prestation</a></p>
    </div>
  </div>
  <div class="wrap service-resultats">
    <h3>Nos résultats sur des canapés</h3>
    {carrousel_canapes()}
  </div>
</section>

<section class="section" id="matelas">
  <div class="wrap service-block">
    <div class="service-media">{picture("matelas","Illustration : aspirateur sur un matelas blanc", sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON["bed"]}</span>
      <h2>Matelas</h2>
      <p>Traces de transpiration, auréoles, poussière et acariens : le matelas est nettoyé sur la face de couchage, puis séché par extraction. Vous dormez dessus le soir même.</p>
      <ul class="pricelist">
        {"".join(price_row(*x) for x in PRIX_MATELAS)}
      </ul>
      <p class="small muted">Deuxième face ou sommier tapissier : sur demande.</p>
      <p><a class="link-more" href="nettoyage-matelas-toulouse.html">Tout savoir sur cette prestation</a></p>
    </div>
  </div>
</section>

<section class="section section-alt" id="tapis">
  <div class="wrap service-block reverse">
    <div class="service-media">{picture("tapis","Tapis de salon bleu à médaillon nettoyé à domicile par Nadifa Propreté", sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON["rug"]}</span>
      <h2>Tapis et moquettes</h2>
      <p>Le tapis est nettoyé chez vous, sans l'emporter : dépoussiérage, injection-extraction, remise en forme des fibres. Pour les moquettes, comptez une pièce en une heure environ.</p>
      <ul class="pricelist">
        {"".join(price_row(*x) for x in PRIX_TAPIS)}
      </ul>
      <p><a class="link-more" href="nettoyage-tapis-moquette-toulouse.html">Tout savoir sur cette prestation</a></p>
    </div>
  </div>
</section>

<section class="section" id="remise">
  <div class="wrap narrow">
    <p class="eyebrow">Remise</p>
    <h2>−{REMISE_POURCENT}&nbsp;% dès deux prestations</h2>
    <p>Dès deux prestations dans la même intervention (même jour, même adresse), nous retirons {REMISE_POURCENT}&nbsp;% du total des prestations. La remise vaut pour toutes les catégories, voiture comprise. Le total est arrondi à l'euro du dessous. Le déplacement, quand il est facturé, n'est pas remisé.</p>
    <ul class="pricelist">
      {remise_exemple("Canapé 2 ou 3 places + matelas 2 places", [ligne(PRIX_CANAPE, "Canapé 2 ou 3 places"), ligne(PRIX_MATELAS, "Matelas 2 places")])}
      {remise_exemple("Canapé 2 ou 3 places + fauteuil", [ligne(PRIX_CANAPE, "Canapé 2 ou 3 places"), ligne(PRIX_CANAPE, "Fauteuil")])}
      {remise_exemple("Canapé 2 ou 3 places + voiture Formule Premium", [ligne(PRIX_CANAPE, "Canapé 2 ou 3 places"), ligne(PRIX_VOITURE, "Formule Premium")])}
    </ul>
    <p class="small muted">Pour la voiture, le prix dépend du véhicule : l'exemple part du prix de départ, et le devis sur photo annonce le prix total avant l'intervention.</p>
  </div>
</section>

<section class="section section-tight" id="autres">
  <div class="wrap narrow">
    <p class="center small muted">Une autre demande ? <a href="{WA_DEVIS}" target="_blank" rel="noopener">Écrivez-nous avec quelques photos</a>.</p>
  </div>
</section>
{cta_band()}
'''
    return h + header("services.html") + body + footer()

# ---------- RESERVATION ----------
def page_reservation():
    h = head("Réserver un nettoyage à domicile à Toulouse | Nadifa Propreté",
             "Réservez le nettoyage de votre canapé, matelas, tapis ou voiture à Toulouse : formulaire en 1 minute, réponse sur WhatsApp, intervention sous 48 h.",
             "reservation.html", extra=breadcrumb("Réserver","reservation.html"))
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Réservation</p>
    <h1>Réserver un nettoyage à domicile à Toulouse</h1>
    <p class="lead">Remplissez le formulaire : votre demande s'ouvre dans WhatsApp, prête à envoyer. On vous rappelle rapidement pour confirmer le tarif et le créneau. Rien n'est enregistré sur ce site.</p>
  </div>
</section>

<section class="section">
  <div class="wrap grid-form">
    <form class="form" id="booking" novalidate>
      <div class="field">
        <label for="f-name">Votre prénom / nom</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required placeholder="Ex. : Monsieur X">
      </div>
      <div class="field">
        <label for="f-phone">Téléphone</label>
        <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required placeholder="06 00 00 00 00">
      </div>
      <div class="field">
        <label for="f-service">Prestation</label>
        <select id="f-service" name="service" required>
          <option value="">Choisir…</option>
          <optgroup label="Voiture">
            <option>Voiture – Formule Basique</option>
            <option>Voiture – Formule Premium</option>
          </optgroup>
          <optgroup label="Canapés et fauteuils">
            <option>Canapé 2 ou 3 places</option>
            <option>Canapé 4 ou 5 places ou d'angle</option>
            <option>Fauteuil</option>
          </optgroup>
          <optgroup label="Matelas">
            <option>Matelas 1 place</option>
            <option>Matelas 2 places</option>
            <option>Matelas king size</option>
          </optgroup>
          <optgroup label="Tapis et moquettes">
            <option>Petit tapis (jusqu'à 2 × 2 m)</option>
            <option>Grand tapis (jusqu'à 2 × 3 m)</option>
            <option>Tapis plus grand que 2 × 3 m</option>
            <option>Moquette</option>
          </optgroup>
          <optgroup label="Autres">
            <option>Autre demande</option>
          </optgroup>
        </select>
      </div>
      <div class="field-row">
        <div class="field">
          <label for="f-city">Ville / quartier</label>
          <input id="f-city" name="city" type="text" autocomplete="address-level2" placeholder="Ex. : Toulouse Minimes">
        </div>
        <div class="field">
          <label for="f-date">Date souhaitée</label>
          <input id="f-date" name="date" type="date">
        </div>
      </div>
      <div class="field">
        <label for="f-msg">Précisions <span class="muted">(matière, taille, taches, étage…)</span></label>
        <textarea id="f-msg" name="message" rows="4" placeholder="Ex. : canapé d'angle en tissu gris, taches de café, 2e étage sans ascenseur"></textarea>
      </div>
      <p class="form-error" id="form-error" hidden>Merci d'indiquer votre nom, votre téléphone et la prestation.</p>
      <div class="form-actions">
        <button class="btn btn-primary btn-lg" type="submit">{ICON["wa"]} Envoyer sur WhatsApp</button>
        <a class="btn btn-ghost" id="mail-fallback" href="mailto:{EMAIL}?subject=Demande%20de%20nettoyage">{ICON["mail"]} Plutôt par e-mail</a>
      </div>
      <p class="small muted">Pensez à joindre une photo dans WhatsApp après l'envoi : c'est ce qui permet de donner un prix fixe.</p>
    </form>

    <aside class="aside">
      <div class="aside-card">
        <h2>Vous préférez appeler ?</h2>
        <p><a class="big-link" href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a></p>
        <p class="muted">Tous les jours sauf le vendredi, de 7 h à 22 h 30. Si nous sommes en intervention, laissez un message ou écrivez sur WhatsApp : on vous rappelle rapidement.</p>
      </div>
      <div class="aside-card">
        <h2>Le jour de l'intervention</h2>
        <ul class="checklist">
          <li>{ICON["check"]} Une prise électrique à proximité</li>
          <li>{ICON["check"]} Le meuble accessible (coussins et objets retirés)</li>
          <li>{ICON["check"]} Pour une voiture : les objets personnels sortis, une place où stationner</li>
          <li>{ICON["check"]} Comptez 45 min à 2 h selon la prestation, puis quelques heures de séchage</li>
        </ul>
      </div>
      <div class="aside-card aside-quiet">
        <h2>Zone d'intervention</h2>
        <p class="muted">Toulouse et communes proches. <a href="contact.html#zone">Voir la liste</a>.</p>
      </div>
    </aside>
  </div>
</section>
'''
    return h + header("reservation.html") + body + footer()

# ---------- CONTACT ----------

def page_contact():
    h = head("Contact et zone d'intervention à Toulouse | Nadifa Propreté",
             "Contactez Nadifa Propreté par téléphone, WhatsApp ou e-mail. Nettoyage à domicile à Toulouse, Blagnac, Colomiers, Tournefeuille et communes proches.",
             "contact.html", extra=breadcrumb("Contact","contact.html"))
    zones = "".join(f"<li>{z}</li>" for z in ZONES)
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Contacter Nadifa Propreté à Toulouse</h1>
    <p class="lead">Le plus rapide : une photo sur WhatsApp. On vous rappelle rapidement avec un prix fixe et un créneau.</p>
  </div>
</section>

<section class="section">
  <div class="wrap grid-3 contact-cards">
    <a class="contact-card" href="{WA_DEVIS}" target="_blank" rel="noopener">
      <span class="icon">{ICON["wa"]}</span>
      <h2>WhatsApp</h2>
      <p class="big">{PHONE_H}</p>
      <p class="muted">On vous rappelle rapidement, photos bienvenues</p>
    </a>
    <a class="contact-card" href="tel:{PHONE_T}">
      <span class="icon">{ICON["phone"]}</span>
      <h2>Téléphone</h2>
      <p class="big">{PHONE_H}</p>
      <p class="muted">Tous les jours sauf le vendredi, 7 h – 22 h 30</p>
    </a>
    <a class="contact-card" href="mailto:{EMAIL}">
      <span class="icon">{ICON["mail"]}</span>
      <h2>E-mail</h2>
      <p class="big big-mail">{EMAIL}</p>
      <p class="muted">Pour les devis détaillés et les professionnels</p>
    </a>
  </div>
</section>

<section class="section section-alt" id="zone">
  <div class="wrap grid-2 zone-grid">
    <div>
      <p class="eyebrow">Zone d'intervention</p>
      <h2>Toulouse et communes proches</h2>
      <p>Nous nous déplaçons à domicile, sur votre lieu de travail ou sur votre parking, à Toulouse et dans les communes listées. {DEPLACEMENT}</p>
      <p><a class="btn btn-secondary" href="{GBP}" target="_blank" rel="noopener">{ICON["pin"]} Nous trouver sur Google Maps</a></p>
    </div>
    <ul class="zones">{zones}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <p class="eyebrow">Professionnels</p>
    <h2>Commerces, bureaux et locaux d'entreprise</h2>
    <p>Vitres et vitrines, bureaux, locaux commerciaux : nous intervenons chez les professionnels de Toulouse et des communes proches, sur devis gratuit après visite de vos locaux.</p>
    <p><a class="btn btn-secondary" href="nettoyage-professionnels-toulouse.html">Voir l'offre pour les professionnels</a></p>
  </div>
</section>
{cta_band()}
'''
    return h + header("contact.html") + body + footer()

# ---------- PAGES SERVICE DÉDIÉES (SEO) ----------
def breadcrumb3(name, path):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"Accueil","item":"{BASE}/"}},
{{"@type":"ListItem","position":2,"name":"Services","item":"{BASE}/services.html"}},
{{"@type":"ListItem","position":3,"name":"{name}","item":"{BASE}/{path}"}}]}}
</script>
'''

def ld_service(name, service_type, desc, path, min_price=None, offers=None):
    offer = (f''',
  "offers": {{ "@type": "Offer", "priceCurrency": "EUR", "priceSpecification": {{ "@type": "PriceSpecification", "minPrice": "{min_price}", "priceCurrency": "EUR" }} }}''' if min_price else "")
    if offers:  # prix fixes : une offre par prestation
        offer = ',\n  "offers": [\n    ' + ",\n    ".join(offers) + "\n  ]"
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{name}",
  "serviceType": "{service_type}",
  "description": "{desc}",
  "url": "{BASE}/{path}",
  "provider": {{ "@type": "LocalBusiness", "@id": "{BASE}/#business", "name": "Nadifa Propreté", "telephone": "{PHONE_T}", "url": "{BASE}/" }},
  "areaServed": [{AREA_LD}]{offer}
}}
</script>
'''

# Méthode de la page Canapé : (identifiant, bouton, [(image, titre, texte), …]).
# Ce sont les gestes réels de Nadifa, écrits avec nos mots. Les images sont des illustrations, jamais présentées comme un résultat.
ALT_ILLUSTRATIONS = {
 "etape-injection":"Illustration : main gantée qui injecte une solution sur l'assise d'un canapé en tissu",
 "etape-brossage":"Illustration : main gantée qui brosse l'assise d'un canapé en tissu avec une brosse souple sur perceuse",
 "etape-brossage-main":"Illustration : main gantée qui brosse l'assise d'un canapé en velours avec une brosse à main",
 "etape-vapeur":"Illustration : main gantée qui passe de la vapeur sur l'assise d'un canapé en tissu",
 "etape-extraction":"Illustration : main gantée qui aspire l'eau de l'assise d'un canapé en tissu",
 "etape-cuir-examen":"Illustration : main gantée qui teste un produit sur le coin d'un accoudoir en cuir",
 "etape-cuir-nettoyage":"Illustration : main gantée qui nettoie une assise en cuir à la brosse souple",
 "etape-cuir-essuyage":"Illustration : main gantée qui essuie une assise en cuir avec une microfibre",
}
MATIERES = [
 ("tissu","Tissu &amp; lin",[
   ("etape-injection","Injection","Nous répartissons sur le tissu une solution choisie pour ses fibres. L'eau est dosée pour ne pas tremper la mousse."),
   ("etape-brossage","Brossage","Une brosse souple sur perceuse travaille les taches et les zones de contact, à vitesse réglée, sans agresser le tissu."),
   ("etape-vapeur","Vapeur","Si les fibres et les colles le supportent, un passage de vapeur ciblé complète le nettoyage. Sinon, nous la laissons de côté."),
   ("etape-extraction","Extraction","La machine aspire l'eau chargée de saleté. Quelques passages à sec enlèvent l'humidité en trop et préparent le séchage."),
 ]),
 ("microfibre","Microfibre",[
   ("etape-injection","Injection","Nous avançons zone par zone pour garder la main sur la quantité d'eau, avec un produit dosé selon la réaction de la fibre."),
   ("etape-brossage","Brossage","La brosse souple insiste sur les accoudoirs, les assises et les endroits les plus touchés, avec une pression légère."),
   ("etape-vapeur","Vapeur","La vapeur vient en plus, seulement après avoir contrôlé le tissu, les colles et les assemblages."),
   ("etape-extraction","Extraction","L'aspiration retire l'eau et les résidus, puis les fibres sont remises en place pour un aspect régulier."),
 ]),
 ("velours","Velours",[
   ("etape-injection","Injection","Le velours passe à la machine seulement si le tissu et son support le permettent. Sinon, le travail se fait à la main."),
   ("etape-brossage-main","Brossage","Le brossage reste à la main, avec une brosse souple, toujours dans le sens du poil."),
   ("etape-vapeur","Vapeur","Nous l'utilisons uniquement si le velours et les colles la supportent. Sinon, nous passons cette étape."),
   ("etape-extraction","Extraction","L'humidité est retirée, le poil est replacé, puis nous regardons le canapé sous plusieurs angles pour repérer les traces."),
 ]),
 ("cuir","Cuir &amp; simili",[
   ("etape-cuir-examen","Examen et test","Nous regardons la finition, les plis et les zones fragiles, puis nous testons le produit sur un endroit discret."),
   ("etape-cuir-nettoyage","Nettoyage à la main","Produit adapté, brosse souple et microfibres, par petites zones. Ni machine à injection, ni vapeur, et jamais trop de liquide."),
   ("etape-cuir-essuyage","Essuyage et conseils","Nous essuyons les résidus et contrôlons le rendu. Un soin est posé seulement si le cuir en a besoin, et vous repartez avec nos conseils d'entretien."),
 ]),
]

def bloc_methode(matieres):
    onglets, panneaux = "", ""
    for i, (mid, label, etapes) in enumerate(matieres):
        onglets += f'<button type="button" role="tab" class="mat-tab" id="tab-{mid}" aria-controls="mat-{mid}" aria-selected="{"true" if i == 0 else "false"}">{label}</button>'
        cartes = "".join(f'''<li>{picture(img, ALT_ILLUSTRATIONS[img], sizes="(max-width: 560px) 110px, (max-width: 1100px) 45vw, 25vw", w=1400, h=1046)}
          <div class="mat-texte"><span class="step-num">{n}</span><h3>{titre}</h3><p>{texte}</p></div></li>''' for n, (img, titre, texte) in enumerate(etapes, 1))
        trois = " trois" if len(etapes) == 3 else ""
        panneaux += f'<div class="mat-panel" id="mat-{mid}" role="tabpanel" aria-labelledby="tab-{mid}" tabindex="0"><ol class="mat-etapes{trois}">{cartes}</ol></div>'
    return f'''
<section class="section" id="methode">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Comment nous nettoyons</p>
      <h2>Notre méthode, matière par matière</h2>
      <p class="muted">Avant tout, nous regardons la matière, nous aspirons le canapé et nous faisons un test discret. Choisissez votre matière pour voir les étapes.</p>
    </div>
    <div class="mat">
      <div class="mat-tabs" role="tablist" aria-label="Choisir la matière du canapé">{onglets}</div>
      {panneaux}
    </div>
    <p class="mat-honnete">Un travail soigné et un avis franc : nous ne garantissons pas la disparition de toutes les taches. Certaines taches anciennes ou certaines teintures peuvent rester atténuées, et un nettoyage ne répare ni l'usure, ni une brûlure, ni une décoloration.</p>
    <p class="small muted">Images d'illustration créées par IA : elles montrent le geste, pas un résultat.</p>
  </div>
</section>
'''

SVC_PAGES = [
 dict(path="nettoyage-canape-toulouse.html", crumb="Nettoyage de canapé", icon="sofa", img="injection-canape", matieres=MATIERES,
      img_alt="Buse d'injection-extraction sur un canapé en tissu clair pendant le nettoyage",
      hero_img="canape-page-hero", hero_alt="Canapé gris à boudins après nettoyage à domicile par Nadifa Propreté à Toulouse",
      title="Nettoyage canapé à domicile à Toulouse | Nadifa Propreté",
      desc="Nettoyage de canapé et fauteuil à domicile à Toulouse, en tissu ou en cuir : canapé 2 ou 3 places 69 €, 4 ou 5 places ou d'angle 79 €, fauteuil 25 €.",
      h1="Nettoyage de canapé à domicile à Toulouse",
      lead="Tissu, microfibre, velours, lin ou cuir : votre canapé est nettoyé en profondeur chez vous. Vous envoyez une photo, vous recevez un prix fixe, nous venons sous 48 h.",
      stype="Nettoyage de textile d'ameublement", min_price=None,
      intro=["Un canapé en tissu accumule au fil des mois poussière, sueur, traces de boisson et odeurs. Un coup d'aspirateur ne touche que la surface : la saleté reste dans la mousse et dans la fibre.",
             "L'injection-extraction injecte de l'eau et un produit adapté au textile au cœur de la fibre, puis aspire immédiatement le tout avec la saleté dissoute. Le canapé est nettoyé en profondeur, sans être détrempé."],
      included=["Assise, dossier et accoudoirs","Détachage des taches et auréoles","Nettoyage en profondeur adapté à la matière","Nettoyage à la vapeur quand la matière le permet","Séchage en quelques heures"],
      prices=PRIX_CANAPE,
      price_note="Devis sur photo : le prix total vous est annoncé avant l'intervention.",
      faq=[("Combien de temps faut-il pour que le canapé sèche ?","Quelques heures. L'extraction retire la majeure partie de l'eau ; une pièce aérée accélère encore le séchage."),
           ("Faut-il déplacer le canapé ?","Non. Nous intervenons dans la pièce où il se trouve. Il nous faut seulement une prise électrique à proximité."),
           ("Les vieilles taches partent-elles ?","La plupart, oui : boissons, sueur, auréoles, poussière incrustée. Certaines teintures (encre, colorant) peuvent laisser une marque atténuée. Envoyez une photo, nous vous disons franchement ce qu'il est possible d'obtenir."),
           ("Et les canapés en cuir ?","Oui, nous nettoyons aussi les canapés en cuir, au même prix que les canapés en tissu.")]),
 dict(path="nettoyage-matelas-toulouse.html", crumb="Nettoyage de matelas", icon="bed", img="matelas",
      img_alt="Illustration : aspirateur sur un matelas blanc",
      title="Nettoyage matelas à domicile à Toulouse | Nadifa Propreté",
      desc="Nettoyage de matelas à domicile à Toulouse par injection-extraction : 1 place 45 €, 2 places 55 €, king size 65 €. Sec le soir même.",
      h1="Nettoyage de matelas à domicile à Toulouse",
      lead="Traces de transpiration, auréoles, poussière et acariens : le matelas est nettoyé chez vous, sur la face de couchage, puis séché par extraction. Vous dormez dessus le soir même.",
      stype="Nettoyage de literie", min_price=None,
      intro=["On passe environ un tiers de sa vie sur son matelas. Il absorbe transpiration, peaux mortes et poussière, qui nourrissent les acariens et laissent des auréoles jaunes.",
             "Le nettoyage par injection-extraction va chercher la saleté dans l'épaisseur du garnissage, là où l'aspirateur ne va pas. Le matelas reste chez vous, il n'y a rien à transporter."],
      included=["Aspiration minutieuse de la face de couchage et des bords","Pré-traitement des auréoles et des taches","Injection-extraction sur toute la face","Séchage accéléré par extraction : sec en quelques heures"],
      prices=PRIX_MATELAS,
      price_note="Deuxième face ou sommier tapissier : sur demande. Devis sur photo : le prix total vous est annoncé avant l'intervention.",
      faq=[("Peut-on dormir dessus le soir même ?","Oui. Comptez quelques heures de séchage ; en aérant la chambre, le matelas est sec avant le coucher."),
           ("Faut-il retourner le matelas ?","Nous nettoyons la face de couchage. La deuxième face se fait sur demande, si le matelas est réversible."),
           ("Les taches d'urine ou de transpiration partent-elles ?","Elles sont très nettement atténuées, souvent complètement. Envoyez une photo pour un avis honnête avant de réserver.")]),
 dict(path="nettoyage-tapis-moquette-toulouse.html", crumb="Nettoyage de tapis et moquette", icon="rug", img="tapis",
      img_alt="Tapis de salon bleu à médaillon nettoyé à domicile par Nadifa Propreté à Toulouse",
      title="Nettoyage tapis et moquette à domicile à Toulouse | Nadifa Propreté",
      desc="Nettoyage de tapis et moquette à domicile à Toulouse par injection-extraction, sans emporter le tapis : petit tapis 35 €, grand tapis 45 €, moquette 8 €/m².",
      h1="Nettoyage de tapis et moquette à domicile à Toulouse",
      lead="Votre tapis est nettoyé chez vous, sans l'emporter : dépoussiérage, injection-extraction, remise en forme des fibres. Pour les moquettes, comptez environ une heure par pièce.",
      stype="Nettoyage de tapis et moquettes", min_price=None,
      intro=["Un tapis de salon retient la poussière, les miettes, les poils d'animaux et les taches du quotidien. Avec le temps, les couleurs se ternissent et les fibres se tassent.",
             "Pas besoin de le rouler ni de le déposer au pressing : nous le nettoyons sur place. Même chose pour les moquettes de chambre, de salon, de bureau ou d'escalier."],
      included=["Dépoussiérage en profondeur","Pré-traitement des taches","Injection-extraction avec un produit adapté à la fibre","Remise en forme des fibres"],
      prices=PRIX_TAPIS,
      price_note="Devis sur photo : le prix total vous est annoncé avant l'intervention (indiquez les dimensions du tapis ou la surface de moquette).",
      faq=[("Faut-il emporter le tapis ?","Non, il est nettoyé chez vous. Il suffit de libérer la surface et d'avoir une prise électrique."),
           ("Combien de temps pour une moquette ?","Environ une heure par pièce, puis quelques heures de séchage."),
           ("Tous les tapis peuvent-ils être nettoyés ?","La plupart des tapis en fibres synthétiques, laine ou coton, oui. Pour un tapis ancien ou fragile, envoyez une photo : nous vous dirons s'il vaut mieux le confier à un spécialiste.")]),
 dict(path="nettoyage-interieur-voiture-toulouse.html", crumb="Nettoyage intérieur de voiture", icon="car", img="voiture-207",
      img_alt="Intérieur d'une Peugeot 207 après nettoyage par Nadifa Propreté à Toulouse : tableau de bord, siège et moquette",
      title="Nettoyage intérieur voiture à Toulouse dès 50 € | Nadifa Propreté",
      desc="Nettoyage intérieur de voiture à Toulouse, chez vous ou au travail : Formule Basique dès 50 €, Premium avec shampoing des sièges dès 70 €. Devis sur photo.",
      h1="Nettoyage intérieur de voiture à Toulouse",
      lead="Voiture personnelle, utilitaire qui tourne sur les chantiers, véhicule de famille : nous nettoyons l'habitacle sur votre parking, chez vous ou au travail. Formule Basique dès 50 €, Premium dès 70 €.",
      stype="Nettoyage automobile intérieur", min_price="50",
      intro=["Miettes, sable, poussière sur le tableau de bord, taches sur les sièges, tapis de sol pleins de débris : l'intérieur d'une voiture se salit vite, surtout avec des enfants ou un usage professionnel.",
             "Nous venons avec le matériel : aspirateur professionnel, produits pour plastiques et machine d'injection-extraction pour les sièges et moquettes. Vous n'avez pas à vous déplacer en station."],
      included=["Aspiration complète de l'habitacle et du coffre","Dépoussiérage des plastiques, du tableau de bord, de la console et des aérateurs","Nettoyage des tapis de sol","Formule Premium : shampoing des sièges, tapis et moquettes par injection-extraction"],
      prices=PRIX_VOITURE,
      price_note="Le tarif dépend de la taille du véhicule (citadine, berline, SUV, utilitaire) et de son état. Devis sur photo : le prix total vous est annoncé avant l'intervention.",
      faq=[("Où se fait le nettoyage ?","Là où la voiture est garée : devant chez vous, sur votre lieu de travail ou sur un parking, à Toulouse et dans les communes proches."),
           ("Combien de temps ça prend ?","Entre 45 minutes et 2 heures selon la formule, la taille du véhicule et son état."),
           ("Nettoyez-vous les véhicules professionnels ?","Oui : utilitaires d'artisans, VTC, véhicules de société. Pour un entretien régulier de plusieurs véhicules, écrivez-nous pour un tarif adapté."),
           ("Que dois-je préparer ?","Sortez vos objets personnels de l'habitacle et du coffre. Nous avons besoin d'une place pour stationner à côté du véhicule.")]),
]

def page_service(d):
    others = "".join(f'<a class="btn btn-secondary" href="{o["path"]}">{o["crumb"]}</a>' for o in SVC_PAGES if o is not d)
    offers = None if d["min_price"] else ld_offers(d["prices"], d["stype"])  # voiture : prix « à partir de », une seule offre
    if offers:  # la description Google est écrite à la main : elle doit reprendre chaque prix de la grille
        manquants = [p for _, _, p in d["prices"] if p[0].isdigit() and p not in d["desc"]]
        if manquants:
            raise ValueError(f"{d['path']} : prix absent(s) de la description Google : {', '.join(manquants)}")
    h = head(d["title"], d["desc"], d["path"], extra=breadcrumb3(d["crumb"], d["path"]) + ld_service(d["crumb"], d["stype"], d["desc"], d["path"], d["min_price"], offers))
    intro = "".join(f"<p>{x}</p>" for x in d["intro"])
    included = "".join(f'<li>{ICON["check"]} {x}</li>' for x in d["included"])
    prices = "".join(price_row(*x) for x in d["prices"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in d["faq"])
    actions = f'''<div class="hero-actions">
      <a class="btn btn-primary" href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} Obtenir mon prix sur WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a>
    </div>'''
    fil_ariane = f'<p class="eyebrow"><a href="services.html">Services</a> · {d["crumb"]}</p>'
    if "matieres" in d:  # page Canapé : grande photo, résultats et méthode par matière
        grille_prix = " · ".join(f"<span>{nom}&nbsp;: {prix}</span>" for nom, _, prix in d["prices"])
        haut_de_page = f'''
<section class="page-hero">
  {picture(d["hero_img"], d["hero_alt"], sizes="100vw", cls="page-hero-img", eager=True, w=1400, h=700)}
  <div class="wrap">
    <div class="page-hero-texte">
      {fil_ariane}
      <h1>{d["h1"]}</h1>
      <p class="lead">{d["lead"]}</p>
      <p class="page-hero-prix">{grille_prix}</p>
      {actions}
    </div>
  </div>
</section>

<section class="section" id="resultats">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Avant / après</p>
      <h2>Nos résultats sur des canapés</h2>
    </div>
    {carrousel_canapes()}
  </div>
</section>
'''
        methode = bloc_methode(d["matieres"])
        fond_pourquoi = "section section-alt"
    else:
        haut_de_page = f'''
<section class="page-head">
  <div class="wrap">
    {fil_ariane}
    <h1>{d["h1"]}</h1>
    <p class="lead">{d["lead"]}</p>
    {actions}
  </div>
</section>
'''
        methode = ""
        fond_pourquoi = "section"
    body = f'''{haut_de_page}
<section class="{fond_pourquoi}">
  <div class="wrap service-block">
    <div class="service-media">{picture(d["img"], d["img_alt"], sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON[d["icon"]]}</span>
      <h2>Pourquoi un nettoyage professionnel</h2>
      {intro}
    </div>
  </div>
</section>
{methode}
<section class="section section-alt">
  <div class="wrap grid-2">
    <div>
      <h2>Ce qui est compris</h2>
      <ul class="checklist">{included}</ul>
    </div>
    <div>
      <h2>Tarifs</h2>
      <ul class="pricelist">{prices}</ul>
      <p class="small muted">{d["price_note"]}</p>
      <p class="small muted">Dès deux prestations dans la même intervention, −{REMISE_POURCENT}&nbsp;% sur le total : <a href="services.html#remise">voir la remise</a>.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Comment ça se passe</h2></div>
    <ol class="steps">
      <li><span class="step-num">1</span><h3>Vous envoyez une photo</h3><p>Sur WhatsApp ou par téléphone. On vous rappelle rapidement avec un prix fixe.</p></li>
      <li><span class="step-num">2</span><h3>On fixe un créneau</h3><p>Généralement sous 48 h, tous les jours sauf le vendredi, de 7 h à 22 h 30.</p></li>
      <li><span class="step-num">3</span><h3>Nettoyage sur place</h3><p>Chez vous ou là où est garé le véhicule. Il suffit d'une prise électrique.</p></li>
      <li><span class="step-num">4</span><h3>Vous réglez</h3><p>Vous réglez après l'intervention.</p></li>
    </ol>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap narrow">
    <div class="section-head"><h2>Questions fréquentes</h2></div>
    {faq}
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <h2>Zone d'intervention</h2>
    <p>Nous intervenons à Toulouse (tous quartiers) et dans les communes proches : {ZONES_TXT}. {DEPLACEMENT} <a href="contact.html#zone">Voir la zone d'intervention</a>.</p>
    <h2>Nos autres prestations</h2>
    <div class="hero-actions">{others}</div>
  </div>
</section>
{cta_band()}
'''
    return h + header("services.html") + body + footer()

# ---------- PAGE PROFESSIONNELS ----------
PROS_PATH = "nettoyage-professionnels-toulouse.html"
PROS_WA = wa("Bonjour Nadifa Propreté, je représente une entreprise et je souhaite un devis pour : ")
PROS_FAQ = [
    ("Combien coûte l'intervention ?","Pour vos locaux, nous ne publions pas de prix : chaque local est différent. Après la visite, nous vous remettons un devis, et le prix annoncé est celui que vous payez."),
    ("Faut-il vous voir sur place avant ?","Pour vos locaux, oui : nous venons les visiter avant de chiffrer, pour voir les surfaces, les accès et l'état des lieux."),
    ("Une seule intervention ou un passage régulier ?","Les deux : un passage ponctuel, ou un contrat avec un rythme fixé ensemble, par exemple chaque mois. Vous recevez une facture."),
    ("Quels locaux nettoyez-vous ?","Commerces à vitrine, bureaux et locaux commerciaux, à Toulouse et dans les communes proches. Écrivez-nous pour un autre type de local."),
]

def page_pros():
    titre = "Nettoyage pour professionnels à Toulouse | Nadifa Propreté"
    desc = "Nadifa Propreté nettoie les vitres, vitrines, bureaux et locaux commerciaux des professionnels à Toulouse et communes proches. Devis gratuit après visite."
    h = head(titre, desc, PROS_PATH, extra=breadcrumb("Professionnels", PROS_PATH) + ld_service("Nettoyage pour professionnels", "Nettoyage de vitres, de bureaux et de locaux commerciaux", desc, PROS_PATH))
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in PROS_FAQ)
    services = [
        ("Vitres et vitrines", "Commerces, cabinets et bureaux : vitrines et baies vitrées propres, à l'intérieur comme à l'extérieur.", None),
        ("Ménage de bureaux", "Bureaux, salles de réunion et espaces communs entretenus à un rythme fixé avec vous.", None),
        ("Locaux commerciaux", "Boutiques, salles d'accueil et locaux ouverts au public.", None),
        ("Fauteuils, chaises et moquette", "Le textile de vos locaux est nettoyé sur place par injection-extraction.", "nettoyage-tapis-moquette-toulouse.html"),
        ("Intérieur des véhicules de société", "Utilitaires, véhicules d'artisans ou de VTC : nous venons là où ils sont garés.", "nettoyage-interieur-voiture-toulouse.html"),
    ]
    cartes = "".join(
        f'<li>{ICON["check"]} <strong>{t}</strong> : {d}' + (f' <a href="{u}">Voir la prestation</a>' if u else "") + "</li>"
        for t, d, u in services)
    actions = f'''<div class="hero-actions">
      <a class="btn btn-primary" href="{PROS_WA}" target="_blank" rel="noopener">{ICON["wa"]} Devis gratuit sur WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a>
    </div>'''
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Professionnels</p>
    <h1>Nettoyage de vitres, de bureaux et de locaux à Toulouse</h1>
    <p class="lead">Commerces, cabinets, bureaux : nous nettoyons vos locaux et vos vitrines, avec un devis gratuit établi après visite.</p>
    {actions}
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <h2>Ce que nous nettoyons</h2>
    <ul class="checklist">{cartes}</ul>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><h2>Comment ça se passe</h2></div>
    <ol class="steps">
      <li><span class="step-num">1</span><h3>Vous nous contactez</h3><p>Par WhatsApp, par téléphone ou par e-mail. On vous rappelle rapidement.</p></li>
      <li><span class="step-num">2</span><h3>Nous visitons vos locaux</h3><p>Nous regardons les surfaces, les accès et l'état des lieux.</p></li>
      <li><span class="step-num">3</span><h3>Vous recevez un devis gratuit</h3><p>Le prix annoncé est celui que vous payez, sans surprise.</p></li>
      <li><span class="step-num">4</span><h3>Nous intervenons</h3><p>À un créneau fixé avec vous. Vous recevez ensuite une facture.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <div class="section-head"><h2>Questions fréquentes</h2></div>
    {faq}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap narrow">
    <h2>Zone d'intervention</h2>
    <p>Nous intervenons à Toulouse (tous quartiers) et dans les communes proches : {ZONES_TXT}. <a href="contact.html#zone">Voir la zone d'intervention</a>.</p>
    <p>Vous êtes un particulier ? <a href="services.html">Voir nos prestations pour les particuliers</a>.</p>
  </div>
</section>
{cta_band("Parlons de vos locaux", "Écrivez-nous sur WhatsApp ou appelez-nous pour fixer la visite de vos locaux.", PROS_WA, "Devis gratuit")}
'''
    return h + header(PROS_PATH) + body + footer()

# ---------- MENTIONS LEGALES ----------
def page_mentions():
    h = head("Mentions légales | Nadifa Propreté",
             "Mentions légales du site Nadifa Propreté, entreprise de nettoyage à domicile à Toulouse.",
             "mentions-legales.html", extra='<meta name="robots" content="noindex, follow">\n')
    body = f'''
<section class="page-head">
  <div class="wrap"><p class="eyebrow">Informations</p><h1>Mentions légales</h1></div>
</section>
<section class="section">
  <div class="wrap narrow legal">
    <h2>Éditeur du site</h2>
    <p>Nadifa Propreté<br>Ibrahim Maiga, entrepreneur individuel (micro-entreprise)<br>SIRET : 989 023 213 00014<br>Siège : 7 place de Milan, 31100 Toulouse<br>Téléphone : <a href="tel:{PHONE_T}">{PHONE_H}</a> · E-mail : <a href="mailto:{EMAIL}">{EMAIL}</a><br>Directeur de la publication : Ibrahim Maiga<br>TVA non applicable, article 293 B du CGI.</p>

    <h2>Hébergement</h2>
    <p>GitHub Pages, GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>

    <h2>Données personnelles et cookies</h2>
    <p>Ce site ne dépose aucun cookie et n'utilise aucun outil de mesure d'audience. Le traitement des informations que vous nous transmettez (devis, prestation, facturation) est détaillé dans la <a href="politique-confidentialite.html">politique de confidentialité</a>.</p>

{mediation_html()}    <h2>Propriété intellectuelle</h2>
    <p>Le nom, le logo, les textes et les photographies de réalisations sont la propriété de Nadifa Propreté. L'image du matelas est une illustration générique, utilisée à titre d'exemple. Les images des étapes de la page canapé sont des illustrations créées par IA.</p>

    <h2>Assurance et responsabilité</h2>
    <p>Les prestations sont réalisées avec des produits et un matériel adaptés aux textiles traités. Un test de tenue de couleur est effectué sur une zone discrète avant tout nettoyage lorsque la matière le justifie.</p>
  </div>
</section>
'''
    return h + header("") + body + footer()

def mediation_html():
    if not MEDIATEUR:
        return ""
    m = MEDIATEUR
    return f"""    <h2>Médiation de la consommation</h2>
    <p>Conformément aux articles L612-1 et suivants du Code de la consommation, après une réclamation écrite adressée à Nadifa Propreté restée sans solution satisfaisante, vous pouvez saisir gratuitement le médiateur de la consommation dont nous relevons : {m["nom"]}, {m["adresse"]}, <a href="{m["site"]}" target="_blank" rel="noopener">{m["site"].split("//")[-1].rstrip("/")}</a>.</p>

"""

# ---------- POLITIQUE DE CONFIDENTIALITE ----------
def page_confidentialite():
    h = head("Politique de confidentialité | Nadifa Propreté",
             "Comment Nadifa Propreté utilise et protège les informations transmises pour un devis ou une prestation de nettoyage à Toulouse.",
             "politique-confidentialite.html", extra='<meta name="robots" content="noindex, follow">\n')
    body = f'''
<section class="page-head">
  <div class="wrap"><p class="eyebrow">Informations</p><h1>Politique de confidentialité</h1><p class="lead">Mise à jour le 27 septembre 2026.</p></div>
</section>
<section class="section">
  <div class="wrap narrow legal">
    <h2>Qui est responsable de vos données ?</h2>
    <p>Ibrahim Maiga, entrepreneur individuel exerçant sous le nom Nadifa Propreté, SIRET 989 023 213 00014, 7 place de Milan, 31100 Toulouse. Contact : <a href="mailto:{EMAIL}">{EMAIL}</a> ou <a href="tel:{PHONE_T}">{PHONE_H}</a>.</p>

    <h2>Quelles données, et d'où viennent-elles ?</h2>
    <ul>
      <li>Les informations que vous nous envoyez vous-même, par WhatsApp, téléphone, e-mail ou via le formulaire de réservation : nom, téléphone, commune et adresse d'intervention, prestation souhaitée, date, photos des éléments à nettoyer et contenu de vos messages.</li>
      <li>Si vous nous contactez après avoir vu une de nos publicités sur Facebook, Instagram ou WhatsApp, ou si vous remplissez un formulaire publicitaire Meta : les informations que vous y saisissez, que Meta nous transmet.</li>
      <li>Les informations nécessaires à la facturation de la prestation.</li>
    </ul>
    <p>Le formulaire de réservation de ce site ne stocke rien : il prépare un message que vous envoyez vous-même depuis WhatsApp ou votre messagerie. Ce site ne dépose aucun cookie et n'utilise ni outil de mesure d'audience ni pixel publicitaire.</p>

    <h2>Pourquoi, et sur quelle base ?</h2>
    <ul>
      <li>Vous répondre, établir un devis et organiser l'intervention : mesures précontractuelles et exécution du contrat (article 6.1.b du RGPD).</li>
      <li>Établir et conserver les factures : obligation légale (article 6.1.c du RGPD).</li>
      <li>Vous demander votre avis après une prestation et vous recontacter au sujet d'une demande en cours : intérêt légitime (article 6.1.f du RGPD). Vous pouvez vous y opposer à tout moment.</li>
      <li>Utiliser des photos avant/après de vos éléments nettoyés dans nos publications ou publicités : uniquement avec votre accord explicite, et sans aucune information permettant de vous identifier. Vous pouvez retirer cet accord à tout moment.</li>
    </ul>

    <h2>Qui y a accès ?</h2>
    <p>Uniquement Ibrahim Maiga. Aucune donnée n'est vendue ni cédée. Les services techniques utilisés pour échanger avec vous traitent ces données pour notre compte ou en tant que responsables distincts : WhatsApp et Meta Platforms Ireland (messagerie, publicités et formulaires publicitaires), Google (messagerie e-mail) et GitHub (hébergement du site, qui peut conserver des journaux techniques de connexion). Certains de ces prestataires peuvent transférer des données hors de l'Union européenne, notamment aux États-Unis, dans le cadre des garanties prévues par le RGPD (décision d'adéquation EU-US Data Privacy Framework ou clauses contractuelles types).</p>

    <h2>Combien de temps ?</h2>
    <ul>
      <li>Demandes de devis sans suite : au plus 3 ans après le dernier contact.</li>
      <li>Clients : le temps de la relation commerciale, puis 3 ans après la dernière prestation.</li>
      <li>Factures et pièces comptables : 10 ans, comme l'impose le Code de commerce.</li>
      <li>Photos envoyées pour un devis : supprimées une fois la prestation réalisée ou le devis refusé, sauf accord de votre part pour leur réutilisation.</li>
    </ul>

    <h2>Vos droits</h2>
    <p>Vous pouvez demander l'accès à vos données, leur rectification, leur suppression, leur portabilité, la limitation de leur traitement, ou vous opposer à leur utilisation, en écrivant à <a href="mailto:{EMAIL}">{EMAIL}</a>. Nous répondons dans un délai d'un mois. Si vous estimez que vos droits ne sont pas respectés, vous pouvez adresser une réclamation à la CNIL (<a href="https://www.cnil.fr/fr/plaintes" target="_blank" rel="noopener">cnil.fr/fr/plaintes</a>).</p>
  </div>
</section>
'''
    return h + header("") + body + footer()

def page_404():
    h = head("Page introuvable | Nadifa Propreté", "Cette page n'existe pas ou plus.", "404.html", extra='<meta name="robots" content="noindex">\n')
    body = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">Erreur 404</p><h1>Cette page n'existe pas</h1><p class="lead">Elle a peut-être été déplacée. Retrouvez nos prestations ou contactez-nous directement.</p>
<div class="hero-actions"><a class="btn btn-primary" href="./">Retour à l'accueil</a><a class="btn btn-ghost" href="services.html">Voir les services</a></div></div></section>
'''
    return h + header("") + body + footer()

CSS = r'''
:root{
  --navy:#0b1f33; --navy-2:#122b45; --ink:#13202e; --text:#2b3a4a; --muted:#5f6f80;
  --accent:#0cc0df; --accent-2:#089fb9; --accent-soft:#e3f8fc; --bg:#ffffff; --bg-alt:#f3f8fb;
  --line:#e2e9ef; --navy-rgb:11,31,51; --radius:16px; --shadow:0 10px 30px rgba(11,31,51,.08);
  --font:"Inter","Segoe UI",system-ui,-apple-system,Roboto,"Helvetica Neue",Arial,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
html,body{overflow-x:clip}
body{margin:0;font-family:var(--font);color:var(--text);background:var(--bg);line-height:1.6;font-size:17px}
img{max-width:100%;height:auto;display:block}
a{color:var(--accent-2)}
h1,h2,h3{color:var(--ink);line-height:1.15;margin:0 0 .5em;font-weight:800;letter-spacing:-.01em}
h1{font-size:clamp(1.9rem,4.2vw,3rem)}
h2{font-size:clamp(1.5rem,3vw,2.1rem)}
h3{font-size:1.15rem}
p{margin:0 0 1em}
.wrap{width:min(1140px,100% - 2.5rem);margin-inline:auto}
.narrow{max-width:780px}
.center{text-align:center}
.muted{color:var(--muted)}
.small{font-size:.92rem}
.eyebrow{color:var(--accent-2);font-weight:700;text-transform:uppercase;letter-spacing:.08em;font-size:.8rem;margin-bottom:.6em}
.lead{font-size:1.15rem;color:var(--muted);max-width:60ch}
.skip{position:absolute;left:-999px;top:0;background:var(--navy);color:#fff;padding:.5rem 1rem;z-index:100}
.skip:focus{left:1rem;top:1rem}
svg{width:1.2em;height:1.2em;vertical-align:-.25em;flex:none}

/* buttons */
.btn{display:inline-flex;align-items:center;gap:.55em;padding:.8em 1.35em;border-radius:999px;font-weight:700;text-decoration:none;border:2px solid transparent;cursor:pointer;font-family:inherit;font-size:1rem;transition:transform .15s,box-shadow .15s,background .15s;line-height:1.2}
.btn:hover{transform:translateY(-1px)}
.btn-lg{padding:.95em 1.6em;font-size:1.05rem}
.btn-primary{background:var(--accent);color:#04202a;box-shadow:0 6px 18px rgba(12,192,223,.35)}
.btn-primary:hover{background:#22cbe6}
.btn-secondary{background:var(--navy);color:#fff}
.btn-secondary:hover{background:var(--navy-2)}
.btn-ghost{background:#fff;color:var(--ink);border-color:var(--line)}
.btn-ghost:hover{border-color:var(--accent)}
.btn-light{background:#fff;color:var(--navy)}
.btn-outline-light{border-color:rgba(255,255,255,.6);color:#fff}
.btn-outline-light:hover{background:rgba(255,255,255,.1)}

/* header */
.site-header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.header-inner{display:flex;align-items:center;justify-content:space-between;gap:1rem;min-height:70px}
.brand{display:flex;align-items:center;gap:.6rem;text-decoration:none;color:var(--ink)}
.brand .brand-mark{width:44px;height:44px;flex:none;border-radius:12px;box-shadow:0 4px 12px rgba(12,192,223,.35)}
.brand-name{font-weight:800;font-size:1.2rem;letter-spacing:-.01em}
.brand-name span{color:var(--accent-2)}
.brand-logo{height:46px;width:auto;display:block}
.brand-plate{background:#fff;border-radius:12px;padding:.45rem .8rem;display:inline-flex;margin-bottom:1rem}
.brand-plate .brand-logo{height:40px}
.nav ul{list-style:none;margin:0;padding:0;display:flex;gap:1.4rem;align-items:center}
.nav{display:flex;align-items:center;gap:1.4rem}
.nav a:not(.btn){color:var(--ink);text-decoration:none;font-weight:600;padding:.4em 0;border-bottom:2px solid transparent}
.nav a:not(.btn):hover,.nav a[aria-current="page"]{border-bottom-color:var(--accent)}
.btn-nav{padding:.6em 1.1em;font-size:.95rem;white-space:nowrap}
.site-header .brand{flex-shrink:0}
.nav-toggle{display:none;background:none;border:0;width:44px;height:44px;padding:0;cursor:pointer;color:var(--ink);-webkit-appearance:none;appearance:none;border-radius:10px}
.nav-toggle svg{width:28px;height:28px;vertical-align:middle}
.nav-toggle .ico-close{display:none}
.nav-toggle[aria-expanded="true"] .ico-burger{display:none}
.nav-toggle[aria-expanded="true"] .ico-close{display:inline}
@media (max-width:960px){
  .nav-toggle{display:inline-block}
  .nav{position:absolute;left:0;right:0;top:70px;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;align-items:stretch;padding:1rem 1.25rem 1.25rem;gap:.5rem;display:none;box-shadow:var(--shadow)}
  .nav.open{display:flex}
  .nav ul{flex-direction:column;align-items:stretch;gap:0}
  .nav ul a{display:block;padding:.7em 0;border-bottom:1px solid var(--line)!important}
}

/* hero */
.hero{background:radial-gradient(1200px 600px at 85% -10%,var(--accent-soft),transparent 60%),linear-gradient(180deg,#fff,var(--bg-alt));padding:3.5rem 0 3rem}
.hero-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:3rem;align-items:center}
.hero-actions{display:flex;flex-wrap:wrap;gap:.8rem;margin:1.6rem 0}
.hero-proof{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;font-weight:600;color:var(--ink);font-size:.95rem}
.hero-proof li{display:inline-flex;align-items:center;gap:.4em}
.hero-proof svg{color:var(--accent-2)}
.hero-media{margin:0;position:relative}
@media (max-width:900px){
  .hero{padding:2.2rem 0 2.5rem}
  .hero-grid{grid-template-columns:1fr;gap:2rem}
}

/* sections */
.section{padding:4.5rem 0}
.section-tight{padding:2.5rem 0}
.section-alt{background:var(--bg-alt)}
.section-dark{background:linear-gradient(160deg,var(--navy),#0e2a46);color:#d7e3ee}
.section-dark h2,.section-dark h3{color:#fff}
.section-dark .eyebrow{color:var(--accent)}
.section-head{max-width:720px;margin-bottom:2.5rem}
.section-head.center,.center .section-head{margin-inline:auto}
.grid-2{display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:1.4rem;margin-bottom:2rem}
@media (max-width:980px){.grid-4{grid-template-columns:repeat(2,1fr)}}
@media (max-width:760px){.grid-2,.grid-3{grid-template-columns:1fr}}
@media (max-width:520px){.grid-4{grid-template-columns:1fr}}

/* cards */
.card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-4px);box-shadow:var(--shadow)}
.card-media img{aspect-ratio:4/3;object-fit:cover;width:100%}
.card-body{padding:1.2rem 1.3rem 1.4rem;display:flex;flex-direction:column;gap:.4rem;flex:1}
.card-body p{color:var(--muted);font-size:.97rem;flex:1}
.icon{display:inline-flex;width:46px;height:46px;border-radius:12px;background:var(--accent-soft);color:var(--accent-2);align-items:center;justify-content:center;margin-bottom:.4rem}
.icon svg{width:24px;height:24px}
.section-dark .icon{background:rgba(12,192,223,.15);color:var(--accent)}
.link-more{color:var(--accent-2);font-weight:700;font-size:.95rem}
.link-more::after{content:" →"}

/* steps */
.steps{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;counter-reset:s}
.steps li{background:#fff;border-radius:var(--radius);padding:1.5rem;border:1px solid var(--line);position:relative}
.step-num{display:inline-flex;width:38px;height:38px;border-radius:50%;background:var(--navy);color:#fff;font-weight:800;align-items:center;justify-content:center;margin-bottom:.8rem}
.steps p{color:var(--muted);font-size:.97rem;margin:0}
@media (max-width:980px){.steps{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.steps{grid-template-columns:1fr}}

/* curseur avant / après (voitures) */
.compare{position:relative;aspect-ratio:1;overflow:hidden;border-radius:var(--radius);user-select:none;-webkit-user-select:none;background:var(--bg-alt);touch-action:pan-y;cursor:ew-resize}
.compare.dragging{cursor:grabbing}
.compare img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;margin:0;border-radius:0;box-shadow:none;aspect-ratio:auto;pointer-events:none;-webkit-user-drag:none}
.compare .cmp-left{clip-path:inset(0 calc(100% - var(--pos)) 0 0)}
.cmp-line{position:absolute;top:0;bottom:0;left:var(--pos);width:3px;background:#fff;transform:translateX(-50%);box-shadow:0 0 0 1px rgba(11,31,51,.25);pointer-events:none;will-change:left}
.cmp-handle{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:46px;height:46px;border-radius:50%;background:#fff;color:var(--navy);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(11,31,51,.35)}
.cmp-handle svg{width:26px;height:26px}
.cmp-label{position:absolute;top:.8rem;background:rgba(11,31,51,.8);color:#fff;font-weight:700;font-size:.8rem;padding:.35em .7em;border-radius:999px;pointer-events:none;letter-spacing:.03em}
.cmp-label-l{left:.8rem}.cmp-label-r{right:.8rem}
.cmp-range{position:absolute;left:0;bottom:0;width:100%;height:2px;margin:0;padding:0;opacity:0;pointer-events:none}
.cmp-range:focus-visible + .cmp-line,.compare:has(.cmp-range:focus-visible) .cmp-handle{outline:3px solid var(--accent)}
.results .result .compare{border-radius:0}
a.card-body{text-decoration:none;color:inherit}

/* boutons avant / après (canapés) */
.ba{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.ba-media{position:relative;aspect-ratio:3/2;background:var(--bg-alt)}
.ba .ba-img{position:absolute;inset:0;width:100%;height:100%;aspect-ratio:auto;object-fit:cover;transition:opacity .25s}
.ba.is-apres .ba-avant{opacity:0}
.ba-tag{position:absolute;top:.8rem;left:.8rem;background:rgba(var(--navy-rgb),.8);color:var(--bg);font-weight:700;font-size:.8rem;padding:.35em .7em;border-radius:999px;letter-spacing:.03em}
.ba-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.5rem .8rem;padding:.7rem .8rem}
.ba-titre{color:var(--muted);font-size:.85rem;flex:1 1 11rem}
.ba-btns{display:inline-flex;gap:.2rem;margin-left:auto;padding:.2rem;border:1px solid var(--line);border-radius:999px;background:var(--bg)}
.ba-btn{border:0;background:none;font:inherit;font-weight:700;font-size:.85rem;color:var(--ink);padding:.45em 1.1em;min-height:40px;border-radius:999px;cursor:pointer}
.ba-btn[aria-pressed="true"]{background:var(--navy);color:var(--bg)}
.ba-btn:focus-visible,.ba-fleche:focus-visible,.mat-tab:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.hero-media .ba{box-shadow:0 25px 60px rgba(var(--navy-rgb),.2)}
.card-media .ba{border:0;border-radius:0}
.card-media .ba-media{aspect-ratio:4/3}
.ba-carrousel{margin-bottom:2rem}
.ba-fleches{display:flex;justify-content:flex-end;gap:.5rem;margin-bottom:.8rem}
.ba-fleches[hidden]{display:none}
.ba-fleche{display:flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0;border-radius:50%;border:1px solid var(--line);background:var(--bg);color:var(--ink);box-shadow:var(--shadow);cursor:pointer}
.ba-fleche:hover:not(:disabled){border-color:var(--accent)}
.ba-fleche:disabled{opacity:.4;cursor:default;box-shadow:none}
.ba-bande{display:flex;gap:1.2rem;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:.8rem;scrollbar-width:thin}
.ba-bande .ba{flex:none;width:min(520px,84vw);scroll-snap-align:start}
.service-resultats{margin-top:3rem}

/* results */
.result{margin:0;background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.result figcaption{padding:1rem 1.2rem;color:var(--muted);font-size:.95rem}

/* features */
.features .feature{padding:1.4rem;border-radius:var(--radius);background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.features .feature p{margin:0;font-size:.97rem;opacity:.9}
.features-light .feature{background:#fff;border:1px solid var(--line)}
.features-light .feature p{color:var(--muted)}

/* reviews */
.rating{display:flex;align-items:center;gap:.15em;color:#f5b301;font-weight:700}
.rating span{color:var(--ink);margin-left:.5em}
.review{margin:0;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1.6rem;position:relative}
.review::before{content:"“";position:absolute;top:-.2em;left:1rem;font-size:5rem;color:var(--accent-soft);font-family:Georgia,serif;line-height:1}
.review p{position:relative;font-size:1.02rem}
.review footer{font-weight:700;color:var(--ink);font-size:.93rem}
.reviews-carousel{position:relative;margin-bottom:1.8rem}
.reviews-band{overflow-x:auto;scroll-snap-type:x mandatory;padding:1.2rem 0 .6rem}
.reviews-band.has-arrows{scrollbar-width:none;scroll-snap-type:none}
.reviews-band.has-arrows::-webkit-scrollbar{display:none}
.reviews-track{display:flex;width:max-content}
.reviews-track .review{flex:none;width:min(360px,80vw);margin-right:1.5rem;scroll-snap-align:start}
.reviews-band.is-moving{overflow:hidden;scroll-snap-type:none}
.reviews-band.is-moving .reviews-track{animation:reviews-scroll 50s linear infinite}
.reviews-carousel:focus-within .reviews-band.is-moving .reviews-track{animation-play-state:paused}
@media (hover:hover){.reviews-carousel:hover .reviews-band.is-moving .reviews-track{animation-play-state:paused}}
@keyframes reviews-scroll{to{transform:translateX(-50%)}}
.reviews-arrow{position:absolute;top:50%;z-index:2;display:flex;align-items:center;justify-content:center;width:44px;height:44px;margin-top:-22px;padding:0;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--ink);box-shadow:var(--shadow);cursor:pointer}
.reviews-arrow:hover{border-color:var(--accent)}
.reviews-arrow[hidden]{display:none}
.reviews-prev{left:-1rem}
.reviews-next{right:-1rem}
@media (max-width:760px){.reviews-arrow{width:40px;height:40px;margin-top:-20px}}

/* faq */
details{background:#fff;border:1px solid var(--line);border-radius:12px;padding:0 1.2rem;margin-bottom:.8rem}
summary{cursor:pointer;font-weight:700;color:var(--ink);padding:1rem 0;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-size:1.4rem;color:var(--accent-2);font-weight:400}
details[open] summary::after{content:"−"}
details p{margin:0 0 1.1rem;color:var(--muted)}

/* cta band */
.cta-band{background:linear-gradient(120deg,var(--accent-2),var(--accent));color:#fff;padding:3.5rem 0}
.cta-band h2{color:#fff;margin-bottom:.3em}
.cta-band p{margin:0;max-width:56ch;opacity:.95}
.cta-inner{display:flex;justify-content:space-between;align-items:center;gap:2rem;flex-wrap:wrap}
.cta-actions{display:flex;gap:.8rem;flex-wrap:wrap}

/* page head */
.page-head{background:linear-gradient(180deg,#fff,var(--bg-alt));padding:3rem 0 2.5rem;border-bottom:1px solid var(--line)}
.page-head .hero-actions{margin-bottom:0}

/* page Canapé : grande photo */
.page-hero{position:relative;background:var(--navy);color:var(--bg);overflow:hidden}
.page-hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.page-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(var(--navy-rgb),.94) 0%,rgba(var(--navy-rgb),.82) 45%,rgba(var(--navy-rgb),.1) 100%)}
.page-hero .wrap{position:relative;z-index:1;padding:4.5rem 0}
.page-hero-texte{max-width:620px}
.page-hero h1{color:var(--bg)}
.page-hero .lead{color:var(--bg)}
.page-hero .eyebrow,.page-hero .eyebrow a{color:var(--accent)}
.page-hero-prix{font-weight:700;margin:0}
.page-hero-prix span{white-space:nowrap}
.page-hero .hero-actions{margin-bottom:0}
@media (max-width:860px){
  .page-hero-img{position:static;height:auto;aspect-ratio:2/1}
  .page-hero::after{display:none}
  .page-hero .wrap{padding:1.8rem 0 2.2rem}
}

/* page Canapé : méthode par matière */
.mat-tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:.3rem;padding:.3rem;margin-bottom:1.6rem;background:var(--bg-alt);border-radius:var(--radius)}
.mat-tab{border:0;background:none;font:inherit;font-weight:700;color:var(--ink);padding:.7em .5em;min-height:44px;border-radius:999px;cursor:pointer}
.mat-tab[aria-selected="true"]{background:var(--navy);color:var(--bg)}
.mat-etapes{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem}
.mat-etapes.trois{grid-template-columns:repeat(3,1fr)}
.mat-etapes li{background:var(--bg);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.mat-etapes img{width:100%;aspect-ratio:4/3;object-fit:cover}
.mat-texte{padding:1.1rem 1.2rem 1.3rem}
.mat-texte p{color:var(--muted);margin:0}
.mat-honnete{margin:1.8rem 0 .4rem;color:var(--ink);font-weight:600}
@media (max-width:1100px){.mat-etapes,.mat-etapes.trois{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){
  .mat-tabs{grid-template-columns:repeat(2,1fr)}
  .mat-etapes,.mat-etapes.trois{grid-template-columns:1fr}
  .mat-etapes li{display:grid;grid-template-columns:110px 1fr}
  .mat-etapes img{height:100%;aspect-ratio:auto;object-fit:contain;background:var(--accent-soft)}
  .mat-texte{padding:.8rem .9rem}
}

/* services page */
.service-block{display:grid;grid-template-columns:.9fr 1.1fr;gap:3rem;align-items:center}
.service-block.reverse .service-media{order:2}
.service-media img{border-radius:var(--radius);aspect-ratio:1;object-fit:cover;box-shadow:var(--shadow)}
.pricelist{list-style:none;padding:0;margin:1.2rem 0}
.pricelist li{display:grid;grid-template-columns:1fr auto;gap:.5rem 1rem;align-items:center;padding:.9rem 0;border-top:1px solid var(--line)}
.pricelist li:last-child{border-bottom:1px solid var(--line)}
.pricelist strong{display:block;color:var(--ink)}
.pricelist .muted{display:block;font-size:.92rem}
.price{font-weight:800;color:var(--ink);font-size:1.15rem;white-space:nowrap}
@media (max-width:860px){.service-block{grid-template-columns:1fr;gap:1.6rem}.service-block.reverse .service-media{order:0}}

/* form */
.grid-form{display:grid;grid-template-columns:1.2fr .8fr;gap:2.5rem;align-items:start}
@media (max-width:860px){.grid-form{grid-template-columns:1fr}}
.form{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1.8rem;box-shadow:var(--shadow)}
.field{margin-bottom:1.1rem}
.field-row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
@media (max-width:520px){.field-row{grid-template-columns:1fr}}
label{display:block;font-weight:700;color:var(--ink);margin-bottom:.35rem;font-size:.95rem}
input,select,textarea{width:100%;font:inherit;padding:.75em .9em;border:1.5px solid var(--line);border-radius:10px;background:#fbfdfe;color:var(--ink)}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(12,192,223,.2)}
input[aria-invalid="true"],select[aria-invalid="true"]{border-color:#d9534f}
.form-error{color:#b3261e;font-weight:600}
.form-actions{display:flex;gap:.8rem;flex-wrap:wrap;margin:1.2rem 0 .8rem}
.aside{display:grid;gap:1.2rem}
.aside-card{background:var(--bg-alt);border-radius:var(--radius);padding:1.5rem}
.aside-card h2{font-size:1.15rem}
.aside-quiet{background:#fff;border:1px solid var(--line)}
.big-link{font-size:1.5rem;font-weight:800;color:var(--ink);text-decoration:none}
.checklist{list-style:none;padding:0;margin:0;display:grid;gap:.5rem}
.checklist svg{color:var(--accent-2)}

/* contact */
.contact-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:1.8rem;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s}
.contact-card:hover{transform:translateY(-4px);box-shadow:var(--shadow)}
.contact-card h2{font-size:1.1rem;margin:.3rem 0}
.contact-card .big{font-size:1.35rem;font-weight:800;color:var(--ink);margin:0 0 .2rem}
.contact-card .big-mail{font-size:1.05rem;word-break:break-all}
.zone-grid{align-items:center}
.zones{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(2,1fr);gap:.4rem .8rem}
.zones li{background:#fff;border:1px solid var(--line);border-radius:8px;padding:.5em .8em;font-size:.95rem}
.zones li::before{content:"📍 ";font-size:.85em}

/* legal */
.legal h2{font-size:1.2rem;margin-top:1.8rem}

/* footer */
.site-footer{background:var(--navy);color:#c6d3df;padding:3.5rem 0 1.5rem;margin-bottom:64px}
.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:2.5rem}
.footer-title{color:#fff;font-size:1rem;text-transform:uppercase;letter-spacing:.08em;margin-bottom:1rem}
.footer-links{list-style:none;padding:0;margin:0;display:grid;gap:.5rem}
.footer-links a{color:#e6eef5;text-decoration:none}
.footer-links a:hover{color:var(--accent)}
.site-footer .muted{color:#9fb1c2}
.footer-bottom{border-top:1px solid rgba(255,255,255,.1);margin-top:2.5rem;padding-top:1.2rem;font-size:.85rem;color:#8fa2b5}
@media (max-width:760px){.footer-grid{grid-template-columns:1fr;gap:2rem}}
@media (min-width:961px){.site-footer{margin-bottom:0}}

/* mobile bar */
.mobile-bar{position:fixed;left:0;right:0;bottom:0;display:none;grid-template-columns:1fr 1.4fr;gap:.6rem;padding:.6rem .8rem calc(.6rem + env(safe-area-inset-bottom));background:rgba(255,255,255,.95);backdrop-filter:blur(10px);border-top:1px solid var(--line);z-index:40}
.mobile-bar a{display:inline-flex;align-items:center;justify-content:center;gap:.5em;padding:.8em;border-radius:999px;font-weight:700;text-decoration:none;color:var(--ink);border:2px solid var(--line)}
.mobile-bar .mobile-bar-wa{background:var(--accent);color:#04202a;border-color:var(--accent)}
@media (max-width:960px){.mobile-bar{display:grid}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}.reviews-band.is-moving{overflow-x:auto}.reviews-band.is-moving .reviews-track{animation:none}}
'''

JS = r'''
(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
    document.addEventListener('click',function(e){if(!n.contains(e.target)&&!t.contains(e.target)&&n.classList.contains('open')){n.classList.remove('open');t.setAttribute('aria-expanded','false');}});}
  document.querySelectorAll('.compare').forEach(function(c){
    var r=c.querySelector('.cmp-range'), active=false;
    function setPct(p){p=Math.max(0,Math.min(100,p));c.style.setProperty('--pos',p+'%');if(r)r.value=Math.round(p);}
    function pct(e){var b=c.getBoundingClientRect();return (e.clientX-b.left)/b.width*100;}
    c.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'&&e.button!==0)return;active=true;c.classList.add('dragging');try{c.setPointerCapture(e.pointerId);}catch(x){}setPct(pct(e));e.preventDefault();});
    c.addEventListener('pointermove',function(e){if(!active)return;setPct(pct(e));e.preventDefault();});
    function end(){active=false;c.classList.remove('dragging');}
    c.addEventListener('pointerup',end);c.addEventListener('pointercancel',end);c.addEventListener('lostpointercapture',end);
    if(r){r.addEventListener('input',function(){setPct(+r.value);});}
    setPct(+c.dataset.start||50);
  });
  var f=document.getElementById('booking');
  if(!f)return;
  var WA='33647271062', MAIL='nadifa.proprete@gmail.com';
  function v(id){var el=document.getElementById(id);return el?el.value.trim():'';}
  function build(){
    var d=v('f-date'), dd='';
    if(d){var p=d.split('-');dd=p.length===3?(p[2]+'/'+p[1]+'/'+p[0]):d;}
    return 'Bonjour Nadifa Propreté, je souhaite réserver une intervention.\n'
      +'• Nom : '+v('f-name')+'\n'
      +'• Téléphone : '+v('f-phone')+'\n'
      +'• Prestation : '+v('f-service')+'\n'
      +(v('f-city')?'• Lieu : '+v('f-city')+'\n':'')
      +(dd?'• Date souhaitée : '+dd+'\n':'')
      +(v('f-msg')?'• Précisions : '+v('f-msg')+'\n':'')
      +'Merci de me confirmer le tarif et un créneau.';
  }
  var m=document.getElementById('mail-fallback');
  function syncMail(){ if(m){m.href='mailto:'+MAIL+'?subject='+encodeURIComponent('Demande de nettoyage – '+(v('f-service')||'devis'))+'&body='+encodeURIComponent(build());} }
  f.addEventListener('input',syncMail); syncMail();
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var ok=true, err=document.getElementById('form-error');
    ['f-name','f-phone','f-service'].forEach(function(id){var el=document.getElementById(id);var bad=!el.value.trim();el.setAttribute('aria-invalid',bad?'true':'false');if(bad)ok=false;});
    if(!ok){err.hidden=false;return;}
    err.hidden=true;
    window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(build()),'_blank','noopener');
  });
})();
(function(){
  var b=document.querySelector('.reviews-band'),prev=document.querySelector('.reviews-prev'),next=document.querySelector('.reviews-next');
  if(!b||!prev||!next)return;
  var t=b.querySelector('.reviews-track'),n=t.children.length,still=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  [].slice.call(t.children).forEach(function(c){var k=c.cloneNode(true);k.setAttribute('aria-hidden','true');t.appendChild(k);});
  function step(){return t.children[1].getBoundingClientRect().left-t.children[0].getBoundingClientRect().left;}
  function go(d){
    var s=step(),x=b.scrollLeft;
    if(b.classList.contains('is-moving')){x=-new DOMMatrix(getComputedStyle(t).transform).m41;b.classList.remove('is-moving');}
    if(x>=s*n)x-=s*n;
    if(d<0&&x<s/2)x+=s*n;
    b.scrollLeft=x;
    b.scrollTo({left:(Math.round(x/s)+d)*s,behavior:still?'auto':'smooth'});
  }
  prev.addEventListener('click',function(){go(-1);});
  next.addEventListener('click',function(){go(1);});
  b.classList.add('has-arrows');prev.hidden=next.hidden=false;
  if(!still)b.classList.add('is-moving');
})();
(function(){
  document.querySelectorAll('.ba').forEach(function(f){
    var tag=f.querySelector('.ba-tag'),btns=f.querySelectorAll('.ba-btn');
    btns.forEach(function(b){b.addEventListener('click',function(){
      f.classList.toggle('is-apres',b.dataset.ba==='apres');
      tag.textContent=b.textContent;
      btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
    });});
  });
  var still=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.ba-carrousel').forEach(function(c){
    var b=c.querySelector('.ba-bande'),fl=c.querySelector('.ba-fleches'),p=c.querySelector('.ba-prev'),n=c.querySelector('.ba-next');
    function pas(){return b.children[1].offsetLeft-b.children[0].offsetLeft;}
    function maj(){p.disabled=b.scrollLeft<=2;n.disabled=b.scrollLeft+b.clientWidth>=b.scrollWidth-2;}
    p.addEventListener('click',function(){b.scrollBy({left:-pas(),behavior:still?'auto':'smooth'});});
    n.addEventListener('click',function(){b.scrollBy({left:pas(),behavior:still?'auto':'smooth'});});
    b.addEventListener('scroll',maj,{passive:true});
    fl.hidden=false;maj();
  });
  document.querySelectorAll('.mat').forEach(function(m){
    var tabs=[].slice.call(m.querySelectorAll('[role=tab]'));
    function choisir(t,focus){
      tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!on;});
      if(focus)t.focus();
    }
    tabs.forEach(function(t,i){
      t.addEventListener('click',function(){choisir(t);});
      t.addEventListener('keydown',function(e){var d=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(d){e.preventDefault();choisir(tabs[(i+d+tabs.length)%tabs.length],true);}});
    });
    choisir(tabs[0]);
  });
})();
'''

MANIFEST = '''{
  "name": "Nadifa Propreté",
  "short_name": "Nadifa",
  "start_url": "./",
  "display": "browser",
  "background_color": "#ffffff",
  "theme_color": "#0b1f33",
  "icons": [
    { "src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
'''
ROBOTS = f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n"
today = datetime.date.today().isoformat()
SITEMAP = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f'  <url><loc>{BASE}/{p}</loc><lastmod>{today}</lastmod><changefreq>{f}</changefreq><priority>{pr}</priority></url>\n'
    for p,f,pr in [("","weekly","1.0"),("services.html","monthly","0.9")] + [(d["path"],"monthly","0.9") for d in SVC_PAGES] + [("reservation.html","monthly","0.8"),("nettoyage-professionnels-toulouse.html","monthly","0.8"),("contact.html","monthly","0.7")]) + "</urlset>\n"

ASSET_V = hashlib.md5((CSS+JS).encode()).hexdigest()[:8]
pages = {"index.html":page_index(),"services.html":page_services(),"reservation.html":page_reservation(),"contact.html":page_contact(),"mentions-legales.html":page_mentions(),"politique-confidentialite.html":page_confidentialite(),"404.html":page_404(),PROS_PATH:page_pros()}
pages.update({d["path"]:page_service(d) for d in SVC_PAGES})
for name,content in pages.items():
    open(os.path.join(OUT,name),"w",encoding="utf-8").write(content)
open(os.path.join(OUT,"assets/css/style.css"),"w").write(CSS.strip()+"\n")
open(os.path.join(OUT,"assets/js/main.js"),"w").write(JS.strip()+"\n")
open(os.path.join(OUT,"site.webmanifest"),"w").write(MANIFEST)
open(os.path.join(OUT,"robots.txt"),"w").write(ROBOTS)
open(os.path.join(OUT,"sitemap.xml"),"w").write(SITEMAP)
open(os.path.join(OUT,".nojekyll"),"w").write("")
print("ok", {k:len(v) for k,v in pages.items()})
