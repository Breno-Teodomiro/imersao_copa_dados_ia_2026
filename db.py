from collections import Counter

import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_client() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def email_already_registered(email: str) -> bool:
    resp = get_client().table("participants").select("id").eq("email", email).execute()
    return len(resp.data) > 0


def register_participant(name: str, phone: str, email: str) -> str:
    try:
        resp = (
            get_client()
            .table("participants")
            .insert({"name": name, "phone": phone, "email": email})
            .execute()
        )
        return resp.data[0]["id"]
    except Exception as exc:
        msg = str(exc)
        if "23505" in msg or "duplicado" in msg.lower() or "duplicate" in msg.lower():
            raise ValueError("Este e-mail já está cadastrado.") from exc
        raise


def save_picks(participant_id: str, picks: dict[str, tuple[str, str]]) -> None:
    rows = [
        {
            "participant_id": participant_id,
            "group_code": group,
            "first_place": first,
            "second_place": second,
        }
        for group, (first, second) in picks.items()
    ]
    get_client().table("picks").upsert(
        rows, on_conflict="participant_id,group_code"
    ).execute()


def save_knockout_picks(participant_id: str, round_name: str, winners: list[str]) -> None:
    rows = [
        {
            "participant_id": participant_id,
            "round": round_name,
            "match_index": i,
            "winner": winner,
        }
        for i, winner in enumerate(winners)
    ]
    get_client().table("knockout_picks").upsert(
        rows, on_conflict="participant_id,round,match_index"
    ).execute()


def get_champion_votes() -> tuple[list[tuple[str, int]], int]:
    """Ranking das seleções mais escolhidas como campeãs no bolão.

    Retorna ([(seleção, votos), ...] ordenado desc, total de bolões finalizados).
    """
    resp = (
        get_client()
        .table("knockout_picks")
        .select("winner")
        .eq("round", "final")
        .execute()
    )
    counts = Counter(r["winner"] for r in resp.data)
    total = sum(counts.values())
    return counts.most_common(), total
