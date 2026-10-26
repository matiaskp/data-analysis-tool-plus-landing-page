"""Messaging signals: whether a business sells over WhatsApp, and with what.

For a WhatsApp CRM, the best prospect is a business whose own site already
sends customers to WhatsApp: a wa.me link, a click-to-chat button, "write to
us on WhatsApp". How many numbers it lists says whether a team shares the
chats, and the chat or CRM tool it already embeds says who the incumbent is.

Pure functions over HTML the profile collector already downloaded: no extra
requests. Patterns match link targets, script hosts and widget names, not
ordinary words, so a page that merely mentions WhatsApp in a blog post
doesn't count.
"""

import re
from urllib.parse import unquote

# Links and widgets that open a WhatsApp chat with the business.
WHATSAPP_LINK_RE = re.compile(
    r"""(?:https?:)?//(?:wa\.me|api\.whatsapp\.com/send|web\.whatsapp\.com/send|"""
    r"""chat\.whatsapp\.com)[^"'\s<>]*|whatsapp://send[^"'\s<>]*""",
    re.IGNORECASE)
WHATSAPP_WIDGETS = (
    r"joinchat",                       # Joinchat (WordPress)
    r"click-to-chat|ht-ctc",           # Click to Chat (WordPress)
    r"wa-chat-widget|whatsapp-widget|wa_btn|wa-float|whatsapp-float|float-whatsapp",
    r"getbutton\.io",                  # GetButton chat widget
    r"elfsight\.com/whatsapp",
)
# "Write to us on WhatsApp" in Spanish (tú and voseo, since that's how
# Paraguayan and Argentine sites write it), Portuguese and English.
WHATSAPP_CTA_RE = re.compile(
    r"(?:escr[ií]b(?:enos|inos)|contact[aá](?:nos|enos)|consult[aá](?:nos|enos)|"
    r"habl[aá](?:nos|enos)|fale conosco|chat with us|message us|text us)"
    r"[^<]{0,40}whats\s?app",
    re.IGNORECASE)
_PHONE_PARAM_RE = re.compile(r"(?:wa\.me/|phone=)\+?(\d[\d\s\-().]{6,})", re.IGNORECASE)

# Chat / CRM tools a business might already use for WhatsApp: the incumbent.
CHAT_TOOLS: dict[str, tuple[str, ...]] = {
    "Kommo": (r"kommo\.com", r"amocrm\.(?:com|ru)", r"gso\.amocrm"),
    "Leadsales": (r"leadsales\.(?:io|services)",),
    "Whaticket": (r"whaticket\.com",),
    "Cliengo": (r"cliengo\.com", r"s\.cliengo"),
    "Mercately": (r"mercately\.com",),
    "Wati": (r"wati\.io",),
    "Callbell": (r"callbell\.eu",),
    "Treble": (r"treble\.ai",),
    "Botmaker": (r"botmaker\.com",),
    "Tidio": (r"code\.tidio\.co",),
    "HubSpot": (r"js\.hs-scripts\.com", r"js\.hsforms\.net"),
    "Zoho": (r"salesiq\.zoho", r"zohopublic"),
    "Respond.io": (r"respond\.io",),
    "ManyChat": (r"manychat\.com",),
    "Chatwoot": (r"chatwoot",),
}

# Online-store platforms: a shop that also answers on WhatsApp is the
# storefront-webhook prospect.
ECOM_PLATFORMS: dict[str, tuple[str, ...]] = {
    "Tiendanube": (r"tiendanube\.com", r"nuvemshop", r"mitiendanube\.com", r"d26lpennugtm8s\.cloudfront\.net"),
    "Shopify": (r"cdn\.shopify\.com", r"myshopify\.com"),
    "WooCommerce": (r"woocommerce", r"wc-ajax"),
    "VTEX": (r"vteximg\.com", r"vtexassets\.com", r"\.vtex\.com"),
    "Wix Stores": (r"wixstores", r"wix-ecommerce"),
    "Jumpseller": (r"jumpseller",),
    "Magento": (r"mage/cookies", r"Magento_"),
    "PrestaShop": (r"prestashop",),
}

INSTAGRAM_RE = re.compile(r"""https?://(?:www\.)?instagram\.com/(?!p/|reel/|explore/)[A-Za-z0-9_.]{2,}""",
                          re.IGNORECASE)


def whatsapp_links(html: str) -> list[str]:
    return WHATSAPP_LINK_RE.findall(html or "")


def has_whatsapp_contact(html: str) -> bool:
    """The site offers a WhatsApp chat: a link, a chat widget, or a call to action."""
    html = html or ""
    return bool(whatsapp_links(html)
                or any(re.search(p, html, re.IGNORECASE) for p in WHATSAPP_WIDGETS)
                or WHATSAPP_CTA_RE.search(html))


def whatsapp_numbers(html: str) -> int:
    """How many distinct WhatsApp numbers the site's chat links open.

    Compared on their last eight digits, so "+595 981 123456" and
    "0981123456" are one number.
    """
    seen = set()
    for link in whatsapp_links(html):
        m = _PHONE_PARAM_RE.search(unquote(link))
        if m:
            digits = re.sub(r"\D", "", m.group(1))
            if len(digits) >= 7:
                seen.add(digits[-8:])
    return len(seen)


def _match_table(html: str, table: dict[str, tuple[str, ...]]) -> list[str]:
    html = html or ""
    return sorted(name for name, patterns in table.items()
                  if any(re.search(p, html, re.IGNORECASE) for p in patterns))


def chat_tools(html: str) -> list[str]:
    return _match_table(html, CHAT_TOOLS)


def ecom_platforms(html: str) -> list[str]:
    return _match_table(html, ECOM_PLATFORMS)


def has_instagram(html: str) -> bool:
    return bool(INSTAGRAM_RE.search(html or ""))
