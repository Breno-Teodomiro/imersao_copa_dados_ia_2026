import streamlit as st
import db

st.set_page_config(
    page_title="Bolão Copa do Mundo 2026",
    page_icon="⚽",
    layout="centered",
)

# ── Data ──────────────────────────────────────────────────────────────────────

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
    "México": "🇲🇽",
    "África do Sul": "🇿🇦",
    "Coreia do Sul": "🇰🇷",
    "Tchéquia": "🇨🇿",
    "Canadá": "🇨🇦",
    "Bósnia e Herzegovina": "🇧🇦",
    "Catar": "🇶🇦",
    "Suíça": "🇨🇭",
    "Brasil": "🇧🇷",
    "Marrocos": "🇲🇦",
    "Escócia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Haiti": "🇭🇹",
    "Estados Unidos": "🇺🇸",
    "Paraguai": "🇵🇾",
    "Turquia": "🇹🇷",
    "Austrália": "🇦🇺",
    "Alemanha": "🇩🇪",
    "Curaçao": "🇨🇼",
    "Costa do Marfim": "🇨🇮",
    "Equador": "🇪🇨",
    "Países Baixos": "🇳🇱",
    "Japão": "🇯🇵",
    "Suécia": "🇸🇪",
    "Tunísia": "🇹🇳",
    "Bélgica": "🇧🇪",
    "Egito": "🇪🇬",
    "Irã": "🇮🇷",
    "Nova Zelândia": "🇳🇿",
    "Espanha": "🇪🇸",
    "Cabo Verde": "🇨🇻",
    "Arábia Saudita": "🇸🇦",
    "Uruguai": "🇺🇾",
    "França": "🇫🇷",
    "Senegal": "🇸🇳",
    "Iraque": "🇮🇶",
    "Noruega": "🇳🇴",
    "Argentina": "🇦🇷",
    "Argélia": "🇩🇿",
    "Áustria": "🇦🇹",
    "Jordânia": "🇯🇴",
    "Portugal": "🇵🇹",
    "Rep. Dem. do Congo": "🇨🇩",
    "Uzbequistão": "🇺🇿",
    "Colômbia": "🇨🇴",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Croácia": "🇭🇷",
    "Gana": "🇬🇭",
    "Panamá": "🇵🇦",
}


def flag(team: str) -> str:
    return FLAGS.get(team, "🏳")


def team_options(teams: list[str]) -> list[str]:
    return [f"{flag(t)} {t}" for t in teams]


def strip_flag(label: str) -> str:
    """Remove the flag emoji prefix from a selectbox label."""
    parts = label.split(" ", 1)
    return parts[1] if len(parts) == 2 else label


# ── Session state ─────────────────────────────────────────────────────────────

st.session_state.setdefault("step", 1)
st.session_state.setdefault("participant_id", None)
st.session_state.setdefault("participant_name", None)
st.session_state.setdefault("error", None)


# ── Helpers ───────────────────────────────────────────────────────────────────

def render_progress(step: int) -> None:
    labels = {1: "Passo 1 de 3 — Registro", 2: "Passo 2 de 3 — Palpites dos grupos", 3: "Concluído!"}
    values = {1: 0.15, 2: 0.55, 3: 1.0}
    st.progress(values[step], text=labels[step])


def render_header() -> None:
    with st.container(horizontal_alignment="center"):
        st.title("⚽ Bolão Copa do Mundo 2026")
        st.caption("Selecione o 1º e 2º lugar de cada grupo e registre seu palpite!")


# ── Step 1: Registration ──────────────────────────────────────────────────────

def submit_registration() -> None:
    name = st.session_state.get("reg_name", "").strip()
    phone = st.session_state.get("reg_phone", "").strip()
    email = st.session_state.get("reg_email", "").strip()

    if not name or not phone or not email:
        st.session_state.error = "Preencha todos os campos."
        return
    if "@" not in email:
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
        st.session_state.error = "Erro ao conectar com o servidor. Tente novamente."


def render_step1() -> None:
    render_header()
    render_progress(1)
    st.space("medium")

    with st.container(border=True):
        st.subheader("Suas informações")
        st.text_input("Nome completo", key="reg_name", placeholder="Ex: João Silva")
        st.text_input("Telefone", key="reg_phone", placeholder="Ex: (11) 99999-9999")
        st.text_input("E-mail", key="reg_email", placeholder="Ex: joao@email.com")

        if st.session_state.error:
            st.error(st.session_state.error)

        st.button("Continuar →", type="primary", on_click=submit_registration)


# ── Step 2: Group picks ───────────────────────────────────────────────────────

def submit_picks() -> None:
    picks: dict[str, tuple[str, str]] = {}

    for group, teams in GROUPS.items():
        first_label = st.session_state.get(f"first_{group}", "")
        second_label = st.session_state.get(f"second_{group}", "")
        first = strip_flag(first_label)
        second = strip_flag(second_label)

        if first == second:
            st.session_state.error = (
                f"Grupo {group}: 1º e 2º lugar não podem ser o mesmo time."
            )
            return
        picks[group] = (first, second)

    try:
        db.save_picks(st.session_state.participant_id, picks)
        st.session_state.error = None
        st.session_state.step = 3
    except Exception as exc:
        st.session_state.error = f"Erro ao salvar palpites: {exc}"


def render_group_card(group: str, teams: list[str], col) -> None:
    options = team_options(teams)
    with col:
        with st.container(border=True):
            st.markdown(f"**Grupo {group}**")
            st.selectbox(
                "🥇 1º lugar",
                options=options,
                key=f"first_{group}",
                label_visibility="visible",
            )
            # Exclude the team chosen as 1st from 2nd place options
            first_label = st.session_state.get(f"first_{group}", options[0])
            second_options = [o for o in options if o != first_label]
            st.selectbox(
                "🥈 2º lugar",
                options=second_options,
                key=f"second_{group}",
                label_visibility="visible",
            )


def render_step2() -> None:
    render_header()
    render_progress(2)
    st.space("small")

    st.subheader(f"Olá, {st.session_state.participant_name}! Faça seus palpites:")
    st.caption("Para cada grupo, escolha o time que você acha que ficará em 1º e 2º lugar.")
    st.space("small")

    group_list = list(GROUPS.items())
    # 3 columns, 4 rows of groups
    for row_start in range(0, 12, 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = row_start + i
            if idx < len(group_list):
                group, teams = group_list[idx]
                render_group_card(group, teams, col)
        st.space("small")

    if st.session_state.error:
        st.error(st.session_state.error)

    st.space("medium")
    with st.container(horizontal_alignment="center"):
        st.button("Enviar meu bolão ✅", type="primary", on_click=submit_picks)


# ── Step 3: Confirmation ──────────────────────────────────────────────────────

def reset_state() -> None:
    for key in ["step", "participant_id", "participant_name", "error",
                "reg_name", "reg_phone", "reg_email"]:
        st.session_state.pop(key, None)
    for group in GROUPS:
        st.session_state.pop(f"first_{group}", None)
        st.session_state.pop(f"second_{group}", None)
    st.session_state.step = 1


def render_step3() -> None:
    render_header()
    render_progress(3)
    st.balloons()
    st.space("medium")

    with st.container(border=True, horizontal_alignment="center"):
        st.success(
            f"🏆 Bolão registrado com sucesso, **{st.session_state.participant_name}**! Boa sorte!"
        )
        st.write("Seus palpites foram salvos. Acompanhe os resultados durante a Copa!")
        st.space("small")
        st.button("Fazer novo bolão", on_click=reset_state)


# ── Router ────────────────────────────────────────────────────────────────────

step = st.session_state.step

if step == 1:
    render_step1()
elif step == 2:
    render_step2()
elif step == 3:
    render_step3()
