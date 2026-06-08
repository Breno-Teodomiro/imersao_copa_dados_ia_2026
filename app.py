import random
import streamlit as st
import db

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="⚽",
    layout="wide",
)

# ── CSS Premium ───────────────────────────────────────────────────────────────

st.html("""
<style>
/* ── Fundo e tipografia global ── */
.stApp { background: linear-gradient(160deg, #0A0E1A 0%, #0D1528 50%, #0A0E1A 100%); }

/* ── Header hero ── */
.hero-banner {
    background: linear-gradient(135deg, #003D20 0%, #006400 40%, #00A854 70%, #FFB800 100%);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 8px;
    text-align: center;
    box-shadow: 0 8px 40px rgba(0,212,106,0.25);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "⚽";
    position: absolute;
    font-size: 160px;
    opacity: 0.07;
    right: -10px;
    top: -20px;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -1px;
    text-shadow: 0 2px 12px rgba(0,0,0,0.4);
}
.hero-sub {
    font-size: 1.05rem;
    color: rgba(255,255,255,0.85);
    margin-top: 8px;
}

/* ── Cartão de grupo ── */
.group-card {
    background: linear-gradient(145deg, #141824, #1A2035);
    border: 1px solid #2A3040;
    border-radius: 16px;
    padding: 0;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}
.group-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,212,106,0.15); }
.group-header {
    background: linear-gradient(90deg, #00D46A, #00A854);
    padding: 10px 16px;
    font-size: 0.85rem;
    font-weight: 700;
    color: #0A0E1A;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.team-row {
    display: flex;
    align-items: center;
    padding: 10px 16px;
    border-bottom: 1px solid #1E2538;
    gap: 12px;
    font-size: 0.95rem;
    color: #E8ECF0;
}
.team-row:last-child { border-bottom: none; }
.team-flag { font-size: 1.5rem; line-height: 1; }
.team-name { flex: 1; font-weight: 500; }

/* ── Cartão de partida knockout ── */
.match-card {
    background: linear-gradient(145deg, #141824, #1A2035);
    border: 1px solid #2A3040;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35);
    margin-bottom: 4px;
}
.match-header {
    background: #1E2538;
    padding: 6px 14px;
    font-size: 0.75rem;
    color: #6B7A99;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.match-teams {
    padding: 12px 16px;
    display: flex;
    gap: 10px;
    align-items: center;
    font-size: 0.9rem;
    color: #C8D0E0;
    font-weight: 600;
}
.match-vs { color: #FFB800; font-weight: 700; font-size: 0.8rem; }

/* ── Step indicator ── */
.step-pill {
    display: inline-block;
    background: #1A2035;
    border: 1px solid #2A3040;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.8rem;
    color: #6B7A99;
    margin: 2px;
}
.step-pill.active {
    background: linear-gradient(90deg, #003D20, #006400);
    border-color: #00D46A;
    color: #00FF80;
    font-weight: 700;
}
.step-pill.done {
    background: #0D2818;
    border-color: #006400;
    color: #00D46A;
}

/* ── Botão primário customizado ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(90deg, #00D46A, #00A854) !important;
    color: #0A0E1A !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 32px !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 20px rgba(0,212,106,0.3) !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(0,212,106,0.45) !important;
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input {
    background: #141824 !important;
    border: 1px solid #2A3040 !important;
    border-radius: 10px !important;
    color: #E8ECF0 !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #00D46A !important;
    box-shadow: 0 0 0 2px rgba(0,212,106,0.2) !important;
}

/* ── Selectbox / Radio ── */
div[data-testid="stSelectbox"] > div > div {
    background: #141824 !important;
    border: 1px solid #2A3040 !important;
    border-radius: 10px !important;
}

/* ── Segmented control ── */
div[data-testid="stSegmentedControl"] { gap: 4px; }

/* ── Progress ── */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #00D46A, #00A854) !important;
    border-radius: 99px !important;
}

/* ── Sucesso / erro ── */
div[data-testid="stAlert"][data-baseweb="notification"] {
    border-radius: 12px !important;
}

/* ── Acessibilidade: foco visível ── */
:focus-visible { outline: 2px solid #00D46A !important; outline-offset: 3px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0A0E1A; }
::-webkit-scrollbar-thumb { background: #2A3040; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00D46A; }
</style>
""")

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

FLAGS: dict[str, str] = {
    "México": "🇲🇽", "África do Sul": "🇿🇦", "Coreia do Sul": "🇰🇷", "Tchéquia": "🇨🇿",
    "Canadá": "🇨🇦", "Bósnia e Herzegovina": "🇧🇦", "Catar": "🇶🇦", "Suíça": "🇨🇭",
    "Brasil": "🇧🇷", "Marrocos": "🇲🇦", "Escócia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Haiti": "🇭🇹",
    "Estados Unidos": "🇺🇸", "Paraguai": "🇵🇾", "Turquia": "🇹🇷", "Austrália": "🇦🇺",
    "Alemanha": "🇩🇪", "Curaçao": "🇨🇼", "Costa do Marfim": "🇨🇮", "Equador": "🇪🇨",
    "Países Baixos": "🇳🇱", "Japão": "🇯🇵", "Suécia": "🇸🇪", "Tunísia": "🇹🇳",
    "Bélgica": "🇧🇪", "Egito": "🇪🇬", "Irã": "🇮🇷", "Nova Zelândia": "🇳🇿",
    "Espanha": "🇪🇸", "Cabo Verde": "🇨🇻", "Arábia Saudita": "🇸🇦", "Uruguai": "🇺🇾",
    "França": "🇫🇷", "Senegal": "🇸🇳", "Iraque": "🇮🇶", "Noruega": "🇳🇴",
    "Argentina": "🇦🇷", "Argélia": "🇩🇿", "Áustria": "🇦🇹", "Jordânia": "🇯🇴",
    "Portugal": "🇵🇹", "Rep. Dem. do Congo": "🇨🇩", "Uzbequistão": "🇺🇿", "Colômbia": "🇨🇴",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croácia": "🇭🇷", "Gana": "🇬🇭", "Panamá": "🇵🇦",
}

# Chaveamento R32 da Copa 2026 (baseado no bracket oficial FIFA)
R32_TEMPLATE = [
    ("A1", "B2"), ("C1", "D2"), ("E1", "F2"), ("G1", "H2"),
    ("I1", "J2"), ("K1", "L2"), ("B1", "A2"), ("D1", "C2"),
    ("F1", "E2"), ("H1", "G2"), ("J1", "I2"), ("L1", "K2"),
    ("3rd_1", "3rd_2"), ("3rd_3", "3rd_4"), ("3rd_5", "3rd_6"), ("3rd_7", "3rd_8"),
]

ROUND_LABELS = {
    "r32": "Oitavas de Final", "r16": "Quartas de Final",
    "qf": "Semifinal", "sf": "Final", "final": "🏆 Campeão",
}
ROUND_ORDER = ["r32", "r16", "qf", "sf", "final"]


# ── Helpers ───────────────────────────────────────────────────────────────────

def flag(team: str) -> str:
    return FLAGS.get(team, "🏳")


def fmt(team: str) -> str:
    return f"{flag(team)} {team}"


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


# ── Session state ─────────────────────────────────────────────────────────────

st.session_state.setdefault("step", 1)
st.session_state.setdefault("participant_id", None)
st.session_state.setdefault("participant_name", None)
st.session_state.setdefault("error", None)
st.session_state.setdefault("group_picks", {})   # {"A": ("Time1","Time2"), ...}
st.session_state.setdefault("r32_teams", [])      # [(teamA, teamB), ...]
st.session_state.setdefault("r32_winners", [])
st.session_state.setdefault("r16_winners", [])
st.session_state.setdefault("qf_winners", [])
st.session_state.setdefault("sf_winners", [])


# ── Componentes visuais ───────────────────────────────────────────────────────

def render_hero() -> None:
    st.html("""
    <div class="hero-banner" role="banner">
        <p class="hero-title">⚽ Bolão Copa do Mundo 2026</p>
        <p class="hero-sub">🇨🇦 🇲🇽 🇺🇸 &nbsp;|&nbsp; 48 seleções &nbsp;·&nbsp; 12 grupos &nbsp;·&nbsp; 6 fases</p>
    </div>
    """)


def render_steps(current: int) -> None:
    steps = [
        (1, "Registro"),
        (2, "Grupos"),
        (3, "Oitavas"),
        (4, "Quartas"),
        (5, "Semifinal"),
        (6, "Final"),
        (7, "✅ Concluído"),
    ]
    pills_html = ""
    for num, label in steps:
        if num < current:
            cls = "done"
            icon = "✓ "
        elif num == current:
            cls = "active"
            icon = ""
        else:
            cls = ""
            icon = ""
        pills_html += f'<span class="step-pill {cls}" aria-current="{"step" if num == current else "false"}">{icon}{label}</span>'

    st.html(f'<div style="display:flex;flex-wrap:wrap;gap:4px;margin:12px 0 20px;" role="navigation" aria-label="Progresso do bolão">{pills_html}</div>')


def render_group_table(group: str, teams: list[str]) -> None:
    rows = "".join(
        f'<div class="team-row"><span class="team-flag" role="img" aria-label="bandeira {t}">{flag(t)}</span>'
        f'<span class="team-name">{t}</span></div>'
        for t in teams
    )
    st.html(f'<div class="group-card"><div class="group-header">Grupo {group}</div>{rows}</div>')


def render_match_card(label: str, team_a: str, team_b: str) -> None:
    st.html(f"""
    <div class="match-card" role="article" aria-label="Partida: {team_a} x {team_b}">
        <div class="match-header">{label}</div>
        <div class="match-teams">
            <span>{flag(team_a)} {team_a}</span>
            <span class="match-vs">VS</span>
            <span>{flag(team_b)} {team_b}</span>
        </div>
    </div>
    """)


def render_winner_select(key: str, team_a: str, team_b: str) -> str:
    options = [fmt(team_a), fmt(team_b)]
    choice = st.segmented_control(
        "Quem avança?",
        options=options,
        key=key,
        label_visibility="collapsed",
    )
    return choice or options[0]


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

        st.text_input("Nome completo", key="reg_name", placeholder="Ex: João Silva",
                      help="Seu nome será exibido no ranking")
        st.text_input("Telefone", key="reg_phone", placeholder="(11) 99999-9999")
        st.text_input("E-mail", key="reg_email", placeholder="joao@email.com",
                      help="Usado para identificar seu bolão")

        if st.session_state.error:
            st.error(st.session_state.error, icon=":material/error:")

        st.space("small")
        st.button("Começar meu bolão →", type="primary", on_click=submit_registration,
                  help="Clique para prosseguir para os palpites dos grupos")

    with col_info:
        st.subheader(":material/emoji_events: Como funciona")
        st.space("small")
        for step_num, (icon, text) in enumerate([
            (":material/groups:", "Palpite nos **12 grupos** — escolha o 1º e 2º de cada grupo"),
            (":material/sports_soccer:", "**Oitavas de final** — 32 times entram, 16 avançam"),
            (":material/bolt:", "**Quartas, Semifinal e Final** — até o campeão!"),
            (":material/star:", "Registre seu palpite completo e torça pela sua seleção"),
        ], 1):
            with st.container(border=True):
                st.markdown(f"{icon} {text}")


# ── Step 2: Palpites dos grupos ───────────────────────────────────────────────

def submit_group_picks() -> None:
    picks: dict[str, tuple[str, str]] = {}
    for group, teams in GROUPS.items():
        first_key = f"g_first_{group}"
        second_key = f"g_second_{group}"
        first = st.session_state.get(first_key)
        second = st.session_state.get(second_key)

        if not first or not second:
            st.session_state.error = f"Grupo {group}: selecione o 1º e 2º lugar."
            return

        first_name = first.split(" ", 1)[1] if " " in first else first
        second_name = second.split(" ", 1)[1] if " " in second else second

        if first_name == second_name:
            st.session_state.error = f"Grupo {group}: 1º e 2º lugar não podem ser o mesmo time."
            return
        picks[group] = (first_name, second_name)

    try:
        db.save_picks(st.session_state.participant_id, picks)
        r32 = build_r32_teams(picks)
        st.session_state.group_picks = picks
        st.session_state.r32_teams = r32
        st.session_state.error = None
        st.session_state.step = 3
    except Exception as exc:
        st.session_state.error = f"Erro ao salvar: {exc}"


def render_step2() -> None:
    render_hero()
    render_steps(2)

    st.subheader(f":material/groups: Palpites dos grupos — olá, {st.session_state.participant_name}!")
    st.caption("Para cada grupo, visualize os times e selecione quem termina em **1º e 2º lugar**.")
    st.space("small")

    group_items = list(GROUPS.items())

    for row_start in range(0, 12, 3):
        cols = st.columns(3, gap="medium")
        for col_idx, col in enumerate(cols):
            idx = row_start + col_idx
            if idx >= len(group_items):
                break
            group, teams = group_items[idx]
            options = [fmt(t) for t in teams]

            with col:
                render_group_table(group, teams)
                st.space("small")

                first_val = st.session_state.get(f"g_first_{group}", options[0])
                st.selectbox(
                    f"🥇 1º lugar — Grupo {group}",
                    options=options,
                    key=f"g_first_{group}",
                    label_visibility="visible",
                )
                second_options = [o for o in options if o != first_val]
                st.selectbox(
                    f"🥈 2º lugar — Grupo {group}",
                    options=second_options,
                    key=f"g_second_{group}",
                    label_visibility="visible",
                )
                st.space("small")

        st.space("small")

    if st.session_state.error:
        st.error(st.session_state.error, icon=":material/error:")

    st.space("medium")
    with st.container(horizontal_alignment="center"):
        st.button("Confirmar palpites dos grupos →", type="primary", on_click=submit_group_picks)


# ── Step 3: Oitavas de Final (R32) ────────────────────────────────────────────

def submit_r32() -> None:
    winners: list[str] = []
    r32 = st.session_state.r32_teams
    for i, (ta, tb) in enumerate(r32):
        choice = st.session_state.get(f"r32_{i}", fmt(ta))
        name = choice.split(" ", 1)[1] if " " in choice else choice
        winners.append(name)
    try:
        db.save_knockout_picks(st.session_state.participant_id, "r32", winners)
        st.session_state.r32_winners = winners
        st.session_state.error = None
        st.session_state.step = 4
    except Exception as exc:
        st.session_state.error = f"Erro ao salvar: {exc}"


def render_knockout_step(
    step_num: int,
    round_key: str,
    matches: list[tuple[str, str]],
    on_submit,
    key_prefix: str,
) -> None:
    render_hero()
    render_steps(step_num)

    label = ROUND_LABELS[round_key]
    st.subheader(f":material/sports_soccer: {label}")
    st.caption("Selecione o time que você acredita que vai avançar em cada partida.")
    st.space("small")

    cols_per_row = 4 if len(matches) >= 8 else 2
    match_items = list(enumerate(matches))

    for row_start in range(0, len(match_items), cols_per_row):
        cols = st.columns(cols_per_row, gap="medium")
        for col_idx, col in enumerate(cols):
            idx = row_start + col_idx
            if idx >= len(match_items):
                break
            i, (ta, tb) = match_items[idx]
            with col:
                render_match_card(f"Partida {i+1}", ta, tb)
                options = [fmt(ta), fmt(tb)]
                st.segmented_control(
                    f"Quem avança? Partida {i+1}",
                    options=options,
                    key=f"{key_prefix}_{i}",
                    label_visibility="collapsed",
                )
        st.space("small")

    if st.session_state.error:
        st.error(st.session_state.error, icon=":material/error:")

    st.space("medium")
    with st.container(horizontal_alignment="center"):
        st.button(f"Confirmar {label} →", type="primary", on_click=on_submit)


# ── Step 4: Quartas de Final ──────────────────────────────────────────────────

def submit_r16() -> None:
    r16_matches = next_round_matches(st.session_state.r32_winners)
    winners: list[str] = []
    for i, (ta, tb) in enumerate(r16_matches):
        choice = st.session_state.get(f"r16_{i}", fmt(ta))
        name = choice.split(" ", 1)[1] if " " in choice else choice
        winners.append(name)
    try:
        db.save_knockout_picks(st.session_state.participant_id, "r16", winners)
        st.session_state.r16_winners = winners
        st.session_state.error = None
        st.session_state.step = 5
    except Exception as exc:
        st.session_state.error = f"Erro ao salvar: {exc}"


# ── Step 5: Semifinal ─────────────────────────────────────────────────────────

def submit_qf() -> None:
    qf_matches = next_round_matches(st.session_state.r16_winners)
    winners: list[str] = []
    for i, (ta, tb) in enumerate(qf_matches):
        choice = st.session_state.get(f"qf_{i}", fmt(ta))
        name = choice.split(" ", 1)[1] if " " in choice else choice
        winners.append(name)
    try:
        db.save_knockout_picks(st.session_state.participant_id, "qf", winners)
        st.session_state.qf_winners = winners
        st.session_state.error = None
        st.session_state.step = 6
    except Exception as exc:
        st.session_state.error = f"Erro ao salvar: {exc}"


# ── Step 6: Final ─────────────────────────────────────────────────────────────

def submit_sf() -> None:
    sf_matches = next_round_matches(st.session_state.qf_winners)
    winners: list[str] = []
    for i, (ta, tb) in enumerate(sf_matches):
        choice = st.session_state.get(f"sf_{i}", fmt(ta))
        name = choice.split(" ", 1)[1] if " " in choice else choice
        winners.append(name)
    try:
        db.save_knockout_picks(st.session_state.participant_id, "sf", winners)
        st.session_state.sf_winners = winners
        st.session_state.error = None
        st.session_state.step = 7
    except Exception as exc:
        st.session_state.error = f"Erro ao salvar: {exc}"


def submit_final() -> None:
    sf_winners = st.session_state.sf_winners
    if len(sf_winners) < 2:
        st.session_state.error = "Erro interno: finalistas não definidos."
        return
    ta, tb = sf_winners[0], sf_winners[1]
    choice = st.session_state.get("final_0", fmt(ta))
    champion = choice.split(" ", 1)[1] if " " in choice else choice
    try:
        db.save_knockout_picks(st.session_state.participant_id, "final", [champion])
        st.session_state.champion = champion
        st.session_state.error = None
        st.session_state.step = 8
    except Exception as exc:
        st.session_state.error = f"Erro ao salvar: {exc}"


def render_final_step() -> None:
    sf_winners = st.session_state.sf_winners
    if len(sf_winners) < 2:
        st.error("Erro: não há finalistas definidos.")
        return

    ta, tb = sf_winners[0], sf_winners[1]
    render_hero()
    render_steps(6)

    st.subheader(":material/emoji_events: A Grande Final!")
    st.caption("Chegou a hora: quem será o Campeão do Mundo 2026?")
    st.space("medium")

    col1, col2, col3 = st.columns([2, 1, 2], gap="large")
    with col1:
        st.html(f"""
        <div style="text-align:center;padding:32px;background:linear-gradient(145deg,#141824,#1A2035);
             border:2px solid #2A3040;border-radius:20px;">
            <div style="font-size:4rem;">{flag(ta)}</div>
            <div style="font-size:1.2rem;font-weight:700;color:#E8ECF0;margin-top:12px;">{ta}</div>
        </div>
        """)
    with col2:
        st.html('<div style="display:flex;align-items:center;justify-content:center;height:100%;font-size:2rem;font-weight:900;color:#FFB800;">VS</div>')
    with col3:
        st.html(f"""
        <div style="text-align:center;padding:32px;background:linear-gradient(145deg,#141824,#1A2035);
             border:2px solid #2A3040;border-radius:20px;">
            <div style="font-size:4rem;">{flag(tb)}</div>
            <div style="font-size:1.2rem;font-weight:700;color:#E8ECF0;margin-top:12px;">{tb}</div>
        </div>
        """)

    st.space("large")

    options = [fmt(ta), fmt(tb)]
    with st.container(horizontal_alignment="center"):
        st.html('<p style="text-align:center;font-size:1.1rem;color:#A0AEC0;margin-bottom:8px;">Quem levanta a taça?</p>')
        st.segmented_control(
            "Campeão",
            options=options,
            key="final_0",
            label_visibility="collapsed",
        )
        st.space("small")
        st.button("🏆 Registrar meu campeão!", type="primary", on_click=submit_final)

    if st.session_state.error:
        st.error(st.session_state.error, icon=":material/error:")


# ── Step 8: Confirmação ───────────────────────────────────────────────────────

def reset_state() -> None:
    keys_to_clear = [
        "step", "participant_id", "participant_name", "error",
        "group_picks", "r32_teams", "r32_winners", "r16_winners",
        "qf_winners", "sf_winners", "champion",
        "reg_name", "reg_phone", "reg_email",
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)
    for group in GROUPS:
        st.session_state.pop(f"g_first_{group}", None)
        st.session_state.pop(f"g_second_{group}", None)
    for prefix in ["r32", "r16", "qf", "sf"]:
        for i in range(16):
            st.session_state.pop(f"{prefix}_{i}", None)
    st.session_state.pop("final_0", None)
    st.session_state.step = 1


def render_step8() -> None:
    render_hero()
    render_steps(7)
    st.balloons()

    champion = st.session_state.get("champion", "?")
    name = st.session_state.participant_name

    st.space("medium")
    with st.container(horizontal_alignment="center"):
        st.html(f"""
        <div style="text-align:center;padding:48px 32px;background:linear-gradient(135deg,#003D20,#006400);
             border-radius:24px;box-shadow:0 8px 40px rgba(0,212,106,0.3);">
            <div style="font-size:5rem;">{flag(champion)}</div>
            <h1 style="color:#00FF80;font-size:2rem;margin:16px 0 8px;">Bolão registrado! 🎉</h1>
            <p style="color:rgba(255,255,255,0.9);font-size:1.15rem;">Parabéns, <strong>{name}</strong>!</p>
            <p style="color:rgba(255,255,255,0.75);margin-top:8px;">
                Seu campeão: <strong style="color:#FFB800">{flag(champion)} {champion}</strong>
            </p>
        </div>
        """)
        st.space("large")

        # Resumo dos grupos
        with st.expander(":material/list: Ver resumo dos meus palpites", expanded=False):
            picks = st.session_state.group_picks
            cols = st.columns(4, gap="small")
            for i, (g, (f_team, s_team)) in enumerate(picks.items()):
                with cols[i % 4]:
                    st.markdown(f"**Grupo {g}**")
                    st.caption(f"🥇 {fmt(f_team)}")
                    st.caption(f"🥈 {fmt(s_team)}")

        st.space("medium")
        st.button(":material/refresh: Fazer novo bolão", on_click=reset_state)


# ── Router ────────────────────────────────────────────────────────────────────

step = st.session_state.step

if step == 1:
    render_step1()

elif step == 2:
    render_step2()

elif step == 3:
    r32_matches = st.session_state.r32_teams or []

    def _submit_r32():
        winners: list[str] = []
        for i, (ta, tb) in enumerate(r32_matches):
            choice = st.session_state.get(f"r32_{i}", fmt(ta))
            name = choice.split(" ", 1)[1] if " " in choice else choice
            winners.append(name)
        try:
            db.save_knockout_picks(st.session_state.participant_id, "r32", winners)
            st.session_state.r32_winners = winners
            st.session_state.error = None
            st.session_state.step = 4
        except Exception as exc:
            st.session_state.error = f"Erro ao salvar: {exc}"

    render_knockout_step(3, "r32", r32_matches, _submit_r32, "r32")

elif step == 4:
    r16_matches = next_round_matches(st.session_state.r32_winners)

    def _submit_r16():
        winners: list[str] = []
        for i, (ta, tb) in enumerate(r16_matches):
            choice = st.session_state.get(f"r16_{i}", fmt(ta))
            name = choice.split(" ", 1)[1] if " " in choice else choice
            winners.append(name)
        try:
            db.save_knockout_picks(st.session_state.participant_id, "r16", winners)
            st.session_state.r16_winners = winners
            st.session_state.error = None
            st.session_state.step = 5
        except Exception as exc:
            st.session_state.error = f"Erro ao salvar: {exc}"

    render_knockout_step(4, "r16", r16_matches, _submit_r16, "r16")

elif step == 5:
    qf_matches = next_round_matches(st.session_state.r16_winners)

    def _submit_qf():
        winners: list[str] = []
        for i, (ta, tb) in enumerate(qf_matches):
            choice = st.session_state.get(f"qf_{i}", fmt(ta))
            name = choice.split(" ", 1)[1] if " " in choice else choice
            winners.append(name)
        try:
            db.save_knockout_picks(st.session_state.participant_id, "qf", winners)
            st.session_state.qf_winners = winners
            st.session_state.error = None
            st.session_state.step = 6
        except Exception as exc:
            st.session_state.error = f"Erro ao salvar: {exc}"

    render_knockout_step(5, "qf", qf_matches, _submit_qf, "qf")

elif step == 6:
    sf_matches = next_round_matches(st.session_state.qf_winners)

    def _submit_sf():
        winners: list[str] = []
        for i, (ta, tb) in enumerate(sf_matches):
            choice = st.session_state.get(f"sf_{i}", fmt(ta))
            name = choice.split(" ", 1)[1] if " " in choice else choice
            winners.append(name)
        try:
            db.save_knockout_picks(st.session_state.participant_id, "sf", winners)
            st.session_state.sf_winners = winners
            st.session_state.error = None
            st.session_state.step = 7
        except Exception as exc:
            st.session_state.error = f"Erro ao salvar: {exc}"

    render_knockout_step(6, "sf", sf_matches, _submit_sf, "sf")

elif step == 7:
    render_final_step()

elif step == 8:
    render_step8()
