import streamlit as st
import requests
import datetime
import calendar
import json
import base64

# SUPABASE - nowa chmura
from supabase import create_client, Client

# ==========================================
# 1. KONFIGURASJON AV SIDEN
# ==========================================
st.set_page_config(page_title="SmartStyre | Kirkegata 6", page_icon="🏢", layout="wide")

# ==========================================
# 2. DESIGN (Modern Premium SaaS & Nordic Elegance)
# ==========================================
st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@500;600;700;800&display=swap');

    [data-testid="stAppViewContainer"] { background-color: #F8FAFC !important; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; box-shadow: 2px 0 15px rgba(0,0,0,0.02); }
    
    .stApp, p, label, li, input, textarea, .stSelectbox { font-family: 'Inter', sans-serif !important; color: #334155 !important; }
    
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif !important; color: #0F172A !important; letter-spacing: -0.5px; }
    h1 { text-align: center; margin-bottom: 40px !important; font-size: 3.5rem !important; font-weight: 700 !important; letter-spacing: -1px; }

    header {visibility: hidden;} #MainMenu {visibility: hidden;} footer {visibility: hidden;}

    .stButton > button, .stDownloadButton > button {
        background-color: #0F172A !important; color: #FFFFFF !important; border-radius: 8px !important; border: 1px solid #0F172A !important;
        padding: 10px 24px !important; font-family: 'Inter', sans-serif !important; font-weight: 600 !important; font-size: 0.85em !important;
        text-transform: uppercase; letter-spacing: 1.2px !important; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06) !important; 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { 
        background-color: #334155 !important; border-color: #334155 !important; transform: translateY(-2px) !important; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05) !important;
    }
    .stButton button p, .stDownloadButton button p { color: #FFFFFF !important; margin: 0 !important; }

    .nordic-card { 
        background-color: #FFFFFF; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); 
        margin-bottom: 24px; border: 1px solid #F1F5F9; border-top: 4px solid #0F172A; transition: all 0.3s ease;
    }
    .nordic-card:hover { box-shadow: 0 10px 25px rgba(0,0,0,0.06); }

    .kpi-boks {
        background-color: #FFFFFF; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid #F1F5F9; border-top: 4px solid #3B82F6; text-align: center; transition: transform 0.3s ease;
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
        background-color: #FFFFFF; padding: 20px 24px; border-radius: 10px; border-left: 4px solid #3B82F6; margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02); border-top: 1px solid #F1F5F9; border-right: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9; transition: all 0.2s ease;
    }
    .dok-rad:hover { box-shadow: 0 6px 16px rgba(0,0,0,0.05); transform: translateY(-1px); }
    
    .mappe-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 20px; margin-top: 40px; }
    
    input, textarea, .stSelectbox > div > div { border-radius: 8px !important; border: 1px solid #E2E8F0 !important; font-family: 'Inter', sans-serif !important; }
    input:focus, textarea:focus { border-color: #3B82F6 !important; box-shadow: 0 0 0 1px #3B82F6 !important; }
    
    .nordic-meta { font-size: 0.75em; text-transform: uppercase; letter-spacing: 1.5px; color: #94A3B8; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px; font-weight: 700; }
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

DOMYSLNE_DANE = {
    "alle_beboere": [
        {"Navn": "Akram Zalmai", "E-post": "zalmai44@gmail.com", "Seksjon": "Seksjon 1"},
        {"Navn": "Galina Novikova", "E-post": "ngiv1005@gmail.com", "Seksjon": "Seksjon 2"},
        {"Navn": "etasje oppgang B", "E-post": "asammad35@hotmail.com", "Seksjon": "Oppgang B"}
    ],
    "beboer_data": {},
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
            res = supabase.table("smartstyre_data").select("json_data").eq("id", 1).execute()
            if res.data and len(res.data) > 0:
                dane = res.data[0]["json_data"]
                if isinstance(dane, str): dane = json.loads(dane)
                if not dane: dane = DOMYSLNE_DANE.copy()
                for k in DOMYSLNE_DANE:
                    if k not in dane: dane[k] = DOMYSLNE_DANE[k]
                return dane
            else:
                # Jeśli tabela jest pusta, załaduj domyślne dane
                supabase.table("smartstyre_data").insert({"id": 1, "json_data": DOMYSLNE_DANE}).execute()
        except Exception as e:
            pass
    return DOMYSLNE_DANE.copy()

def zapisz_dane(dane):
    if supabase:
        try:
            supabase.table("smartstyre_data").update({"json_data": dane}).eq("id", 1).execute()
        except Exception as e:
            st.error(f"Feil ved lagring til skyen: {e}")

if "db" not in st.session_state:
    st.session_state.db = wczytaj_dane()

db = st.session_state.db

# --- HÅNDTERING AV FILER I SKYEN (Supabase Storage) ---
def lagre_opplastet_fil(uploaded_file):
    if uploaded_file is not None and supabase:
        file_bytes = uploaded_file.getvalue()
        file_name = uploaded_file.name
        try:
            # Slett først hvis filen eksisterer for å tillate oppdatering
            supabase.storage.from_("dokumenty").remove([file_name])
        except: pass
        try:
            supabase.storage.from_("dokumenty").upload(file_name, file_bytes)
            return file_name
        except Exception as e:
            st.error(f"Feil ved opplasting til skyen: {e}")
    return None

def get_file_bytes(filnavn):
    if supabase:
        try:
            return supabase.storage.from_("dokumenty").download(filnavn)
        except: return None
    return None

def vis_fil_rad(filnavn, tittel, unik_id, er_admin_slett=None):
    mime = "application/octet-stream"
    if filnavn.lower().endswith('.pdf'): mime = "application/pdf"
    elif filnavn.lower().endswith(('.png', '.jpg', '.jpeg')): mime = "image/jpeg"
    
    st.markdown(f'''<div class="dok-rad"><div style="font-weight: 600; color: #0F172A; font-size: 1.1em;">{tittel}</div><div style="font-size: 0.85em; color: #64748B; margin-top: 6px;">{filnavn}</div></div>''', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1.5, 1.5, 1])
    
    bytes_data = get_file_bytes(filnavn)
    
    with col_a:
        if bytes_data:
            if st.button("👁️ Vis dokument", key=f"se_{unik_id}", use_container_width=True):
                st.session_state[f"vis_popup_{unik_id}"] = True
        else:
            st.button("👁️ Vis dokument", key=f"se_dis_{unik_id}", use_container_width=True, disabled=True)
            
    with col_b:
        if bytes_data:
            st.download_button("📥 Last ned", data=bytes_data, file_name=filnavn, mime=mime, key=f"dl_{unik_id}", use_container_width=True)
        else:
            st.markdown("<div style='padding-top: 8px; color: #94A3B8; font-size: 0.85em; font-style: italic; text-align: center;'>Ikke lastet opp i skyen</div>", unsafe_allow_html=True)
            
    with col_c:
        if er_admin_slett:
            if st.button("🗑️ Slett", key=f"slett_{unik_id}", use_container_width=True):
                if supabase and bytes_data:
                    try: supabase.storage.from_("dokumenty").remove([filnavn])
                    except: pass
                er_admin_slett()
                st.rerun()

    if st.session_state.get(f"vis_popup_{unik_id}", False) and bytes_data:
        @st.dialog(f"Dokument: {tittel}", width="large")
        def vis_modal():
            b64 = base64.b64encode(bytes_data).decode('utf-8')
            st.markdown(f'''<div style="text-align: right; margin-bottom: 15px;"><a href="data:{mime};base64,{b64}" target="_blank" style="color: #3B82F6; font-weight: 600; text-decoration: underline; font-family: 'Inter', sans-serif;">↗ Åpne filen i en ny fane (for å zoome / skrive ut)</a></div>''', unsafe_allow_html=True)
            if mime == "image/jpeg": st.image(bytes_data, use_container_width=True)
            elif mime == "application/pdf":
                pdf_display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="650px" type="application/pdf" style="border-radius: 8px; border: 1px solid #E2E8F0;"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                try: st.text(bytes_data.decode('utf-8'))
                except: st.info("Denne filtypen kan kun lastes ned, ikke forhåndsvises.")
            st.divider()
            if st.button("Lukk vindu", use_container_width=True, key=f"lukk_{unik_id}"):
                st.session_state[f"vis_popup_{unik_id}"] = False
                st.rerun()
        vis_modal()

# ==========================================
# 4. SIKKERHET (INNLOGGING)
# ==========================================
if "er_logget_inn" not in st.session_state: st.session_state.er_logget_inn = False

if not st.session_state.er_logget_inn:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown('''<div class="nordic-card" style="text-align: center; padding: 50px;"><h1 style="margin-bottom: 40px !important;">SmartStyre</h1>''', unsafe_allow_html=True)
        with st.form("login"):
            bruk = st.text_input("Brukernavn:")
            passw = st.text_input("Passord:", type="password")
            st.write("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Logg inn", use_container_width=True):
                if bruk.strip().lower() == "kirkegata6" and passw == "Styret2026":
                    st.session_state.er_logget_inn = True
                    st.rerun()
                else: st.error("Feil brukernavn eller passord.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if "innlogget_bruker" not in st.session_state: st.session_state.innlogget_bruker = "Weronika Bhatti"

# ==========================================
# 5. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-top: 30px; font-size: 2em;'>SmartStyre</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8em; letter-spacing: 3px; color: #94A3B8; margin-bottom: 40px;'>KIRKEGATA 6</p>", unsafe_allow_html=True)
    
    if ai_klar and supabase:
        st.markdown("<div style='background-color: #F0FDF4; padding: 12px; border-radius: 8px; border: 1px solid #BBF7D0; text-align: center; margin-bottom: 30px;'><span style='color: #15803D; font-weight: 600; font-size: 0.85em; font-family: \"Inter\", sans-serif;'>✓ Skyserver og AI Aktiv</span></div>", unsafe_allow_html=True)
    
    styremedlemmer = ["Weronika Bhatti", "Ine Foss", "Maria Frang"]
    valgt_m = st.selectbox("Aktiv Profil:", styremedlemmer, index=styremedlemmer.index(st.session_state.innlogget_bruker))
    if valgt_m != st.session_state.innlogget_bruker:
        st.session_state.innlogget_bruker = valgt_m
        st.rerun()

    st.write("---")
    st.markdown('''<p style="font-family: 'Inter', sans-serif; font-weight: 600; color: #64748B; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px;">Styrets sammensetning</p>''', unsafe_allow_html=True)
    for m in styremedlemmer:
        if m == st.session_state.innlogget_bruker: st.markdown(f"<span style='color: #0F172A; font-weight: 600;'>{m} (Du)</span>", unsafe_allow_html=True)
        else: st.markdown(f"<span style='color: #94A3B8;'>{m}</span>", unsafe_allow_html=True)
        
    st.write("---")
    if st.button("Logg ut", use_container_width=True):
        st.session_state.er_logget_inn = False
        st.rerun()

# ==========================================
# 6. HOVEDAPP / FANER
# ==========================================
st.markdown("<h1>SmartStyre</h1>", unsafe_allow_html=True)

faner = st.tabs(["📊 Oversikt", "✉️ Innboks", "👥 Beboere", "📂 Arkiv", "📅 Kalender", "⚙️ Sikkerhet"])

# --- Fane 1: Oversikt ---
with faner[0]:
    st.write("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='kpi-boks'><div class='kpi-tittel'>Registrerte Seksjoner</div><div class='kpi-tall'>{len(db['alle_beboere'])}</div></div>", unsafe_allow_html=True)
    with c2:
        moter = len([o for o in db['kalender_oppgaver'] if o.get('type') == 'Møte'])
        st.markdown(f"<div class='kpi-boks' style='border-top-color: #10B981;'><div class='kpi-tittel'>Planlagte Møter</div><div class='kpi-tall'>{moter}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='kpi-boks' style='border-top-color: #F59E0B;'><div class='kpi-tittel'>Dokumentmapper</div><div class='kpi-tall'>{len(db['bygg_mapper'])}</div></div>", unsafe_allow_html=True)
    
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("### Neste kalenderhendelse")
    fremtidige = sorted(db['kalender_oppgaver'], key=lambda x: x['dato'])
    if fremtidige:
        neste = fremtidige[0]
        st.info(f"**{neste['dato']} kl. {neste.get('tid','')}** — {neste['oppgave']}\n\n*Detaljer: {neste.get('detaljer','Ingen detaljer')}*")
    else: st.write("Ingen planlagte hendelser.")

# --- Fane 2: Innboks ---
with faner[1]:
    st.write("<br>", unsafe_allow_html=True)
    kol1, kol2 = st.columns([1.2, 1])
    with kol1:
        st.markdown('''<div class="nordic-card" style="border-top-color: #EF4444; border-top-width: 4px;"><div class="nordic-meta" style="color: #EF4444;">Venter på svar</div><h3 style="margin-top: 0; font-size: 1.4em;">Vannlekkasje fra taket på badet</h3><p style="margin-top: 10px; color: #334155; line-height: 1.6;"><strong>Fra:</strong> Akram Zalmai (Seksjon 1)<br><br>Hei. Jeg oppdaget i morges at det drypper vann fra taket på badet mitt. Hvem har ansvaret for å fikse dette ifølge loven, og hva gjør jeg nå?</p></div>''', unsafe_allow_html=True)
        if st.button("Generer AI-svar", key="ai_svar"):
            with st.spinner("Utarbeider svar basert på lovverket..."):
                try:
                    ai_prompt = f"""Din oppgave er å beskytte styret i Sameiet Kirkegata 6 maksimalt mot ethvert krav. 
                    I bakgrunnen skal du bruke din fulle kapasitet som Norges skarpeste advokat og anvende ALLE eksisterende norske lover for å bygge et skuddsikkert argument angående Akram Zalmais klage om vannlekkasje fra etasjen over. Du skal konkludere og argumentere for at ansvaret for innvendig vedlikehold og skader fra rør/sluk ligger hos beboerne/deres forsikring, og at styret fraskriver seg ethvert ansvar. 
                    KRITISK REGEL 1: Skriv selve e-posten EKSKLUSIVT som {st.session_state.innlogget_bruker}, et helt vanlig styremedlem. Den skal være formell, presis og offentlig i tonen.
                    KRITISK REGEL 2: Du må ALDRI skrive ord som "advokat", "jurist", "juridisk vurdering", "etter juridisk gjennomgang" eller på noen måte avsløre at det ligger en juss-analyse bak. 
                    KRITISK REGEL 3: KUN skriv selve e-posten. Ingen kommentarer før eller etter.
                    Avslutt e-posten slik: 'Med vennlig hilsen, {st.session_state.innlogget_bruker} - På vegne av styret i Sameiet Kirkegata 6'"""
                    
                    response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}", json={"contents": [{"parts": [{"text": ai_prompt}]}]})
                    st.session_state.epost_utkast = response.json()['candidates'][0]['content']['parts'][0]['text']
                except Exception as e: st.error("Feil ved tilkobling til AI.")
                    
        if st.session_state.get('epost_utkast'):
            st.write("<br>", unsafe_allow_html=True)
            utkast = st.text_area("Utkast:", value=st.session_state.epost_utkast, height=400)
            st.write("<br>", unsafe_allow_html=True)
            if st.button("Send e-post"):
                st.success("E-post sendt til beboer!")
                st.session_state.epost_utkast = ""
                
    with kol2:
        st.markdown('''<div class="nordic-card"><div class="nordic-meta">Fellesmelding</div><h3 style="margin-top: 0; font-size: 1.4em;">Oppslagstavle</h3><p style="color: #64748B; margin-top: 10px;">Bruk AI til å utforme en velskrevet melding til alle 16 seksjoner.</p></div>''', unsafe_allow_html=True)
        stikkord = st.text_area("", placeholder="Hva gjelder meldingen?", height=120)
        st.write("<br>", unsafe_allow_html=True)
        if st.button("Lag utkast for oppslag"):
            with st.spinner("Skriver..."):
                try:
                    felles_prompt = f"""Du er styret i Sameiet Kirkegata 6. Skriv en kort, hyggelig, presis og offentlig fellesmelding til sameiet basert på disse stikkordene: {stikkord}. Sørg for at meldingen er juridisk trygg (uten å nevne juss eller advokat). Skriv KUN meldingen. Signer som {st.session_state.innlogget_bruker}."""
                    response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}", json={"contents": [{"parts": [{"text": felles_prompt}]}]})
                    st.session_state.felles_utkast = response.json()['candidates'][0]['content']['parts'][0]['text']
                except: pass
        if st.session_state.get('felles_utkast'):
            st.write("<br>", unsafe_allow_html=True)
            f_utkast = st.text_area("Utkast til tavle:", value=st.session_state.felles_utkast, height=200)
            st.write("<br>", unsafe_allow_html=True)
            if st.button("Publiser til tavle"):
                st.success("Oppslag publisert!")
                st.session_state.felles_utkast = ""

# --- Fane 3: Beboere ---
with faner[2]:
    st.markdown("### Personregister")
    st.write(f"Aktiv profil for redigering: **{st.session_state.innlogget_bruker}**")
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("➕ Legg til ny beboer"): st.session_state.vis_ny_beb = True
    if st.session_state.get('vis_ny_beb', False):
        with st.form("ny_beb_form"):
            st.markdown("#### Ny Beboer")
            n = st.text_input("Navn:")
            e = st.text_input("E-post:")
            s = st.text_input("Seksjon:")
            if st.form_submit_button("Lagre beboer"):
                if n and e:
                    db["alle_beboere"].append({"Navn": n, "E-post": e, "Seksjon": s})
                    zapisz_dane(db)
                    st.session_state.vis_ny_beb = False
                    st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    valgt_epost = st.session_state.get("valgt_beboer_epost")
    
    if valgt_epost:
        akt_beboer = next((b for b in db["alle_beboere"] if b["E-post"] == valgt_epost), None)
        if akt_beboer:
            st.markdown(f'''<div class="nordic-card" style="border-top-color: #0F172A; background-color: #F8FAFC;">
                <div class="nordic-meta">Valgt Profil</div>
                <h3 style="margin-top: 0; color: #0F172A; font-size: 1.8em;">👤 {akt_beboer['Navn']} — {akt_beboer['Seksjon']}</h3>
                <p style="color: #475569; margin-bottom: 0; font-size: 1.1em;">E-post: <strong>{akt_beboer['E-post']}</strong></p>
            </div>''', unsafe_allow_html=True)
            
            c_btn1, c_btn2, c_btn3 = st.columns([1, 1, 3])
            with c_btn1:
                if st.button("Lukk profil", use_container_width=True): 
                    st.session_state.valgt_beboer_epost = None; st.session_state.redigerer_beboer = False; st.rerun()
            with c_btn2:
                if st.button("Rediger profil", use_container_width=True): st.session_state.redigerer_beboer = not st.session_state.get('redigerer_beboer', False); st.rerun()
            with c_btn3:
                if st.button("Slett beboer fra systemet"):
                    db["alle_beboere"] = [b for b in db["alle_beboere"] if b["E-post"] != valgt_epost]
                    zapisz_dane(db); st.session_state.valgt_beboer_epost = None; st.rerun()

            if st.session_state.get('redigerer_beboer', False):
                st.markdown('''<div class="nordic-card"><div class="nordic-meta">Rediger Beboeropplysninger</div>''', unsafe_allow_html=True)
                with st.form("form_rediger_beboer"):
                    nytt_navn = st.text_input("Fullt navn:", value=akt_beboer["Navn"])
                    ny_epost = st.text_input("E-postadresse:", value=akt_beboer["E-post"])
                    ny_seksjon = st.text_input("Seksjon / Leilighet:", value=akt_beboer["Seksjon"])
                    st.write("<br>", unsafe_allow_html=True)
                    if st.form_submit_button("Lagre endringer"):
                        for b in db["alle_beboere"]:
                            if b["E-post"] == valgt_epost:
                                b["Navn"] = nytt_navn; b["E-post"] = ny_epost; b["Seksjon"] = ny_seksjon
                        if ny_epost != valgt_epost and valgt_epost in db["beboer_data"]:
                            db["beboer_data"][ny_epost] = db["beboer_data"].pop(valgt_epost)
                        zapisz_dane(db)
                        st.session_state.redigerer_beboer = False; st.session_state.valgt_beboer_epost = ny_epost; st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            if valgt_epost not in db["beboer_data"]: db["beboer_data"][valgt_epost] = {"dokumenter": [], "korrespondanse": []}
            dp = db["beboer_data"][valgt_epost]
            
            st.write("<br>", unsafe_allow_html=True)

            c_dok, c_korr = st.columns(2)
            with c_dok:
                st.markdown("#### Dokumenter i skyen")
                with st.expander("➕ Last opp dokument"):
                    with st.form(f"upl_b_{valgt_epost}"):
                        t = st.text_input("Tittel:")
                        f = st.file_uploader("Fil:")
                        if st.form_submit_button("Lagre til skyen"):
                            if t and f:
                                l_navn = lagre_opplastet_fil(f)
                                dp["dokumenter"].append({"tittel": t, "filnavn": l_navn})
                                zapisz_dane(db); st.rerun()
                for idx, d in enumerate(dp["dokumenter"]):
                    def slett_d(idx=idx): dp["dokumenter"].pop(idx); zapisz_dane(db)
                    vis_fil_rad(d['filnavn'], d['tittel'], f"b_{valgt_epost}_{idx}", er_admin_slett=slett_d)

            with c_korr:
                st.markdown("#### Logg & Samtaler")
                with st.expander("➕ Skriv notat"):
                    with st.form(f"notat_{valgt_epost}"):
                        em = st.text_input("Emne:")
                        innh = st.text_area("Notat:")
                        if st.form_submit_button("Lagre notat"):
                            if em and innh:
                                dp["korrespondanse"].append({"dato": datetime.date.today().strftime("%d.%m.%Y"), "emne": em, "innhold": innh})
                                zapisz_dane(db); st.rerun()
                for idx, k in enumerate(dp["korrespondanse"]):
                    st.markdown(f'''<div style="background-color: #FFFFFF; padding: 20px 24px; border-radius: 10px; margin-bottom: 16px; border-left: 4px solid #3B82F6; box-shadow: 0 4px 12px rgba(0,0,0,0.03); border-top: 1px solid #F1F5F9; border-right: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9;"><div style="font-size: 0.75em; color: #3B82F6; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">{k['dato']}</div><div style="font-weight: 700; color: #0F172A; margin-top: 6px; font-size: 1.1em;">{k['emne']}</div><div style="color: #475569; font-size: 0.95em; margin-top: 8px; line-height: 1.5;">{k['innhold']}</div></div>''', unsafe_allow_html=True)
                    if st.button("Slett notat", key=f"sl_k_{idx}_{valgt_epost}"):
                        dp["korrespondanse"].pop(idx); zapisz_dane(db); st.rerun()
            st.write("---")

    col_v, col_h = st.columns(2)
    for i, b in enumerate(db["alle_beboere"]):
        with (col_v if i % 2 == 0 else col_h):
            st.markdown(f'''<div class="nordic-card" style="padding: 24px; margin-bottom: 16px; text-align: left; border-top-color: #CBD5E1;">
                <h4 style="margin:0; font-size:1.2em; color: #0F172A;">{b['Navn']}</h4>
                <p style="color:#64748B; font-size:0.9em; margin:8px 0 20px 0;">{b['Seksjon']} | {b['E-post']}</p>
            </div>''', unsafe_allow_html=True)
            if st.button("Åpne profil", key=f"apne_{b['E-post']}", use_container_width=True):
                st.session_state.valgt_beboer_epost = b['E-post']; st.session_state.redigerer_beboer = False; st.rerun()

# --- Fane 4: Sentralt Arkiv ---
with faner[3]:
    st.markdown("### Sentralt Dokumentarkiv")
    st.write("<br>", unsafe_allow_html=True)
    
    with st.expander("📁 Opprett ny mappe"):
        with st.form("ny_mappe_form"):
            mn = st.text_input("Mappenavn:")
            st.write("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Opprett mappe"):
                if mn and mn not in db["bygg_mapper"]:
                    db["bygg_mapper"][mn] = []; zapisz_dane(db); st.rerun()
    
    for mappe_navn, filer in db["bygg_mapper"].items():
        st.markdown(f"<div class='mappe-header'>", unsafe_allow_html=True)
        c_t, c_opp, c_slett = st.columns([4, 2, 2])
        with c_t: st.markdown(f"<h3 style='margin: 0; font-size: 1.6em;'>📁 {mappe_navn}</h3>", unsafe_allow_html=True)
        with c_opp:
            if st.button("➕ Last opp her", key=f"vis_opp_{mappe_navn}", use_container_width=True): st.session_state[f"form_opplast_{mappe_navn}"] = not st.session_state.get(f"form_opplast_{mappe_navn}", False); st.rerun()
        with c_slett:
            if st.button("🗑️ Slett mappe", key=f"slett_{mappe_navn}", use_container_width=True):
                db["bygg_mapper"].pop(mappe_navn); zapisz_dane(db); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.get(f"form_opplast_{mappe_navn}", False):
            with st.form(f"opplast_{mappe_navn}"):
                st.markdown(f"**Last opp fil til {mappe_navn}**")
                t_dok = st.text_input("Tittel på filen:")
                f_opp = st.file_uploader("Velg dokument:")
                st.write("<br>", unsafe_allow_html=True)
                if st.form_submit_button("Lagre i skyen"):
                    if t_dok and f_opp:
                        l_navn = lagre_opplastet_fil(f_opp)
                        db["bygg_mapper"][mappe_navn].append({"tittel": t_dok, "filnavn": l_navn})
                        zapisz_dane(db); st.session_state[f"form_opplast_{mappe_navn}"] = False; st.rerun()
        
        if not filer: st.markdown("<p style='color:#94A3B8; font-style:italic; font-size:0.95em;'>Ingen filer i mappen.</p>", unsafe_allow_html=True)
        for idx, fil in enumerate(filer):
            def slett_arkiv_d(m=mappe_navn, i=idx): db["bygg_mapper"][m].pop(i); zapisz_dane(db)
            vis_fil_rad(fil['filnavn'], fil['tittel'], f"ark_{mappe_navn}_{idx}", er_admin_slett=slett_arkiv_d)
        st.write("<br><br>", unsafe_allow_html=True)

# --- Fane 5: Kalender ---
with faner[4]:
    st.markdown("### Styrets Kalender & Planlegging")
    k_fane1, k_fane2, k_fane3 = st.tabs(["📅 Månedskalender", "📋 Årshjul & Aktiviteter", "➕ Ny hendelse"])
    
    with k_fane1:
        st.write("<br>", unsafe_allow_html=True)
        col_aar, col_maned = st.columns([1, 1])
        with col_aar: valgt_aar = st.selectbox("Velg år:", [2026, 2027], index=0)
        with col_maned:
            maned_navn = ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"]
            valgt_maned_navn = st.selectbox("Velg måned:", maned_navn, index=9)
            valgt_maned = maned_navn.index(valgt_maned_navn) + 1

        st.markdown(f'''<h3 style="text-align: center; margin: 25px 0 30px 0; font-family: 'Playfair Display', serif; font-size: 2em;">{valgt_maned_navn} {valgt_aar}</h3>''', unsafe_allow_html=True)
        forste_ukedag, dager_i_mnd = calendar.monthrange(valgt_aar, valgt_maned)
        ukedager = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
        
        table_html = "<table class='kalender-table'><thead><tr>"
        for d in ukedager: table_html += f"<th>{d}</th>"
        table_html += "</tr></thead><tbody><tr>"
        for _ in range(forste_ukedag): table_html += "<td class='empty'></td>"
            
        gjeldende_dag_i_uke = forste_ukedag
        for dag in range(1, dager_i_mnd + 1):
            if gjeldende_dag_i_uke == 7:
                table_html += "</tr><tr>"; gjeldende_dag_i_uke = 0
            dato_str = f"{valgt_aar}-{valgt_maned:02d}-{dag:02d}"
            hendelser = [o for o in db["kalender_oppgaver"] if o["dato"] == dato_str]
            td_class = "has-event" if hendelser else ""
            table_html += f"<td class='{td_class}'><strong>{dag}</strong>"
            for h in hendelser:
                tid_visning = f"kl. {h.get('tid', '')} " if h.get('tid') else ""
                table_html += f"<br><span class='event-badge'>{tid_visning}{h['oppgave']}</span>"
            table_html += "</td>"; gjeldende_dag_i_uke += 1
        while gjeldende_dag_i_uke < 7: table_html += "<td class='empty'></td>"; gjeldende_dag_i_uke += 1
        table_html += "</tr></tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
        
    with k_fane2:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown('''<h4 style="font-family: 'Playfair Display', serif;">Alle aktiviteter</h4>''', unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        for oppg in db["kalender_oppgaver"]:
            st.markdown(f'''<div class="nordic-card" style="border-top-color:#10B981; padding:30px;">
                <div style="font-size:0.8em; font-weight:700; color:#10B981; text-transform:uppercase; letter-spacing: 1.5px;">{oppg['dato']} - kl. {oppg.get('tid','')}</div>
                <h4 style="margin:10px 0; font-size: 1.4em;">{oppg['oppgave']}</h4>
                <p style="margin:0; color:#475569; line-height: 1.6;">{oppg.get('detaljer','')}</p>
            </div>''', unsafe_allow_html=True)
            if st.button("Slett hendelse", key=f"s_kal_{oppg['id']}"):
                db["kalender_oppgaver"] = [o for o in db["kalender_oppgaver"] if o["id"] != oppg["id"]]
                zapisz_dane(db); st.rerun()
            st.write("<br>", unsafe_allow_html=True)

    with k_fane3:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown('''<h4 style="font-family: 'Playfair Display', serif;">Ny aktivitet</h4>''', unsafe_allow_html=True)
        with st.form("kal_ny"):
             k_dato = st.date_input("Dato:")
             k_tid = st.text_input("Klokkeslett (eks. 18:00):", "18:00")
             k_tittel = st.text_input("Tittel:")
             k_det = st.text_area("Beskrivelse:")
             st.write("<br>", unsafe_allow_html=True)
             if st.form_submit_button("Lagre i kalender"):
                 ny_id = max([o["id"] for o in db["kalender_oppgaver"]], default=0) + 1
                 db["kalender_oppgaver"].append({"id": ny_id, "dato": str(k_dato), "tid": k_tid, "oppgave": k_tittel, "detaljer": k_det, "type": "Aktivitet"})
                 db["kalender_oppgaver"] = sorted(db["kalender_oppgaver"], key=lambda k: k['dato'])
                 zapisz_dane(db); st.rerun()

# --- Fane 6: Sikkerhet ---
with faner[5]:
    st.markdown("### ⚙️ Sikkerhet & Database-Backup")
    st.write("<br>", unsafe_allow_html=True)
    st.write("Last ned en komplett kopi av sky-databasen for styret (GDPR-kompatibelt).")
    st.write("<br>", unsafe_allow_html=True)
    db_bytes = json.dumps(db, ensure_ascii=False, indent=4).encode('utf-8')
    st.download_button(label="💾 Last ned hele databasen", data=db_bytes, file_name=f"SmartStyre_Backup_K6_{datetime.date.today().strftime('%Y-%m-%d')}.json", mime="application/json")
