"""Selling in Spanish: locale config, search language, the Spanish gate,
Spanish opt-outs, the locale skill, and the messaging signals."""

import pytest

from harvey.agents.handler import _opt_out_reason
from harvey.brain import Brain
from harvey.collectors import discover as D
from harvey.collectors import messaging as M
from harvey.config import ComplianceConfig, LocaleConfig
from harvey.gate import pre_send_check
from harvey.send_window import zone_for
from harvey.signals import SIGNAL_CATALOG


class _Cfg:
    """The parts of HarveyConfig build_queries reads."""

    class icp:
        industries = ["inmobiliaria"]
        geography = ["Asunción, Paraguay"]
        geo_coordinates = {}
        keyword_variants = {}

    class product:
        name = "Example CRM"

    locale = LocaleConfig(language="es", country="py")


def test_locale_defaults_to_english_and_normalises_codes():
    assert LocaleConfig().language == "en"
    loc = LocaleConfig(language=" ES ", country="py")
    assert (loc.language, loc.country) == ("es", "PY")
    with pytest.raises(ValueError):
        LocaleConfig(language="spanish")
    with pytest.raises(ValueError):
        LocaleConfig(country="PRY")


def test_queries_carry_the_market_language_and_country():
    (q,) = D.build_queries(_Cfg)
    assert (q.language, q.country) == ("es", "PY")
    assert q.keyword() == "inmobiliaria Asunción, Paraguay"


def test_a_paraguayan_place_resolves_to_asuncion_time():
    assert zone_for("Asunción, Paraguay") == "America/Asuncion"


@pytest.mark.parametrize("body", [
    "Hola Carla, ¿usted maneja las consultas de la web?",
    "Hola Carla, ¿tenés un minuto esta semana?",
    "Si te interesa, escribinos y te mostramos.",
])
def test_gate_rejects_usted_and_voseo(body):
    result = pre_send_check("carla@inmobiliaria.example", "los chats", body)
    assert not result.ok
    assert any("register" in r for r in result.reasons)


def test_gate_accepts_tu_and_ustedes():
    body = "Hola Carla, ¿cómo manejan hoy ustedes las consultas que llegan por WhatsApp?"
    assert pre_send_check("carla@inmobiliaria.example", "los chats", body).ok


def test_gate_rejects_spanish_ai_tells():
    body = "Hola Carla, espero que te encuentres bien. ¿Cómo manejan las consultas?"
    result = pre_send_check("carla@inmobiliaria.example", "los chats", body)
    assert any("banned phrases" in r for r in result.reasons)


def test_spanish_opt_out_line_is_accepted():
    line = "¿No te interesa? Responde «no, gracias» y no te vuelvo a escribir."
    assert ComplianceConfig(opt_out_line=line).opt_out_line == line
    with pytest.raises(ValueError):
        ComplianceConfig(opt_out_line="Si no te interesa, avísame.")


@pytest.mark.parametrize("reply", [
    "No, gracias", "no gracias.", "Baja", "No me interesa",
    "Por favor dame de baja de esta lista", "No me escribas más",
    "Sácame de tu lista por favor",
])
def test_spanish_opt_outs_are_honoured(reply):
    assert _opt_out_reason(reply, reply) is not None


@pytest.mark.parametrize("reply", [
    "Sí, me interesa. ¿Cuánto cuesta para 3 usuarios?",
    "¿Lo quieres para el lunes, sí o no, gracias",
    "Hola, gracias por escribir. ¿Funciona con dos números?",
])
def test_ordinary_spanish_replies_are_not_opt_outs(reply):
    assert _opt_out_reason(reply, reply) is None


def test_spanish_locale_skill_frames_prospect_facing_agents(tmp_path):
    english = Brain(state=None)
    spanish = Brain(state=None, language="es")
    assert "Writing in Spanish" not in english.load_skills_for_agent("writer")
    for agent in ("writer", "handler"):
        assert "Writing in Spanish" in spanish.load_skills_for_agent(agent)
    assert "Writing in Spanish" not in spanish.load_skills_for_agent("scout")


# ── Messaging signals ────────────────────────────────────────────────

SHOP = """
<html><head><script src="https://d26lpennugtm8s.cloudfront.net/stores/001/x.js"></script></head>
<body>
<a href="https://wa.me/595981000001?text=Hola">Ventas</a>
<a href="https://api.whatsapp.com/send?phone=%2B595%20982%20000002">Soporte</a>
<a href="https://wa.me/0981000001">Ventas otra vez</a>
<a href="https://www.instagram.com/tienda.example/">Instagram</a>
<script src="https://code.tidio.co/abc.js"></script>
</body></html>
"""


def test_messaging_signals_from_a_shop_page():
    assert M.has_whatsapp_contact(SHOP)
    assert M.whatsapp_numbers(SHOP) == 2      # 0981000001 is +595 981 000001
    assert M.chat_tools(SHOP) == ["Tidio"]
    assert M.ecom_platforms(SHOP) == ["Tiendanube"]
    assert M.has_instagram(SHOP)


def test_a_whatsapp_call_to_action_counts_without_a_link():
    assert M.has_whatsapp_contact("<p>Escríbenos por WhatsApp al 0981 000 003</p>")
    assert M.has_whatsapp_contact('<div class="joinchat__button"></div>')


def test_a_page_that_only_mentions_whatsapp_does_not_count():
    page = ("<p>WhatsApp cambió sus políticas este año.</p>"
            '<a href="https://www.instagram.com/p/abc123/">post</a>')
    assert not M.has_whatsapp_contact(page)
    assert M.whatsapp_numbers(page) == 0
    assert not M.has_instagram(page)          # a post link isn't their profile
    assert M.chat_tools(page) == [] and M.ecom_platforms(page) == []


def test_messaging_signals_are_in_the_catalog():
    codes = {s["code"] for s in SIGNAL_CATALOG}
    assert {"WHATSAPP_CONTACT", "WHATSAPP_NUMBERS", "INCUMBENT_CHAT_TOOL",
            "ECOM_PLATFORM", "INSTAGRAM_LINKED"} <= codes


@pytest.mark.parametrize("term,tag", [
    ("inmobiliaria", "office=estate_agent"),
    ("distribuidora", "shop=wholesale"),
    ("concesionaria de autos", "shop=car"),
    ("clínica odontológica", "amenity=dentist"),
    ("centro de estética", "shop=beauty"),
    ("agencia de viajes", "shop=travel_agency"),
])
def test_openstreetmap_understands_spanish_industries(term, tag):
    assert tag in D.OpenStreetMap()._tags(term)


@pytest.mark.asyncio
async def test_profiling_records_the_messaging_signals(tmp_path):
    import os
    from harvey.collectors.profile import ProfileCollector
    from harvey.models.company import Company
    from harvey.signals import seed_signal_catalog
    from harvey.state import StateManager

    state = StateManager(os.path.join(tmp_path, "t.db"))
    await state.init_db()
    await seed_signal_catalog(state)
    wanted = {"WHATSAPP_CONTACT", "WHATSAPP_NUMBERS", "INCUMBENT_CHAT_TOOL",
              "ECOM_PLATFORM", "INSTAGRAM_LINKED"}
    for code in wanted:
        await state.set_signal_status(code, "confirmed")
    c = ProfileCollector.__new__(ProfileCollector)
    c.confirmed = await state.confirmed_signal_codes()
    c.site_names = {}
    c.state = state

    async def fake_get(url):
        return SHOP
    c._get = fake_get

    cid = await state.add_company(Company(name="Tienda", domain="tienda.example"))
    obs = {o["signal_code"]: o for o in await c.profile_company(cid, "tienda.example")}
    assert set(obs) == wanted
    assert obs["WHATSAPP_CONTACT"]["value_num"] == 1
    assert obs["WHATSAPP_NUMBERS"]["value_num"] == 2
    assert obs["INCUMBENT_CHAT_TOOL"]["value_text"] == "Tidio"
    assert obs["ECOM_PLATFORM"]["value_text"] == "Tiendanube"
