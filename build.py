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
  "title": "PickForge — editorial product guides with affiliate disclosure",
  "description": "PickForge publishes product and travel guides. Comparisons use published specifications and stated limits. Affiliate relationships are disclosed. This site does not sell products.",
  "skip": "Skip to content", "nav_label": "Sections", "lang_label": "Language",
  "keywords": "product guides, travel gear, affiliate disclosure, editorial reviews, partner programs, generative SEO",
  "nav": ["Guides", "Standards", "Disclosure", "Publisher"],
  "eyebrow": "Independent product guides · Affiliate disclosure on every page",
  "h1": "Guides from published specs, not a lab",
  "lead": "PickForge publishes practical roundups for travel, home office, and everyday tech. We compare published specifications, weights, and stated limits. We do not claim hands-on tests. When a guide includes an affiliate link, the relationship is labeled before the link.",
  "cue": "Scroll to see what we cover",
  "about_k": "What this site is", "about_h": "A content-only website",
  "about_p": ["PickForge is a <strong>content-only</strong> website operated as an independent editorial brand. We write and maintain buying guides, packing lists, and product comparison notes for readers who shop through major retailers.",
              "We do not process orders, hold inventory, or offer financial or medical advice. Purchases happen on retailer and marketplace sites; we may use tracked affiliate links from various partner programs and disclose that on <a href=\"#disclosure\">every page</a> and inside each guide.",
              "The guides on this site are the content. A purchase, if you choose to make one, happens on the retailer’s own site."],
  "guides_k": "Guides", "guides_h": "What we’re writing about",
  "articles_h": "The guides",
  "guides": [
    ("Travel", "Carry-on size: what usually fits", "Personal-item fares versus a full carry-on, and which published numbers (liters, laptop sleeve, empty weight) actually predict the sizer."),
    ("Home office", "USB microphone under $200", "When a USB dynamic mic is enough for calls, when XLR is worth it, and what “noise floor” means in an ordinary room."),
    ("Travel tech", "Travel chargers: US and EU plugs", "The three lines to read on a brick — input voltage, USB-C watts, and the physical plug — plus a short packing list."),
    ("Method", "How we research and link", "What a comparison on this site is, what it is not, and how a paid link is labeled."),
  ],
  "std_k": "Standards", "std_h": "How we work",
  "standards": [
    ("Editorial process", "We compare published specifications and stated limits. We do not run a lab. A guide says so when we have not used the item."),
    ("Not a store", "Purchases happen on retailer, marketplace, and booking sites. We do not run checkout or customer accounts on this domain."),
    ("Monetization transparency", "We may earn commissions through affiliate and partner programs. A commission does not change the order of a list. A paid link is labeled next to the link."),
    ("Updates", "We revise a guide when the model line changes or a limit we cited no longer matches the source."),
  ],
  "disc_h": "Affiliate disclosure",
  "disc_p": "PickForge participates in affiliate and partner programs, including the <strong>Amazon Associates Program</strong>. We may earn a commission if you buy through a link on this site. A link that can earn a commission is labeled as a paid link next to that link.",
  "disc_fine": [
    "Prices, availability, and offers change. Confirm them on the merchant’s site before you buy. Retailer names and logos are trademarks of their owners.",
    "Amazon does not sponsor or endorse PickForge. The sentence below is the program disclosure.",
  ],
  "priv_h": "Privacy",
  "priv": ["This site is static: no user login, no contact form, and no newsletter signup.",
           "Hosting providers may log standard access data (IP, user agent). Retailers may set cookies when you follow links; see their policies.",
           "We do not sell personal information."],
  "faq_h": "Questions",
  "faq": [
    ("What is PickForge?", "An independent site with product and travel guides, operated as editorial content with public affiliate disclosure."),
    ("Do you test the products?", "No. Guides compare published specifications and stated limits. If that changes for a specific item, the guide will say we used it."),
    ("Do affiliate links change the order?", "No. A commission does not reorder a list."),
    ("Do you sell products?", "No. Purchases happen on retailer sites. We don’t run checkout, hold inventory, or keep customer accounts."),
    ("Are there product links on this site today?", "Some guides explain what to look for and do not link a specific product yet. When a product link can earn a commission, it is labeled as a paid link."),
    ("How do I contact the publisher?", "This site has no contact form and no newsletter. Correspondence about the Associates account stays inside that account."),
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
    ("Last updated", "11 November 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["Privacy", "Disclosure", "Publisher"],
  "home": "PickForge home",
  "story_label": "About PickForge",
},
"ru": {
  "title": "PickForge: независимые гайды по товарам для путешествий, домашнего офиса и техники",
  "description": "PickForge публикует гайды по товарам и путешествиям. Сравнения строятся на опубликованных характеристиках и заявленных ограничениях. Партнёрские отношения раскрыты. Сайт ничего не продаёт.",
  "skip": "Перейти к содержимому", "nav_label": "Разделы", "lang_label": "Язык",
  "keywords": "гайды по товарам, travel, раскрытие партнёрских ссылок, редакционные обзоры, партнёрские программы",
  "nav": ["Гайды", "Принципы", "Раскрытие", "Издатель"],
  "eyebrow": "Независимые гайды · Раскрытие партнёрских отношений на каждой странице",
  "h1": "Гайды по опубликованным характеристикам, не из лаборатории",
  "lead": "PickForge публикует практические подборки для путешествий, домашнего офиса и повседневной техники. Мы сравниваем опубликованные характеристики, вес и заявленные ограничения. Ручные тесты не заявляем. Если в гайде есть партнёрская ссылка, отношение указано до ссылки.",
  "cue": "Листайте, чтобы увидеть, о чём мы пишем",
  "about_k": "Что это за сайт", "about_h": "Сайт только с контентом",
  "about_p": ["PickForge — <strong>контентный</strong> сайт независимой редакции. Мы ведём гайды по покупкам, списки в дорогу и сравнения товаров для читателей, которые покупают у крупных ритейлеров.",
              "Мы не принимаем заказы, не храним товары и не даём финансовых или медицинских советов. Покупки — на сайтах продавцов и маркетплейсов; возможны партнёрские ссылки из разных программ, о чём сказано <a href=\"#disclosure\">на каждой странице</a> и в гайдах.",
              "Гайды на этом сайте и есть контент. Покупка, если вы её совершаете, проходит на сайте продавца."],
  "guides_k": "Гайды", "guides_h": "О чём мы пишем",
  "articles_h": "Тексты гайдов",
  "guides": [
    ("Путешествия", "Размер ручной клади: что обычно проходит", "Тариф только с личной вещью против полноценной ручной клади и какие опубликованные цифры (литры, карман для ноутбука, вес пустого рюкзака) реально предсказывают калибратор."),
    ("Домашний офис", "USB-микрофон до $200", "Когда хватает USB-динамического микрофона для звонков, когда нужен XLR и что значит «уровень шума» в обычной комнате."),
    ("Техника в дорогу", "Зарядки: вилки США и ЕС", "Три строки на блоке — входное напряжение, ватты USB-C и физическая вилка — и короткий список в дорогу."),
    ("Методика", "Как мы собираем гайд и ставим ссылку", "Чем является сравнение на этом сайте, чем не является и как помечается платная ссылка."),
  ],
  "std_k": "Принципы", "std_h": "Как мы работаем",
  "standards": [
    ("Редакционный процесс", "Сравниваем опубликованные характеристики и заявленные ограничения. Лаборатории нет. Если вещь не использовали, гайд так и пишет."),
    ("Мы не магазин", "Покупки совершаются на сайтах продавцов, маркетплейсов и бронирования. На этом домене нет оформления заказа и личных кабинетов."),
    ("Прозрачная монетизация", "Возможна комиссия через партнёрские программы. Комиссия не меняет порядок списка. Платная ссылка помечена рядом со ссылкой."),
    ("Обновления", "Гайд правим, когда меняется линейка моделей или цитируемое ограничение больше не совпадает с источником."),
  ],
  "disc_h": "Раскрытие партнёрских отношений",
  "disc_p": "PickForge участвует в партнёрских программах, включая <strong>Amazon Associates</strong>. Мы можем получить комиссию, если вы покупаете по ссылке на этом сайте. Ссылка, по которой возможна комиссия, помечена как платная рядом с ней.",
  "disc_fine": [
    "Цены, наличие и условия меняются. Перед покупкой проверьте их на сайте продавца. Названия и логотипы — товарные знаки владельцев.",
    "Amazon не спонсирует и не поддерживает PickForge. Ниже — обязательная формулировка программы на английском.",
  ],
  "priv_h": "Конфиденциальность",
  "priv": ["Сайт статический: без регистрации, формы обратной связи и рассылки.",
           "Хостинг-провайдеры могут записывать стандартные данные доступа (IP-адрес, user agent). Продавцы могут устанавливать cookie, когда вы переходите по ссылкам; см. их политики.",
           "Мы не продаём персональные данные."],
  "faq_h": "Вопросы",
  "faq": [
    ("Что такое PickForge?", "Независимый сайт с гайдами по товарам и путешествиям: редакционный контент с открытым раскрытием партнёрских отношений."),
    ("Вы тестируете товары?", "Нет. Гайды сравнивают опубликованные характеристики и заявленные ограничения. Если по конкретной вещи это изменится, гайд напишет, что мы её использовали."),
    ("Влияют ли комиссии на порядок?", "Нет. Комиссия не меняет порядок списка."),
    ("Вы продаёте товары?", "Нет. Покупки совершаются на сайтах продавцов. У нас нет оформления заказов, склада и аккаунтов покупателей."),
    ("Есть ли сейчас ссылки на товары?", "Часть гайдов объясняет, на что смотреть, и пока не ссылается на конкретный товар. Когда ссылка может принести комиссию, она помечена как платная."),
    ("Как связаться с издателем?", "На сайте нет формы и рассылки. Переписка по аккаунту Associates остаётся внутри этого аккаунта."),
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
    ("Обновлено", "11 ноября 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["Конфиденциальность", "Раскрытие", "Издатель"],
  "home": "PickForge — главная",
  "story_label": "О PickForge",
},
"he": {
  "title": "PickForge: מדריכי מוצרים עצמאיים לטיולים, למשרד הביתי ולטכנולוגיה יומיומית",
  "description": "PickForge מפרסם מדריכי מוצרים וטיולים. ההשוואות מבוססות על מפרט שפורסם ומגבלות מוצהרות. קשרי שותפים מפורסמים. האתר לא מוכר מוצרים.",
  "skip": "דילוג לתוכן", "nav_label": "אזורים באתר", "lang_label": "שפה",
  "keywords": "מדריכי מוצרים, ציוד טיולים, גילוי נאות, תוכן מערכתי, תוכניות שותפים",
  "nav": ["מדריכים", "סטנדרטים", "גילוי נאות", "מוציא לאור"],
  "eyebrow": "מדריכים עצמאיים · גילוי נאות על שותפות בכל עמוד",
  "h1": "מדריכים לפי מפרט שפורסם, לא ממעבדה",
  "lead": "PickForge מפרסם סקירות מעשיות לטיולים, למשרד הביתי ולטכנולוגיה יומיומית. אנחנו משווים מפרט שפורסם, משקל ומגבלות מוצהרות. אין כאן טענה לבדיקה בידיים. כשיש קישור שותפים במדריך, הקשר מצוין לפני הקישור.",
  "cue": "גללו כדי לראות על מה אנחנו כותבים",
  "about_k": "מה האתר הזה", "about_h": "אתר תוכן בלבד",
  "about_p": ["PickForge הוא אתר <strong>תוכן בלבד</strong> של מו״ל עצמאי. אנחנו כותבים מדריכי קנייה, רשימות אריזה והשוואות מוצרים לקוראים שקונים אצל קמעונאים גדולים.",
              "אין לנו הזמנות, מלאי או ייעוץ פיננסי/רפואי. הרכישות באתרי קמעונאים ושווקים; ייתכן שימוש בקישורי שותפים מתוכניות שונות עם גילוי נאות <a href=\"#disclosure\">בכל עמוד</a> ובמדריכים.",
              "המדריכים באתר הם התוכן. רכישה, אם תבחרו לבצע אותה, מתבצעת באתר הקמעונאי."],
  "guides_k": "מדריכים", "guides_h": "על מה אנחנו כותבים",
  "articles_h": "המדריכים במלואם",
  "guides": [
    ("טיולים", "גודל כבודת יד: מה בדרך כלל נכנס", "תעריף עם חפץ אישי בלבד מול כבודת יד מלאה, ואילו מספרים שפורסמו (ליטרים, תא למחשב, משקל ריק) באמת מנבאים את תא המדידה."),
    ("משרד ביתי", "מיקרופון USB עד 200 דולר", "מתי מיקרופון דינמי ב-USB מספיק לשיחות, מתי שווה XLR, ומהי ״רצפת רעש״ בחדר רגיל."),
    ("טכנולוגיה לטיולים", "מטענים: תקעי ארה״ב ואירופה", "שלוש שורות על הלבנה — מתח כניסה, וואט ב-USB-C והתקע הפיזי — ורשימת אריזה קצרה."),
    ("שיטה", "איך אנחנו חוקרים ומקשרים", "מהי השוואה באתר הזה, מה היא לא, ואיך מסומן קישור בתשלום."),
  ],
  "std_k": "סטנדרטים", "std_h": "איך אנחנו עובדים",
  "standards": [
    ("תהליך מערכתי", "משווים מפרט שפורסם ומגבלות מוצהרות. אין מעבדה. אם לא השתמשנו בפריט, המדריך אומר זאת."),
    ("לא חנות", "הרכישות מתבצעות באתרי קמעונאים, שווקים והזמנות. אין באתר הזה קופה או חשבונות לקוח."),
    ("שקיפות במונטיזציה", "ייתכן עמלה מתוכניות שותפים. עמלה לא משנה את סדר הרשימה. קישור בתשלום מסומן ליד הקישור."),
    ("עדכונים", "מעדכנים מדריך כשקו הדגמים משתנה או כשמגבלה שציטטנו כבר לא תואמת את המקור."),
  ],
  "disc_h": "גילוי נאות על שותפות",
  "disc_p": "PickForge משתתף בתוכניות שותפים, כולל <strong>Amazon Associates</strong>. ייתכן שנקבל עמלה אם תקנו דרך קישור באתר. קישור שיכול להניב עמלה מסומן כקישור בתשלום לידו.",
  "disc_fine": [
    "מחירים, זמינות והצעות משתנים. אשרו אותם באתר הסוחר לפני קנייה. שמות ולוגואים הם סימנים מסחריים של בעליהם.",
    "Amazon לא נותנת חסות ל-PickForge ולא תומכת בו. המשפט למטה הוא נוסח הגילוי הנדרש, באנגלית.",
  ],
  "priv_h": "פרטיות",
  "priv": ["האתר סטטי: אין הרשמה, טופס יצירת קשר או ניוזלטר.",
           "ספקי האחסון עשויים לתעד נתוני גישה סטנדרטיים (כתובת IP, סוג דפדפן). קמעונאים עשויים להגדיר עוגיות כשעוברים דרך קישורים; ראו את המדיניות שלהם.",
           "איננו מוכרים מידע אישי."],
  "faq_h": "שאלות",
  "faq": [
    ("מה זה PickForge?", "אתר עצמאי עם מדריכי מוצרים וטיולים, שפועל כתוכן מערכתי עם גילוי נאות פומבי על שותפויות."),
    ("אתם בודקים את המוצרים?", "לא. המדריכים משווים מפרט שפורסם ומגבלות מוצהרות. אם זה ישתנה לפריט מסוים, המדריך יציין שהשתמשנו בו."),
    ("האם עמלה משנה את הסדר?", "לא. עמלה לא משנה את סדר הרשימה."),
    ("אתם מוכרים מוצרים?", "לא. הרכישות מתבצעות באתרי הקמעונאים. אין לנו קופה, מלאי או חשבונות לקוח."),
    ("יש כיום קישורים למוצרים?", "חלק מהמדריכים מסבירים על מה להסתכל ועדיין לא מקשרים למוצר מסוים. כשקישור יכול להניב עמלה, הוא מסומן כקישור בתשלום."),
    ("איך יוצרים קשר עם המוציא לאור?", "אין באתר טופס ואין ניוזלטר. התכתבות על חשבון Associates נשארת בתוך החשבון."),
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
    ("עודכן לאחרונה", "11 בנובמבר 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["פרטיות", "גילוי נאות", "מוציא לאור"],
  "home": "PickForge — דף הבית",
  "story_label": "אודות PickForge",
},
}

ARTICLE_IDS = ["carry-on", "usb-mic", "chargers", "method"]
ARTICLES = {
"en": [
  {"id": "carry-on", "kicker": "Travel", "title": "Carry-on size: what usually fits", "paras": [
    "Airlines publish two different limits: a larger carry-on and a smaller personal item. A 40–45 L travel pack often meets a generous carry-on rule and fails a strict sizer, or a fare that allows only a personal item. A 20–28 L pack is the safer size for those fares.",
    "The published numbers that predict the sizer are stated volume, laptop-sleeve length, empty weight, and whether the hip belt and straps tuck away. Brands do not measure liters the same way, so treat the volume as a range. A dangling belt fails a sizer even when the liters look fine.",
    "We have not weighed these bags. Before a trip, read the airline’s current baggage page for your fare. A screenshot in a blog is not the rule.",
  ]},
  {"id": "usb-mic", "kicker": "Home office", "title": "USB microphone under $200", "paras": [
    "For calls and a spoken podcast in an ordinary room, a USB dynamic microphone usually beats a cheap condenser. A condenser hears the room: the fridge, the keyboard, the bare wall. A dynamic mic hears what is close to it.",
    "XLR plus an interface is the better path if you already plan to change microphones later. It costs more than one USB mic and adds a box. Under $200, one USB dynamic mic and a stand is the whole setup.",
    "“Noise floor” here means the hiss and room sound you still hear when you are not talking. A rug, a full bookshelf, and not talking into a bare wall change that more than a second microphone in the same price band. We are not publishing measured decibel figures. Those depend on the room.",
  ]},
  {"id": "chargers", "kicker": "Travel tech", "title": "Travel chargers: US and EU plugs", "paras": [
    "Read three lines on the brick. Input 100–240 V, 50/60 Hz means dual voltage. A US-only 120 V brick is unsafe on 230 V. USB-C Power Delivery watts: a phone is fine around 20 W; a laptop often wants 45–65 W, or whatever the laptop maker prints. The plug face is separate: a GaN brick still needs the pins for the country, or one passive adapter.",
    "Do not stack a voltage converter on a dual-voltage brick. For two weeks, pack one dual-voltage brick, one USB-C cable rated for those watts, and one passive plug adapter if the pins do not match. Leave a second brick at home unless a second person is charging a laptop at the same time.",
  ]},
  {"id": "method", "kicker": "Method", "title": "How we research and link", "paras": [
    "A pick on this site is a comparison of published specifications and stated limits, plus a note on who the item is for. It is not a lab test. If we have not used an item, the guide says so.",
    "A commission does not change the order of a list. If a link can earn a commission, it is labeled as a paid link, and this site states: As an Amazon Associate I earn from qualifying purchases.",
    "We revise a guide when the model line changes or a limit we cited no longer matches the source.",
  ]},
],
"ru": [
  {"id": "carry-on", "kicker": "Путешествия", "title": "Размер ручной клади: что обычно проходит", "paras": [
    "Авиакомпании публикуют два разных лимита: большую ручную кладь и меньшую личную вещь. Рюкзак на 40–45 л часто проходит щедрый лимит ручной клади и не проходит строгий калибратор или тариф, где разрешена только личная вещь. Для таких тарифов спокойнее рюкзак на 20–28 л.",
    "Опубликованные цифры, которые предсказывают калибратор: заявленный объём, длина кармана для ноутбука, вес пустого рюкзака и убираются ли пояс и лямки. Литры бренды меряют по-разному, поэтому объём — это диапазон. Свисающий пояс не проходит калибратор, даже если литры выглядят нормально.",
    "Мы эти рюкзаки не взвешивали. Перед поездкой читайте актуальную страницу багажа вашей авиакомпании для вашего тарифа. Скриншот в блоге — не правило.",
  ]},
  {"id": "usb-mic", "kicker": "Домашний офис", "title": "USB-микрофон до $200", "paras": [
    "Для звонков и разговорного подкаста в обычной комнате USB-динамический микрофон обычно лучше дешёвого конденсаторного. Конденсаторный слышит комнату: холодильник, клавиатуру, голую стену. Динамический слышит то, что близко к нему.",
    "XLR и аудиоинтерфейс лучше, если микрофоны планируете менять. Это дороже одного USB-микрофона и добавляет коробку. До $200 весь комплект — один USB-динамический микрофон и стойка.",
    "«Уровень шума» здесь — шипение и звук комнаты, которые слышно, когда вы молчите. Ковёр, заполненная полка и речь не в голую стену меняют это сильнее, чем второй микрофон в том же бюджете. Измеренные децибелы мы не публикуем: они зависят от комнаты.",
  ]},
  {"id": "chargers", "kicker": "Техника в дорогу", "title": "Зарядки: вилки США и ЕС", "paras": [
    "На блоке читайте три строки. Вход 100–240 В, 50/60 Гц — это два напряжения. Блок только на 120 В опасен в сети 230 В. Ватты USB-C Power Delivery: телефону хватает около 20 Вт; ноутбуку часто нужно 45–65 Вт или то, что написал производитель ноутбука. Вилка отдельно: GaN-блоку всё равно нужны штыри страны или один пассивный переходник.",
    "Не ставьте преобразователь напряжения на блок, который и так на 100–240 В. На две недели: один такой блок, один кабель USB-C на эти ватты и один пассивный переходник, если штыри не подходят. Второй блок оставьте дома, если второй человек не заряжает ноутбук одновременно.",
  ]},
  {"id": "method", "kicker": "Методика", "title": "Как мы собираем гайд и ставим ссылку", "paras": [
    "Подборка на этом сайте — сравнение опубликованных характеристик и заявленных ограничений плюс пометка, кому вещь подходит. Это не лабораторный тест. Если вещь не использовали, гайд так и пишет.",
    "Комиссия не меняет порядок списка. Если по ссылке возможна комиссия, она помечена как платная, и на сайте есть фраза: As an Amazon Associate I earn from qualifying purchases.",
    "Гайд правим, когда меняется линейка или процитированное ограничение больше не совпадает с источником.",
  ]},
],
"he": [
  {"id": "carry-on", "kicker": "טיולים", "title": "גודל כבודת יד: מה בדרך כלל נכנס", "paras": [
    "חברות תעופה מפרסמות שתי מגבלות שונות: כבודת יד גדולה יותר וחפץ אישי קטן יותר. תיק של 40–45 ליטר לרוב עומד בכלל נדיב לכבודת יד ונכשל בתא מדידה קפדני, או בתעריף שמאפשר רק חפץ אישי. לחפץ אישי בטוח יותר תיק של 20–28 ליטר.",
    "המספרים שפורסמו ומנבאים את תא המדידה: נפח מוצהר, אורך תא למחשב, משקל ריק, והאם חגורת המותן והרצועות נכנסות פנימה. מותגים לא מודדים ליטרים באותה שיטה, אז התייחסו לנפח כטווח. חגורה משתלשלת נכשלת בתא המדידה גם כשהליטרים נראים תקינים.",
    "לא שקלנו את התיקים האלה. לפני טיסה קראו את דף הכבודה העדכני של חברת התעופה לתעריף שלכם. צילום מסך בבלוג אינו הכלל.",
  ]},
  {"id": "usb-mic", "kicker": "משרד ביתי", "title": "מיקרופון USB עד 200 דולר", "paras": [
    "לשיחות ולפודקאסט מדובר בחדר רגיל, מיקרופון דינמי ב-USB בדרך כלל עדיף על קונדנסר זול. קונדנסר שומע את החדר: מקרר, מקלדת, קיר חשוף. מיקרופון דינמי שומע את מה שקרוב אליו.",
    "XLR עם כרטיס קול עדיף אם כבר מתכננים להחליף מיקרופונים. זה יקר ממיקרופון USB אחד ומוסיף קופסה. מתחת ל-200 דולר כל המערכת היא מיקרופון דינמי אחד ב-USB ומעמד.",
    "״רצפת רעש״ כאן היא הרחש וקול החדר שנשמעים כשלא מדברים. שטיח, מדף מלא, ולא לדבר אל קיר חשוף משנים את זה יותר ממיקרופון שני באותו תקציב. איננו מפרסמים דציבלים שנמדדו. הם תלויים בחדר.",
  ]},
  {"id": "chargers", "kicker": "טכנולוגיה לטיולים", "title": "מטענים: תקעי ארה״ב ואירופה", "paras": [
    "קראו שלוש שורות על הלבנה. כניסה 100–240 וולט, 50/60 הרץ, פירושה שני מתחים. לבנה של 120 וולט בלבד מסוכנת ברשת של 230 וולט. וואט ב-USB-C: לטלפון מספיקים כ-20 וואט; למחשב נייד לרוב צריך 45–65 וואט, או מה שיצרן המחשב הדפיס. צורת התקע נפרדת: לבנת GaN עדיין צריכה את הפינים של המדינה, או מתאם פסיבי אחד.",
    "אל תחברו ממיר מתח על לבנה שכבר תומכת ב-100–240 וולט. לשבועיים: לבנה אחת כזו, כבל USB-C אחד שמדורג לוואטים האלה, ומתאם פסיבי אחד אם הפינים לא מתאימים. השאירו לבנה שנייה בבית אלא אם אדם שני טוען מחשב נייד באותו זמן.",
  ]},
  {"id": "method", "kicker": "שיטה", "title": "איך אנחנו חוקרים ומקשרים", "paras": [
    "בחירה באתר הזה היא השוואה של מפרט שפורסם ומגבלות מוצהרות, ועוד הערה למי הפריט מתאים. זו לא בדיקת מעבדה. אם לא השתמשנו בפריט, המדריך אומר זאת.",
    "עמלה לא משנה את סדר הרשימה. אם קישור יכול להניב עמלה, הוא מסומן כקישור בתשלום, והאתר מציין: As an Amazon Associate I earn from qualifying purchases.",
    "מעדכנים מדריך כשקו הדגמים משתנה או כשמגבלה שציטטנו כבר לא תואמת את המקור.",
  ]},
],
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
        f'<li><span class="topic">{html.escape(t)}</span><div><h3><a href="#{ARTICLE_IDS[i]}">{html.escape(h)}</a></h3><p>{html.escape(p)}</p></div></li>'
        for i, (t, h, p) in enumerate(c["guides"]))
    articles = "\n".join(
        f'<article class="article" id="{a["id"]}"><p class="kicker">{html.escape(a["kicker"])}</p><h2>{html.escape(a["title"])}</h2>'
        + "".join(f"<p>{html.escape(p)}</p>" for p in a["paras"]) + "</article>"
        for a in ARTICLES[lang])
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
      <section class="articles" id="articles" aria-labelledby="art-h">
        <h2 class="sec" id="art-h">{c["articles_h"]}</h2>
{articles}
      </section>
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
    for a in ARTICLES[lang]:
        out += [f"## {a['title']}", ""] + [p + "\n" for p in a["paras"]]
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

## Affiliate disclosure

- Amazon Associates participant.
- Required statement, shown on every page: {AMAZON_EXACT}
- Guides compare published specifications. The site does not claim hands-on tests and does not sell products.

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
