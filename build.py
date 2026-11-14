#!/usr/bin/env python3
"""
PickForge static site generator.
All page text lives in CONTENT below (EN / RU / HE). Edit it, then run:

    python3 build.py https://your-user.github.io/pickforge/

The URL argument becomes the canonical base for every page, hreflang link,
sitemap entry, robots.txt, llms.txt and JSON-LD block. Without an argument,
the placeholder https://pickforge.example/ is used.
"""
import json, os, re, sys, html
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent
DEFAULT_ORIGIN = "https://drsemfrankenstein.github.io/pickforge-site"
# AliExpress link API baked into data-ali-endpoint for static hosts (GitHub Pages has no /api).
DEFAULT_ALI_LINK_API = "https://pickforge-mcp.onrender.com/api/links/aliexpress"
ALI_LINK_API = os.environ.get("PICKFORGE_ALI_LINK_API", "").strip()
if len(sys.argv) > 2:
    ALI_LINK_API = sys.argv[2].strip()
SITE_URL = (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ORIGIN + "/").rstrip("/") + "/"
if not ALI_LINK_API and "github.io" in SITE_URL:
    ALI_LINK_API = DEFAULT_ALI_LINK_API
UPDATED_ISO = "2026-11-14"
MCP_NAME = "PickForge"
MCP_URL = "https://pickforge-mcp.onrender.com/sse"
MCP_HEALTH_URL = "https://pickforge-mcp.onrender.com/health"
API_HEALTH_URL = "https://pickforge-api.onrender.com/health"
FOOT_HEALTH_URLS = (MCP_HEALTH_URL, API_HEALTH_URL, MCP_URL)
CLAUDE_CONNECT = "https://claude.ai/customize/connectors?" + urlencode({
    "modal": "add-custom-connector",
    "connectorName": MCP_NAME,
    "connectorUrl": MCP_URL,
})
CHATGPT_CONNECT = "https://chatgpt.com/plugins"
GROK_CONNECT = "https://grok.com/connectors"
CHATGPT_GUIDE = "https://developers.openai.com/api/docs/guides/custom-mcp-server"
AMAZON_EXACT = "As an Amazon Associate I earn from qualifying purchases."
ASSOCIATES_ID = "pickforge-20"
LANGS = ["en", "ru", "he"]
HERO_CONNECTOR_ICONS = frozenset({"claude", "chatgpt", "grok"})
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
  "description": "PickForge is a product-search tool for AI assistants, with labeled affiliate links. This page includes an Amazon.com link builder and the affiliate disclosure. PickForge does not sell products.",
  "skip": "Skip to content", "nav_label": "Sections", "lang_label": "Language",
  "keywords": "PickForge, affiliate disclosure, AI assistant tool, product search, partner programs",
  "nav": ["Service", "Links", "Partners", "Assistant", "Disclosure"],
  "eyebrow": "Product search for AI assistants · Affiliate disclosure on every page",
  "h1": "Product search with affiliate links, for AI assistants",
  "lead": "PickForge is a tool an AI assistant can call when you ask it to find a product. It returns a labeled affiliate link. This page also builds an Amazon.com link in your browser. You pay the store, not PickForge.",
  "cue": "Scroll for details",
  "hero_asst_h": "Connect an assistant",
  "hero_asst_p": "Opens that product’s plugin settings. Claude fills in the name and server address. You confirm before adding.",
  "hero_more": "All setup options",
  "about_k": "What this site is", "about_h": "An information page for a service in development",
  "about_p": ["PickForge is an independent project. This page describes the service, how we handle affiliate links, and who runs it. It is not a store and does not sell products.",
              "Amazon.com links on this page are built in your browser as a full amazon.com address with Associates ID pickforge-20. An AliExpress promotion link is created only by the AliExpress Portals API on our server. This page does not call that API and does not invent one.",
              "Purchases happen on the store’s site, where the price is shown. We do not process orders, hold inventory, or give financial or medical advice."],
  "guides_k": "Service", "guides_h": "What the tool does",
  "guides": [
    ("Search", "Search by request", "A user asks an AI assistant for a product type or a budget. The assistant calls the tool, which searches partner catalogues for matching items."),
    ("Links", "Affiliate links, labeled", "An Amazon.com link on this page is the full address with our Associates ID. An AliExpress promotion link is created only by the official Portals API. A link that can earn a commission is labeled."),
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
  "disc_p": "PickForge participates in the <strong>Amazon Associates Program</strong> and the <strong>AliExpress Affiliate Program</strong> (Portals). If you buy through a link we label, we may earn a commission. You do not pay extra.",
  "disc_fine": [
    "Prices, availability, and offers change. Confirm them on the store’s site before you buy. Store names are trademarks of their owners.",
    "Amazon.com links on this page are the full amazon.com address, including Associates ID pickforge-20. We do not hide that address behind a short link. Amazon does not sponsor or endorse PickForge. The sentence below is the program disclosure.",
  ],
  "priv_h": "Privacy",
  "priv": ["This page is static: no user login, no contact form, and no newsletter signup.",
           "The link builder runs in your browser. The product address or search words are not sent to PickForge. Opening a link sends you to Amazon or, when our server has issued one, to AliExpress. Those stores may set their own cookies.",
           "The assistant tool, when it is published, receives a search request only to return results. We do not sell personal information. Hosting providers may log standard access data (IP, user agent)."],
  "faq_h": "Questions",
  "faq": [
    ("What is PickForge?", "An independent project building a tool that lets AI assistants search products and return affiliate links. The service is in development."),
    ("Do you sell products?", "No. Purchases happen on merchant sites. We do not run checkout, hold inventory, or keep customer accounts."),
    ("Do affiliate links change the results?", "No. A commission does not change the order of search results."),
    ("Are affiliate links labeled?", "Yes. A link that can earn a commission is labeled as a partner link."),
    ("Can I make an Amazon link on this page?", "Yes. The builder returns a full amazon.com address with tag pickforge-20. Open it from this page. The page does not show a price."),
    ("Can I make an AliExpress link on this page?", "Paste an AliExpress product URL and the builder calls the Portals API when a public link endpoint is configured. On static GitHub Pages without that API, use search words or an Amazon URL instead."),
    ("How do I add PickForge to Claude, ChatGPT, or Grok?", "Use the buttons under Connect an assistant. Claude opens Add custom connector with the name and server address filled in. ChatGPT opens Plugins: choose Add custom MCP server and enter the name, description, and connection on this page. Grok opens Connectors: choose New Connector, then Custom. You confirm before PickForge is added."),
    ("How do I contact the publisher?", "This page has no contact form."),
  ],
  "link": {
    "h": "Make a store link",
    "p": "Paste search words, an Amazon product page, or an AliExpress item URL. PickForge detects the store automatically.",
    "label": "Search, Amazon page, or AliExpress URL",
    "placeholder": "Cordless vacuum, amazon.com/…/dp/…, or aliexpress.com/item/…",
    "autoNote": "Search words become an Amazon link with tag=pickforge-20. Amazon and AliExpress URLs are recognized from the address.",
    "submit": "Make link",
    "working": "Building your link…",
    "openAmazon": "Open on Amazon",
    "openAli": "Open on AliExpress",
    "copy": "Copy",
    "copied": "Copied",
    "copy_fail": "Copy failed",
    "kicker": "Affiliate link",
    "amazon_disclose": "Affiliate link. As an Amazon Associate I earn from qualifying purchases. Check the current price on Amazon.",
    "aliDisclose": "Affiliate link. AliExpress Portals issued this promotion link.",
    "noscript": "This link builder needs JavaScript.",
    "readyAmazon": "Amazon link ready. Open it from this page.",
    "readyAli": "AliExpress promotion link ready.",
    "err_empty": "Enter a product page or search words.",
    "err_short": "Paste the full amazon.com page. Short links such as amzn.to are not used here.",
    "err_region": "This Associates ID is for Amazon.com only. Other Amazon sites need their own ID.",
    "err_page": "Paste an Amazon.com product page (/dp/…) or a search page.",
    "err_query": "Enter at least two characters.",
    "err_unknown": "Use search words, an amazon.com page, or an AliExpress product URL.",
    "err_ali_no_api": "AliExpress links need the PickForge link API, which is not wired on this static page. Use search words or an Amazon URL.",
    "err_ali_page": "Paste an AliExpress product page. The address must contain /item/ and the product number.",
    "err_ali_fetch": "Could not reach the PickForge link API. Run pickforge-mcp locally on port 3099, or rebuild this page with a public data-ali-endpoint URL.",
  },
  "partners": {
    "h": "Partners",
    "p": "Product search and labeled affiliate links use these programs. Checkout stays on each merchant’s site. Store names are trademarks of their owners.",
    "items": [
      ("Amazon", "amazon", "Amazon Associates", "Product and search links on amazon.com include Associates ID pickforge-20."),
      ("AliExpress", "aliexpress", "AliExpress Portals", "Official promotion links are created only through the Portals affiliate API."),
    ],
  },
  "assistant": {
    "h": "Add the tool to an assistant",
    "p": [
      "The product search is an MCP server: a service the assistant calls when you ask it to find a product. It returns links. A link that can earn a commission is labeled. You pay the store, not PickForge.",
      "PickForge is not in a plugin directory. The server address is https://pickforge-mcp.onrender.com/sse. Each link opens that product’s add-plugin page. The name, description, and connection are on the card. Claude’s link fills in the name and server address. You confirm before it is added. Do not paste a localhost address.",
    ],
    "field_labels": {"name": "Name", "description": "Description", "connection": "Connection"},
    "mcp_description": "Product search with labeled affiliate links. You pay the store, not PickForge.",
    "connectors": [
      ("Claude", CLAUDE_CONNECT, "Opens Add custom connector with the name and server address filled in. Review them, then add.", "claude", ("name", "connection")),
      ("ChatGPT", CHATGPT_CONNECT, "Opens ChatGPT Plugins. Choose Add custom MCP server and enter the name, description, and connection. Authentication: No authentication. Then choose Create as a plugin.", "chatgpt", ("name", "description", "connection")),
      ("ChatGPT guide", CHATGPT_GUIDE, "OpenAI’s steps for adding a custom MCP server.", "chatgpt"),
      ("Grok", GROK_CONNECT, "Opens Grok connectors. Choose New Connector, then Custom, and enter the name and server address.", "grok", ("name", "connection")),
    ],
  },
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
    ("Last updated", "14 November 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["Privacy", "Links", "Disclosure", "Publisher"],
  "foot_health": ["Health MCP", "Health API", "SSE (MCP)"],
  "home": "PickForge home",
  "story_label": "About PickForge",
},
"ru": {
  "title": "PickForge: поиск товаров и партнёрские ссылки для ИИ-ассистентов",
  "description": "PickForge — инструмент поиска товаров для ИИ-ассистентов с помеченными партнёрскими ссылками. На странице есть сборка ссылки Amazon.com и раскрытие партнёрских отношений. PickForge ничего не продаёт.",
  "skip": "Перейти к содержимому", "nav_label": "Разделы", "lang_label": "Язык",
  "keywords": "PickForge, раскрытие партнёрских ссылок, инструмент для ИИ-ассистентов, поиск товаров, партнёрские программы",
  "nav": ["Сервис", "Ссылки", "Партнёры", "Ассистент", "Раскрытие"],
  "eyebrow": "Поиск товаров для ИИ-ассистентов · Раскрытие партнёрских отношений на каждой странице",
  "h1": "Поиск товаров с партнёрскими ссылками для ИИ-ассистентов",
  "lead": "PickForge — инструмент, который ИИ-ассистент вызывает, когда вы просите найти товар. Он возвращает помеченную партнёрскую ссылку. На этой странице также собирается ссылка Amazon.com в вашем браузере. Платите магазину, не PickForge.",
  "cue": "Листайте, чтобы увидеть подробности",
  "hero_asst_h": "Подключить ассистента",
  "hero_asst_p": "Открывает настройки плагинов. Claude подставляет имя и адрес сервера. Подтвердите перед добавлением.",
  "hero_more": "Все способы подключения",
  "about_k": "Что это за сайт", "about_h": "Информационная страница сервиса в разработке",
  "about_p": ["PickForge — независимый проект. Эта страница описывает сервис, то, как мы работаем с партнёрскими ссылками, и кто за ним стоит. Это не магазин, и мы ничего не продаём.",
              "Ссылки Amazon.com на этой странице собираются в браузере: полный адрес amazon.com с идентификатором Associates pickforge-20. Партнёрскую ссылку AliExpress создаёт только API AliExpress Portals на нашем сервере. Эта страница не вызывает этот API и не подделывает ссылку.",
              "Покупка проходит на сайте магазина, где видна цена. Мы не принимаем заказы, не храним товары и не даём финансовых или медицинских советов."],
  "guides_k": "Сервис", "guides_h": "Что делает инструмент",
  "guides": [
    ("Поиск", "Поиск по запросу", "Пользователь просит ИИ-ассистента подобрать тип товара или бюджет. Ассистент вызывает инструмент, который ищет подходящие позиции в партнёрских каталогах."),
    ("Ссылки", "Партнёрские ссылки с пометкой", "Ссылка Amazon.com на этой странице — полный адрес с нашим идентификатором Associates. Партнёрскую ссылку AliExpress создаёт только официальный API Portals. Ссылка, которая может принести комиссию, помечена."),
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
  "disc_p": "PickForge участвует в <strong>Amazon Associates</strong> и в <strong>партнёрской программе AliExpress</strong> (Portals). Если вы купите товар по ссылке, которую мы пометили, мы можем получить комиссию. Доплаты нет.",
  "disc_fine": [
    "Цены, наличие и условия меняются. Перед покупкой проверьте их на сайте магазина. Названия магазинов — товарные знаки владельцев.",
    "Ссылки Amazon.com на этой странице — полный адрес amazon.com, включая идентификатор Associates pickforge-20. Мы не прячем его за коротким адресом. Amazon не спонсирует и не поддерживает PickForge. Ниже — обязательная формулировка программы на английском.",
  ],
  "priv_h": "Конфиденциальность",
  "priv": ["Эта страница статическая: без регистрации, формы обратной связи и рассылки.",
           "Сборщик ссылок работает в вашем браузере. Адрес товара или слова поиска не отправляются в PickForge. Переход открывает Amazon или, если ссылку выдал наш сервер, AliExpress. Эти магазины могут ставить свои cookie.",
           "Инструмент ассистента, когда он будет опубликован, получает поисковый запрос только чтобы вернуть результат. Мы не продаём персональные данные. Хостинг может записывать обычные данные доступа (IP-адрес, user agent)."],
  "faq_h": "Вопросы",
  "faq": [
    ("Что такое PickForge?", "Независимый проект: инструмент, с помощью которого ИИ-ассистенты ищут товары и возвращают партнёрские ссылки. Сервис в разработке."),
    ("Вы продаёте товары?", "Нет. Покупки совершаются на сайтах продавцов. Мы не ведём оформление заказов, не храним товары и не ведём аккаунты покупателей."),
    ("Влияют ли комиссии на результаты?", "Нет. Комиссия не меняет порядок результатов поиска."),
    ("Помечены ли партнёрские ссылки?", "Да. Ссылка, которая может принести комиссию, помечена как партнёрская."),
    ("Можно ли собрать ссылку Amazon на этой странице?", "Да. Сборщик возвращает полный адрес amazon.com с tag=pickforge-20. Откройте его с этой страницы. Цену страница не показывает."),
    ("Можно ли собрать ссылку AliExpress на этой странице?", "Вставьте URL товара AliExpress — сборщик вызовет API Portals, если подключён публичный endpoint. На статической копии без API используйте слова поиска или URL Amazon."),
    ("Как добавить PickForge в Claude, ChatGPT или Grok?", "Кнопки в блоке «Подключить ассистента» открывают настройки плагинов. Claude открывает Add custom connector с уже заполненными именем и адресом сервера. ChatGPT открывает Plugins: выберите Add custom MCP server и введите имя, описание и подключение с этой страницы. Grok открывает Connectors: New Connector, затем Custom. Подтвердите, прежде чем PickForge будет добавлен."),
    ("Как связаться с издателем?", "На этой странице нет формы обратной связи."),
  ],
  "link": {
    "h": "Собрать ссылку магазина",
    "p": "Вставьте слова поиска, страницу товара Amazon или адрес товара AliExpress. PickForge сам определит магазин.",
    "label": "Поиск, страница Amazon или URL AliExpress",
    "placeholder": "Пылесос, amazon.com/…/dp/… или aliexpress.com/item/…",
    "autoNote": "Слова поиска становятся ссылкой Amazon с tag=pickforge-20. Адреса Amazon и AliExpress распознаются автоматически.",
    "submit": "Собрать ссылку",
    "working": "Собираем ссылку…",
    "openAmazon": "Открыть на Amazon",
    "openAli": "Открыть на AliExpress",
    "copy": "Копировать",
    "copied": "Скопировано",
    "copy_fail": "Не скопировалось",
    "kicker": "Партнёрская ссылка",
    "amazon_disclose": "Партнёрская ссылка. As an Amazon Associate I earn from qualifying purchases. Цену смотрите на Amazon.",
    "aliDisclose": "Партнёрская ссылка. Её выдал AliExpress Portals.",
    "noscript": "Сборщику ссылок нужен JavaScript.",
    "readyAmazon": "Ссылка Amazon готова. Откройте её с этой страницы.",
    "readyAli": "Партнёрская ссылка AliExpress готова.",
    "err_empty": "Введите страницу товара или слова поиска.",
    "err_short": "Вставьте полную страницу amazon.com. Короткие ссылки вроде amzn.to здесь не используются.",
    "err_region": "Этот идентификатор Associates только для Amazon.com. Для других сайтов Amazon нужен свой идентификатор.",
    "err_page": "Вставьте страницу товара Amazon.com (/dp/…) или страницу поиска.",
    "err_query": "Введите хотя бы два символа.",
    "err_unknown": "Используйте слова поиска, страницу amazon.com или URL товара AliExpress.",
    "err_ali_no_api": "Для AliExpress нужен API PickForge, которого нет на этой статической странице. Введите слова поиска или URL Amazon.",
    "err_ali_page": "Вставьте страницу товара AliExpress. В адресе должны быть /item/ и номер товара.",
    "err_ali_fetch": "Не удалось связаться с API PickForge. Запустите pickforge-mcp локально на порту 3099 или пересоберите страницу с публичным data-ali-endpoint.",
  },
  "partners": {
    "h": "Партнёры",
    "p": "Поиск и помеченные партнёрские ссылки идут через эти программы. Оплата — на сайте магазина. Названия магазинов — торговые марки их владельцев.",
    "items": [
      ("Amazon", "amazon", "Amazon Associates", "Ссылки на товары и поиск на amazon.com с идентификатором Associates pickforge-20."),
      ("AliExpress", "aliexpress", "AliExpress Portals", "Партнёрские ссылки создаёт только официальный API Portals."),
    ],
  },
  "assistant": {
    "h": "Добавить инструмент в ассистент",
    "p": [
      "Поиск товаров — это MCP-сервер: служба, которую ассистент вызывает, когда вы просите найти товар. Он возвращает ссылки. Ссылка, которая может принести комиссию, помечена. Платите магазину, не PickForge.",
      "PickForge ещё нет в каталоге плагинов. Адрес сервера: https://pickforge-mcp.onrender.com/sse. Каждая ссылка открывает страницу добавления плагина. Имя, описание и подключение указаны на карточке. Ссылка Claude подставляет имя и адрес сервера. Подтвердите, прежде чем сервер будет добавлен. Не вставляйте адрес localhost.",
    ],
    "field_labels": {"name": "Имя", "description": "Описание", "connection": "Подключение"},
    "mcp_description": "Поиск товаров с помеченными партнёрскими ссылками. Платите магазину, не PickForge.",
    "connectors": [
      ("Claude", CLAUDE_CONNECT, "Открывает Add custom connector: имя и адрес сервера уже заполнены. Проверьте их и добавьте.", "claude", ("name", "connection")),
      ("ChatGPT", CHATGPT_CONNECT, "Открывает ChatGPT Plugins. Выберите Add custom MCP server и введите имя, описание и подключение. Authentication: No authentication. Затем Create as a plugin.", "chatgpt", ("name", "description", "connection")),
      ("Инструкция ChatGPT", CHATGPT_GUIDE, "Шаги OpenAI для своего MCP-сервера.", "chatgpt"),
      ("Grok", GROK_CONNECT, "Открывает коннекторы Grok. Выберите New Connector, затем Custom, и введите имя и адрес сервера.", "grok", ("name", "connection")),
    ],
  },
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
    ("Обновлено", "14 ноября 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["Конфиденциальность", "Ссылки", "Раскрытие", "Издатель"],
  "foot_health": ["Health MCP", "Health API", "SSE (MCP)"],
  "home": "PickForge — главная",
  "story_label": "О PickForge",
},
"he": {
  "title": "PickForge: חיפוש מוצרים וקישורי שותפים לעוזרי AI",
  "description": "PickForge הוא כלי חיפוש מוצרים לעוזרי AI, עם קישורי שותפים מסומנים. בעמוד יש בונה קישור ל-Amazon.com וגילוי נאות. PickForge לא מוכר מוצרים.",
  "skip": "דילוג לתוכן", "nav_label": "אזורים באתר", "lang_label": "שפה",
  "keywords": "PickForge, גילוי נאות על שותפים, כלי לעוזרי AI, חיפוש מוצרים, תוכניות שותפים",
  "nav": ["השירות", "קישורים", "שותפים", "עוזר", "גילוי נאות"],
  "eyebrow": "חיפוש מוצרים לעוזרי AI · גילוי נאות על שותפות בכל עמוד",
  "h1": "חיפוש מוצרים עם קישורי שותפים, לעוזרי AI",
  "lead": "PickForge הוא כלי שעוזר AI מפעיל כשמבקשים ממנו למצוא מוצר. הוא מחזיר קישור שותפים מסומן. בעמוד הזה נבנית גם כתובת Amazon.com בדפדפן. התשלום הוא לחנות, לא ל-PickForge.",
  "cue": "גללו לפרטים",
  "hero_asst_h": "חיבור עוזר",
  "hero_asst_p": "פותח את הגדרות התוספים. Claude ממלא את השם ואת כתובת השרת. יש לאשר לפני ההוספה.",
  "hero_more": "כל אפשרויות החיבור",
  "about_k": "מה האתר הזה", "about_h": "עמוד מידע לשירות בפיתוח",
  "about_p": ["PickForge הוא פרויקט עצמאי. עמוד זה מתאר את השירות, איך אנחנו עובדים עם קישורי שותפים ומי עומד מאחוריו. זו לא חנות, ואיננו מוכרים מוצרים.",
              "קישורי Amazon.com בעמוד הזה נבנים בדפדפן: כתובת amazon.com מלאה עם מזהה Associates‏ pickforge-20. קישור קידום של AliExpress נוצר רק ב-API של AliExpress Portals בשרת שלנו. העמוד לא קורא ל-API הזה ולא ממציא קישור.",
              "הרכישה מתבצעת באתר החנות, שם מוצג המחיר. איננו מקבלים הזמנות, לא שומרים מלאי ולא נותנים ייעוץ פיננסי או רפואי."],
  "guides_k": "השירות", "guides_h": "מה הכלי עושה",
  "guides": [
    ("חיפוש", "חיפוש לפי בקשה", "המשתמש מבקש מעוזר AI סוג מוצר או תקציב. העוזר מפעיל את הכלי, שמחפש פריטים מתאימים בקטלוגים של שותפים."),
    ("קישורים", "קישורי שותפים עם סימון", "קישור Amazon.com בעמוד הזה הוא הכתובת המלאה עם מזהה ה-Associates שלנו. קישור קידום של AliExpress נוצר רק ב-API הרשמי של Portals. קישור שעשוי להניב עמלה מסומן."),
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
  "disc_p": "PickForge משתתף ב-<strong>Amazon Associates</strong> וב-<strong>תוכנית השותפים של AliExpress</strong>‏ (Portals). אם תרכוש דרך קישור שסימנו, ייתכן שנקבל עמלה. אין תוספת תשלום.",
  "disc_fine": [
    "מחירים, זמינות והצעות משתנים. אשרו אותם באתר החנות לפני קנייה. שמות החנויות הם סימנים מסחריים של בעליהם.",
    "קישורי Amazon.com בעמוד הזה הם הכתובת המלאה ב-amazon.com, כולל מזהה Associates‏ pickforge-20. איננו מסתירים אותה מאחורי כתובת קצרה. Amazon לא נותנת חסות ל-PickForge ולא תומכת בו. המשפט למטה הוא נוסח הגילוי הנדרש, באנגלית.",
  ],
  "priv_h": "פרטיות",
  "priv": ["העמוד סטטי: אין הרשמה, טופס יצירת קשר או ניוזלטר.",
           "בונה הקישורים רץ בדפדפן. כתובת המוצר או מילות החיפוש לא נשלחות ל-PickForge. פתיחת קישור מעבירה אל Amazon, או אל AliExpress אם השרת שלנו הנפיק את הקישור. החנויות עשויות להגדיר עוגיות משלהן.",
           "כלי העוזר, כשיפורסם, מקבל בקשת חיפוש רק כדי להחזיר תוצאה. איננו מוכרים מידע אישי. ספק האחסון עשוי לתעד נתוני גישה רגילים (כתובת IP, סוג דפדפן)."],
  "faq_h": "שאלות",
  "faq": [
    ("מה זה PickForge?", "פרויקט עצמאי: כלי שמאפשר לעוזרי AI לחפש מוצרים ולהחזיר קישורי שותפים. השירות בפיתוח."),
    ("אתם מוכרים מוצרים?", "לא. רכישות מתבצעות באתרי הסוחרים. איננו מנהלים קופה, לא שומרים מלאי ולא מנהלים חשבונות לקוח."),
    ("האם עמלות משנות את התוצאות?", "לא. עמלה לא משנה את סדר תוצאות החיפוש."),
    ("האם קישורי השותפים מסומנים?", "כן. קישור שעשוי להניב עמלה מסומן כקישור שותפים."),
    ("אפשר לבנות קישור Amazon בעמוד הזה?", "כן. הבונה מחזיר כתובת amazon.com מלאה עם tag=pickforge-20. פתחו אותה מהעמוד הזה. העמוד לא מציג מחיר."),
    ("אפשר לבנות קישור AliExpress בעמוד הזה?", "הדביקו כתובת מוצר ב-AliExpress — הבונה קורא ל-API של Portals כשיש endpoint ציבורי. בגרסה הסטטית בלי API השתמשו במילות חיפוש או בכתובת Amazon."),
    ("איך מוסיפים את PickForge ל-Claude, ל-ChatGPT או ל-Grok?", "הכפתורים תחת «חיבור עוזר» פותחים את הגדרות התוספים. Claude פותח Add custom connector עם שם וכתובת שרת מלאים. ChatGPT פותח Plugins: בחרו Add custom MCP server והזינו את השם, התיאור והחיבור מהעמוד הזה. Grok פותח Connectors: New Connector ואז Custom. יש לאשר לפני ש-PickForge נוסף."),
    ("איך יוצרים קשר עם המוציא לאור?", "בעמוד זה אין טופס יצירת קשר."),
  ],
  "link": {
    "h": "בניית קישור לחנות",
    "p": "הדביקו מילות חיפוש, עמוד מוצר ב-Amazon או כתובת פריט ב-AliExpress. PickForge מזהה את החנות אוטומטית.",
    "label": "חיפוש, עמוד Amazon או כתובת AliExpress",
    "placeholder": "שואב אבק, amazon.com/…/dp/… או aliexpress.com/item/…",
    "autoNote": "מילות חיפוש הופכות לקישור Amazon עם tag=pickforge-20. כתובות Amazon ו-AliExpress מזוהות מהקישור.",
    "submit": "בניית קישור",
    "working": "בונים את הקישור…",
    "openAmazon": "פתיחה ב-Amazon",
    "openAli": "פתיחה ב-AliExpress",
    "copy": "העתקה",
    "copied": "הועתק",
    "copy_fail": "ההעתקה נכשלה",
    "kicker": "קישור שותפים",
    "amazon_disclose": "קישור שותפים. As an Amazon Associate I earn from qualifying purchases. את המחיר בודקים ב-Amazon.",
    "aliDisclose": "קישור שותפים. קישור קידום זה הונפק ב-AliExpress Portals.",
    "noscript": "בונה הקישורים צריך JavaScript.",
    "readyAmazon": "קישור Amazon מוכן. פתחו אותו מהעמוד הזה.",
    "readyAli": "קישור הקידום של AliExpress מוכן.",
    "err_empty": "הזינו עמוד מוצר או מילות חיפוש.",
    "err_short": "הדביקו את עמוד amazon.com המלא. קישורים קצרים כמו amzn.to לא בשימוש כאן.",
    "err_region": "מזהה ה-Associates הזה הוא ל-Amazon.com בלבד. לאתרי Amazon אחרים צריך מזהה משלהם.",
    "err_page": "הדביקו עמוד מוצר ב-Amazon.com‏ (/dp/…) או עמוד חיפוש.",
    "err_query": "הזינו לפחות שני תווים.",
    "err_unknown": "השתמשו במילות חיפוש, בעמוד amazon.com או בכתובת מוצר ב-AliExpress.",
    "err_ali_no_api": "קישורי AliExpress דורשים את ה-API של PickForge, שלא מחובר בעמוד הסטטי הזה. השתמשו במילות חיפוש או בכתובת Amazon.",
    "err_ali_page": "הדביקו עמוד מוצר ב-AliExpress. בכתובת חייבים להיות /item/ ומספר המוצר.",
    "err_ali_fetch": "לא ניתן להגיע ל-API של PickForge. הריצו pickforge-mcp מקומית בפורט 3099, או בנו מחדש את העמוד עם כתובת data-ali-endpoint ציבורית.",
  },
  "partners": {
    "h": "שותפים",
    "p": "חיפוש מוצרים וקישורי שותפים מסומנים עוברים דרך התוכניות האלה. התשלום נשאר באתר הסוחר. שמות החנויות הם סימני מסחר של הבעלים.",
    "items": [
      ("Amazon", "amazon", "Amazon Associates", "קישורי מוצר וחיפוש ב-amazon.com כוללים את מזהה Associates‏ pickforge-20."),
      ("AliExpress", "aliexpress", "AliExpress Portals", "קישורי קידום רשמיים נוצרים רק ב-API השותפים של Portals."),
    ],
  },
  "assistant": {
    "h": "הוספת הכלי לעוזר",
    "p": [
      "חיפוש המוצרים הוא שרת MCP: שירות שהעוזר קורא לו כשמבקשים למצוא מוצר. הוא מחזיר קישורים. קישור שעשוי להניב עמלה מסומן. התשלום הוא לחנות, לא ל-PickForge.",
      "PickForge לא רשום בקטלוג תוספים. כתובת השרת: https://pickforge-mcp.onrender.com/sse. כל קישור פותח את עמוד הוספת התוסף. השם, התיאור והחיבור מופיעים בכרטיס. הקישור של Claude ממלא את השם ואת כתובת השרת. יש לאשר לפני ההוספה. אל תדביקו כתובת localhost.",
    ],
    "field_labels": {"name": "שם", "description": "תיאור", "connection": "חיבור"},
    "mcp_description": "חיפוש מוצרים עם קישורי שותפים מסומנים. התשלום הוא לחנות, לא ל-PickForge.",
    "connectors": [
      ("Claude", CLAUDE_CONNECT, "פותח את Add custom connector עם שם וכתובת שרת מלאים. בדקו אותם ואז הוסיפו.", "claude", ("name", "connection")),
      ("ChatGPT", CHATGPT_CONNECT, "פותח את ChatGPT Plugins. בחרו Add custom MCP server והזינו שם, תיאור וחיבור. Authentication: No authentication. אחר כך Create as a plugin.", "chatgpt", ("name", "description", "connection")),
      ("מדריך ChatGPT", CHATGPT_GUIDE, "השלבים של OpenAI להוספת שרת MCP משלכם.", "chatgpt"),
      ("Grok", GROK_CONNECT, "פותח את מחברי Grok. בחרו New Connector ואז Custom, והזינו שם וכתובת שרת.", "grok", ("name", "connection")),
    ],
  },
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
    ("עודכן לאחרונה", "14 בנובמבר 2026"),
  ],
  "assoc": "As an Amazon Associate I earn from qualifying purchases.",
  "foot_links": ["פרטיות", "קישורים", "גילוי נאות", "מוציא לאור"],
  "foot_health": ["Health MCP", "Health API", "SSE (MCP)"],
  "home": "PickForge — דף הבית",
  "story_label": "אודות PickForge",
},
}

def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))

def connector_fields_html(labels, description, keys):
    if not keys:
        return ""
    values = {"name": MCP_NAME, "description": description, "connection": MCP_URL}
    bits = []
    for key in keys:
        bits.append(
            "<div>"
            f"<dt>{html.escape(labels[key])}</dt>"
            f"<dd><code>{html.escape(values[key])}</code></dd>"
            "</div>"
        )
    return f'<dl class="connector-fields">{"".join(bits)}</dl>'

def connector_li(rel, row, labels, description):
    name, href, detail = row[0], row[1], row[2]
    icon = row[3] if len(row) > 3 else None
    keys = row[4] if len(row) > 4 else ()
    icon_bit = ""
    if icon:
        src = f"{rel}assets/connectors/{icon}.svg"
        icon_bit = (
            f'<span class="connector-icon" aria-hidden="true">'
            f'<img src="{html.escape(src)}" alt="" width="40" height="40" loading="lazy" decoding="async">'
            f"</span>"
        )
    return (
        f'<li class="connector-card">'
        f"{icon_bit}"
        f'<div class="connector-body">'
        f'<a href="{html.escape(href, quote=True)}" rel="noopener noreferrer">{html.escape(name)}</a>'
        f"<p>{html.escape(detail)}</p>"
        f"{connector_fields_html(labels, description, keys)}"
        f"</div></li>"
    )

def connector_md(row, labels, description):
    lines = [f"- [{row[0]}]({row[1]}): {row[2]}"]
    values = {"name": MCP_NAME, "description": description, "connection": MCP_URL}
    for key in (row[4] if len(row) > 4 else ()):
        lines.append(f"  - {labels[key]}: {values[key]}")
    return "\n".join(lines)

def connector_hero_li(rel, name, href, icon):
    src = f"{rel}assets/connectors/{icon}.svg"
    icon_bit = (
        f'<span class="connector-icon" aria-hidden="true">'
        f'<img src="{html.escape(src)}" alt="" width="40" height="40" loading="lazy" decoding="async">'
        f"</span>"
    )
    return (
        f'<li class="connector-card connector-card--compact">'
        f"{icon_bit}"
        f'<a href="{html.escape(href, quote=True)}" rel="noopener noreferrer">{html.escape(name)}</a>'
        f"</li>"
    )

def hero_connectors_html(rel, rows):
    picked = [r for r in rows if len(r) > 4 and r[3] in HERO_CONNECTOR_ICONS]
    return "\n".join(connector_hero_li(rel, r[0], r[1], r[3]) for r in picked)

def partners_section_html(rel, partners):
    cards = []
    for name, icon, program, detail in partners["items"]:
        src = f"{rel}assets/stores/{icon}.svg"
        cards.append(
            f'<li class="partner-card">'
            f'<span class="partner-icon" aria-hidden="true">'
            f'<img src="{html.escape(src)}" alt="" width="56" height="56" loading="lazy" decoding="async">'
            f"</span>"
            f'<div class="partner-body">'
            f'<p class="partner-name">{html.escape(name)}</p>'
            f'<p class="partner-program">{html.escape(program)}</p>'
            f"<p>{html.escape(detail)}</p>"
            f"</div></li>"
        )
    return (
        f'<section class="partners" id="partners" aria-labelledby="partners-h">'
        f'<h2 class="sec" id="partners-h">{html.escape(partners["h"])}</h2>'
        f'<p class="partners-intro">{html.escape(partners["p"])}</p>'
        f'<ul class="partners-grid">{"".join(cards)}</ul>'
        f"</section>"
    )

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
    fh = " · ".join(
        f'<a href="{u}" rel="noopener noreferrer" target="_blank">{html.escape(l)}</a>'
        for l, u in zip(c["foot_health"], FOOT_HEALTH_URLS)
    )
    L = c["link"]
    link_json = json.dumps({
        "placeholder": L["placeholder"], "autoNote": L["autoNote"],
        "kicker": L["kicker"], "amazonDisclose": L["amazon_disclose"], "aliDisclose": L["aliDisclose"],
        "openAmazon": L["openAmazon"], "openAli": L["openAli"],
        "copy": L["copy"], "copied": L["copied"], "copyFail": L["copy_fail"],
        "working": L["working"],
        "readyAmazon": L["readyAmazon"], "readyAli": L["readyAli"],
        "err_empty": L["err_empty"], "err_short": L["err_short"],
        "err_region": L["err_region"], "err_page": L["err_page"], "err_query": L["err_query"],
        "err_unknown": L["err_unknown"], "err_ali_no_api": L["err_ali_no_api"],
        "err_ali_page": L["err_ali_page"], "err_ali_fetch": L["err_ali_fetch"],
    }, ensure_ascii=False).replace("<", "\\u003c")
    P = c["partners"]
    partners_block = partners_section_html(rel, P)
    A = c["assistant"]
    assistant_ps = "".join(f"<p>{html.escape(p)}</p>" for p in A["p"])
    connectors = "\n".join(
        connector_li(rel, row, A["field_labels"], A["mcp_description"])
        for row in A["connectors"]
    )
    hero_connectors = hero_connectors_html(rel, A["connectors"])
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
      <a href="#links">{n[1]}</a>
      <a href="#partners">{n[2]}</a>
      <a href="#assistant">{n[3]}</a>
      <a class="keep" href="#disclosure">{n[4]}</a>
    </nav>
    <div class="langs" role="group" aria-label="{c["lang_label"]}">{langs}</div>
  </div>
</header>

<main id="main">
  <section class="story" id="story" aria-label="{c["story_label"]}">
    <div class="stage" aria-hidden="true"><div class="sprite" id="sprite"></div></div>
    <div class="chapters">
      <div class="chapter hero" id="top">
        <div class="panel hero-split">
          <div class="hero-copy">
            <p class="eyebrow">{c["eyebrow"]}</p>
            <h1>{c["h1"]}</h1>
            <p class="lead">{c["lead"]}</p>
            <p class="notice">{AMAZON_EXACT}</p>
            <p class="cue">{c["cue"]}</p>
          </div>
          <aside class="hero-aside" aria-labelledby="hero-asst-h">
            <p class="kicker" id="hero-asst-h">{html.escape(c["hero_asst_h"])}</p>
            <p class="fine hero-aside-note">{html.escape(c["hero_asst_p"])}</p>
            <ul class="connectors connectors--hero">
{hero_connectors}
            </ul>
            <p class="hero-more"><a href="#assistant">{html.escape(c["hero_more"])}</a></p>
          </aside>
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
      <section class="tool" id="links" data-link-tool data-tag="{ASSOCIATES_ID}" data-ali-endpoint="{html.escape(ALI_LINK_API)}" data-icon-amazon="{rel}assets/stores/amazon.svg" data-icon-ali="{rel}assets/stores/aliexpress.svg" aria-labelledby="links-h">
        <div>
          <h2 id="links-h">{html.escape(L["h"])}</h2>
        </div>
        <div class="tool-body">
          <p>{html.escape(L["p"])}</p>
          <p class="amazon-exact">{AMAZON_EXACT}</p>
          <form id="link-form" action="">
            <label class="sr" for="link-input">{html.escape(L["label"])}</label>
            <input id="link-input" name="q" type="text" autocomplete="off" spellcheck="false" maxlength="4000" placeholder="{html.escape(L["placeholder"])}" required>
            <button type="submit">{html.escape(L["submit"])}</button>
          </form>
          <p class="fine" id="link-note"></p>
          <p class="status" id="link-status" role="status"></p>
          <div id="link-result" hidden>
            <p class="kicker" id="link-kicker"></p>
            <p class="url" id="link-out"></p>
            <p class="fine" id="link-disclose"></p>
            <div class="actions">
              <a id="link-open" rel="noopener"><img id="link-open-icon" alt="" width="18" height="18" hidden decoding="async"><span id="link-open-label"></span></a>
              <button type="button" id="link-copy"></button>
            </div>
          </div>
          <noscript><p>{html.escape(L["noscript"])}</p></noscript>
        </div>
      </section>
      <script type="application/json" id="link-strings">{link_json}</script>
      {partners_block}
      <section class="assistant" id="assistant" aria-labelledby="asst-h">
        <h2 class="sec" id="asst-h">{html.escape(A["h"])}</h2>
        <div>{assistant_ps}<ul class="connectors connectors--setup">{connectors}</ul><p class="assistant-health" dir="ltr">{fh}</p></div>
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
    <span><a href="#privacy">{fl[0]}</a> · <a href="#links">{fl[1]}</a> · <a href="#disclosure">{fl[2]}</a> · <a href="#publisher">{fl[3]}</a></span>
  </div>
</footer>
<script src="{rel}assets/site.js" defer></script>
<script type="module" src="{rel}assets/link-generator.js"></script>
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
    L = c["link"]
    out += [f"## {L['h']}", "", L["p"], "", L["autoNote"], ""]
    Pr = c["partners"]
    out += [f"## {Pr['h']}", "", Pr["p"], ""]
    out += [f"- **{name}** ({program}): {detail}" for name, _icon, program, detail in Pr["items"]] + [""]
    A = c["assistant"]
    out += [f"## {A['h']}", ""] + [p + "\n" for p in A["p"]]
    out += [connector_md(row, A["field_labels"], A["mcp_description"]) for row in A["connectors"]] + [""]
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

- Amazon Associates participant. Associates ID on this site: {ASSOCIATES_ID}. Storefront: amazon.com only.
- AliExpress Affiliate Program (Portals). Official promotion links are created by the Portals API on the server. This page does not invent one.
- Required statement, shown on every page: {AMAZON_EXACT}
- Amazon links built on this page are full https://www.amazon.com addresses with tag={ASSOCIATES_ID}. No price is shown. Open the link from this page.
- The service does not sell products and does not claim hands-on product tests.

## Pages

- [English]({url('en')}) · [Markdown]({url('en')}index.md)
- [Russian]({url('ru')}) · [Markdown]({url('ru')}index.md)
- [Hebrew]({url('he')}) · [Markdown]({url('he')}index.md)

## Service

""" + "\n".join(f"- {h}: {p}" for t, h, p in e["guides"]) + f"""

## Assistant connectors

The public MCP address is {MCP_URL} (SSE). Name: {MCP_NAME}. Description: {e["assistant"]["mcp_description"]}
Claude opens Add custom connector with the name and address filled in. ChatGPT opens Plugins: choose Add custom MCP server and enter the name, description, and connection, with no authentication. Grok opens Connectors: choose New Connector, then Custom. Confirm before adding. Do not paste a localhost address.

""" + "\n".join(f"- {row[0]}: {row[1]}" for row in e["assistant"]["connectors"]) + f"""

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
