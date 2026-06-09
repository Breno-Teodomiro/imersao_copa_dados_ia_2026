import random
import streamlit as st
import db

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="⚽",
    layout="wide",
)

# ── Dados ─────────────────────────────────────────────────────────────────────

GROUPS: dict[str, list[str]] = {
    "A": ["México", "África do Sul", "Coreia do Sul", "Tchéquia"],
    "B": ["Canadá", "Bósnia e Herzegovina", "Catar", "Suíça"],
    "C": ["Brasil", "Marrocos", "Escócia", "Haiti"],
    "D": ["Estados Unidos", "Paraguai", "Turquia", "Austrália"],
    "E": ["Alemanha", "Curaçao", "Costa do Marfim", "Equador"],
    "F": ["Países Baixos", "Japão", "Suécia", "Tunísia"],
    "G": ["Bélgica", "Egito", "Irã", "Nova Zelândia"],
    "H": ["Espanha", "Cabo Verde", "Arábia Saudita", "Uruguai"],
    "I": ["França", "Senegal", "Iraque", "Noruega"],
    "J": ["Argentina", "Argélia", "Áustria", "Jordânia"],
    "K": ["Portugal", "Rep. Dem. do Congo", "Uzbequistão", "Colômbia"],
    "L": ["Inglaterra", "Croácia", "Gana", "Panamá"],
}

# Código ISO 3166-1 (flagcdn.com) para imagem de bandeira de cada seleção
CODES: dict[str, str] = {
    "México": "mx", "África do Sul": "za", "Coreia do Sul": "kr", "Tchéquia": "cz",
    "Canadá": "ca", "Bósnia e Herzegovina": "ba", "Catar": "qa", "Suíça": "ch",
    "Brasil": "br", "Marrocos": "ma", "Escócia": "gb-sct", "Haiti": "ht",
    "Estados Unidos": "us", "Paraguai": "py", "Turquia": "tr", "Austrália": "au",
    "Alemanha": "de", "Curaçao": "cw", "Costa do Marfim": "ci", "Equador": "ec",
    "Países Baixos": "nl", "Japão": "jp", "Suécia": "se", "Tunísia": "tn",
    "Bélgica": "be", "Egito": "eg", "Irã": "ir", "Nova Zelândia": "nz",
    "Espanha": "es", "Cabo Verde": "cv", "Arábia Saudita": "sa", "Uruguai": "uy",
    "França": "fr", "Senegal": "sn", "Iraque": "iq", "Noruega": "no",
    "Argentina": "ar", "Argélia": "dz", "Áustria": "at", "Jordânia": "jo",
    "Portugal": "pt", "Rep. Dem. do Congo": "cd", "Uzbequistão": "uz", "Colômbia": "co",
    "Inglaterra": "gb-eng", "Croácia": "hr", "Gana": "gh", "Panamá": "pa",
}

# Chaveamento R32 (bracket oficial FIFA 2026)
R32_TEMPLATE = [
    ("A1", "B2"), ("C1", "D2"), ("E1", "F2"), ("G1", "H2"),
    ("I1", "J2"), ("K1", "L2"), ("B1", "A2"), ("D1", "C2"),
    ("F1", "E2"), ("H1", "G2"), ("J1", "I2"), ("L1", "K2"),
    ("3rd_1", "3rd_2"), ("3rd_3", "3rd_4"), ("3rd_5", "3rd_6"), ("3rd_7", "3rd_8"),
]

ROUND_LABELS = {
    "r32": "16-avos de Final", "r16": "Oitavas de Final",
    "qf": "Quartas de Final", "sf": "Semifinal",
}


# ── Helpers de bandeira ───────────────────────────────────────────────────────

def flag_url(team: str, w: int = 40) -> str:
    code = CODES.get(team, "un")
    return f"https://flagcdn.com/w{w}/{code}.png"


def flag_img(team: str, w: int = 40) -> str:
    return (
        f'<img src="{flag_url(team, w)}" alt="Bandeira {team}" loading="lazy" '
        f'style="width:{w}px;height:auto;border-radius:4px;'
        f'box-shadow:0 2px 6px rgba(0,0,0,0.45);vertical-align:middle;display:inline-block;">'
    )


def build_r32_teams(picks: dict[str, tuple[str, str]]) -> list[tuple[str, str]]:
    """Resolve o chaveamento R32 com os times reais dos palpites do usuário."""
    thirds: list[str] = []
    for g, teams in GROUPS.items():
        first, second = picks.get(g, (teams[0], teams[1]))
        thirds += [t for t in teams if t != first and t != second]
    random.shuffle(thirds)
    selected_thirds = thirds[:8]

    resolved: list[tuple[str, str]] = []
    third_idx = 0
    for slot_a, slot_b in R32_TEMPLATE:
        def resolve(slot: str) -> str:
            nonlocal third_idx
            if slot.startswith("3rd"):
                t = selected_thirds[third_idx] if third_idx < len(selected_thirds) else "?"
                third_idx += 1
                return t
            grp, pos = slot[0], slot[1]
            first, second = picks.get(grp, (GROUPS[grp][0], GROUPS[grp][1]))
            return first if pos == "1" else second
        resolved.append((resolve(slot_a), resolve(slot_b)))
    return resolved


def next_round_matches(winners: list[str]) -> list[tuple[str, str]]:
    return [(winners[i], winners[i + 1]) for i in range(0, len(winners), 2)]


def collect_winners(round_key: str, matches: list[tuple[str, str]]) -> list[str]:
    """Lê os vencedores escolhidos com segurança (nunca retorna None)."""
    winners: list[str] = []
    for i, (ta, _tb) in enumerate(matches):
        choice = st.session_state.get(f"{round_key}_{i}") or ta
        winners.append(choice)
    return winners


# ── CSS Premium ───────────────────────────────────────────────────────────────

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.stApp {
    background:
        radial-gradient(1200px 600px at 80% -10%, rgba(0,212,106,0.10), transparent),
        radial-gradient(900px 500px at 0% 0%, rgba(255,184,0,0.06), transparent),
        linear-gradient(160deg, #070B14 0%, #0B1322 55%, #070B14 100%);
}
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 2rem; max-width: 1280px; }

/* ── Hero ── */
.hero {
    position: relative;
    background:
        linear-gradient(135deg, rgba(0,61,32,0.95) 0%, rgba(0,100,64,0.95) 35%, rgba(0,168,84,0.92) 65%, rgba(255,184,0,0.92) 110%);
    border-radius: 24px;
    padding: 44px 48px;
    margin-bottom: 4px;
    text-align: center;
    overflow: hidden;
    box-shadow: 0 12px 50px rgba(0,212,106,0.22), inset 0 1px 0 rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.08);
}
.hero::after {
    content: "⚽";
    position: absolute; font-size: 220px; opacity: 0.06;
    right: -30px; top: -50px; transform: rotate(-15deg);
}
.hero h1 {
    font-size: 2.7rem; font-weight: 900; color: #fff; margin: 0;
    letter-spacing: -1.2px; text-shadow: 0 3px 16px rgba(0,0,0,0.35);
}
.hero p { font-size: 1.05rem; color: rgba(255,255,255,0.9); margin: 10px 0 0; font-weight: 500; }

/* ── Step pills ── */
.steps { display:flex; flex-wrap:wrap; gap:6px; margin:18px 0 24px; }
.pill {
    display:inline-flex; align-items:center; gap:5px;
    background:#10182A; border:1px solid #1F2A40; border-radius:99px;
    padding:7px 16px; font-size:0.78rem; font-weight:600; color:#5C6B85;
    transition: all .25s;
}
.pill.active {
    background:linear-gradient(90deg,#006400,#00A854);
    border-color:#00D46A; color:#fff;
    box-shadow:0 4px 16px rgba(0,212,106,0.35);
}
.pill.done { background:#0A2417; border-color:#00643f; color:#00D46A; }

/* ── Group card ── */
.gcard {
    background: linear-gradient(160deg, #111A2C, #0D1422);
    border:1px solid #1E2A40; border-radius:18px; overflow:hidden;
    box-shadow:0 6px 24px rgba(0,0,0,0.4);
    transition: transform .2s, box-shadow .2s, border-color .2s;
}
.gcard:hover { transform:translateY(-3px); box-shadow:0 10px 34px rgba(0,212,106,0.16); border-color:#2A3A56; }
.ghead {
    background:linear-gradient(90deg,#00D46A,#00A854);
    color:#06140C; font-weight:800; font-size:0.82rem; letter-spacing:1.5px;
    padding:11px 18px; text-transform:uppercase;
    display:flex; align-items:center; gap:8px;
}
.trow {
    display:flex; align-items:center; gap:13px; padding:11px 18px;
    border-bottom:1px solid #18223A; font-size:0.96rem; color:#DCE3EE; font-weight:500;
}
.trow:last-child { border-bottom:none; }
.trow:hover { background:rgba(0,212,106,0.05); }

/* ── Knockout match ── */
.komatch {
    background:linear-gradient(160deg,#111A2C,#0D1422);
    border:1px solid #1E2A40; border-radius:16px; padding:14px 16px 4px;
    box-shadow:0 5px 20px rgba(0,0,0,0.38);
}
.konum { font-size:0.7rem; font-weight:700; color:#FFB800; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; }
.koteams { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:10px; }
.koteam { display:flex; flex-direction:column; align-items:center; gap:6px; flex:1; }
.koteam span { font-size:0.82rem; font-weight:600; color:#DCE3EE; text-align:center; line-height:1.2; }
.kovs { font-size:0.75rem; font-weight:800; color:#5C6B85; padding:0 4px; }

/* ── Final showdown ── */
.finalist {
    text-align:center; padding:34px 24px;
    background:linear-gradient(160deg,#111A2C,#0D1422);
    border:2px solid #1E2A40; border-radius:22px;
    box-shadow:0 8px 30px rgba(0,0,0,0.4);
}
.finalist .name { font-size:1.35rem; font-weight:800; color:#fff; margin-top:16px; }

/* ── Buttons ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background:linear-gradient(90deg,#00D46A,#00A854) !important;
    color:#06140C !important; font-weight:800 !important;
    border:none !important; border-radius:14px !important;
    padding:13px 38px !important; font-size:1.02rem !important;
    box-shadow:0 6px 24px rgba(0,212,106,0.32) !important; transition:all .2s !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform:translateY(-2px) !important; box-shadow:0 9px 32px rgba(0,212,106,0.5) !important;
}
div[data-testid="stButton"] > button[kind="secondary"] {
    background:#111A2C !important; border:1px solid #2A3A56 !important;
    color:#DCE3EE !important; border-radius:12px !important; font-weight:600 !important;
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input, div[data-baseweb="select"] > div {
    background:#0D1422 !important; border:1px solid #1E2A40 !important;
    border-radius:11px !important; color:#DCE3EE !important;
}
div[data-testid="stTextInput"] input:focus { border-color:#00D46A !important; box-shadow:0 0 0 3px rgba(0,212,106,0.18) !important; }

/* ── Segmented control (escolha do vencedor) ── */
div[data-testid="stSegmentedControl"] button {
    border-radius:10px !important; font-weight:600 !important;
}
div[data-testid="stSegmentedControl"] button[aria-checked="true"],
div[data-testid="stSegmentedControl"] button[kind="segmented_controlActive"] {
    background:linear-gradient(90deg,#006400,#00A854) !important; color:#fff !important;
    border-color:#00D46A !important;
}

/* ── Progress ── */
div[data-testid="stProgress"] > div > div { background:linear-gradient(90deg,#00D46A,#FFB800) !important; }

/* ── Alerts arredondados ── */
div[data-testid="stAlert"] { border-radius:13px !important; }

/* ── Acessibilidade: foco visível ── */
:focus-visible { outline:3px solid #00D46A !important; outline-offset:3px !important; border-radius:6px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:8px; height:8px; }
::-webkit-scrollbar-track { background:#070B14; }
::-webkit-scrollbar-thumb { background:#1E2A40; border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:#00A854; }
</style>
""")


# ── Session state ─────────────────────────────────────────────────────────────

st.session_state.setdefault("step", 1)
st.session_state.setdefault("participant_id", None)
st.session_state.setdefault("participant_name", None)
st.session_state.setdefault("error", None)
st.session_state.setdefault("group_picks", {})
st.session_state.setdefault("r32_teams", [])
st.session_state.setdefault("r32_winners", [])
st.session_state.setdefault("r16_winners", [])
st.session_state.setdefault("qf_winners", [])
st.session_state.setdefault("sf_winners", [])
st.session_state.setdefault("champion", None)


# ── Componentes ───────────────────────────────────────────────────────────────

def render_hero() -> None:
    st.html("""
    <div class="hero" role="banner">
        <h1>⚽ Bolão Copa do Mundo 2026</h1>
        <p>🇨🇦 🇲🇽 🇺🇸 &nbsp;·&nbsp; 48 seleções &nbsp;·&nbsp; 12 grupos &nbsp;·&nbsp; do grupo à final</p>
    </div>
    """)


def render_steps(current: int) -> None:
    steps = [
        (1, "Registro"), (2, "Grupos"), (3, "16-avos"), (4, "Oitavas"),
        (5, "Quartas"), (6, "Semifinal"), (7, "Final"), (8, "Concluído"),
    ]
    html = '<div class="steps" role="navigation" aria-label="Progresso">'
    for num, label in steps:
        if num < current:
            html += f'<span class="pill done" aria-label="{label} concluído">✓ {label}</span>'
        elif num == current:
            html += f'<span class="pill active" aria-current="step">{label}</span>'
        else:
            html += f'<span class="pill">{label}</span>'
    html += "</div>"
    st.html(html)


def render_group_card(group: str, teams: list[str]) -> None:
    rows = "".join(
        f'<div class="trow">{flag_img(t, 40)}<span>{t}</span></div>' for t in teams
    )
    st.html(f'<div class="gcard"><div class="ghead">🏆 Grupo {group}</div>{rows}</div>')


def render_ko_match(num: int, ta: str, tb: str) -> None:
    st.html(f"""
    <div class="komatch">
        <div class="konum">Partida {num}</div>
        <div class="koteams">
            <div class="koteam">{flag_img(ta, 56)}<span>{ta}</span></div>
            <div class="kovs">VS</div>
            <div class="koteam">{flag_img(tb, 56)}<span>{tb}</span></div>
        </div>
    </div>
    """)


# ── Step 1: Registro ──────────────────────────────────────────────────────────

def submit_registration() -> None:
    name = st.session_state.get("reg_name", "").strip()
    phone = st.session_state.get("reg_phone", "").strip()
    email = st.session_state.get("reg_email", "").strip()
    if not name or not phone or not email:
        st.session_state.error = "Preencha todos os campos."
        return
    if "@" not in email or "." not in email.split("@")[-1]:
        st.session_state.error = "Informe um e-mail válido."
        return
    try:
        if db.email_already_registered(email):
            st.session_state.error = "Este e-mail já está cadastrado."
            return
        pid = db.register_participant(name, phone, email)
        st.session_state.participant_id = pid
        st.session_state.participant_name = name
        st.session_state.error = None
        st.session_state.step = 2
    except ValueError as exc:
        st.session_state.error = str(exc)
    except Exception:
        st.session_state.error = "Erro de conexão. Tente novamente."


def render_step1() -> None:
    render_hero()
    render_steps(1)
    col_form, col_info = st.columns([1, 1], gap="large")

    with col_form:
        st.subheader(":material/person: Quem é você?")
        st.caption("Preencha seus dados para participar do bolão.")
        st.space("small")
        st.text_input("Nome completo", key="reg_name", placeholder="Ex: João Silva")
        st.text_input("Telefone", key="reg_phone", placeholder="(11) 99999-9999")
        st.text_input("E-mail", key="reg_email", placeholder="joao@email.com",
                      help="Usado para identificar seu bolão")
        if st.session_state.error:
            st.error(st.session_state.error, icon=":material/error:")
        st.space("small")
        st.button("Começar meu bolão →", type="primary", on_click=submit_registration)

    with col_info:
        st.subheader(":material/emoji_events: Como funciona")
        st.space("small")
        for icon, text in [
            (":material/groups:", "Palpite nos **12 grupos** — o 1º e 2º de cada"),
            (":material/sports_soccer:", "**Oitavas** — 32 times entram, 16 avançam"),
            (":material/bolt:", "**Quartas → Semi → Final** — até o campeão!"),
            (":material/military_tech:", "Os 8 melhores 3ºs entram por sorteio"),
        ]:
            with st.container(border=True):
                st.markdown(f"{icon} {text}")


# ── Step 2: Grupos ────────────────────────────────────────────────────────────

def submit_group_picks() -> None:
    picks: dict[str, tuple[str, str]] = {}
    for group, _teams in GROUPS.items():
        first = st.session_state.get(f"g_first_{group}")
        second = st.session_state.get(f"g_second_{group}")
        if not first or not second:
            st.session_state.error = f"Grupo {group}: selecione o 1º e 2º lugar."
            return
        if first == second:
            st.session_state.error = f"Grupo {group}: 1º e 2º não podem ser o mesmo time."
            return
        picks[group] = (first, second)
    try:
        db.save_picks(st.session_state.participant_id, picks)
        st.session_state.group_picks = picks
        st.session_state.r32_teams = build_r32_teams(picks)
        st.session_state.error = None
        st.session_state.step = 3
    except Exception as exc:
        st.session_state.error = f"Erro ao salvar: {exc}"


def render_step2() -> None:
    render_hero()
    render_steps(2)
    st.subheader(f":material/groups: Fase de grupos — olá, {st.session_state.participant_name}!")
    st.caption("Veja a bandeira de cada seleção e escolha quem termina em **1º** e **2º** em cada grupo.")
    st.space("small")

    items = list(GROUPS.items())
    for row in range(0, 12, 3):
        cols = st.columns(3, gap="medium")
        for c, col in enumerate(cols):
            idx = row + c
            if idx >= len(items):
                break
            group, teams = items[idx]
            with col:
                render_group_card(group, teams)
                st.space("small")
                first_val = st.session_state.get(f"g_first_{group}", teams[0])
                st.selectbox(f"🥇 1º lugar — Grupo {group}", options=teams,
                             key=f"g_first_{group}")
                second_opts = [t for t in teams if t != first_val]
                st.selectbox(f"🥈 2º lugar — Grupo {group}", options=second_opts,
                             key=f"g_second_{group}")
                st.space("small")
        st.space("small")

    if st.session_state.error:
        st.error(st.session_state.error, icon=":material/error:")
    st.space("medium")
    with st.container(horizontal_alignment="center"):
        st.button("Confirmar grupos → Oitavas", type="primary", on_click=submit_group_picks)


# ── Knockout genérico (Oitavas, Quartas, Semi) ────────────────────────────────

def render_knockout(step_num: int, round_key: str, matches: list[tuple[str, str]],
                    next_step: int) -> None:
    render_hero()
    render_steps(step_num)
    label = ROUND_LABELS[round_key]
    st.subheader(f":material/sports_soccer: {label}")
    st.caption("Toque na seleção que você acredita que **avança** em cada partida.")
    st.space("small")

    cols_per_row = 4 if len(matches) >= 8 else max(2, len(matches))
    for row in range(0, len(matches), cols_per_row):
        cols = st.columns(cols_per_row, gap="medium")
        for c, col in enumerate(cols):
            idx = row + c
            if idx >= len(matches):
                break
            ta, tb = matches[idx]
            with col:
                render_ko_match(idx + 1, ta, tb)
                key = f"{round_key}_{idx}"
                if st.session_state.get(key) not in (ta, tb):
                    st.session_state[key] = ta
                st.segmented_control(
                    f"Quem avança na partida {idx + 1}?",
                    options=[ta, tb],
                    key=key,
                    label_visibility="collapsed",
                )
        st.space("small")

    if st.session_state.error:
        st.error(st.session_state.error, icon=":material/error:")
    st.space("medium")

    def advance():
        winners = collect_winners(round_key, matches)
        try:
            db.save_knockout_picks(st.session_state.participant_id, round_key, winners)
            st.session_state[f"{round_key}_winners"] = winners
            st.session_state.error = None
            st.session_state.step = next_step
        except Exception as exc:
            st.session_state.error = f"Erro ao salvar: {exc}"

    with st.container(horizontal_alignment="center"):
        st.button(f"Confirmar {label} →", type="primary", on_click=advance)


# ── Step 6: Final ─────────────────────────────────────────────────────────────

def render_final() -> None:
    sf_winners = st.session_state.sf_winners
    if len(sf_winners) < 2:
        st.error("Erro: finalistas não definidos. Refaça o bolão.")
        return
    ta, tb = sf_winners[0], sf_winners[1]

    render_hero()
    render_steps(7)
    st.subheader(":material/emoji_events: A Grande Final!")
    st.caption("Chegou a hora — quem será o **Campeão do Mundo 2026**?")
    st.space("medium")

    c1, c2, c3 = st.columns([2, 1, 2], gap="large")
    with c1:
        st.html(f'<div class="finalist">{flag_img(ta, 160)}<div class="name">{ta}</div></div>')
    with c2:
        st.html('<div style="display:flex;align-items:center;justify-content:center;height:100%;'
                'font-size:2.4rem;font-weight:900;color:#FFB800;">VS</div>')
    with c3:
        st.html(f'<div class="finalist">{flag_img(tb, 160)}<div class="name">{tb}</div></div>')

    st.space("large")

    def crown():
        champion = st.session_state.get("final_0") or ta
        try:
            db.save_knockout_picks(st.session_state.participant_id, "final", [champion])
            st.session_state.champion = champion
            st.session_state.error = None
            st.session_state.step = 8
        except Exception as exc:
            st.session_state.error = f"Erro ao salvar: {exc}"

    with st.container(horizontal_alignment="center"):
        st.html('<p style="text-align:center;font-size:1.15rem;color:#A0AEC0;margin-bottom:10px;">'
                'Quem levanta a taça? 🏆</p>')
        if st.session_state.get("final_0") not in (ta, tb):
            st.session_state["final_0"] = ta
        st.segmented_control("Campeão", options=[ta, tb],
                             key="final_0", label_visibility="collapsed")
        st.space("small")
        st.button("🏆 Coroar meu campeão!", type="primary", on_click=crown)

    if st.session_state.error:
        st.error(st.session_state.error, icon=":material/error:")


# ── Step 7: Confirmação ───────────────────────────────────────────────────────

def reset_state() -> None:
    keys = ["step", "participant_id", "participant_name", "error", "group_picks",
            "r32_teams", "r32_winners", "r16_winners", "qf_winners", "sf_winners",
            "champion", "reg_name", "reg_phone", "reg_email", "final_0"]
    for k in keys:
        st.session_state.pop(k, None)
    for g in GROUPS:
        st.session_state.pop(f"g_first_{g}", None)
        st.session_state.pop(f"g_second_{g}", None)
    for prefix in ["r32", "r16", "qf", "sf"]:
        for i in range(16):
            st.session_state.pop(f"{prefix}_{i}", None)
    st.session_state.step = 1


def render_confirmation() -> None:
    render_hero()
    render_steps(8)
    st.balloons()
    champion = st.session_state.get("champion", "?")
    name = st.session_state.participant_name

    st.space("medium")
    with st.container(horizontal_alignment="center"):
        st.html(f"""
        <div style="text-align:center;padding:46px 32px;border-radius:26px;
             background:linear-gradient(135deg,#003D20,#006400,#00A854);
             box-shadow:0 12px 50px rgba(0,212,106,0.32);border:1px solid rgba(255,255,255,0.1);">
            {flag_img(champion, 160)}
            <h1 style="color:#fff;font-size:2.1rem;margin:18px 0 6px;">Bolão registrado! 🎉</h1>
            <p style="color:rgba(255,255,255,0.92);font-size:1.18rem;margin:0;">Parabéns, <strong>{name}</strong>!</p>
            <p style="color:#FFD54F;font-size:1.3rem;font-weight:700;margin-top:12px;">
                Seu campeão: {champion} 🏆</p>
        </div>
        """)
        st.space("large")

        with st.expander(":material/list: Ver resumo dos meus palpites", expanded=False):
            picks = st.session_state.group_picks
            st.markdown("**Fase de grupos**")
            cols = st.columns(4, gap="small")
            for i, (g, (f_team, s_team)) in enumerate(picks.items()):
                with cols[i % 4]:
                    st.html(
                        f'<div style="padding:8px 0;"><strong>Grupo {g}</strong><br>'
                        f'<span style="font-size:0.85rem;color:#A0AEC0;">'
                        f'{flag_img(f_team, 24)} {f_team}<br>{flag_img(s_team, 24)} {s_team}</span></div>'
                    )
            champ = st.session_state.get("champion", "?")
            st.markdown("**Trajetória final**")
            st.html(
                f'<div style="color:#A0AEC0;font-size:0.9rem;">'
                f'Campeão escolhido: {flag_img(champ, 28)} <strong style="color:#00D46A;">{champ}</strong></div>'
            )

        st.space("medium")
        st.button(":material/refresh: Fazer novo bolão", on_click=reset_state)


# ── Router ────────────────────────────────────────────────────────────────────

step = st.session_state.step

if step == 1:
    render_step1()
elif step == 2:
    render_step2()
elif step == 3:
    render_knockout(3, "r32", st.session_state.r32_teams or [], 4)
elif step == 4:
    render_knockout(4, "r16", next_round_matches(st.session_state.r32_winners), 5)
elif step == 5:
    render_knockout(5, "qf", next_round_matches(st.session_state.r16_winners), 6)
elif step == 6:
    render_knockout(6, "sf", next_round_matches(st.session_state.qf_winners), 7)
elif step == 7:
    render_final()
else:
    render_confirmation()
