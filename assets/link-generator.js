const ASIN_RE = /\/(?:dp|gp\/product|gp\/aw\/d|exec\/obidos\/ASIN)\/([A-Z0-9]{10})(?=[/?#]|$)/i;
const ALI_ITEM_RE = /\/(?:item|i)\/(\d{6,20})(?:\.html)?(?=[/?#]|$)/i;
const LOCAL_ALI_API = "http://127.0.0.1:3099/api/links/aliexpress";
const DEFAULT_ALI_API = "https://pickforge-mcp.onrender.com/api/links/aliexpress";

function fail(code) {
  const error = new Error(code);
  error.code = code;
  throw error;
}

function cleanQuery(value) {
  return value.replace(/[\u0000-\u001f]/g, " ").replace(/\s+/g, " ").trim().slice(0, 200);
}

function isAliExpressHost(hostname) {
  const host = hostname.toLowerCase().replace(/\.$/, "");
  return host === "aliexpress.com"
    || host === "aliexpress.ru"
    || host.endsWith(".aliexpress.com")
    || host.endsWith(".aliexpress.ru");
}

function isAmazonComHost(hostname) {
  const host = hostname.toLowerCase().replace(/\.$/, "");
  if (host === "amzn.to" || host === "a.co" || host.endsWith(".amzn.to")) return "short";
  if (host === "amazon.com" || host.endsWith(".amazon.com")) return "amazon";
  return null;
}

/** @returns {"amazon" | "aliexpress" | "unknown"} */
export function detectLinkMode(input) {
  const raw = String(input || "").trim();
  if (!raw) return "unknown";
  if (!/^https?:\/\//i.test(raw)) return "amazon";
  let uri;
  try {
    uri = new URL(raw);
  } catch {
    return "unknown";
  }
  if (uri.protocol !== "https:" && uri.protocol !== "http:") return "unknown";
  if (isAliExpressHost(uri.hostname)) return "aliexpress";
  const amazon = isAmazonComHost(uri.hostname);
  if (amazon === "amazon") return "amazon";
  if (amazon === "short") return "unknown";
  return "unknown";
}

export function amazonLink(input, tag) {
  const raw = String(input || "").trim();
  const associateTag = String(tag || "").trim();
  if (!raw) fail("empty");
  if (!associateTag) fail("empty");

  if (!/^https?:\/\//i.test(raw)) {
    const query = cleanQuery(raw);
    if (query.length < 2) fail("query");
    const search = new URL("https://www.amazon.com/s");
    search.searchParams.set("k", query);
    search.searchParams.set("tag", associateTag);
    return search.toString();
  }

  let uri;
  try {
    uri = new URL(raw);
  } catch {
    fail("page");
  }
  if (uri.protocol !== "https:" && uri.protocol !== "http:") fail("page");

  const amazon = isAmazonComHost(uri.hostname);
  if (amazon === "short") fail("short");
  if (amazon !== "amazon") fail("region");

  const asin = (uri.pathname.match(ASIN_RE) || [])[1];
  if (asin) {
    const product = new URL(`https://www.amazon.com/dp/${asin.toUpperCase()}`);
    product.searchParams.set("tag", associateTag);
    return product.toString();
  }

  const keywords = uri.searchParams.get("k");
  if ((uri.pathname === "/s" || uri.pathname === "/s/") && keywords) {
    const query = cleanQuery(keywords);
    if (query.length < 2) fail("query");
    const search = new URL("https://www.amazon.com/s");
    search.searchParams.set("k", query);
    const department = uri.searchParams.get("i") || "";
    if (/^[a-z0-9-]{1,40}$/i.test(department)) search.searchParams.set("i", department);
    search.searchParams.set("tag", associateTag);
    return search.toString();
  }

  fail("page");
}

export function canonicalAliExpressUrl(input) {
  const raw = String(input || "").trim();
  if (!raw) fail("empty");
  let uri;
  try {
    uri = new URL(raw);
  } catch {
    fail("ali_page");
  }
  if (uri.protocol !== "https:" && uri.protocol !== "http:") fail("ali_page");
  if (!isAliExpressHost(uri.hostname)) fail("ali_page");
  const id = (uri.pathname.match(ALI_ITEM_RE) || [])[1];
  if (!id) fail("ali_page");
  return `https://www.aliexpress.com/item/${id}.html`;
}

function resolveAliEndpoint(root) {
  const fromData = (root.dataset.aliEndpoint || "").trim();
  if (fromData) return fromData;
  if (typeof location === "undefined") return "";
  if (location.protocol === "file:") return LOCAL_ALI_API;
  const host = location.hostname;
  if (host === "localhost" || host === "127.0.0.1") {
    if (location.port === "3099") {
      return new URL("/api/links/aliexpress", location.origin).href;
    }
    return LOCAL_ALI_API;
  }
  if (host.endsWith("github.io")) {
    return DEFAULT_ALI_API;
  }
  return "";
}

async function aliExpressLink(sourceUrl, endpoint) {
  if (!endpoint) fail("ali_no_api");
  let res;
  try {
    res = await fetch(`${endpoint}?url=${encodeURIComponent(sourceUrl)}`, {
      method: "GET",
      credentials: "omit",
      mode: "cors",
    });
  } catch {
    fail("ali_fetch");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok || !data.affiliateUrl) {
    throw new Error(data.error || "AliExpress link service failed.");
  }
  return data.affiliateUrl;
}

function paintYield() {
  return new Promise((resolve) => {
    requestAnimationFrame(() => requestAnimationFrame(resolve));
  });
}

function boot() {
  if (typeof document === "undefined") return;
  const root = document.querySelector("[data-link-tool]");
  const stringsNode = document.getElementById("link-strings");
  if (!root || !stringsNode) return;

  const copy = JSON.parse(stringsNode.textContent);
  const tag = root.dataset.tag || "";
  const aliEndpoint = resolveAliEndpoint(root);
  const form = document.getElementById("link-form");
  const input = document.getElementById("link-input");
  const status = document.getElementById("link-status");
  const result = document.getElementById("link-result");
  const out = document.getElementById("link-out");
  const open = document.getElementById("link-open");
  const copyButton = document.getElementById("link-copy");
  const kicker = document.getElementById("link-kicker");
  const disclose = document.getElementById("link-disclose");
  const note = document.getElementById("link-note");
  const openIcon = document.getElementById("link-open-icon");
  const openLabel = document.getElementById("link-open-label");
  const storeIcons = {
    amazon: root.dataset.iconAmazon || "",
    aliexpress: root.dataset.iconAli || "",
  };

  if (note && copy.autoNote) note.textContent = copy.autoNote;
  if (input && copy.placeholder) input.placeholder = copy.placeholder;

  function setStatus(text, kind) {
    status.textContent = text || "";
    status.className = "status" + (kind ? " " + kind : "");
  }

  function showResult(link, discloseText, openLabelText, mode) {
    kicker.textContent = copy.kicker;
    out.textContent = link;
    disclose.textContent = discloseText;
    open.href = link;
    const icon = storeIcons[mode] || "";
    if (openIcon) {
      openIcon.hidden = !icon;
      if (icon) openIcon.src = icon;
    }
    if (openLabel) openLabel.textContent = openLabelText;
    else open.textContent = openLabelText;
    copyButton.textContent = copy.copy;
    result.hidden = false;
  }

  copyButton.addEventListener("click", async () => {
    const value = out.textContent;
    if (!value) return;
    const label = copyButton.textContent;
    try {
      await navigator.clipboard.writeText(value);
      copyButton.textContent = copy.copied;
    } catch {
      copyButton.textContent = copy.copyFail;
    }
    setTimeout(() => { copyButton.textContent = label; }, 1400);
  });

  const submitButton = form.querySelector('button[type="submit"]');

  function setWorking(on) {
    form.setAttribute("aria-busy", on ? "true" : "false");
    if (input) input.readOnly = on;
    if (submitButton) {
      submitButton.disabled = on;
      submitButton.classList.toggle("is-busy", on);
    }
    if (on && copy.working) {
      setStatus(copy.working, "busy");
    }
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const value = input.value.trim();
    result.hidden = true;
    setStatus("");

    const mode = detectLinkMode(value);
    if (mode === "unknown") {
      if (/^https?:\/\//i.test(value) && (value.includes("amzn.to") || value.includes("a.co/"))) {
        setStatus(copy.err_short, "warn");
        return;
      }
      setStatus(copy.err_unknown, "warn");
      return;
    }

    setWorking(true);
    await paintYield();

    try {
      if (mode === "aliexpress") {
        const link = await aliExpressLink(canonicalAliExpressUrl(value), aliEndpoint);
        showResult(link, copy.aliDisclose, copy.openAli, "aliexpress");
        setStatus(copy.readyAli, "ok");
        return;
      }

      const link = amazonLink(value, tag);
      showResult(link, copy.amazonDisclose, copy.openAmazon, "amazon");
      setStatus(copy.readyAmazon, "ok");
    } catch (error) {
      const code = error && error.code;
      const message = code && copy["err_" + code]
        ? copy["err_" + code]
        : (error.message || copy.err_page);
      setStatus(message, "warn");
    } finally {
      setWorking(false);
    }
  });
}

boot();
