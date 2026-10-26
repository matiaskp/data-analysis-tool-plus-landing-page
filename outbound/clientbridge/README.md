# Harvey for ClientBridge: setup on your PC

Harvey finds small businesses in Paraguay that sell over WhatsApp, writes them
short cold emails in Spanish (tú), sends them only after you approve each one,
and drafts answers to replies. Everything runs on your machine; nothing here
touches ClientBridge production.

What this fork adds to upstream Harvey (ethanplusai/harvey, MIT):

- `locale: {language: es, country: PY}`: Spanish searches (DataForSEO, Serper),
  Spanish writing rules (`skills/locale_es.md`), and Spanish opt-outs
  ("no, gracias", "baja", "no me escribas"…), which are always honoured.
- A pre-send gate that blocks "usted", voseo and Spanish AI clichés.
- New free signals: `WHATSAPP_CONTACT`, `WHATSAPP_NUMBERS`,
  `INCUMBENT_CHAT_TOOL` (Kommo, Leadsales, Whaticket…), `ECOM_PLATFORM`
  (Tiendanube, Shopify, WooCommerce…), `INSTAGRAM_LINKED`.
- OpenStreetMap discovery that understands our industries in Spanish
  (inmobiliaria, distribuidora, concesionaria, clínica, estética…).
- ClientBridge config, product facts and competitor notes in this folder.

## What it costs

| | Cheapest | Recommended |
|---|---|---|
| Model | your Claude Pro/Max subscription | same |
| Finding businesses | OpenStreetMap: $0 | + DataForSEO Google Maps, ~$0.002 a search ($1 free credit covers a first run) |
| Email verification | Reoon free tier: 600/month, $0 | same |
| Sending mailbox | a new, separate Gmail account: $0 | a second domain (~$10/year) + Google Workspace (~$7/month) |
| Warmup | Harvey's built-in slow ramp: $0 | a warmup service (optional) |

**$0 is possible.** The paid options only buy reach and inbox placement.
Don't send cold email from clientbridge-crm.com or your personal address.

## 1. Install (once)

You need Python 3.11+ and the Claude Code CLI logged in (`claude login`).

**Windows (PowerShell):**
```powershell
git clone https://github.com/matiaskp/data-analysis-tool-plus-landing-page.git growth
cd growth\outbound
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python clientbridge\setup_clientbridge.py
```

**macOS / Linux:**
```bash
git clone https://github.com/matiaskp/data-analysis-tool-plus-landing-page.git growth
cd growth/outbound
python3.13 -m venv .venv && source .venv/bin/activate
pip install -e .
python clientbridge/setup_clientbridge.py
```

The setup script writes `harvey.local.yaml` and the product files into
`skills/`, then lists what you still have to fill in.

## 2. Fill in `harvey.local.yaml`

Open it and replace every `CHANGE_ME`:

- `persona.name`: your first name, as you sign.
- `persona.email`: the sending mailbox (step 3).
- `compliance.postal_address`: a real address where you receive mail (Ley 7593/2025).
- `channels.email.warmup.start_date`: today's date, the day the mailbox starts.

Run `python clientbridge/setup_clientbridge.py` again: it says "complete" when you're done.

## 3. Mailbox and keys (`.env`)

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

- **Gmail:** create a Google Cloud OAuth client (Desktop app), put
  `GMAIL_CLIENT_ID` / `GMAIL_CLIENT_SECRET` in `.env`, then run `harvey gmail auth`
  and log in with the **sending** account. `harvey gmail test` checks it.
- **Reoon** (free, 600 checks a month): `REOON_API_KEY`. Without a verifier,
  every address stays a "guess" and Harvey never sends to it.
- Optional: `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` for Google Maps discovery.

If you use your own domain: `harvey warmup yourdomain.com` checks SPF, DKIM and DMARC.

## 4. Find and read businesses

```bash
harvey signals --confirm free           # turn on every free signal
harvey discover --estimate              # what it will search, and the cost
harvey discover                         # free OpenStreetMap
harvey discover --provider dataforseo_maps --max-spend 1.00   # optional, wider
harvey profile                          # read their websites (free)
harvey dashboard                        # open the printed link
```

In the dashboard's **Signals** tab, build the first cohort:

> **Must have** `WHATSAPP_CONTACT` · **Must not have** `INCUMBENT_CHAT_TOOL`

Then add `RUNNING_META_ADS` (they pay for ads that end in WhatsApp) or
`WHATSAPP_NUMBERS ≥ 2` (a team on several numbers) for the sharpest lists.

`harvey export` writes the deliverable contacts to a CSV, which is useful even
before you send anything: call or visit the best ten yourself.

## 5. Write, approve, send

```bash
harvey run          # the loop: writes sequences, waits for you, sends, reads replies
```

Every email waits in the dashboard's **Outbox** (`A` approve, `E` edit, `R` reject).
Read the first 20 carefully. If something sounds off, edit
`skills/locale_es.md` or `skills/product_knowledge.md`; the next cycle uses it.
Leave autopilot off for the first month.

When someone replies interested: answer from the Outbox, or move them to
WhatsApp with your ClientBridge number (they meet the product there), and add
them as a deal in a ClientBridge workspace of your own (never the Demo
Workspace). Add every new customer's domain to `compliance.do_not_contact`.

## Rules that stay on

- Email only for first contact. Never cold-message anyone on WhatsApp.
- Product facts come from `skills/product_knowledge.md`, which lists what is
  live. AI replies, the Cloud API, SIFEN and broadcasts are **not** live: never sell them.
- Opt-outs are permanent. The bounce kill switch is at 3%.

## Updating Harvey from upstream

From the repository root:
```bash
git subtree pull --prefix outbound https://github.com/ethanplusai/harvey main --squash
```
Then run `pytest` inside `outbound/`.
