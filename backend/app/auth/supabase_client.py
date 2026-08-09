"""
Module 6a: Supabase client (auth + database).

Why Supabase instead of building auth from scratch: authentication is a
solved, security-sensitive problem (password hashing, session tokens,
OAuth flows). Reimplementing it adds real security risk for very little
project-specific learning value. Using a managed provider here and
explaining *why* is a stronger engineering decision than rolling your
own -- it focuses effort on this project's actual differentiator (the
ML/NLP pipeline), not on infrastructure that doesn't showcase anything
unique.

Same lazy-loading + "gracefully unconfigured" pattern used for the LLM
feedback module: no real Supabase project exists yet in this build
environment, so the client is initialized on first use, not at import,
and every route checks is_configured() before touching it -- so the
rest of the app keeps working even before real credentials are added.
"""
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_client_cache = {}


def is_configured() -> bool:
    return bool(SUPABASE_URL and SUPABASE_KEY)


def get_client():
    if not is_configured():
        raise RuntimeError(
            "Supabase not configured. Add SUPABASE_URL and SUPABASE_KEY to .env "
            "(see .env.example) -- get these from your Supabase project's "
            "Settings > API page."
        )
    if "client" not in _client_cache:
        from supabase import create_client
        _client_cache["client"] = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client_cache["client"]
