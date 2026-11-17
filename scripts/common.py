"""Shared helpers: DOI/title normalization, polite HTTP with retries, paths."""
import re
import time
import unicodedata
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
SEED_XLSX = ROOT / "example_reviews" / "LLM_process_control_systematic_search.xlsx"
CORPUS = ROOT / "corpus"
LOGS = ROOT / "logs"
RAW = ROOT / "logs" / "raw_search"  # cached API responses (JSON) for reproducibility

SEARCH_DATE = "2026-10-28"
PRIOR_SEARCH_DATE = "2026-10-14"
WINDOW_START = "2022-11-01"

UA = "lit-review-LLM-process-control/0.1 (academic systematic review; BYU PRISM group)"
MAX_WAIT = 120  # seconds; longer Retry-After means give up now and re-run later
SESSION = requests.Session()
SESSION.headers["User-Agent"] = UA


def get(url, params=None, headers=None, tries=6, timeout=60, ok=(200,)):
    """GET with exponential backoff on 429/5xx. Returns Response or None."""
    delay = 2.0
    for _ in range(tries):
        try:
            r = SESSION.get(url, params=params, headers=headers, timeout=timeout)
        except requests.RequestException:
            time.sleep(delay)
            delay *= 2
            continue
        if r.status_code in ok:
            return r
        if r.status_code in (429, 500, 502, 503, 504):
            ra = r.headers.get("Retry-After")
            if ra and ra.isdigit() and float(ra) > MAX_WAIT:  # quota exhausted (e.g. OpenAlex daily credits)
                return r
            time.sleep(float(ra) if ra and ra.isdigit() else delay)
            delay = min(delay * 2, 60)
            continue
        return r
    return None


def norm_doi(doi):
    if not doi or not isinstance(doi, str):
        return ""
    d = doi.strip().split(";")[0].strip().lower()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", d)
    return d.rstrip(". ")


def arxiv_id_from_doi(doi):
    m = re.match(r"10\.48550/arxiv\.(.+)$", norm_doi(doi))
    return m.group(1) if m else ""


def norm_title(t):
    if not t or not isinstance(t, str):
        return ""
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"<[^>]+>", " ", t)  # strip markup like <i>
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def is_preprint_doi(doi):
    d = norm_doi(doi)
    return d.startswith(("10.48550/arxiv", "10.2139/ssrn", "10.13140/rg", "10.5281/zenodo",
                         "10.36227/techrxiv", "10.20944/preprints", "10.21203/rs",
                         "10.31224/", "10.26434/chemrxiv"))


# Eligibility pre-filter (same logic as the 14 Oct screen: LLM term AND control/process term)
LLM_RE = re.compile(
    r"\b(large language models?|llms?|gpt-?[345o]\w*|chatgpt|language models?|agentic|llm[- ]?agents?|"
    r"vision[- ]language models?|vlms?|foundation models?|generative ai|genai|claude|gemini|llama|qwen|deepseek)\b",
    re.I)
CTRL_RE = re.compile(
    r"\b(process control|control loop|controller|pid|mpc|model predictive|setpoint|set-point|supervisory|"
    r"plc|iec 61131|structured text|ladder|dcs|scada|distributed control|automation|"
    r"fault|alarm|abnormal|operator|control room|tennessee eastman|tclab|cstr|quadruple tank|four-tank|"
    r"distillation|reactor|bioreactor|fermentation|crystalli[sz]ation|wastewater|water treatment|"
    r"chemical process|chemical plant|process industr\w*|process monitoring|soft sensor|system identification|"
    r"closed[- ]loop|control system|industrial control|plant|refiner\w*|boiler|batch process|digital twin)\b",
    re.I)


def prefilter(title, abstract=""):
    text = f"{title or ''} {abstract or ''}"
    return bool(LLM_RE.search(text)) and bool(CTRL_RE.search(text))
