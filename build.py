#!/usr/bin/env python3
"""
PickForge static site generator.
All page text lives in CONTENT below (EN / RU / HE). Edit it, then run:

    python3 build.py https://your-user.github.io/pickforge/

The URL argument becomes the canonical base for every page, hreflang link,
sitemap entry, robots.txt, llms.txt and JSON-LD block. Without an argument,
the placeholder https://pickforge.example/ is used.
"""
import json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_ORIGIN = "https://drsemfrankenstein.github.io/pickforge-site"
SITE_URL = (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ORIGIN + "/").rstrip("/") + "/"
UPDATED_ISO = "2026-11-11"
AMAZON_EXACT = "As an Amazon Associate I earn from qualifying purchases."
ASSOCIATES_ID = "pickforge-20"
LANGS = ["en", "ru", "he"]
PATHS = {"en": "", "ru": "ru/", "he": "he/"}
NATIVE = {"en": "English", "ru": "Русский", "he": "עברית"}
SHORT = {"en": "EN", "ru": "RU", "he": "HE"}
OG_LOCALE = {"en": "en_US", "ru": "ru_RU", "he": "he_IL"}
FONTS = {
    "en": "family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400",
    "ru": "family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,800&family=Rubik:wght@400..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400",
    "he": "family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,800&family=Rubik:wght@400..800&family=Frank+Ruhl+Libre:wght@400;600",
}
CONTENT = {
"en": {
  "title": "PickForge: product search and affiliate links for AI assistants",
  "description": "PickForge is developing a tool that lets AI assistants search products and return affiliate links. This page describes the service and its affiliate disclosures. PickForge does not sell products.",
  "skip": "Skip to content", "nav_label": "Sections", "lang_label": "Language",
  "keywords": "PickForge, affiliate disclosure, AI assistant tool, product search, partner programs",
  "nav": ["Service", "How we work", "Disclosure", "Publisher"],
  "eyebrow": "Product search for AI assistants · Affiliate disclosure on every page",
  "h1": "Product search with affiliate links, for AI assistants",
  "lead": "PickForge is building a tool that helps an AI assistant find a product the user asks about and return a link. Some links carry our affiliate tracking ID. The tool runs on our server; this page describes it and explains the affiliate relationships.",
  "cue": "Scroll for details",
  "about_k": "What this site is", "about_h": "An information page for a service in development",
  "about_p": ["PickForge is an independent project. This page describes the service, how we handle affiliate links, and who runs it. It is not a store and does not sell products.",
              "The service is in development. Search and link generation run on PickForge’s own server, not on this page. Purchases happen on the merchant’s site, where prices and availability are shown.",
              "We do not process orders, hold inventory, or give financial or medical advice."],
  "guides_k": "Service", "guides_h": "What the tool does",
  "guides": [
    ("Search", "Search by request", "A user asks an AI assistant for a product type or a budget. The assistant calls the tool, which searches partner catalogues for matching items."),
    ("Links", "Affiliate links, labeled", "Links to merchants can carry our partner tracking ID. Where a link can earn a commission, it is labeled next to the link."),
    ("Scope", "Not a store", "Checkout, payment, and accounts happen on the merchant’s site. The tool does not take orders or payments."),
  ],
  "std_k": "How we work", "std_h": "Principles",
  "standards": [
    ("Data", "A search request is used only to answer that request. We do not sell personal data."),
    ("Commissions", "A commission does not change the order of search results. A link that can earn a commission is labeled."),
    ("No hands-on claims", "We do not claim product tests. Product information comes from merchant and partner data."),
    ("Updates", "We update this page when the service, partner programs, or disclosures change."),
  ],
  "disc_h": "Affiliate disclosure",
  "disc_p": "PickForge participates in affiliate and partner programs, including the <strong>Amazon Associates Program</strong> and other partner programs. If you buy a product through a link the tool returns, we may earn a commission. A partner link is labeled as one wherever the tool shows it.",
  "disc_fine": [
    "Prices, availability, and offers change. Confirm them on the merchant’s site before you buy. Retailer names and logos are trademarks of their owners.",
    "Amazon does not sponsor or endorse PickForge. The sentence below is the program disclosure.",
  ],
  "priv_h": "Privacy",
  "priv": ["This page is static: no user login, no contact form, and no newsletter signup.",
           "The service receives search requests to return results and does not use them for other purposes. Hosting providers may log standard access data (IP, user agent). Merchants may set cookies when you follow links; see their policies.",
           "We do not sell personal information."],
  "faq_h": "Questions",
  "faq": [
    ("What is PickForge?", "An independent project building a tool that lets AI assistants search products and return affiliate links. The service is in development."),
    ("Do you sell products?", "No. Purchases happen on merchant sites. We do not run checkout, hold inventory, or keep customer accounts."),
    ("Do affiliate links change the results?", "No. A commission does not change the order of search results."),
    ("Are affiliate links labeled?", "Yes. A link that can earn a commission is labeled as a partner link."),
    ("How do I contact the publisher?", "This page has no contact form."),
  ],
  "geo_h": "For AI & generative search (GEO)",
  "geo_p": "Structured copies of this page for search engines and assistants. Cite PickForge as the publisher. We do not run checkout or hold inventory.",
  "geo_links": [
    ("llms.txt", "Short site summary"),
    ("llms-full.txt", "Full text, all languages"),
    ("index.md", "Markdown version of this page"),
    ("sitemap.xml", "Sitemap with hreflang"),
    ("robots.txt", "Crawler rules"),
  ],
  "pub_h": "Publisher",
  "pub": [
    ("Publisher", "PickForge"),
    ("Entity type", "Independent project (not a retailer)"),
    ("Location", "Israel"),
    ("Last updated", "11 November 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["Privacy", "Disclosure", "Publisher"],
  "home": "PickForge home",
  "story_label": "About PickForge",
},
"ru": {
  "title": "PickForge: поиск товаров и партнёрские ссылки для ИИ-ассистентов",
  "description": "PickForge разрабатывает инструмент, с помощью которого ИИ-ассистент ищет товары и возвращает партнёрские ссылки. Эта страница описывает сервис и раскрытие партнёрских отношений. PickForge ничего не продаёт.",
  "skip": "Перейти к содержимому", "nav_label": "Разделы", "lang_label": "Язык",
  "keywords": "PickForge, раскрытие партнёрских ссылок, инструмент для ИИ-ассистентов, поиск товаров, партнёрские программы",
  "nav": ["Сервис", "Как мы работаем", "Раскрытие", "Издатель"],
  "eyebrow": "Поиск товаров для ИИ-ассистентов · Раскрытие партнёрских отношений на каждой странице",
  "h1": "Поиск товаров с партнёрскими ссылками для ИИ-ассистентов",
  "lead": "PickForge разрабатывает инструмент, который помогает ИИ-ассистенту найти товар по запросу пользователя и вернуть ссылку. Часть ссылок содержит наш партнёрский идентификатор. Инструмент работает на нашем сервере; эта страница его описывает и объясняет партнёрские отношения.",
  "cue": "Листайте, чтобы увидеть подробности",
  "about_k": "Что это за сайт", "about_h": "Информационная страница сервиса в разработке",
  "about_p": ["PickForge — независимый проект. Эта страница описывает сервис, то, как мы работаем с партнёрскими ссылками, и кто за ним стоит. Это не магазин, и мы ничего не продаём.",
              "Сервис в разработке. Поиск и генерация ссылок работают на сервере PickForge, а не на этой странице. Покупки совершаются на сайте продавца, где видны цены и наличие.",
              "Мы не принимаем заказы, не храним товары и не даём финансовых или медицинских советов."],
  "guides_k": "Сервис", "guides_h": "Что делает инструмент",
  "guides": [
    ("Поиск", "Поиск по запросу", "Пользователь просит ИИ-ассистента подобрать тип товара или бюджет. Ассистент вызывает инструмент, который ищет подходящие позиции в партнёрских каталогах."),
    ("Ссылки", "Партнёрские ссылки с пометкой", "Ссылки на продавцов могут содержать наш партнёрский идентификатор. Если ссылка может принести комиссию, это указано рядом с ней."),
    ("Границы", "Не магазин", "Оформление заказа, оплата и аккаунты происходят на сайте продавца. Инструмент не принимает заказы и платежи."),
  ],
  "std_k": "Как мы работаем", "std_h": "Принципы",
  "standards": [
    ("Данные", "Поисковый запрос используется только для ответа на него. Мы не продаём персональные данные."),
    ("Комиссии", "Комиссия не меняет порядок результатов поиска. Ссылка, которая может принести комиссию, помечена."),
    ("Без заявлений о тестах", "Мы не заявляем о ручных тестах товаров. Информация о товарах берётся из данных продавцов и партнёрских программ."),
    ("Обновления", "Мы обновляем эту страницу, когда меняются сервис, партнёрские программы или раскрытие."),
  ],
  "disc_h": "Раскрытие партнёрских отношений",
  "disc_p": "PickForge участвует в партнёрских программах, включая <strong>Amazon Associates</strong> и другие партнёрские программы. Если вы купите товар по ссылке, которую вернул инструмент, мы можем получить комиссию. Партнёрская ссылка помечается как таковая там, где инструмент её показывает.",
  "disc_fine": [
    "Цены, наличие и условия меняются. Перед покупкой проверьте их на сайте продавца. Названия и логотипы — товарные знаки владельцев.",
    "Amazon не спонсирует и не поддерживает PickForge. Ниже — обязательная формулировка программы на английском.",
  ],
  "priv_h": "Конфиденциальность",
  "priv": ["Эта страница статическая: без регистрации, формы обратной связи и рассылки.",
           "Сервис получает поисковые запросы, чтобы вернуть результаты, и не использует их для других целей. Хостинг-провайдеры могут записывать стандартные данные доступа (IP-адрес, user agent). Продавцы могут устанавливать cookie, когда вы переходите по ссылкам; см. их политики.",
           "Мы не продаём персональные данные."],
  "faq_h": "Вопросы",
  "faq": [
    ("Что такое PickForge?", "Независимый проект: инструмент, с помощью которого ИИ-ассистенты ищут товары и возвращают партнёрские ссылки. Сервис в разработке."),
    ("Вы продаёте товары?", "Нет. Покупки совершаются на сайтах продавцов. Мы не ведём оформление заказов, не храним товары и не ведём аккаунты покупателей."),
    ("Влияют ли комиссии на результаты?", "Нет. Комиссия не меняет порядок результатов поиска."),
    ("Помечены ли партнёрские ссылки?", "Да. Ссылка, которая может принести комиссию, помечена как партнёрская."),
    ("Как связаться с издателем?", "На этой странице нет формы обратной связи."),
  ],
  "geo_h": "Для AI и generative search (GEO)",
  "geo_p": "Структурированные копии этой страницы для поисковиков и ассистентов. Цитируйте PickForge как издателя. Мы не ведём оформление заказов и не храним товары.",
  "geo_links": [
    ("llms.txt", "Краткое описание сайта"),
    ("llms-full.txt", "Полный текст, все языки"),
    ("index.md", "Markdown этой страницы"),
    ("sitemap.xml", "Карта сайта с hreflang"),
    ("robots.txt", "Правила для роботов"),
  ],
  "pub_h": "Издатель",
  "pub": [
    ("Издатель", "PickForge"),
    ("Тип", "Независимый проект (не ритейлер)"),
    ("Страна", "Израиль"),
    ("Обновлено", "11 ноября 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["Конфиденциальность", "Раскрытие", "Издатель"],
  "home": "PickForge — главная",
  "story_label": "О PickForge",
},
"he": {
  "title": "PickForge: חיפוש מוצרים וקישורי שותפים לעוזרי AI",
  "description": "PickForge מפתח כלי שמאפשר לעוזר AI לחפש מוצרים ולהחזיר קישורי שותפים. עמוד זה מתאר את השירות ואת הגילוי על השותפויות. PickForge לא מוכר מוצרים.",
  "skip": "דילוג לתוכן", "nav_label": "אזורים באתר", "lang_label": "שפה",
  "keywords": "PickForge, גילוי נאות על שותפים, כלי לעוזרי AI, חיפוש מוצרים, תוכניות שותפים",
  "nav": ["השירות", "איך אנחנו עובדים", "גילוי נאות", "מוציא לאור"],
  "eyebrow": "חיפוש מוצרים לעוזרי AI · גילוי נאות על שותפות בכל עמוד",
  "h1": "חיפוש מוצרים עם קישורי שותפים, לעוזרי AI",
  "lead": "PickForge בונה כלי שעוזר לעוזר AI למצוא מוצר לפי בקשת המשתמש ולהחזיר קישור. חלק מהקישורים כוללים את מזהה השותפים שלנו. הכלי פועל על השרת שלנו; עמוד זה מתאר אותו ומסביר את קשרי השותפות.",
  "cue": "גללו לפרטים",
  "about_k": "מה האתר הזה", "about_h": "עמוד מידע לשירות בפיתוח",
  "about_p": ["PickForge הוא פרויקט עצמאי. עמוד זה מתאר את השירות, איך אנחנו עובדים עם קישורי שותפים ומי עומד מאחוריו. זו לא חנות, ואיננו מוכרים מוצרים.",
              "השירות בפיתוח. החיפוש ויצירת הקישורים פועלים על השרת של PickForge, לא בעמוד הזה. רכישות מתבצעות באתר הסוחר, שם מוצגים מחירים וזמינות.",
              "איננו מקבלים הזמנות, לא שומרים מלאי ולא נותנים ייעוץ פיננסי או רפואי."],
  "guides_k": "השירות", "guides_h": "מה הכלי עושה",
  "guides": [
    ("חיפוש", "חיפוש לפי בקשה", "המשתמש מבקש מעוזר AI סוג מוצר או תקציב. העוזר מפעיל את הכלי, שמחפש פריטים מתאימים בקטלוגים של שותפים."),
    ("קישורים", "קישורי שותפים עם סימון", "קישורים לסוחרים יכולים לכלול את מזהה השותפים שלנו. כשקישור עשוי להניב עמלה, זה מצוין לידו."),
    ("גבולות", "לא חנות", "הזמנה, תשלום וחשבונות מתבצעים באתר הסוחר. הכלי לא מקבל הזמנות ולא תשלומים."),
  ],
  "std_k": "איך אנחנו עובדים", "std_h": "עקרונות",
  "standards": [
    ("נתונים", "בקשת חיפוש משמשת רק כדי לענות עליה. איננו מוכרים מידע אישי."),
    ("עמלות", "עמלה לא משנה את סדר תוצאות החיפוש. קישור שעשוי להניב עמלה מסומן."),
    ("בלי טענות לבדיקה", "איננו טוענים לבדיקות ידניות של מוצרים. המידע על מוצרים מגיע מנתוני הסוחרים והתוכניות."),
    ("עדכונים", "מעדכנים את העמוד כשהשירות, תוכניות השותפים או הגילוי משתנים."),
  ],
  "disc_h": "גילוי נאות על שותפות",
  "disc_p": "PickForge משתתף בתוכניות שותפים, כולל <strong>Amazon Associates</strong> ותוכניות שותפים נוספות. אם תרכשו מוצר דרך קישור שהכלי החזיר, ייתכן שנקבל עמלה. קישור שותפים מסומן ככזה במקום שבו הכלי מציג אותו.",
  "disc_fine": [
    "מחירים, זמינות והצעות משתנים. אשרו אותם באתר הסוחר לפני קנייה. שמות ולוגואים הם סימנים מסחריים של בעליהם.",
    "Amazon לא נותנת חסות ל-PickForge ולא תומכת בו. המשפט למטה הוא נוסח הגילוי הנדרש, באנגלית.",
  ],
  "priv_h": "פרטיות",
  "priv": ["העמוד סטטי: אין הרשמה, טופס יצירת קשר או ניוזלטר.",
           "השירות מקבל בקשות חיפוש כדי להחזיר תוצאות, ולא משתמש בהן למטרות אחרות. ספקי אחסון עשויים לתעד נתוני גישה סטנדרטיים (כתובת IP, סוג דפדפן). סוחרים עשויים להגדיר עוגיות כשעוברים דרך קישורים; ראו את המדיניות שלהם.",
           "איננו מוכרים מידע אישי."],
  "faq_h": "שאלות",
  "faq": [
    ("מה זה PickForge?", "פרויקט עצמאי: כלי שמאפשר לעוזרי AI לחפש מוצרים ולהחזיר קישורי שותפים. השירות בפיתוח."),
    ("אתם מוכרים מוצרים?", "לא. רכישות מתבצעות באתרי הסוחרים. איננו מנהלים קופה, לא שומרים מלאי ולא מנהלים חשבונות לקוח."),
    ("האם עמלות משנות את התוצאות?", "לא. עמלה לא משנה את סדר תוצאות החיפוש."),
    ("האם קישורי השותפים מסומנים?", "כן. קישור שעשוי להניב עמלה מסומן כקישור שותפים."),
    ("איך יוצרים קשר עם המוציא לאור?", "בעמוד זה אין טופס יצירת קשר."),
  ],
  "geo_h": "ל-AI וחיפוש גנרטיבי (GEO)",
  "geo_p": "עותקים מובנים של העמוד הזה למנועי חיפוש ולעוזרים. צטטו את PickForge כמוציא. איננו מנהלים קופה ואיננו שומרים מלאי.",
  "geo_links": [
    ("llms.txt", "סיכום קצר"),
    ("llms-full.txt", "טקסט מלא, כל השפות"),
    ("index.md", "Markdown של עמוד זה"),
    ("sitemap.xml", "מפת אתר עם hreflang"),
    ("robots.txt", "כללי סריקה"),
  ],
  "pub_h": "מוציא לאור",
  "pub": [
    ("מוציא לאור", "PickForge"),
    ("סוג", "פרויקט עצמאי (לא קמעונאי)"),
    ("מדינה", "ישראל"),
    ("עודכן לאחרונה", "11 בנובמבר 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["פרטיות", "גילוי נאות", "מוציא לאור"],
  "home": "PickForge — דף הבית",
  "story_label": "אודות PickForge",
},
}

def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))

def url(lang):
    return SITE_URL + PATHS[lang]

def lang_href(from_lang, to_lang):
    """File-friendly links (file:// and static hosts without directory index)."""
    if from_lang == to_lang:
        return "index.html"
    if from_lang == "en":
        return f"{PATHS[to_lang]}index.html" if PATHS[to_lang] else "index.html"
    if to_lang == "en":
        return "../index.html"
    return f"../{PATHS[to_lang]}index.html"

def jsonld(lang, c):
    org = {"@type": "Organization", "@id": SITE_URL + "#org", "name": "PickForge",
           "url": SITE_URL, "logo": SITE_URL + "assets/icon-512.png",
           "description": CONTENT["en"]["description"],
           "location": {"@type": "Place", "address": {"@type": "PostalAddress", "addressCountry": "IL"}},
           "knowsAbout": [
             "AI assistant tools", "Product search", "Affiliate disclosure", "Partner programs"
           ]}
    site = {"@type": "WebSite", "@id": SITE_URL + "#website", "name": "PickForge", "url": SITE_URL,
            "inLanguage": LANGS, "publisher": {"@id": SITE_URL + "#org"},
            "potentialAction": {"@type": "ReadAction", "target": url(lang)}}
    page = {"@type": "WebPage", "@id": url(lang) + "#webpage", "url": url(lang), "name": c["title"],
            "description": c["description"], "inLanguage": lang, "isPartOf": {"@id": SITE_URL + "#website"},
            "publisher": {"@id": SITE_URL + "#org"}, "dateModified": UPDATED_ISO,
            "primaryImageOfPage": SITE_URL + "assets/og.jpg",
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".lead", "#disc-h", ".eyebrow"]},
            "about": [{"@type": "Thing", "name": g[1]} for g in c["guides"]]}
    guides = {"@type": "ItemList", "@id": url(lang) + "#guides", "name": c["guides_h"],
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": g[1], "description": g[2]}
                                 for i, g in enumerate(c["guides"])]}
    breadcrumb = {"@type": "BreadcrumbList", "@id": url(lang) + "#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "PickForge", "item": url(lang)},
                    {"@type": "ListItem", "position": 2, "name": c["guides_h"], "item": url(lang) + "#guides"},
                ]}
    faq = {"@type": "FAQPage", "@id": url(lang) + "#faq", "inLanguage": lang,
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in c["faq"]]}
    return json.dumps({"@context": "https://schema.org", "@graph": [org, site, page, guides, breadcrumb, faq]},
                      ensure_ascii=False, indent=2)

def page(lang):
    c = CONTENT[lang]
    rel = "" if lang == "en" else "../"
    d = "rtl" if lang == "he" else "ltr"
    alt = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{url(l)}">' for l in LANGS)
    alt += f'\n<link rel="alternate" hreflang="x-default" href="{url("en")}">'
    og_alt = "\n".join(f'<meta property="og:locale:alternate" content="{OG_LOCALE[l]}">' for l in LANGS if l != lang)
    langs = "".join(
        f'<a href="{lang_href(lang, l)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else "") +
        f' title="{NATIVE[l]}">{SHORT[l]}</a>' for l in LANGS)
    n = c["nav"]
    guides = "\n".join(
        f'<li><span class="topic">{html.escape(t)}</span><div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div></li>'
        for t, h, p in c["guides"])
    stds = "\n".join(f'<div class="standard"><h3>{h}</h3><p>{p}</p></div>' for h, p in c["standards"])
    faq = "\n".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in c["faq"])
    pub = "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in c["pub"])
    priv = "".join(f"<p>{p}</p>" for p in c["priv"])
    fine = "".join(f'<p class="fine">{p}</p>' for p in c["disc_fine"])
    assoc = f'<span>{c["assoc"]}</span>'
    fl = c["foot_links"]
    return f"""<!doctype html>
<html lang="{lang}" dir="{d}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{c["title"]}</title>
<meta name="description" content="{c["description"]}">
<meta name="keywords" content="{c["keywords"]}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="alternate" type="text/plain" href="{rel}llms.txt" title="LLM site summary">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#CFAE87">
<link rel="canonical" href="{url(lang)}">
{alt}
<link rel="alternate" type="text/markdown" href="{rel}{PATHS[lang]}index.md" title="Markdown version">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{rel}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{rel}assets/apple-touch-icon.png">
<link rel="manifest" href="{rel}site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="PickForge">
<meta property="og:title" content="{c["title"]}">
<meta property="og:description" content="{c["description"]}">
<meta property="og:url" content="{url(lang)}">
<meta property="og:image" content="{SITE_URL}assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
{og_alt}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{c["title"]}">
<meta name="twitter:description" content="{c["description"]}">
<meta name="twitter:image" content="{SITE_URL}assets/og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS[lang]}&display=swap" rel="stylesheet">
<link rel="preload" href="{rel}assets/sprite.webp" as="image" type="image/webp">
<link rel="stylesheet" href="{rel}assets/site.css">
<script type="application/ld+json">
{jsonld(lang, c)}
</script>
</head>
<body>
<a class="skip" href="#main">{c["skip"]}</a>

<header class="bar" id="bar">
  <a class="brand" href="#top" aria-label="{c["home"]}" dir="ltr">Pick<span>Forge</span></a>
  <div class="bar-right">
    <nav aria-label="{c["nav_label"]}">
      <a href="#guides">{n[0]}</a>
      <a href="#standards">{n[1]}</a>
      <a class="keep" href="#disclosure">{n[2]}</a>
      <a href="#publisher">{n[3]}</a>
    </nav>
    <div class="langs" role="group" aria-label="{c["lang_label"]}">{langs}</div>
  </div>
</header>

<main id="main">
  <section class="story" id="story" aria-label="{c["story_label"]}">
    <div class="stage" aria-hidden="true"><div class="sprite" id="sprite"></div></div>
    <div class="chapters">
      <div class="chapter hero" id="top">
        <div class="panel">
          <p class="eyebrow">{c["eyebrow"]}</p>
          <h1>{c["h1"]}</h1>
          <p class="lead">{c["lead"]}</p>
          <p class="notice">{AMAZON_EXACT}</p>
          <p class="cue">{c["cue"]}</p>
        </div>
      </div>
      <div class="chapter" id="about">
        <div class="panel">
          <p class="kicker">{c["about_k"]}</p>
          <h2>{c["about_h"]}</h2>
          {"".join(f'<p class="plain">{p}</p>' for p in c["about_p"])}
        </div>
      </div>
      <div class="chapter" id="guides">
        <div class="panel">
          <p class="kicker">{c["guides_k"]}</p>
          <h2>{c["guides_h"]}</h2>
          <ul class="guides">
{guides}
          </ul>
        </div>
      </div>
      <div class="chapter" id="standards">
        <div class="panel">
          <p class="kicker">{c["std_k"]}</p>
          <h2>{c["std_h"]}</h2>
          <div class="standards">
{stds}
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="paper">
    <div class="paper-inner">
      <section class="disclosure" id="disclosure" aria-labelledby="disc-h">
        <h2 id="disc-h">{c["disc_h"]}</h2>
        <div class="body"><p>{c["disc_p"]}</p>{fine}<p class="amazon-exact">{AMAZON_EXACT}</p></div>
      </section>
      <section class="privacy" id="privacy" aria-labelledby="priv-h">
        <h2 class="sec" id="priv-h">{c["priv_h"]}</h2>
        {priv}
      </section>
      <section class="faq" id="faq" aria-labelledby="faq-h">
        <h2 class="sec" id="faq-h">{c["faq_h"]}</h2>
{faq}
      </section>
      <section class="publisher" id="publisher" aria-labelledby="pub-h">
        <h2 class="sec" id="pub-h">{c["pub_h"]}</h2>
        <dl>{pub}</dl>
      </section>
    </div>
  </div>
</main>

<footer>
  <div class="inner">
    <span dir="ltr">© 2026 PickForge</span>
    <span class="assoc">{assoc}</span>
    <span><a href="#privacy">{fl[0]}</a> · <a href="#disclosure">{fl[1]}</a> · <a href="#publisher">{fl[2]}</a></span>
  </div>
</footer>
<script src="{rel}assets/site.js" defer></script>
</body>
</html>
"""

def markdown(lang):
    c = CONTENT[lang]
    out = [f"# PickForge", "", f"> {c['description']}", "", f"Language: {NATIVE[lang]} · URL: {url(lang)} · Updated: {UPDATED_ISO}", "",
           f"## {strip(c['h1'])}", "", strip(c["lead"]), "",
           f"## {c['about_h']}", ""] + [strip(p) + "\n" for p in c["about_p"]]
    out += [f"## {c['guides_h']}", ""] + [f"- **{h}** ({t}): {p}" for t, h, p in c["guides"]] + [""]
    out += [f"## {c['std_h']}", ""] + [f"- **{h}**: {p}" for h, p in c["standards"]] + [""]
    out += [f"## {c['disc_h']}", "", strip(c["disc_p"]), ""] + [strip(p) + "\n" for p in c["disc_fine"]]
    out += [f"## {c['priv_h']}", ""] + [p + "\n" for p in c["priv"]]
    out += [f"## {c['faq_h']}", ""]
    for q, a in c["faq"]:
        out += [f"### {q}", "", a, ""]
    out += [f"## {c['geo_h']}", "", c["geo_p"], ""] + [f"- {label} (`{path}`)" for path, label in c["geo_links"]] + [""]
    out += [f"## {c['pub_h']}", ""] + [f"- {k}: {strip(v)}" for k, v in c["pub"]] + [""]
    return "\n".join(out)

def llms_txt():
    e = CONTENT["en"]
    faq_block = "\n".join(f"- Q: {q}\n  A: {strip(a)}" for q, a in e["faq"])
    return f"""# PickForge

> {e['description']} PickForge does not sell products, process orders or hold inventory. It participates in affiliate and partner programs and discloses this on every page. Entity is PickForge, an independent project (Israel).

## Citation guidance (GEO)

- Publisher: PickForge (independent project, not a retailer)
- Monetization: affiliate and partner programs; commissions do not change search result order
- Languages: English ({url('en')}), Russian ({url('ru')}), Hebrew ({url('he')}, RTL)
- Machine formats: llms.txt, llms-full.txt, index.md per language, JSON-LD on each HTML page, sitemap.xml (hreflang), robots.txt

## Affiliate disclosure

- Amazon Associates participant.
- Required statement, shown on every page: {AMAZON_EXACT}
- The service does not sell products and does not claim hands-on product tests.

## Pages

- [English]({url('en')}) · [Markdown]({url('en')}index.md)
- [Russian]({url('ru')}) · [Markdown]({url('ru')}index.md)
- [Hebrew]({url('he')}) · [Markdown]({url('he')}index.md)

## Service

""" + "\n".join(f"- {h}: {p}" for t, h, p in e["guides"]) + f"""

## FAQ (English)

{faq_block}

## Policies

- Disclosure: {strip(e['disc_p'])}
- Standards: commissions do not determine ranking
- Privacy: static site, no logins, no sale of personal data

## Files

- {SITE_URL}llms-full.txt
- {SITE_URL}sitemap.xml
- {SITE_URL}robots.txt
"""

def sitemap():
    alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{url(l)}"/>' for l in LANGS) + \
           f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url("en")}"/>'
    urls = "".join(f"""
  <url>
    <loc>{url(l)}</loc>
    <lastmod>{UPDATED_ISO}</lastmod>{alts}
  </url>""" for l in LANGS)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}
</urlset>
"""

def robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended",
            "Bingbot", "DuckAssistBot", "Meta-ExternalAgent", "MistralAI-User", "CCBot", "Amazonbot"]
    blocks = "\n\n".join(f"User-agent: {b}\nAllow: /" for b in bots)
    return f"""# PickForge welcomes search engines and AI assistants.
# Summary for language models: {SITE_URL}llms.txt

User-agent: *
Allow: /

{blocks}

Sitemap: {SITE_URL}sitemap.xml
"""

def manifest():
    return json.dumps({"name": "PickForge", "short_name": "PickForge", "description": CONTENT["en"]["description"],
                       "start_url": "./", "scope": "./", "display": "browser", "background_color": "#CFAE87", "theme_color": "#CFAE87",
                       "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
                                 {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2)

def notfound():
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · PickForge</title><meta name="robots" content="noindex">
<meta name="referrer" content="strict-origin-when-cross-origin">
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#CFAE87;color:#2A1C12;font:400 1.1rem/1.6 Georgia,serif;padding:2rem}}
h1{{font:800 2.4rem/1.1 "Helvetica Neue",Arial,sans-serif;margin:0 0 1rem}}a{{color:inherit}}p{{margin:.3rem 0}}</style></head>
<body><main><h1>This page doesn’t exist</h1>
<p><a href="index.html">Go to PickForge (English)</a></p>
<p lang="ru"><a href="ru/index.html">Перейти на PickForge (русский)</a></p>
<p lang="he" dir="rtl"><a href="he/index.html">מעבר ל־PickForge (עברית)</a></p></main></body></html>
"""

# Inline JSON-LD only; site.js is external. Google Fonts loaded from gstatic.
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'none'; "
    "object-src 'none'; "
    "upgrade-insecure-requests"
)

def security_headers():
    return f"""/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-site
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: {CSP}

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=600, must-revalidate

/ru/index.html
  Cache-Control: public, max-age=600, must-revalidate

/he/index.html
  Cache-Control: public, max-age=600, must-revalidate
"""

def netlify_redirects():
    return """# Force HTTPS on Netlify
http://*  https://:splat  301!

/*  /404.html  404
"""

if __name__ == "__main__":
    for l in LANGS:
        d = ROOT / PATHS[l]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page(l), encoding="utf-8")
        (d / "index.md").write_text(markdown(l), encoding="utf-8")
    (ROOT / "llms.txt").write_text(llms_txt(), encoding="utf-8")
    (ROOT / "llms-full.txt").write_text("\n\n---\n\n".join(markdown(l) for l in LANGS), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(robots(), encoding="utf-8")
    (ROOT / "site.webmanifest").write_text(manifest(), encoding="utf-8")
    (ROOT / "404.html").write_text(notfound(), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    (ROOT / "_headers").write_text(security_headers(), encoding="utf-8")
    (ROOT / "_redirects").write_text(netlify_redirects(), encoding="utf-8")
    print("Built for", SITE_URL)
