import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_client() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def email_already_registered(email: str) -> bool:
    resp = get_client().table("participants").select("id").eq("email", email).execute()
    return len(resp.data) > 0


def register_participant(name: str, phone: str, email: str) -> str:
    resp = (
        get_client()
        .table("participants")
        .insert({"name": name, "phone": phone, "email": email})
        .execute()
    )
    return resp.data[0]["id"]


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
