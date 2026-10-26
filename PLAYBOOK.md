# First revenue: what to do this week

ClientBridge has $0 revenue and running costs. The product works. What's
missing is people paying, so for the next 30 days **every hour goes to selling,
not building**, and anything that costs money has to pay for itself first.

**Target for 30 days:** 5 paying workspaces. At ~3 users on Starter that's
about USD 225 a month, plus setup fees (below). The first customers matter
more for proof, referrals and a case study than for the money itself.

---

## Day 1: remove what blocks a sale (about 1 hour, $0)

1. **Email in production.** Invites and password resets fail today. Create a
   new Resend API key, set `RESEND_API_KEY` and a real `EMAIL_FROM_ADDRESS` on
   Railway, then send yourself a password reset to check it works. A customer
   who can't invite their team won't pay for seats.
2. **Accept bank transfer.** Manual provisioning already works. From today,
   offer "pago por transferencia o QR" to anyone in Paraguay who won't pay by
   international card, and set their plan by hand in Strapi.
3. **Check what you spend.** Open Railway → Usage and the Vercel and Sentry
   billing pages, and write down the monthly total. Turn off anything that
   doesn't serve a customer (preview environments, extra services, paid tiers
   you don't use). That total is the number the first customers have to cover.

## Days 1–3: sell to people who already know you ($0)

The fastest first sale is someone who already trusts you. Write by hand,
one at a time, from your own phone, to every business owner you know:
family, friends, former clients, clients of past projects. This isn't cold
outreach: it's you talking to people you know. Never use the bot or the
bridge for it.

> Hola Laura, ¿cómo estás? Lancé ClientBridge, un sistema para negocios que
> venden por WhatsApp: cada chat queda guardado como cliente, todo el equipo
> lo ve y desde ahí se hacen las facturas. Estoy buscando los primeros 10
> negocios para configurárselo yo mismo. ¿Te muestro en 10 minutos cómo se
> vería con tu negocio? Si no es para ti, ¿se te ocurre alguien a quien le sirva?

Goal: 30 messages, 10 conversations, 5 demos, 2–3 customers.

## The offer: "te lo configuro yo"

Sell the result, not the software:

| | |
|---|---|
| **Paid setup**, one-time | You connect their number, import their contacts, set up products and the bot menu, and train the team in a 1-hour call. Charge for it (e.g. the price of one month for the whole team). Revenue on day one, and customers who are set up properly don't leave. |
| **Founding-customer price** for the first 10 | Business features at the Starter price (USD 15 per user) for 6 months, in exchange for a testimonial and a referral. Say it's for the first 10, and mean it. |
| **Quote in guaraníes** | Convert at the day's rate and round. Local businesses think in Gs. |

Show the product with the live demo on your phone (`/demo`, and
`/demo/try-bot` where they play the customer of the bot). Then pair their
number in the same meeting, so they leave already using it.

## Week 1–2: Harvey for cold email ($0–15)

Set up `outbound/` on your PC (`outbound/clientbridge/README.md`).

- Today: install it, run `discover` + `profile` (free) and `export`. That gives
  you a list of businesses that sell on WhatsApp, with the reason for each,
  **before you send a single email**. Call or visit the ten best ones
  yourself this week.
- At the same time, start the sending mailbox (a separate Gmail is $0; your own
  domain is better). Harvey keeps cold email off for 14 days while it warms
  up, then ramps from 5 to 30 a day. Approve every email yourself.
- First cohort: `WHATSAPP_CONTACT` and no `INCUMBENT_CHAT_TOOL`, in
  real estate, distributors and shops in Gran Asunción.

## Week 2–4: other channels that cost nothing

- **Partners.** Find 3 web agencies and 3 accountants (estudios contables) whose
  clients sell on WhatsApp. Offer 20% of what their referrals pay, for as long
  as the referred customer pays. One agency can bring 10 customers.
- **Instagram (@clientbridgecrm2026).** Three short Spanish reels a week:
  - "¿Se te pierden los chats?" (the chat → contact → invoice flow);
  - the bot answering after hours;
  - a real customer, once you have one.
- **Your own WhatsApp.** Your ClientBridge number answers with the auto-reply
  bot, so anyone who writes meets the product.
- **Every customer brings one.** At the 2-week check-in, ask: "¿A quién más le
  serviría esto?"

## What not to do this month

- No new features unless a paying customer, or one about to pay, asks for it.
- No paid ads until 3 customers have paid and you know what they bought it for.
- No paid tools whose cost isn't covered by revenue first.
- No cold WhatsApp messages to strangers, ever (ban risk for every workspace on the bridge).

## Track it (Monday, 10 minutes)

| Week | Messages | Conversations | Demos | Setups paid | Paying workspaces | MRR |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |

If a week ends with demos but no sales, the problem is the offer or the
price: ask the ones who said no why. If it ends without demos, the problem
is volume: send more.
