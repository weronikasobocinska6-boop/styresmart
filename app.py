import streamlit as st
import requests
import datetime
import calendar
import json
import base64

# SUPABASE - chmura
from supabase import create_client, Client

# ==========================================
# 1. KONFIGURASJON AV SIDEN
# ==========================================
st.set_page_config(page_title="SmartStyre | Kirkegata 6", page_icon="🏢", layout="wide")

# ==========================================
# 2. DESIGN (Dagens farger: Fjord Blue, Blå knapper, Off-white)
# ==========================================
st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700;800&display=swap');

    [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; }
    
    /* Mørkeblått sidepanel (Fjord Blue) */
    [data-testid="stSidebar"] { background-color: #0F172A !important; border-right: none !important; box-shadow: 2px 0 15px rgba(0,0,0,0.1); }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] span { color: #F8FAFC !important; }
    
    .stApp, p, label, li, input, textarea, .stSelectbox { font-family: 'Inter', sans-serif !important; color: #334155 !important; }
    
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif !important; color: #0F172A !important; letter-spacing: -0.5px; }
    h1 { text-align: center; margin-bottom: 40px !important; font-size: 3.5rem !important; font-weight: 700 !important; letter-spacing: -1px; }

    header {visibility: hidden;} #MainMenu {visibility: hidden;} footer {visibility: hidden;}

    /* Blå hovedknapper */
    .stButton > button, .stDownloadButton > button {
        background-color: #1D4ED8 !important; color: #FFFFFF !important; border-radius: 8px !important; border: none !important;
        padding: 10px 24px !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; font-size: 0.85em !important;
        text-transform: uppercase; letter-spacing: 1.2px !important; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06) !important; 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; width: 100%;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { 
        background-color: #1E40AF !important; transform: translateY(-2px) !important; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05) !important;
    }
    .stButton button p, .stDownloadButton button p { color: #FFFFFF !important; margin: 0 !important; }

    /* Dine eksisterende kortstrukturer */
    .nordic-card { 
        background-color: #FFFFFF; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); 
        margin-bottom: 24px; border: 1px solid #F1F5F9; border-top: 4px solid #0F172A; transition: all 0.3s ease;
    }
    .nordic-card:hover { box-shadow: 0 10px 25px rgba(0,0,0,0.06); }

    .kpi-boks {
        background-color: #FFFFFF; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid #F1F5F9; border-top: 4px solid #1D4ED8; text-align: center; transition: transform 0.3s ease;
    }
    .kpi-boks:hover { transform: translateY(-3px); }
    .kpi-tall { font-size: 2.8em; font-family: 'Playfair Display', serif; font-weight: 700; color: #0F172A; margin: 10px 0; }
    .kpi-tittel { font-size: 0.85em; text-transform: uppercase; letter-spacing: 2px; color: #64748B; font-weight: 600; }

    .stTabs [data-baseweb="tab-list"] { gap: 32px; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: transparent !important; padding: 12px 0px; font-family: 'Inter', sans-serif !important; font-size: 1.05em !important; font-weight: 500 !important; color: #94A3B8 !important; }
    .stTabs [aria-selected="true"] { color: #0F172A !important; border-bottom: 3px solid #0F172A !important; font-weight: 600 !important; }
    
    .kalender-table { width: 100%; border-collapse: separate; border-spacing: 8px; table-layout: fixed; }
    .kalender-table th { background-color: #F8FAFC; color: #475569; font-family: 'Inter', sans-serif; padding: 12px; text-align: center; font-weight: 600; border-radius: 8px; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; }
    .kalender-table td { background-color: #FFFFFF; border: 1px solid #E2E8F0; height: 90px; vertical-align: top; padding: 12px; border-radius: 8px; font-size: 0.9em; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.01); }
    .kalender-table td:hover { border-color: #CBD5E1; box-shadow: 0 4px 12px rgba(0,0,0,0.03); transform: translateY(-1px); }
    .kalender-table td.empty { background-color: transparent; border: none; box-shadow: none; }
    .kalender-table td.has-event { background-color: #F0FDF4; border-left: 4px solid #10B981; }
    .event-badge { background-color: #10B981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.85em; font-weight: 600; display: inline-block; margin-top: 8px; }

    .dok-rad {
        background-color: #FFFFFF; padding: 20px 24px; border-radius: 10px; border-left: 4px solid #1D4ED8; margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02); border-top: 1px solid #F1F5F9; border-right: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9; transition: all 0.2s ease;
    }
    .dok-rad:hover { box-shadow: 0 6px 16px rgba(0,0,0,0.05); transform: translateY(-1px); }
    
    .mappe-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 20px; margin-top: 40px; }
    
    input, textarea, .stSelectbox > div > div { border-radius: 8px !important; border: 1px solid #E2E8F0 !important; font-family: 'Inter', sans-serif !important; }
    input:focus, textarea:focus { border-color: #1D4ED8 !important; box-shadow: 0 0 0 1px #1D4ED8 !important; }
    
    .nordic-meta { font-size: 0.75em; text-transform: uppercase; letter-spacing: 1.5px; color: #94A3B8; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px; font-weight: 700; }
    
    /* FIX FOR MOBILSKJERMER (Responsive Design) */
    @media (max-width: 768px) {
        h1 { font-size: 2.5rem !important; margin-bottom: 20px !important; }
        .nordic-card { padding: 20px !important; }
        .kpi-tall { font-size: 2rem !important; }
        .kalender-table th { padding: 4px; font-size: 0.7em; }
        .kalender-table td { padding: 4px; height: 60px; font-size: 0.75em; }
        .event-badge { padding: 2px 4px; font-size: 0.7em; }
    }
</style>
''', unsafe_allow_html=True)


# ==========================================
# 3. TILKOBLING TIL SKYDATABASEN (Supabase)
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY", "")
ai_klar = bool(api_key)

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

@st.cache_resource
def init_supabase():
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

supabase = init_supabase()

# PEŁNA LISTA 16 MIESZKAŃCÓW (ODZYSKANA)
DOMYSLNE_DANE = {
    "alle_beboere": [
        {"Navn": "Akram Zalmai", "E-post": "zalmai44@gmail.com", "Seksjon": "Seksjon 1"},
        {"Navn": "Galina Novikova", "E-post": "ngiv1005@gmail.com", "Seksjon": "Seksjon 2"},
        {"Navn": "etasje oppgang B", "E-post": "asammad35@hotmail.com", "Seksjon": "Oppgang B"},
        {"Navn": "Gina Hetlevik", "E-post": "gin-he@online.no", "Seksjon": "Seksjon 3"},
        {"Navn": "Gry Kjersti Berget", "E-post": "gberget@deloitte.no", "Seksjon": "Seksjon 4"},
        {"Navn": "Ingeborg Skoveng", "E-post": "ingeborg@skoveng.no", "Seksjon": "Seksjon 5"},
        {"Navn": "Ingelise Brynlund", "E-post": "ingelise.brynlund@gmail.com", "Seksjon": "Seksjon 6"},
        {"Navn": "Mads K", "E-post": "madk1515@gmail.com", "Seksjon": "Seksjon 7"},
        {"Navn": "Stig Schmidt", "E-post": "sschm@frisurf.no", "Seksjon": "Seksjon 8"},
        {"Navn": "Terje Aarborgh", "E-post": "taarbogh@gmail.com", "Seksjon": "Seksjon 9"},
        {"Navn": "Ine Foss", "E-post": "ine@kvikkerehoder.no", "Seksjon": "Seksjon 10"},
        {"Navn": "Tom Bergersen", "E-post": "tom.bergersen1@gmail.com", "Seksjon": "Seksjon 11"},
        {"Navn": "Sultan Bhatti", "E-post": "Sultan.bhatti91@outlook.com", "Seksjon": "Seksjon 12"},
        {"Navn": "Cecilia", "E-post": "ce.ma.andersson@gmail.com", "Seksjon": "Seksjon 13"},
        {"Navn": "Weronika Sobocinska", "E-post": "weronikasobocinska6@gmail.com", "Seksjon": "Seksjon 14"},
        {"Navn": "Mona Schmidt", "E-post": "moirol@wemail.no", "Seksjon": "Seksjon 15"}
    ],
    "beboer_data": {
        "zalmai44@gmail.com": {
            "dokumenter": [{"tittel": "Tidligere klage på vannlekkasje", "filnavn": "Klage_Vannlekkasje_2024.pdf"}],
            "korrespondanse": [{"dato": "09.10.2026", "emne": "Vannlekkasje fra taket på badet", "innhold": "Rapportert drypping fra overliggende leilighet (etasje oppgang B). Styret har avvist ansvar jf. eierseksjonsloven."}]
        }
    },
    "bygg_mapper": {
        "Forsikring": [],
        "Tegninger & Bygg": [],
        "Økonomi & Budsjett": [],
        "Møtereferater": []
    },
    "kalender_oppgaver": []
}

def wczytaj_dane():
    if supabase:
        try:
            res = supabase.table("smartstyre_data").select("json_data").eq("
