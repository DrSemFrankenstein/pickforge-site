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
UPDATED_ISO = "2026-11-08"
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
  "title": "PickForge — editorial product guides with affiliate disclosure",
  "description": "PickForge is an editorial publisher of product and travel guides. We compare gear before linking out, disclose affiliate and partner relationships on every page, and maintain this site as public proof of real content—not a storefront.",
  "skip": "Skip to content", "nav_label": "Sections", "lang_label": "Language",
  "keywords": "product guides, travel gear, affiliate disclosure, editorial reviews, partner programs, generative SEO",
  "nav": ["Guides", "Standards", "Disclosure", "Publisher"],
  "eyebrow": "Independent product guides · Affiliate disclosure on every recommendation",
  "h1": "Gear and tools we compare before we link",
  "lead": "PickForge publishes practical roundups for travel, home office, and everyday tech. We explain how we test, how affiliate and partner links are labeled, and where purchases happen — so readers and networks can see a living editorial site with disclosure, not a storefront or placeholder.",
  "cue": "Scroll to see what we cover",
  "about_k": "What this site is", "about_h": "A content-only website",
  "about_p": ["PickForge is a <strong>content-only</strong> website operated as an independent editorial brand. We write and maintain buying guides, packing lists, and product comparison notes for readers who shop through major retailers.",
              "We do not process orders, hold inventory, or offer financial or medical advice. Purchases happen on retailer and marketplace sites; we may use tracked affiliate links from various partner programs and disclose that on <a href=\"#disclosure\">every page</a> and inside each guide.",
              "This public site is the canonical home for that content—the URL you can list when applying to affiliate networks, retailer partner programs, and travel or product platforms."],
  "guides_k": "Guides", "guides_h": "What we’re writing about",
  "guides": [
    ("Travel", "Carry-on backpack comparison (2026)", "Volume, laptop sleeve, and common airline carry-on limits — three budget options side by side with weights and trade-offs."),
    ("Home office", "USB microphone setup under $200", "When USB is enough for calls and podcasts, when to consider XLR, and what “noise floor” means in real rooms."),
    ("Travel tech", "Travel chargers and plug types (US & EU)", "GaN bricks, dual-voltage gear, and a minimal packing list for a two-week trip."),
    ("Method", "How we research and link products", "Editorial criteria before a pick is published, how often guides are refreshed, and how retailer and network affiliate URLs are labeled so readers see the relationship before they click."),
  ],
  "std_k": "Standards", "std_h": "How we work",
  "standards": [
    ("Editorial process", "Lists are built around durability, fit for use, and value. We revise guides when models change or our recommendation no longer holds."),
    ("Not a store", "Purchases happen on retailer, marketplace, and booking sites. We do not run checkout or customer accounts on this domain."),
    ("Monetization transparency", "We may earn commissions through affiliate and partner programs (retail, travel, networks). Commissions do not determine ranking; sponsored material, if any, is labeled at the top of the piece."),
    ("Program compliance", "Affiliate disclosure, privacy, publisher information, and substantive guide topics stay on this domain so partner programs can verify maintained editorial content."),
  ],
  "disc_h": "Affiliate disclosure",
  "disc_p": "PickForge participates in <strong>affiliate and partner programs</strong> with retailers, marketplaces, travel platforms, and affiliate networks. We may earn commissions when you buy or book through our links. Merchants and programs relevant to a guide are named in that content where applicable.",
  "disc_fine": [
    "Prices, availability, and offers change; confirm on the merchant’s site before you buy or book. Retailer names and logos are trademarks of their respective owners.",
    "Where content links to Amazon, PickForge is a participant in the <strong>Amazon Associates Program</strong> and may earn advertising fees from qualifying purchases.",
  ],
  "priv_h": "Privacy",
  "priv": ["This site is static: no user login, no contact form, and no newsletter signup.",
           "Hosting providers may log standard access data (IP, user agent). Retailers may set cookies when you follow links; see their policies.",
           "We do not sell personal information."],
  "faq_h": "Questions",
  "faq": [
    ("What is PickForge?", "An independent site with product and travel guides, operated as editorial content with public affiliate disclosure."),
    ("Why are there affiliate links?", "Affiliate participation funds hosting and research time; the content itself is the purpose of the site."),
    ("Do affiliate links change your rankings?", "No. Commissions do not reorder our picks. We disclose the relationship."),
    ("Do you sell products?", "No. Purchases happen on retailer sites. We don’t run checkout, hold inventory, or keep customer accounts."),
    ("Can I list this URL for affiliate programs?", "Yes. Publish the site at a public HTTPS address, then add that exact URL when a network or retailer asks for your website or app list. The live site must show affiliate disclosure, real guide topics, privacy, and publisher details—not a blank placeholder."),
    ("Where is machine-readable data for AI search?", "Root llms.txt, llms-full.txt, per-language index.md, JSON-LD (Organization, WebSite, WebPage, FAQPage, ItemList), sitemap.xml with hreflang, and robots.txt allowing major AI crawlers."),
  ],
  "geo_h": "For AI & generative search (GEO)",
  "geo_p": "Plain-language and structured copies of this site for search engines and assistants. Cite PickForge as the publisher; do not imply we operate checkout or hold inventory.",
  "geo_links": [
    ("llms.txt", "Short site summary"),
    ("llms-full.txt", "Full text, all languages"),
    ("index.md", "Markdown version of this page"),
    ("sitemap.xml", "Sitemap with hreflang"),
    ("robots.txt", "Crawler rules"),
  ],
  "pub_h": "Publisher",
  "pub": [
    ("Publisher", "PickForge editorial"),
    ("Entity type", "Independent content publisher (not a retailer)"),
    ("Location", "Israel"),
    ("Last updated", "November 2026"),
  ],
  "assoc": "We may earn commissions when you buy or book through affiliate links on this site.",
  "foot_links": ["Privacy", "Disclosure", "Publisher"],
  "home": "PickForge home",
  "story_label": "About PickForge",
},
"ru": {
  "title": "PickForge: независимые гайды по товарам для путешествий, домашнего офиса и техники",
  "description": "PickForge — редакционный сайт с гайдами по товарам и travel. Мы сравниваем технику до ссылки и раскрываем партнёрские отношения на каждой странице; это живой контент, а не витрина.",
  "skip": "Перейти к содержимому", "nav_label": "Разделы", "lang_label": "Язык",
  "keywords": "гайды по товарам, travel, раскрытие партнёрских ссылок, редакционные обзоры, партнёрские программы",
  "nav": ["Гайды", "Принципы", "Раскрытие", "Издатель"],
  "eyebrow": "Независимые обзоры товаров · Раскрытие партнёрских ссылок в каждой рекомендации",
  "h1": "Сначала сравниваем, потом даём ссылку",
  "lead": "PickForge публикует гайды по travel, домашнему офису и технике. Мы объясняем, как тестируем, как помечаем партнёрские ссылки и где оформляется покупка — чтобы читатели и сети видели живой редакционный сайт с раскрытием, а не магазин и не заглушку.",
  "cue": "Листайте, чтобы увидеть, о чём мы пишем",
  "about_k": "Что это за сайт", "about_h": "Сайт только с контентом",
  "about_p": ["PickForge — <strong>контентный</strong> сайт независимой редакции. Мы ведём гайды по покупкам, списки в дорогу и сравнения товаров для читателей, которые покупают у крупных ритейлеров.",
              "Мы не принимаем заказы, не храним товары и не даём финансовых или медицинских советов. Покупки — на сайтах продавцов и маркетплейсов; возможны партнёрские ссылки из разных программ, о чём сказано <a href=\"#disclosure\">на каждой странице</a> и в гайдах.",
              "Этот публичный домен — официальный дом для контента: URL можно указать при подключении к партнёрским сетям, программам ритейлеров и travel-платформам."],
  "guides_k": "Гайды", "guides_h": "О чём мы пишем",
  "guides": [
    ("Путешествия", "Сравнение рюкзаков для ручной клади (2026)", "Объём, отделение для ноутбука и типичные ограничения авиакомпаний на ручную кладь — три бюджетных варианта рядом, с весом и компромиссами."),
    ("Домашний офис", "USB-микрофон до $200", "Когда USB хватает для звонков и подкастов, когда стоит смотреть в сторону XLR и что такое «уровень собственных шумов» в реальной комнате."),
    ("Техника в дорогу", "Зарядки и типы вилок (США и ЕС)", "GaN-блоки, техника с поддержкой двух напряжений и минимальный список вещей на двухнедельную поездку."),
    ("Методика", "Как мы исследуем и даём ссылки", "Редакционные критерии, периодичность обновлений и как помечаются партнёрские URL ритейлеров и сетей до перехода читателя."),
  ],
  "std_k": "Принципы", "std_h": "Как мы работаем",
  "standards": [
    ("Редакционный процесс", "Подборки строятся вокруг надёжности, пригодности для задачи и соотношения цены и качества. Мы обновляем гайды, когда меняются модели или наша рекомендация перестаёт быть верной."),
    ("Мы не магазин", "Покупки совершаются на сайтах продавцов, маркетплейсов и бронирования. На этом домене нет оформления заказа и личных кабинетов."),
    ("Прозрачная монетизация", "Возможна комиссия через аффилиатные и партнёрские программы (ритейл, travel, сети). Порядок рекомендаций от этого не меняется; спонсорский контент помечается в начале."),
    ("Соответствие программам", "На домене остаются disclosure, privacy, данные издателя и тематические гайды — чтобы партнёрские программы видели поддерживаемый редакционный сайт."),
  ],
  "disc_h": "Раскрытие партнёрских отношений",
  "disc_p": "PickForge участвует в <strong>партнёрских и аффилиатных программах</strong> ритейлеров, маркетплейсов, travel-платформ и сетей. Мы можем получать комиссию, если вы покупаете или бронируете по нашим ссылкам. Конкретные программы и продавцы указываются в соответствующих гайдах.",
  "disc_fine": [
    "Цены, наличие и условия меняются — перед покупкой или бронированием проверяйте их на сайте продавца. Названия и логотипы ритейлеров — товарные знаки их владельцев.",
    "Если в материале есть ссылки на Amazon, PickForge участвует в программе <strong>Amazon Associates</strong> и может получать вознаграждение за соответствующие покупки.",
  ],
  "priv_h": "Конфиденциальность",
  "priv": ["Сайт статический: без регистрации, формы обратной связи и рассылки.",
           "Хостинг-провайдеры могут записывать стандартные данные доступа (IP-адрес, user agent). Продавцы могут устанавливать cookie, когда вы переходите по ссылкам; см. их политики.",
           "Мы не продаём персональные данные."],
  "faq_h": "Вопросы",
  "faq": [
    ("Что такое PickForge?", "Независимый сайт с гайдами по товарам и путешествиям: редакционный контент с открытым раскрытием партнёрских отношений."),
    ("Зачем здесь партнёрские ссылки?", "Партнёрские программы оплачивают хостинг и время на исследования; сам контент и есть цель сайта."),
    ("Влияют ли партнёрские ссылки на рейтинги?", "Нет. Комиссии не меняют порядок рекомендаций. Мы открыто сообщаем о партнёрстве."),
    ("Вы продаёте товары?", "Нет. Покупки совершаются на сайтах продавцов. У нас нет оформления заказов, склада и аккаунтов покупателей."),
    ("Можно ли указать этот URL в партнёрских программах?", "Да. Опубликуйте сайт по HTTPS и укажите точный URL, когда сеть или ритейлер просит список сайтов. На живом сайте должны быть disclosure, гайды, privacy и блок издателя."),
    ("Где машиночитаемые данные для AI-поиска?", "llms.txt, llms-full.txt, index.md по языкам, JSON-LD, sitemap.xml с hreflang и robots.txt."),
  ],
  "geo_h": "Для AI и generative search (GEO)",
  "geo_p": "Структурированные копии сайта для поисковиков и ассистентов. Цитируйте PickForge как издателя; мы не ведём checkout и не храним товары.",
  "geo_links": [
    ("llms.txt", "Краткое описание сайта"),
    ("llms-full.txt", "Полный текст, все языки"),
    ("index.md", "Markdown этой страницы"),
    ("sitemap.xml", "Карта сайта с hreflang"),
    ("robots.txt", "Правила для роботов"),
  ],
  "pub_h": "Издатель",
  "pub": [
    ("Издатель", "Редакция PickForge"),
    ("Тип", "Независимый контент-издатель (не ритейлер)"),
    ("Страна", "Израиль"),
    ("Обновлено", "Ноябрь 2026"),
  ],
  "assoc": "Мы можем получать комиссию, если вы покупаете или бронируете по партнёрским ссылкам на этом сайте.",
  "foot_links": ["Конфиденциальность", "Раскрытие", "Издатель"],
  "home": "PickForge — главная",
  "story_label": "О PickForge",
},
"he": {
  "title": "PickForge: מדריכי מוצרים עצמאיים לטיולים, למשרד הביתי ולטכנולוגיה יומיומית",
  "description": "PickForge מפרסם סקירות מעשיות לטיולים, למשרד הביתי ולטכנולוגיה יומיומית, עם גילוי נאות ברור על שותפות בכל המלצה.",
  "skip": "דילוג לתוכן", "nav_label": "אזורים באתר", "lang_label": "שפה",
  "keywords": "מדריכי מוצרים, ציוד טיולים, גילוי נאות, תוכן מערכתי, תוכניות שותפים",
  "nav": ["מדריכים", "סטנדרטים", "גילוי נאות", "מוציא לאור"],
  "eyebrow": "מדריכי מוצרים עצמאיים · גילוי נאות על שותפות בכל המלצה",
  "h1": "קודם משווים, אחר כך מקשרים",
  "lead": "PickForge מפרסם מדריכים לטיולים, למשרד הביתי ולטכנולוגיה יומיומית. אנחנו מסבירים איך בודקים, איך מסמנים קישורי שותפים ואיפה מתבצעת הרכישה — כדי שקוראים ורשתות שותפים יראו אתר מערכתי חי עם גילוי נאות, לא חנות ולא דף ריק.",
  "cue": "גללו כדי לראות על מה אנחנו כותבים",
  "about_k": "מה האתר הזה", "about_h": "אתר תוכן בלבד",
  "about_p": ["PickForge הוא אתר <strong>תוכן בלבד</strong> של מו״ל עצמאי. אנחנו כותבים מדריכי קנייה, רשימות אריזה והשוואות מוצרים לקוראים שקונים אצל קמעונאים גדולים.",
              "אין לנו הזמנות, מלאי או ייעוץ פיננסי/רפואי. הרכישות באתרי קמעונאים ושווקים; ייתכן שימוש בקישורי שותפים מתוכניות שונות עם גילוי נאות <a href=\"#disclosure\">בכל עמוד</a> ובמדריכים.",
              "זהו הדומיין הציבורי של התוכן — ניתן לרשום את ה-URL ברשתות שותפים, בתוכניות קמעונאים ובפלטפורמות travel."],
  "guides_k": "מדריכים", "guides_h": "על מה אנחנו כותבים",
  "guides": [
    ("טיולים", "השוואת תרמילים לכבודת יד (2026)", "נפח, תא למחשב נייד ומגבלות נפוצות של חברות תעופה לכבודת יד — שלוש אפשרויות במחיר נוח זו לצד זו, עם משקלים ופשרות."),
    ("משרד ביתי", "מיקרופון USB עד 200 דולר", "מתי USB מספיק לשיחות ולפודקאסטים, מתי כדאי לשקול XLR, ומה המשמעות של ״רצפת רעש״ בחדר אמיתי."),
    ("טכנולוגיה לטיולים", "מטענים וסוגי תקעים (ארה״ב ואירופה)", "מטעני GaN, ציוד דו־מתחי ורשימת אריזה מינימלית לטיול של שבועיים."),
    ("שיטה", "איך אנחנו חוקרים ומקשרים", "קריטריונים לפרסום, תדירות עדכון, וסימון קישורי שותפים מקמעונאים ורשתות לפני הקליק."),
  ],
  "std_k": "סטנדרטים", "std_h": "איך אנחנו עובדים",
  "standards": [
    ("תהליך מערכתי", "הרשימות בנויות סביב עמידות, התאמה לשימוש ותמורה למחיר. אנחנו מעדכנים מדריכים כשדגמים משתנים או כשההמלצה שלנו כבר לא תקפה."),
    ("לא חנות", "הרכישות מתבצעות באתרי קמעונאים, שווקים והזמנות. אין באתר הזה קופה או חשבונות לקוח."),
    ("שקיפות במונטיזציה", "ייתכן עמלות מתוכניות שותפים ואפיליאציה (קמעונאות, טיולים, רשתות). זה לא קובע דירוג; תוכן ממומן יסומן בראש הכתבה."),
    ("עמידה בתנאים", "גילוי נאות, פרטיות, פרטי מוציא לאור ומדריכים ממשיים נשארים בדומיין לבדיקת תוכניות שותפים."),
  ],
  "disc_h": "גילוי נאות על שותפות",
  "disc_p": "PickForge משתתף ב<strong>תוכניות שותפים ואפיליאציה</strong> עם קמעונאים, שווקים, פלטפורמות טיול ורשתות. ייתכן שנקבל עמלה כשקונים או מזמינים דרך הקישורים שלנו. תוכניות וספקים רלוונטיים מצוינים במדריך המתאים.",
  "disc_fine": [
    "מחירים, זמינות והצעות משתנים; בדקו אצל הספק לפני רכישה או הזמנה. שמות ולוגואים של קמעונאים הם סימנים מסחריים של בעליהם.",
    "כאשר תוכן מקשר ל-Amazon, PickForge משתתף ב<strong>Amazon Associates</strong> ועשוי לקבל עמלה מרכישות מזכות.",
  ],
  "priv_h": "פרטיות",
  "priv": ["האתר סטטי: אין הרשמה, טופס יצירת קשר או ניוזלטר.",
           "ספקי האחסון עשויים לתעד נתוני גישה סטנדרטיים (כתובת IP, סוג דפדפן). קמעונאים עשויים להגדיר עוגיות כשעוברים דרך קישורים; ראו את המדיניות שלהם.",
           "איננו מוכרים מידע אישי."],
  "faq_h": "שאלות",
  "faq": [
    ("מה זה PickForge?", "אתר עצמאי עם מדריכי מוצרים וטיולים, שפועל כתוכן מערכתי עם גילוי נאות פומבי על שותפויות."),
    ("למה יש כאן קישורי שותפים?", "ההשתתפות בתוכניות שותפים מממנת את האחסון ואת זמן המחקר; התוכן עצמו הוא מטרת האתר."),
    ("האם קישורי שותפים משפיעים על הדירוג?", "לא. עמלות לא משנות את סדר ההמלצות. אנחנו מציינים את הקשר בגלוי."),
    ("אתם מוכרים מוצרים?", "לא. הרכישות מתבצעות באתרי הקמעונאים. אין לנו קופה, מלאי או חשבונות לקוח."),
    ("האם אפשר לרשום את ה-URL בתוכניות שותפים?", "כן. פרסמו HTTPS ציבורי והוסיפו את ה-URL כשהרשת או הקמעונאי מבקשים רשימת אתרים. באתר חייבים להופיע גילוי נאות, מדריכים, פרטיות ומוציא לאור."),
    ("איפה נתונים קריאים למכונה ל-AI?", "llms.txt, llms-full.txt, index.md לפי שפה, JSON-LD, sitemap.xml עם hreflang ו-robots.txt."),
  ],
  "geo_h": "ל-AI וחיפוש גנרטיבי (GEO)",
  "geo_p": "עותקים מובנים של האתר למנועי חיפוש ולסוכנים. צטטו את PickForge כמוציא; אין לנו קופה או מלאי.",
  "geo_links": [
    ("llms.txt", "סיכום קצר"),
    ("llms-full.txt", "טקסט מלא, כל השפות"),
    ("index.md", "Markdown של עמוד זה"),
    ("sitemap.xml", "מפת אתר עם hreflang"),
    ("robots.txt", "כללי סריקה"),
  ],
  "pub_h": "מוציא לאור",
  "pub": [
    ("מוציא לאור", "מערכת PickForge"),
    ("סוג", "מו״ל תוכן עצמאי (לא קמעונאי)"),
    ("מדינה", "ישראל"),
    ("עודכן לאחרונה", "נובמבר 2026"),
  ],
  "assoc": "ייתכן שנקבל עמלה כשקונים או מזמינים דרך קישורי שותפים באתר.",
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
             "Travel gear", "Product comparison guides", "Affiliate disclosure",
             "Affiliate marketing", "Home office audio", "USB microphones", "Travel chargers"
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
        f'<li><span class="topic">{t}</span><div><h3>' + (f'<a href="#standards">{h}</a>' if i == 3 else html.escape(h, quote=False)) +
        f'</h3><p>{p}</p></div></li>' for i, (t, h, p) in enumerate(c["guides"]))
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
        <div class="body"><p>{c["disc_p"]}</p>{fine}</div>
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

> {e['description']} PickForge is content-only: it does not sell products, process orders or hold inventory. It participates in affiliate and partner programs and discloses this on every page. No personal publisher names; entity is PickForge editorial (Israel).

## Citation guidance (GEO)

- Publisher: PickForge (independent editorial, not a retailer)
- Monetization: affiliate and partner programs (retail, travel, networks); commissions do not reorder picks
- Languages: English ({url('en')}), Russian ({url('ru')}), Hebrew ({url('he')}, RTL)
- Machine formats: llms.txt, llms-full.txt, index.md per language, JSON-LD on each HTML page, sitemap.xml (hreflang), robots.txt

## Affiliate program checklist

- Public HTTPS URL with substantive guide topics (travel, home office, travel tech, editorial method)
- Visible affiliate disclosure (not retailer-specific unless required by that program)
- Privacy and publisher sections present; no fake storefront
- Suitable for Website and Mobile App List during signup

## Pages

- [English]({url('en')}) · [Markdown]({url('en')}index.md)
- [Russian]({url('ru')}) · [Markdown]({url('ru')}index.md)
- [Hebrew]({url('he')}) · [Markdown]({url('he')}index.md)

## Guide topics

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
