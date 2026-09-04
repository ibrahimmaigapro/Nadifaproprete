# -*- coding: utf-8 -*-
import os, html, datetime, hashlib
OUT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://nadifaproprete.fr"
PHONE_H = "06 47 27 10 62"; PHONE_T = "+33647271062"; WA = "33647271062"
EMAIL = "contact@nadifaproprete.fr"
GBP = "https://share.google/19td8ZPjC2HE1T8S3"
YEAR = 2026

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
 "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z" fill="currentColor"/></svg>',
 "camera": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v11H4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
}

MARK = '<svg class="brand-mark" viewBox="0 0 64 64" width="44" height="44" aria-hidden="true"><rect width="64" height="64" rx="16" fill="#0cc0df"/><path d="M18 46V18h7l14 18V18h7v28h-7L25 28v18z" fill="#fff"/><path d="M48 10l1.5 4 4 1.5-4 1.5-1.5 4-1.5-4-4-1.5 4-1.5z" fill="#fff" fill-opacity=".92"/></svg>'

NAV = [("index.html","Accueil"),("services.html","Services & tarifs"),("reservation.html","Réserver"),("contact.html","Contact")]

def head(title, desc, path, og_type="website", extra=""):
    canonical = BASE + ("/" if path=="index.html" else "/"+path)
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="assets/img/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="assets/img/icon-192.png">
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
    <a class="brand" href="index.html" aria-label="Nadifa Propreté, accueil">
      {MARK}
      <span class="brand-name">Nadifa <span>Propreté</span></span>
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
      <a class="brand brand-light" href="index.html">{MARK}<span class="brand-name">Nadifa <span>Propreté</span></span></a>
      <p class="muted">Nettoyage à domicile de canapés, matelas, tapis et intérieurs de voiture. Toulouse et 40 km alentour.</p>
      <p class="muted small">« Nadifa » signifie « propre » en arabe. C'est la promesse.</p>
    </div>
    <div>
      <h2 class="footer-title">Navigation</h2>
      <ul class="footer-links">
        <li><a href="services.html">Services & tarifs</a></li>
        <li><a href="reservation.html">Réserver une intervention</a></li>
        <li><a href="contact.html">Contact & zone desservie</a></li>
        <li><a href="{GBP}" target="_blank" rel="noopener">Avis Google</a></li>
        <li><a href="mentions-legales.html">Mentions légales</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-title">Contact</h2>
      <ul class="footer-links">
        <li><a href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a></li>
        <li><a href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp</a></li>
        <li><a href="mailto:{EMAIL}">{ICON["mail"]} {EMAIL}</a></li>
        <li>{ICON["clock"]} Lundi – samedi, 8 h – 19 h</li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>© {YEAR} Nadifa Propreté · Ibrahim Maiga, micro-entrepreneur · SIRET 989 023 213 00014 · Toulouse</p>
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

# ---------- JSON-LD ----------
LD_BUSINESS = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "{BASE}/#business",
  "name": "Nadifa Propreté",
  "alternateName": "Nadifa Propreté – Nettoyage à domicile Toulouse",
  "description": "Nettoyage à domicile par injection-extraction : canapés, fauteuils, matelas, tapis, moquettes et intérieurs de voiture. Toulouse et agglomération (40 km).",
  "url": "{BASE}/",
  "telephone": "{PHONE_T}",
  "email": "{EMAIL}",
  "image": "{BASE}/assets/img/og-image.jpg",
  "logo": "{BASE}/assets/img/icon-512.png",
  "priceRange": "€€",
  "currenciesAccepted": "EUR",
  "address": {{ "@type": "PostalAddress", "addressLocality": "Toulouse", "postalCode": "31100", "addressCountry": "FR" }},
  "areaServed": [
    {{ "@type": "City", "name": "Toulouse" }},
    {{ "@type": "GeoCircle", "geoMidpoint": {{ "@type": "GeoCoordinates", "latitude": 43.6045, "longitude": 1.4442 }}, "geoRadius": "40000" }}
  ],
  "openingHoursSpecification": [{{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "08:00", "closes": "19:00" }}],
  "sameAs": ["{GBP}"],
  "founder": {{ "@type": "Person", "name": "Ibrahim Maiga" }},
  "hasOfferCatalog": {{
    "@type": "OfferCatalog", "name": "Prestations de nettoyage",
    "itemListElement": [
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Nettoyage intérieur de voiture", "serviceType": "Nettoyage automobile intérieur" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Nettoyage de canapé et fauteuil", "serviceType": "Nettoyage de textile d'ameublement" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Nettoyage de matelas", "serviceType": "Nettoyage de literie" }} }},
      {{ "@type": "Offer", "price": "40", "priceCurrency": "EUR", "itemOffered": {{ "@type": "Service", "name": "Nettoyage de tapis à domicile" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Nettoyage de moquette" }} }},
      {{ "@type": "Offer", "itemOffered": {{ "@type": "Service", "name": "Vitres, après travaux, ménage" }} }}
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
def cta_band():
    return f'''<section class="cta-band">
  <div class="wrap cta-inner">
    <div>
      <h2>Un devis clair en quelques minutes</h2>
      <p>Envoyez une photo de votre canapé, matelas, tapis ou véhicule sur WhatsApp : vous recevez le tarif exact avant toute intervention.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-light" href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} Envoyer une photo</a>
      <a class="btn btn-outline-light" href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a>
    </div>
  </div>
</section>
'''

SERVICES = [
 ("car","Intérieur de voiture","siege-auto","Sièges, tapis de sol, plastiques, vitres intérieures. Formule Entretien ou Rénovation selon l'état.","services.html#voiture","Nettoyage d'un siège de voiture par injection-extraction"),
 ("sofa","Canapés & fauteuils","canape","Tissu, microfibre ou velours : taches, auréoles et odeurs traitées en profondeur, sans abîmer les fibres.","services.html#canapes","Nettoyage d'un canapé en tissu à domicile"),
 ("bed","Matelas","matelas","Poussière, acariens et traces. Un matelas assaini, sec en quelques heures.","services.html#matelas","Nettoyage d'un matelas par injection-extraction"),
 ("rug","Tapis & moquettes","tapis","Tapis nettoyé chez vous en 45 minutes. Moquettes de chambre, salon ou bureau.","services.html#tapis","Nettoyage d'un tapis à domicile"),
]

# ---------- INDEX ----------
def page_index():
    h = head("Nettoyage canapé, matelas, tapis et voiture à Toulouse | Nadifa Propreté",
             "Nadifa Propreté nettoie à domicile vos canapés, matelas, tapis et intérieurs de voiture par injection-extraction. Toulouse et 40 km. Devis fixe avant intervention, sous 48 h.",
             "index.html", extra=LD_BUSINESS + '<link rel="preload" as="image" href="assets/img/hero-dacia-800.webp" imagesrcset="assets/img/hero-dacia-480.webp 480w, assets/img/hero-dacia-800.webp 800w, assets/img/hero-dacia-1400.webp 1400w" imagesizes="(max-width: 900px) 100vw, 50vw">\n')
    cards = "".join(f'''<a class="card service-card" href="{link}">
      <div class="card-media">{picture(img, alt, sizes="(max-width: 700px) 100vw, 25vw", w=1024, h=1024)}</div>
      <div class="card-body">
        <span class="icon">{ICON[ic]}</span>
        <h3>{t}</h3>
        <p>{d}</p>
        <span class="link-more">Voir la prestation</span>
      </div>
    </a>''' for ic,t,img,d,link,alt in SERVICES)
    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <p class="eyebrow">Nettoyage à domicile · Toulouse et agglomération</p>
      <h1>Canapés, matelas, tapis et intérieurs de voiture&nbsp;: propres en profondeur, chez vous.</h1>
      <p class="lead">Injection-extraction professionnelle, produits adaptés à chaque textile et un tarif fixe annoncé avant de commencer. Intervention sous 48&nbsp;h à Toulouse et dans un rayon de 40&nbsp;km.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} Devis gratuit sur WhatsApp</a>
        <a class="btn btn-ghost btn-lg" href="tel:{PHONE_T}">{ICON["phone"]} {PHONE_H}</a>
      </div>
      <ul class="hero-proof">
        <li>{ICON["check"]} Intervention sous 48 h</li>
        <li>{ICON["check"]} Sec en 3 h environ</li>
        <li>{ICON["check"]} Prix fixe, sans surprise</li>
        <li>{ICON["check"]} Avis Google 5/5</li>
      </ul>
    </div>
    <figure class="hero-media">
      {picture("hero-dacia", "Intérieur d'une Dacia Sandero après nettoyage par Nadifa Propreté à Toulouse : tableau de bord, console et moquettes impeccables", sizes="(max-width: 900px) 100vw, 50vw", eager=True, w=1400, h=1867)}
      <figcaption><span class="badge">{ICON["camera"]} Résultat réel · Sandero de chantier, Toulouse</span></figcaption>
    </figure>
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
      <li><span class="step-num">1</span><h3>Vous envoyez une photo</h3><p>Sur WhatsApp ou par téléphone, décrivez ce qu'il faut nettoyer. Vous recevez un prix fixe dans la foulée.</p></li>
      <li><span class="step-num">2</span><h3>On fixe un créneau</h3><p>Généralement sous 48 h, du lundi au samedi, à l'heure qui vous arrange.</p></li>
      <li><span class="step-num">3</span><h3>Nettoyage à domicile</h3><p>Pré-traitement des taches, injection-extraction, finitions. Comptez 45 min à 2 h selon la prestation.</p></li>
      <li><span class="step-num">4</span><h3>Vous profitez</h3><p>Le textile est sec en 3 h environ. Vous vérifiez le résultat avec nous avant de régler.</p></li>
    </ol>
  </div>
</section>

<section class="section" id="resultats">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Avant / après</p>
      <h2>Des résultats visibles, pas des promesses</h2>
    </div>
    <div class="grid-3 results">
      <figure class="result">
        {picture("avant-apres-yaris", "Toyota Yaris avant et après nettoyage intérieur : tapis de sol pleins de débris puis console et moquettes propres", sizes="(max-width: 760px) 100vw, 33vw", w=1400, h=934)}
        <figcaption>Citadine de tous les jours : tapis de sol, console et rangements, avant / après.</figcaption>
      </figure>
      <figure class="result">
        {picture("avant-apres-canape", "Canapé noir en tissu avant et après nettoyage par injection-extraction : traces et auréoles disparues", sizes="(max-width: 760px) 100vw, 33vw", w=1024, h=1024)}
        <figcaption>Canapé d'angle en tissu : auréoles et traces d'usage éliminées.</figcaption>
      </figure>
      <figure class="result">
        {picture("injection-canape", "Buse d'injection-extraction sur un canapé en tissu clair pendant le nettoyage", sizes="(max-width: 760px) 100vw, 33vw", w=1024, h=1024)}
        <figcaption>L'injection-extraction : l'eau et le produit sont injectés dans la fibre puis aspirés avec la saleté.</figcaption>
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
    <div class="grid-3 features">
      <div class="feature"><span class="icon">{ICON["spark"]}</span><h3>Injection-extraction pro</h3><p>Une machine professionnelle qui nettoie dans la fibre, pas seulement en surface. Les taches partent, les odeurs aussi.</p></div>
      <div class="feature"><span class="icon">{ICON["shield"]}</span><h3>Produits adaptés au textile</h3><p>Chaque matière (tissu, microfibre, velours, cuir de siège auto) a son produit. Rien d'agressif, rien qui décolore.</p></div>
      <div class="feature"><span class="icon">{ICON["tag"]}</span><h3>Prix fixe annoncé avant</h3><p>Le tarif est donné sur photo, avant l'intervention. Pas de supplément découvert sur place.</p></div>
      <div class="feature"><span class="icon">{ICON["clock"]}</span><h3>Réactif</h3><p>Réponse rapide sur WhatsApp, intervention sous 48 h dans la plupart des cas.</p></div>
      <div class="feature"><span class="icon">{ICON["wind"]}</span><h3>Séchage rapide</h3><p>Grâce à l'extraction, le textile est sec en 3 h environ. Vous retrouvez votre canapé le soir même.</p></div>
      <div class="feature"><span class="icon">{ICON["pin"]}</span><h3>Local et indépendant</h3><p>Une entreprise toulousaine à taille humaine : c'est la même personne qui répond, qui vient et qui nettoie.</p></div>
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
    <div class="grid-2">
      <blockquote class="review">
        <p>« J'ai fait nettoyer l'intérieur de ma voiture pro, une Sandero Stepway qui vit sur les chantiers. Les tapis étaient pleins de débris et j'avais des taches sur les sièges que je n'arrivais pas à faire partir. Tout est parti. Sièges nickel, moquettes comme neuves, même les aérateurs et les rainures autour du levier de vitesses sont propres. »</p>
        <footer>Abdul M. · Nettoyage intérieur voiture</footer>
      </blockquote>
      <blockquote class="review">
        <p>« La voiture était dans un état catastrophique, je ne la reconnais plus. »</p>
        <footer>Madison V. · Nettoyage intérieur voiture</footer>
      </blockquote>
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
    <details><summary>Combien de temps faut-il pour que ça sèche ?</summary><p>Environ 3 heures pour un canapé ou un matelas, grâce à l'extraction qui retire la majeure partie de l'eau. Une pièce aérée accélère encore le séchage.</p></details>
    <details><summary>Dois-je déplacer mon canapé ou mon matelas ?</summary><p>Non. Nous intervenons à domicile, dans la pièce où se trouve le meuble. Nous avons seulement besoin d'une prise électrique.</p></details>
    <details><summary>Les taches anciennes partent-elles ?</summary><p>La plupart, oui : traces de boisson, sueur, auréoles, poussière incrustée. Certaines teintures (encre, colorant) peuvent laisser une marque atténuée. Envoyez une photo, nous vous dirons franchement ce qu'il est possible d'obtenir.</p></details>
    <details><summary>Où intervenez-vous ?</summary><p>À Toulouse et dans un rayon d'environ 40 km : Blagnac, Colomiers, Tournefeuille, Muret, Balma, L'Union, Ramonville, Labège, Castanet… Le déplacement est compris dans le tarif annoncé.</p></details>
    <details><summary>Comment se passe le paiement ?</summary><p>Vous réglez une fois l'intervention terminée et le résultat vérifié ensemble. Une facture vous est remise.</p></details>
  </div>
</section>
{cta_band()}
'''
    return h + header("index.html") + body + footer()

# ---------- SERVICES ----------
def price_row(name, detail, price, note=""):
    p = f'<span class="price">{price}</span>' if price else '<span class="price price-quote">Prix fixe sur photo</span>'
    return f'<li><div><strong>{name}</strong><span class="muted">{detail}</span></div>{p}{f"<em>{note}</em>" if note else ""}</li>'

def page_services():
    h = head("Services et tarifs : voiture, canapé, matelas, tapis à Toulouse | Nadifa Propreté",
             "Toutes les prestations Nadifa Propreté à Toulouse : formules voiture Entretien et Rénovation, canapés 2 à 4 places, fauteuils, matelas, tapis à domicile dès 40 €, moquettes, vitres, après travaux.",
             "services.html", extra=breadcrumb("Services et tarifs","services.html"))
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Services & tarifs</p>
    <h1>Des prestations claires, un prix fixe annoncé avant</h1>
    <p class="lead">Envoyez une photo sur WhatsApp, vous recevez le tarif exact en quelques minutes. Le déplacement dans Toulouse et l'agglomération est compris.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{WA_DEVIS}" target="_blank" rel="noopener">{ICON["wa"]} Obtenir mon tarif</a>
      <a class="btn btn-ghost" href="reservation.html">Réserver un créneau</a>
    </div>
  </div>
</section>

<section class="section" id="voiture">
  <div class="wrap service-block">
    <div class="service-media">{picture("siege-auto","Nettoyage d'un siège de voiture en tissu par injection-extraction", sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON["car"]}</span>
      <h2>Intérieur de voiture</h2>
      <p>Voiture personnelle, voiture pro qui tourne sur les chantiers, véhicule de famille : nous intervenons sur votre parking, chez vous ou au travail.</p>
      <ul class="pricelist">
        {price_row("Formule Entretien","Aspiration complète, dépoussiérage des plastiques et aérateurs, vitres intérieures, shampoing des sièges et tapis de sol.","")}
        {price_row("Formule Rénovation","Formule Entretien + traitement des taches incrustées, moquettes et coffre en injection-extraction, rénovation des plastiques, désodorisation.","")}
      </ul>
      <p class="small muted">Le tarif dépend de la taille du véhicule (citadine, berline, SUV, utilitaire) et de son état. Il est confirmé sur photo avant l'intervention.</p>
    </div>
  </div>
</section>

<section class="section section-alt" id="canapes">
  <div class="wrap service-block reverse">
    <div class="service-media">{picture("canape","Nettoyage d'un canapé en tissu gris avec une machine à injection-extraction", sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON["sofa"]}</span>
      <h2>Canapés et fauteuils</h2>
      <p>Tissu, microfibre, velours, lin : pré-traitement des taches, injection-extraction sur l'assise, le dossier et les coussins, puis finition. Sec en 3 h environ.</p>
      <ul class="pricelist">
        {price_row("Canapé 2 places","Assise, dossier, accoudoirs et coussins.","")}
        {price_row("Canapé 3 places","Assise, dossier, accoudoirs et coussins.","")}
        {price_row("Canapé 4 places ou d'angle","Méridienne comprise.","")}
        {price_row("Fauteuil","Fauteuil de salon, chaise en tissu, tête de lit.","")}
      </ul>
    </div>
  </div>
</section>

<section class="section" id="matelas">
  <div class="wrap service-block">
    <div class="service-media">{picture("matelas","Nettoyage d'un matelas blanc par injection-extraction", sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON["bed"]}</span>
      <h2>Matelas</h2>
      <p>Traces de transpiration, auréoles, poussière et acariens : le matelas est nettoyé sur la face de couchage, puis séché par extraction. Vous dormez dessus le soir même.</p>
      <ul class="pricelist">
        {price_row("Matelas standard","90 × 190 à 160 × 200 cm, une face.","")}
        {price_row("Matelas king size","180 × 200 cm et plus, une face.","")}
      </ul>
      <p class="small muted">Deuxième face ou sommier tapissier : sur demande.</p>
    </div>
  </div>
</section>

<section class="section section-alt" id="tapis">
  <div class="wrap service-block reverse">
    <div class="service-media">{picture("tapis","Nettoyage d'un tapis à domicile avec une brosse et une bassine", sizes="(max-width: 900px) 100vw, 40vw", w=1024, h=1024)}</div>
    <div class="service-text">
      <span class="icon">{ICON["rug"]}</span>
      <h2>Tapis et moquettes</h2>
      <p>Le tapis est nettoyé chez vous, sans l'emporter : dépoussiérage, injection-extraction, remise en forme des fibres. Pour les moquettes, comptez une pièce en une heure environ.</p>
      <ul class="pricelist">
        {price_row("Tapis à domicile","Jusqu'à 2 × 3 m environ. Durée : 45 min.","40 €")}
        {price_row("Moquette","Chambre, salon, bureau, escalier. Tarif au m².","")}
      </ul>
    </div>
  </div>
</section>

<section class="section" id="autres">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Également</p>
      <h2>Vitres, après travaux et ménage</h2>
    </div>
    <div class="grid-3 features features-light">
      <div class="feature"><span class="icon">{ICON["window"]}</span><h3>Vitres et baies vitrées</h3><p>Intérieur et extérieur accessibles depuis le sol, encadrements compris.</p></div>
      <div class="feature"><span class="icon">{ICON["spark"]}</span><h3>Nettoyage après travaux</h3><p>Poussière de plâtre, traces de peinture, sols et vitres : remise au propre avant d'emménager.</p></div>
      <div class="feature"><span class="icon">{ICON["check"]}</span><h3>Ménage ponctuel ou régulier</h3><p>Appartement, maison, bureau ou logement de location entre deux locataires.</p></div>
    </div>
    <p class="center small muted">Ces prestations sont chiffrées sur devis, après échange de photos ou visite rapide.</p>
  </div>
</section>
{cta_band()}
'''
    return h + header("services.html") + body + footer()

# ---------- RESERVATION ----------
def page_reservation():
    h = head("Réserver un nettoyage à domicile à Toulouse | Nadifa Propreté",
             "Réservez votre nettoyage de canapé, matelas, tapis ou intérieur de voiture à Toulouse. Formulaire en 1 minute, réponse rapide sur WhatsApp, intervention sous 48 h.",
             "reservation.html", extra=breadcrumb("Réserver","reservation.html"))
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Réservation</p>
    <h1>Réserver une intervention</h1>
    <p class="lead">Remplissez le formulaire : votre demande s'ouvre dans WhatsApp, prête à envoyer. Nous confirmons le tarif et le créneau rapidement. Rien n'est enregistré sur ce site.</p>
  </div>
</section>

<section class="section">
  <div class="wrap grid-form">
    <form class="form" id="booking" novalidate>
      <div class="field">
        <label for="f-name">Votre prénom / nom</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required placeholder="Ex. : Sarah D.">
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
            <option>Voiture – Formule Entretien</option>
            <option>Voiture – Formule Rénovation</option>
          </optgroup>
          <optgroup label="Canapés et fauteuils">
            <option>Canapé 2 places</option>
            <option>Canapé 3 places</option>
            <option>Canapé 4 places / d'angle</option>
            <option>Fauteuil</option>
          </optgroup>
          <optgroup label="Matelas">
            <option>Matelas standard</option>
            <option>Matelas king size</option>
          </optgroup>
          <optgroup label="Tapis et moquettes">
            <option>Tapis à domicile</option>
            <option>Moquette</option>
          </optgroup>
          <optgroup label="Autres">
            <option>Vitres</option>
            <option>Nettoyage après travaux</option>
            <option>Ménage</option>
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
        <p class="muted">Du lundi au samedi, 8 h – 19 h. Si nous sommes en intervention, laissez un message ou écrivez sur WhatsApp : nous rappelons dans la journée.</p>
      </div>
      <div class="aside-card">
        <h2>Le jour de l'intervention</h2>
        <ul class="checklist">
          <li>{ICON["check"]} Une prise électrique à proximité</li>
          <li>{ICON["check"]} Le meuble accessible (coussins et objets retirés)</li>
          <li>{ICON["check"]} Pour une voiture : les objets personnels sortis, une place où stationner</li>
          <li>{ICON["check"]} Comptez 45 min à 2 h selon la prestation, puis 3 h de séchage</li>
        </ul>
      </div>
      <div class="aside-card aside-quiet">
        <h2>Zone d'intervention</h2>
        <p class="muted">Toulouse et communes dans un rayon de 40 km. <a href="contact.html#zone">Voir la liste</a>.</p>
      </div>
    </aside>
  </div>
</section>
'''
    return h + header("reservation.html") + body + footer()

# ---------- CONTACT ----------
ZONES = ["Toulouse (tous quartiers)","Blagnac","Colomiers","Tournefeuille","Plaisance-du-Touch","Cugnaux","Muret","Portet-sur-Garonne","Ramonville-Saint-Agne","Labège","Castanet-Tolosan","Saint-Orens-de-Gameville","Balma","L'Union","Saint-Jean","Aucamville","Fenouillet","Castelginest","Léguevin","Grenade","Fronton","Villefranche-de-Lauragais"]

def page_contact():
    h = head("Contact et zone d'intervention à Toulouse | Nadifa Propreté",
             "Contactez Nadifa Propreté à Toulouse : téléphone, WhatsApp, e-mail. Intervention à domicile à Toulouse, Blagnac, Colomiers, Tournefeuille, Muret, Balma et dans un rayon de 40 km.",
             "contact.html", extra=breadcrumb("Contact","contact.html"))
    zones = "".join(f"<li>{z}</li>" for z in ZONES)
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Parlons de ce qu'il faut nettoyer</h1>
    <p class="lead">Le plus rapide : une photo sur WhatsApp. Vous recevez un prix fixe et un créneau dans la journée.</p>
  </div>
</section>

<section class="section">
  <div class="wrap grid-3 contact-cards">
    <a class="contact-card" href="{WA_DEVIS}" target="_blank" rel="noopener">
      <span class="icon">{ICON["wa"]}</span>
      <h2>WhatsApp</h2>
      <p class="big">{PHONE_H}</p>
      <p class="muted">Réponse rapide, photos bienvenues</p>
    </a>
    <a class="contact-card" href="tel:{PHONE_T}">
      <span class="icon">{ICON["phone"]}</span>
      <h2>Téléphone</h2>
      <p class="big">{PHONE_H}</p>
      <p class="muted">Lundi – samedi, 8 h – 19 h</p>
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
      <h2>Toulouse et 40 km alentour</h2>
      <p>Nous nous déplaçons à domicile, sur votre lieu de travail ou sur votre parking. Le déplacement est compris dans le tarif à Toulouse et en première couronne ; au-delà, il est précisé dans le devis.</p>
      <p><a class="btn btn-secondary" href="{GBP}" target="_blank" rel="noopener">{ICON["pin"]} Nous trouver sur Google Maps</a></p>
    </div>
    <ul class="zones">{zones}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <p class="eyebrow">Professionnels</p>
    <h2>Artisans, VTC, agences, locations saisonnières</h2>
    <p>Véhicule pro qui doit rester présentable, canapés d'un meublé entre deux locataires, fauteuils d'un cabinet : nous proposons un entretien régulier avec facture. Écrivez-nous avec le nombre de véhicules ou de logements, nous vous répondons avec un tarif adapté.</p>
  </div>
</section>
{cta_band()}
'''
    return h + header("contact.html") + body + footer()

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

    <h2>Données personnelles</h2>
    <p>Ce site ne dépose aucun cookie et n'utilise aucun outil de mesure d'audience. Le formulaire de réservation ne stocke rien sur le site : il prépare un message que vous envoyez vous-même via WhatsApp ou votre messagerie. Les informations transmises (nom, téléphone, adresse d'intervention) servent uniquement à établir le devis et à réaliser la prestation. Elles sont conservées le temps de la relation commerciale et des obligations comptables. Vous pouvez demander leur consultation, rectification ou suppression à l'adresse e-mail ci-dessus.</p>

    <h2>Propriété intellectuelle</h2>
    <p>Le nom, le logo, les textes et les photographies de réalisations sont la propriété de Nadifa Propreté. Certaines illustrations de prestations sont des images génériques utilisées à titre d'exemple.</p>

    <h2>Assurance et responsabilité</h2>
    <p>Les prestations sont réalisées avec des produits et un matériel adaptés aux textiles traités. Un test de tenue de couleur est effectué sur une zone discrète avant tout nettoyage lorsque la matière le justifie.</p>
  </div>
</section>
'''
    return h + header("") + body + footer()

def page_404():
    h = head("Page introuvable | Nadifa Propreté", "Cette page n'existe pas ou plus.", "404.html", extra='<meta name="robots" content="noindex">\n')
    body = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">Erreur 404</p><h1>Cette page n'existe pas</h1><p class="lead">Elle a peut-être été déplacée. Retrouvez nos prestations ou contactez-nous directement.</p>
<div class="hero-actions"><a class="btn btn-primary" href="index.html">Retour à l'accueil</a><a class="btn btn-ghost" href="services.html">Voir les services</a></div></div></section>
'''
    return h + header("") + body + footer()

CSS = r'''
:root{
  --navy:#0b1f33; --navy-2:#122b45; --ink:#13202e; --text:#2b3a4a; --muted:#5f6f80;
  --accent:#0cc0df; --accent-2:#089fb9; --accent-soft:#e3f8fc; --bg:#ffffff; --bg-alt:#f3f8fb;
  --line:#e2e9ef; --radius:16px; --shadow:0 10px 30px rgba(11,31,51,.08);
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
.brand-light{color:#fff}
.brand-light .brand-name span{color:var(--accent)}
.nav ul{list-style:none;margin:0;padding:0;display:flex;gap:1.4rem;align-items:center}
.nav{display:flex;align-items:center;gap:1.4rem}
.nav a:not(.btn){color:var(--ink);text-decoration:none;font-weight:600;padding:.4em 0;border-bottom:2px solid transparent}
.nav a:not(.btn):hover,.nav a[aria-current="page"]{border-bottom-color:var(--accent)}
.btn-nav{padding:.6em 1.1em;font-size:.95rem}
.nav-toggle{display:none;background:none;border:0;width:44px;height:44px;padding:0;cursor:pointer;color:var(--ink);-webkit-appearance:none;appearance:none;border-radius:10px}
.nav-toggle svg{width:28px;height:28px;vertical-align:middle}
.nav-toggle .ico-close{display:none}
.nav-toggle[aria-expanded="true"] .ico-burger{display:none}
.nav-toggle[aria-expanded="true"] .ico-close{display:inline}
@media (max-width:860px){
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
.hero-media img{border-radius:24px;box-shadow:0 25px 60px rgba(11,31,51,.2);aspect-ratio:3/4;object-fit:cover;width:100%}
.hero-media figcaption{position:absolute;left:1rem;bottom:1rem}
.badge{display:inline-flex;align-items:center;gap:.5em;background:rgba(11,31,51,.85);color:#fff;padding:.5em .9em;border-radius:999px;font-size:.85rem;font-weight:600;backdrop-filter:blur(6px)}
@media (max-width:900px){
  .hero{padding:2.2rem 0 2.5rem}
  .hero-grid{grid-template-columns:1fr;gap:2rem}
  .hero-media img{aspect-ratio:4/3}
}

/* sections */
.section{padding:4.5rem 0}
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

/* results */
.result{margin:0;background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.result img{aspect-ratio:4/3;object-fit:cover;width:100%}
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
.price-quote{font-size:.85rem;color:var(--accent-2);background:var(--accent-soft);padding:.35em .7em;border-radius:999px}
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
@media (min-width:861px){.site-footer{margin-bottom:0}}

/* mobile bar */
.mobile-bar{position:fixed;left:0;right:0;bottom:0;display:none;grid-template-columns:1fr 1.4fr;gap:.6rem;padding:.6rem .8rem calc(.6rem + env(safe-area-inset-bottom));background:rgba(255,255,255,.95);backdrop-filter:blur(10px);border-top:1px solid var(--line);z-index:40}
.mobile-bar a{display:inline-flex;align-items:center;justify-content:center;gap:.5em;padding:.8em;border-radius:999px;font-weight:700;text-decoration:none;color:var(--ink);border:2px solid var(--line)}
.mobile-bar .mobile-bar-wa{background:var(--accent);color:#04202a;border-color:var(--accent)}
@media (max-width:860px){.mobile-bar{display:grid}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
'''

JS = r'''
(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
    document.addEventListener('click',function(e){if(!n.contains(e.target)&&!t.contains(e.target)&&n.classList.contains('open')){n.classList.remove('open');t.setAttribute('aria-expanded','false');}});}
  var f=document.getElementById('booking');
  if(!f)return;
  var WA='33647271062', MAIL='contact@nadifaproprete.fr';
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
    for p,f,pr in [("","weekly","1.0"),("services.html","monthly","0.9"),("reservation.html","monthly","0.8"),("contact.html","monthly","0.7")]) + "</urlset>\n"

ASSET_V = hashlib.md5((CSS+JS).encode()).hexdigest()[:8]
pages = {"index.html":page_index(),"services.html":page_services(),"reservation.html":page_reservation(),"contact.html":page_contact(),"mentions-legales.html":page_mentions(),"404.html":page_404()}
for name,content in pages.items():
    open(os.path.join(OUT,name),"w",encoding="utf-8").write(content)
open(os.path.join(OUT,"assets/css/style.css"),"w").write(CSS.strip()+"\n")
open(os.path.join(OUT,"assets/js/main.js"),"w").write(JS.strip()+"\n")
open(os.path.join(OUT,"site.webmanifest"),"w").write(MANIFEST)
open(os.path.join(OUT,"robots.txt"),"w").write(ROBOTS)
open(os.path.join(OUT,"sitemap.xml"),"w").write(SITEMAP)
open(os.path.join(OUT,".nojekyll"),"w").write("")
print("ok", {k:len(v) for k,v in pages.items()})
