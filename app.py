import streamlit as st
import requests
import datetime
import calendar
import json
import os
import base64

# ==========================================
# 1. ZARZĄDZANIE DANYMI I PLIKAMI
# ==========================================
DB_PATH = "baza_danych.json"
UPLOAD_DIR = "opplastede_filer"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

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
            "dokumenter": [
                {"tittel": "Tidligere klage på vannlekkasje", "filnavn": "Klage_Vannlekkasje_2024.pdf"}
            ],
            "korrespondanse": [
                {"dato": "09.10.2026", "emne": "Vannlekkasje fra taket på badet", "innhold": "Rapportert drypping fra overliggende leilighet (etasje oppgang B). Styret har avvist ansvar jf. eierseksjonsloven."}
            ]
        }
    },
    "bygg_mapper": {
        "Forsikring": [{"tittel": "Forsikringsavtale If", "filnavn": "Forsikringsavtale_If_2026.pdf"}],
        "Tegninger & Bygg": [{"tittel": "Plantegninger 1. etg", "filnavn": "Plantegninger_Kirkegata_6.pdf"}],
        "Økonomi & Budsjett": [
            {"tittel": "Nytt budsjett 2027", "filnavn": "Nytt_budsjett_2027_Sameiet_K6.xlsx"},
            {"tittel": "Budsjett 2027 Sameiet K6", "filnavn": "Budsjett_2027_Sameiet_K6.pdf"},
            {"tittel": "507 - Årsregnskap 2025", "filnavn": "507_Aarsregnskap_2025.pdf"},
            {"tittel": "507 - Økonomirapport pr. Q3 2026", "filnavn": "507_Oekonomirapport_pr_Q3_2026.pdf"}
        ],
        "Møtereferater": []
    },
    "kalender_oppgaver": [
        {"id": 1, "dato": "2026-10-11", "tid": "18:00", "oppgave": "Styremøte", "detaljer": "Gjennomgang av budsjett for 2027", "type": "Møte"},
        {"id": 2, "dato": "2026-10-20", "tid": "18:00", "oppgave": "Ekstraordinært Årsmøte", "detaljer": "Behandling av budsjett og økning av felleskostnader", "type": "Møte"}
    ]
}

def wczytaj_dane():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                dane = json.load(f)
                for klucz in DOMYSLNE_DANE:
                    if klucz not in dane:
                        dane[klucz] = DOMYSLNE_DANE[klucz]
                return dane
        except:
            return DOMYSLNE_DANE
    else:
        zapisz_dane(DOMYSLNE_DANE)
        return DOMYSLNE_DANE

def zapisz_dane(dane):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(dane, f, ensure_ascii=False, indent=4)

if "db" not in st.session_state:
    st.session_state.db = wczytaj_dane()

db = st.session_state.db

def lagre_opplastet_fil(uploaded_file):
    if uploaded_file is not None:
        fil_sti = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(fil_sti, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return uploaded_file.name
    return None

def vis_fil_seksjon(filnavn, tittel, unik_id):
    fil_sti = os.path.join(UPLOAD_DIR, filnavn)
    mime = "application/octet-stream"
    if filnavn.endswith('.pdf'): mime = "application/pdf"
    elif filnavn.endswith(('.png', '.jpg', '.jpeg')): mime = "image/jpeg"
    elif filnavn.endswith('.txt'): mime = "text/plain"

    col_s1, col_s2 = st.columns([1, 1])
    
    with col_s1:
        if st.button("Se i nettleser", key=f"se_{unik_id}"):
            st.session_state[f"vis_popup_{unik_id}"] = True
            
    with col_s2:
        if os.path.exists(fil_sti):
            with open(fil_sti, "rb") as f:
                bytes_data = f.read()
            st.download_button(
                label="Last ned",
                data=bytes_data,
                file_name=filnavn,
                mime=mime,
                key=f"dl_{unik_id}"
            )
        else:
            st.caption("Fil ikke på server")

    if st.session_state.get(f"vis_popup_{unik_id}", False):
        @st.dialog(f"Viser dokument: {tittel}")
        def vis_modal():
            st.write(f"Filnavn: {filnavn}")
            if os.path.exists(fil_sti):
                if filnavn.endswith(('.png', '.jpg', '.jpeg')):
                    st.image(fil_sti)
                elif filnavn.endswith('.pdf'):
                    with open(fil_sti, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    with open(fil_sti, "r", encoding="utf-8", errors="ignore") as f:
                        st.text(f.read())
            else:
                st.warning("Beklager, denne eksempelfilen er ikke lastet opp fysisk på serveren enda.")
            
            if st.button("Lukk vindu", key=f"lukk_modal_{unik_id}"):
                st.session_state[f"vis_popup_{unik_id}"] = False
                st.rerun()
        vis_modal()

# ==========================================
# 2. DESIGN OG OPPSETT (Nordisk stil)
# ==========================================
st.set_page_config(page_title="StyreSmart", page_icon="🏢", layout="wide")

st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

    [data-testid="stAppViewContainer"] { background-color: #F7F6F2 !important; }
    [data-testid="stSidebar"] { background-color: #EFECE5 !important; border-right: 1px solid #E5E2D9 !important; }
    
    .stApp, p, label, li, input, textarea { 
        font-family: 'Lato', sans-serif !important; 
        color: #2D2D2D !important; 
        font-weight: 400 !important; 
    }
    h1, h2, h3, h4 { 
        font-family: 'Playfair Display', serif !important; 
        color: #1A1A1A !important; 
        font-weight: 600 !important; 
        letter-spacing: 0.5px; 
    }
    h1 { text-align: center; margin-bottom: 30px !important; font-size: 3.2rem !important; color: #222222 !important; }

    header {visibility: hidden;} 
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;}

    .stButton > button, .stDownloadButton > button {
        background-color: #2B3A41 !important; 
        color: #FFFFFF !important; 
        border-radius: 4px !important; 
        border: none !important;
        padding: 9px 20px !important; 
        font-family: 'Lato', sans-serif !important; 
        font-weight: 600 !important; 
        font-size: 0.86em !important;
        text-transform: uppercase; 
        letter-spacing: 1.2px !important; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important; 
        transition: all 0.2s ease !important;
        display: inline-flex !important;
        justify-content: center !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { 
        background-color: #1A2429 !important; 
        transform: translateY(-1px) !important; 
        box-shadow: 0 6px 16px rgba(0,0,0,0.12) !important; 
    }
    .stButton button p, .stDownloadButton button p { color: #FFFFFF !important; margin: 0 !important; }

    .nordic-card { 
        background-color: #FFFFFF; 
        padding: 24px 28px; 
        border-radius: 6px; 
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04); 
        margin-bottom: 16px; 
        border-top: 3px solid #D1C7B7; 
    }
    .viktig-boks { 
        background-color: #F1F3ED; 
        padding: 22px 25px; 
        border-radius: 6px; 
        border-left: 5px solid #738269; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04); 
    }
    .tekst-fremhevet { 
        font-family: 'Playfair Display', serif; 
        font-weight: 700; 
        color: #2B3A41; 
        font-size: 1.15em; 
    }
    .nordic-meta { 
        font-size: 0.78em; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
        color: #7A7A7A; 
        margin-bottom: 12px; 
        border-bottom: 1px solid #EBEBEB; 
        padding-bottom: 8px; 
        font-weight: 700; 
    }
    .nordic-text { 
        font-size: 1.02em; 
        line-height: 1.6; 
        color: #333333; 
    }

    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid #DCDCDC; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        white-space: pre-wrap; 
        background-color: transparent !important; 
        border-radius: 0px; 
        padding-top: 10px; 
        padding-bottom: 10px; 
        font-family: 'Playfair Display', serif !important; 
        font-size: 1.15em !important; 
        color: #999999 !important; 
    }
    .stTabs [aria-selected="true"] { 
        color: #1A1A1A !important; 
        border-bottom: 3px solid #1A1A1A !important; 
        font-weight: 600 !important; 
    }
    
    .kalender-table { width: 100%; border-collapse: separate; border-spacing: 6px; table-layout: fixed; }
    .kalender-table th { background-color: #EFECE5; color: #555555; font-family: 'Playfair Display', serif; padding: 10px; text-align: center; font-weight: 600; border-radius: 4px; font-size: 0.95em; }
    .kalender-table td { background-color: #FFFFFF; border: 1px solid #E5E2D9; height: 75px; vertical-align: top; padding: 8px; border-radius: 4px; font-size: 0.85em; }
    .kalender-table td.empty { background-color: transparent; border: none; }
    .kalender-table td.has-event { background-color: #F1F3ED; border-left: 4px solid #738269; }
    .event-badge { background-color: #738269; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.78em; font-weight: 600; display: inline-block; margin-top: 4px; }
    
    .mappe-overskrift {
        font-family: 'Playfair Display', serif;
        font-size: 1.18em;
        font-weight: 600;
        color: #1A1A1A;
        letter-spacing: 0.5px;
        margin-top: 24px;
        margin-bottom: 12px;
        border-bottom: 1px solid #E2DED5;
        padding-bottom: 6px;
    }
    .beboer-boks {
        background-color: #FFFFFF;
        padding: 18px 22px;
        border-radius: 6px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        margin-bottom: 12px;
        border-left: 3px solid #D1C7B7;
        transition: all 0.2s ease;
    }
    .beboer-boks-valgt {
        background-color: #F9FAF8;
        border-left: 4px solid #738269;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    }
</style>
''', unsafe_allow_html=True)

# ==========================================
# 3. SIKKERHET (INNLOGGING)
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY", "")
ai_klar = bool(api_key)

if "er_logget_inn" not in st.session_state:
    st.session_state.er_logget_inn = False

if not st.session_state.er_logget_inn:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="nordic-card" style="text-align: center; padding: 40px;">
            <h2 style="font-family: 'Playfair Display', serif; margin-bottom: 10px;">StyreSmart</h2>
            <p style="color: #666; font-size: 0.9em; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 30px;">Sameiet Kirkegata 6</p>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            bruker_input = st.text_input("Brukernavn:")
            passord_input = st.text_input("Passord:", type="password")
            submitted = st.form_submit_button("Logg inn i portalen")
            
            if submitted:
                if bruker_input.strip().lower() == "kirkegata6" and passord_input == "Styret2026":
                    st.session_state.er_logget_inn = True
                    st.success("Innlogging vellykket!")
                    st.rerun()
                else:
                    st.error("Feil brukernavn eller passord. Bruk 'Kirkegata6' og 'Styret2026'.")
                    
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if "epost_utkast" not in st.session_state: st.session_state.epost_utkast = ""
if "fellesmelding_utkast" not in st.session_state: st.session_state.fellesmelding_utkast = ""
if "innlogget_bruker" not in st.session_state: st.session_state.innlogget_bruker = "Weronika Bhatti"
if "valgt_beboer_epost" not in st.session_state: st.session_state.valgt_beboer_epost = None
if "redigerer_beboer" not in st.session_state: st.session_state.redigerer_beboer = False
if "redigerer_kalender_id" not in st.session_state: st.session_state.redigerer_kalender_id = None
if "vis_ny_beboer_form" not in st.session_state: st.session_state.vis_ny_beboer_form = False

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-top: 15px; color: #1A1A1A;'>StyreSmart</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.85em; letter-spacing: 2px; color: #666;'>KIRKEGATA 6</p>", unsafe_allow_html=True)
    st.write("---")
    if ai_klar:
        st.markdown("<div style='background-color: #E8EDE1; padding: 10px; border-radius: 4px; border-left: 4px solid #738269; text-align: center;'><span style='color: #4A5D3E; font-weight: 700; font-size: 0.85em;'>✓ AI-ASSISTENT TILKOBLET</span></div>", unsafe_allow_html=True)
    else:
        st.error("Mangler API-nøkkel")
        
    st.write("---")
    st.markdown('''<p style="font-family: 'Playfair Display', serif; font-size: 1.15em; border-bottom: 1px solid #DCDCDC; padding-bottom: 5px;">Innlogging / Profil</p>''', unsafe_allow_html=True)
    
    styremedlemmer = ["Weronika Bhatti", "Ine Foss", "Maria Frang"]
    valgt_medlem = st.selectbox("Velg din profil:", styremedlemmer, index=styremedlemmer.index(st.session_state.innlogget_bruker), key="profil_valg_box")
    if valgt_medlem != st.session_state.innlogget_bruker:
        st.session_state.innlogget_bruker = valgt_medlem
        st.rerun()

    st.markdown(f'''<p style="font-size: 0.9em; color: #555; margin-top: 10px;">Aktiv bruker: <strong>{st.session_state.innlogget_bruker}</strong></p>''', unsafe_allow_html=True)
    
    if st.button("Logg ut av portalen"):
        st.session_state.er_logget_inn = False
        st.rerun()

    st.write("---")
    st.markdown('''<p style="font-family: 'Playfair Display', serif; font-size: 1.15em; border-bottom: 1px solid #DCDCDC; padding-bottom: 5px;">Styrets sammensetning</p>''', unsafe_allow_html=True)
    for m in styremedlemmer:
        if m == st.session_state.innlogget_bruker:
            st.markdown(f"**{m}** (Aktiv nå)")
        else:
            st.markdown(f"<span style='color: #888888;'>{m}</span>", unsafe_allow_html=True)

# Hovedskjerm
st.title("Styreportal")
fane1, fane2, fane3, fane4, fane5 = st.tabs(["Innboks", "Beboere", "Arkiv", "Kalender", "Jus"])

# Fane 1
with fane1:
    st.write("<br>", unsafe_allow_html=True)
    kol1, kol2 = st.columns([1.2, 1])
    with kol1:
        st.markdown('''
        <div class="viktig-boks">
            <div class="nordic-meta" style="border-bottom-color: #D3D9CC; color: #5B6B52;">Ubehandlet Henvendelse</div>
            <span class="tekst-fremhevet">Vannlekkasje fra taket på badet</span>
            <p class="nordic-text" style="margin-top: 10px;"><strong>Fra:</strong> Akram Zalmai (Seksjon 1)<br><br>Hei. Jeg oppdaget i morges at det drypper vann fra taket på badet mitt. Hvem har ansvaret for å fikse dette ifølge loven, og hva gjør jeg nå?</p>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("Generer svar", key="generer_svar_1"):
            if ai_klar:
                with st.spinner("Utformer svar..."):
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
                    prompt = f"Du er en bestemt juridisk AI-assistent for styret i Sameiet Kirkegt. 6 (signeres av {st.session_state.innlogget_bruker} på vegne av styret). Beboer Akram Zalmai klager på lekkasje fra etasjen over. Skriv et formelt svar fra styret. Argumenter med Eierseksjonsloven for at innvendig vedlikehold er seksjonseierens ansvar. Avslutt KUN med 'Med vennlig hilsen, {st.session_state.innlogget_bruker} for Styret i Sameiet Kirkegt. 6'."
                    try:
                        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                        if response.status_code == 200: 
                            st.session_state.epost_utkast = response.json()['candidates'][0]['content']['parts'][0]['text']
                    except Exception:
                        st.error("Kunne ikke koble til tjenesten.")

        if st.session_state.epost_utkast:
            st.write("<br>", unsafe_allow_html=True)
            st.session_state.epost_utkast = st.text_area("Svarutkast:", value=st.session_state.epost_utkast, height=300)
            if st.button("Send e-post", key="send_epost_1"):
                st.success(f"E-post sendt og godkjent av {st.session_state.innlogget_bruker}!")
                st.balloons()
                
    with kol2:
        st.markdown('''<div class="nordic-card"><div class="nordic-meta">Fellesmelding</div><h3 style="margin-top: 0; font-size: 1.4em;">Oppslagstavle</h3><div class="nordic-text" style="font-size: 0.95em;">Bruk assistenten til å utforme en velskrevet melding til alle 16 seksjoner.</div></div>''', unsafe_allow_html=True)
        stikkord_felles = st.text_area("", placeholder="Hva gjelder meldingen?", height=100)
        if st.button("Lag utkast", key="lag_utkast_1"):
            if ai_klar and stikkord_felles:
                with st.spinner("Skriver..."):
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
                    prompt = f"Du er styret i Sameiet Kirkegt. 6. Skriv en kort, høflig felles e-post til beboere basert på: {stikkord_felles}. Avslutt med 'Hilsen {st.session_state.innlogget_bruker} for Styret i Sameiet Kirkegt. 6'."
                    try:
                        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                        if response.status_code == 200: 
                            st.session_state.fellesmelding_utkast = response.json()['candidates'][0]['content']['parts'][0]['text']
                    except Exception:
                        pass
        if st.session_state.fellesmelding_utkast:
            st.session_state.fellesmelding_utkast = st.text_area("Utkast:", value=st.session_state.fellesmelding_utkast, height=200)
            if st.button("Publiser til beboere", key="publiser_1"): 
                st.success(f"Fellesmelding publisert av {st.session_state.innlogget_bruker}!")

# Fane 2 (Beboere)
with fane2:
    st.markdown("### Personregister")
    st.write(f"Innlogget som: **{st.session_state.innlogget_bruker}**. Klikk på **Åpne profil** på en beboer for å se samlet korrespondanse, dokumenter eller redigere.")
    st.write("<br>", unsafe_allow_html=True)
    
    if st.button("Legg til ny beboer"):
        st.session_state.vis_ny_beboer_form = not st.session_state.vis_ny_beboer_form
        
    if st.session_state.vis_ny_beboer_form:
        st.markdown('''<div class="nordic-card">''', unsafe_allow_html=True)
        st.markdown('''<div class="nordic-meta">Legg til ny beboer</div>''', unsafe_allow_html=True)
        with st.form("form_ny_beboer"):
            n_navn = st.text_input("Fullt navn:")
            n_epost = st.text_input("E-postadresse:")
            n_seksjon = st.text_input("Seksjon / Leilighet:", placeholder="F.eks: Seksjon 4")
            
            c_s1, c_s2 = st.columns([1, 4])
            with c_s1:
                if st.form_submit_button("Lagre beboer"):
                    if n_navn and n_epost:
                        db["alle_beboere"].append({"Navn": n_navn, "E-post": n_epost, "Seksjon": n_seksjon})
                        zapisz_dane(db)
                        st.session_state.vis_ny_beboer_form = False
                        st.success("Mottager ble lagt til i registeret!")
                        st.rerun()
            with c_s2:
                if st.form_submit_button("Avbryt"):
                    st.session_state.vis_ny_beboer_form = False
                    st.rerun()
        st.markdown('''</div>''', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    valgt_epost = st.session_state.valgt_beboer_epost
    if valgt_epost:
        akt_beboer = next((b for b in db["alle_beboere"] if b["E-post"] == valgt_epost), None)
        if akt_beboer:
            st.markdown(f'''
            <div class="nordic-card" style="border-top: 3px solid #738269;">
                <div class="nordic-meta">Valgt Beboerprofil</div>
                <h3 style="margin-top: 0; color: #1A1A1A;">👤 {akt_beboer['Navn']} — {akt_beboer['Seksjon']}</h3>
                <p style="color: #666666; font-size: 0.95em;">E-post: <strong>{akt_beboer['E-post']}</strong></p>
            </div>
            ''', unsafe_allow_html=True)
            
            k_rad1, k_rad2, k_rad3, _ = st.columns([1.2, 1.2, 1.2, 2])
            with k_rad1:
                if st.button("Rediger", key="btn_toggle_edit"):
                    st.session_state.redigerer_beboer = not st.session_state.redigerer_beboer
            with k_rad2:
                if st.button("Slett beboer", key="btn_slett_beboer"):
                    db["alle_beboere"] = [b for b in db["alle_beboere"] if b["E-post"] != valgt_epost]
                    zapisz_dane(db)
                    st.session_state.valgt_beboer_epost = None
                    st.success("Beboer ble slettet.")
                    st.rerun()
            with k_rad3:
                if st.button("Lukk profil", key="btn_lukk_profil"):
                    st.session_state.valgt_beboer_epost = None
                    st.session_state.redigerer_beboer = False
                    st.rerun()

            if st.session_state.redigerer_beboer:
                st.markdown('''<div class="nordic-card">''', unsafe_allow_html=True)
                st.markdown('''<div class="nordic-meta">Rediger Beboeropplysninger</div>''', unsafe_allow_html=True)
                with st.form("form_rediger_beboer"):
                    nytt_navn = st.text_input("Fullt navn:", value=akt_beboer["Navn"])
                    ny_epost = st.text_input("E-postadresse:", value=akt_beboer["E-post"])
                    ny_seksjon = st.text_input("Seksjon / Leilighet:", value=akt_beboer["Seksjon"])
                    
                    if st.form_submit_button("Lagre endringer"):
                        for b in db["alle_beboere"]:
                            if b["E-post"] == valgt_epost:
                                b["Navn"] = nytt_navn
                                b["E-post"] = ny_epost
                                b["Seksjon"] = ny_seksjon
                        zapisz_dane(db)
                        st.session_state.redigerer_beboer = False
                        st.session_state.valgt_beboer_epost = ny_epost
                        st.success("Zapisano zmiany w bazie!")
                        st.rerun()
                st.markdown('''</div>''', unsafe_allow_html=True)

            if valgt_epost not in db["beboer_data"]:
                db["beboer_data"][valgt_epost] = {"dokumenter": [], "korrespondanse": []}
            data_profil = db["beboer_data"][valgt_epost]

            c_dok, c_korr = st.columns(2)
            with c_dok:
                st.markdown('''<h4 style="color: #1A1A1A; margin-top: 15px;">Tilknyttede Dokumenter</h4>''', unsafe_allow_html=True)
                
                st.markdown('''<div style="background-color: #FFFFFF; padding: 16px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); margin-bottom: 15px;">''', unsafe_allow_html=True)
                st.markdown('''<div class="nordic-meta" style="margin-bottom: 8px;">Last opp nytt dokument</div>''', unsafe_allow_html=True)
                with st.form(f"form_last_opp_person_{valgt_epost}", clear_on_submit=True):
                    pers_dok_tittel = st.text_input("Tittel på fil:")
                    pers_fil = st.file_uploader("Velg dokument:")
                    if st.form_submit_button("Lagre på beboer"):
                        if pers_dok_tittel and pers_fil:
                            lagret_navn = lagre_opplastet_fil(pers_fil)
                            data_profil["dokumenter"].append({"tittel": pers_dok_tittel, "filnavn": lagret_navn})
                            zapisz_dane(db)
                            st.success("Lagret!")
                            st.rerun()
                        else:
                            st.warning("Vennligst fyll ut tittel og velg fil.")
                st.markdown('</div>', unsafe_allow_html=True)

                if not data_profil["dokumenter"]:
                    st.markdown('''<p style="color: #888888; font-style: italic; font-size: 0.9em;">Ingen dokumenter lagret.</p>''', unsafe_allow_html=True)
                else:
                    for idx_d, d in enumerate(data_profil["dokumenter"]):
                        st.markdown(f'''
                        <div style="background-color: #FFFFFF; padding: 14px 18px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); margin-bottom: 10px; border-left: 3px solid #738269;">
                            <div style="font-weight: 600; color: #1A1A1A; font-size: 1.02em;">{d['tittel']}</div>
                            <div style="color: #777; font-size: 0.8em; margin-bottom: 8px;">{d['filnavn']}</div>
                        ''', unsafe_allow_html=True)
                        vis_fil_seksjon(d['filnavn'], d['tittel'], f"pers_dok_{idx_d}_{valgt_epost}")
                        
                        if st.button("Slett dokument", key=f"slett_pers_dok_{idx_d}_{valgt_epost}"):
                            data_profil["dokumenter"].pop(idx_d)
                            zapisz_dane(db)
                            st.success("Slettet!")
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

            with c_korr:
                st.markdown('''<h4 style="color: #1A1A1A; margin-top: 15px;">Samtalehistorikk & E-poster</h4>''', unsafe_allow_html=True)
                
                st.markdown('''<div style="background-color: #FFFFFF; padding: 16px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); margin-bottom: 15px;">''', unsafe_allow_html=True)
                st.markdown('''<div class="nordic-meta" style="margin-bottom: 8px;">Loggfør nytt notat / samtale</div>''', unsafe_allow_html=True)
                with st.form(f"form_ny_korr_{valgt_epost}", clear_on_submit=True):
                    ny_emne = st.text_input("Emne:")
                    ny_tekst = st.text_area("Innhold / referat:")
                    if st.form_submit_button("Legg til notat"):
                        if ny_emne and ny_tekst:
                            data_profil["korrespondanse"].append({
                                "dato": datetime.date.today().strftime("%d.%m.%Y"),
                                "emne": f"{ny_emne} (Loggført av {st.session_state.innlogget_bruker})",
                                "innhold": ny_tekst
                            })
                            zapisz_dane(db)
                            st.success("Loggført!")
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

                if not data_profil["korrespondanse"]:
                    st.markdown('''<p style="color: #888888; font-style: italic; font-size: 0.9em;">Ingen loggført korrespondanse.</p>''', unsafe_allow_html=True)
                else:
                    for idx_k, k in enumerate(data_profil["korrespondanse"]):
                        st.markdown(f'''
                        <div style="background-color: #FFFFFF; padding: 14px 18px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); margin-bottom: 10px; border-left: 3px solid #738269;">
                            <div style="font-size: 0.78em; color: #738269; font-weight: 700; text-transform: uppercase;">{k['dato']}</div>
                            <div style="font-weight: 700; color: #1A1A1A; font-size: 0.98em; margin-top: 2px;">{k['emne']}</div>
                            <div style="color: #444; font-size: 0.9em; margin-top: 4px; line-height: 1.5;">{k['innhold']}</div>
                        ''', unsafe_allow_html=True)
                        if st.button("Slett notat", key=f"slett_korr_{idx_k}_{valgt_epost}"):
                            data_profil["korrespondanse"].pop(idx_k)
                            zapisz_dane(db)
                            st.success("Notat slettet!")
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
            st.write("---")

    col_v, col_h = st.columns(2)
    for i, b in enumerate(db["alle_beboere"]):
        target_col = col_v if i % 2 == 0 else col_h
        with target_col:
            is_active = (st.session_state.valgt_beboer_epost == b['E-post'])
            css_class = "beboer-boks beboer-boks-valgt" if is_active else "beboer-boks"
            st.markdown(f'''
            <div class="{css_class}">
                <div style="font-weight: 700; color: #1A1A1A; font-size: 1.05em;">{b['Navn']} <span style="font-weight: 400; color: #888888; font-size: 0.9em;">({b['Seksjon']})</span></div>
                <div style="color: #555555; font-size: 0.9em; margin-top: 4px;">{b['E-post']}</div>
            </div>
            ''', unsafe_allow_html=True)
            btn_tekst = "Lukk profil" if is_active else "Åpne profil & historikk"
            if st.button(btn_tekst, key=f"btn_beboer_db_{i}"):
                st.session_state.valgt_beboer_epost = None if is_active else b['E-post']
                st.session_state.redigerer_beboer = False
                st.rerun()
            st.write("<br>", unsafe_allow_html=True)

# Fane 3
with fane3:
    st.markdown("### Sentralt Dokumentarkiv")
    st.write("Felles dokumenter og mapper for bygget.")
    st.write("<br>", unsafe_allow_html=True)
    
    col_knapp1, col_knapp2, _ = st.columns([1, 1.2, 2])
    with col_knapp1:
        if st.button("Lag ny mappe"):
            db["vis_ny_mappe_form"] = not db.get("vis_ny_mappe_form", False)
            db["vis_last_opp_form"] = False
            zapisz_dane(db)
    with col_knapp2:
        if st.button("Last opp dokument"):
            db["vis_last_opp_form"] = not db.get("vis_last_opp_form", False)
            db["vis_ny_mappe_form"] = False
            zapisz_dane(db)

    if db.get("vis_ny_mappe_form", False):
        st.markdown('''<div class="nordic-card">''', unsafe_allow_html=True)
        st.markdown('''<div class="nordic-meta">Ny Mappe</div>''', unsafe_allow_html=True)
        with st.form("form_ny_mappe"):
            ny_mappe_navn = st.text_input("Navn på mappen:")
            if st.form_submit_button("Opprett mappe"):
                if ny_mappe_navn and ny_mappe_navn not in db["bygg_mapper"]:
                    db["bygg_mapper"][ny_mappe_navn] = []
                    db["vis_ny_mappe_form"] = False
                    zapisz_dane(db)
                    st.rerun()
        st.markdown('''</div>''', unsafe_allow_html=True)

    if db.get("vis_last_opp_form", False):
        st.markdown('''<div class="nordic-card">''', unsafe_allow_html=True)
        st.markdown('''<div class="nordic-meta">Last opp dokument til arkiv</div>''', unsafe_allow_html=True)
        with st.form("form_last_opp_arkiv"):
            valgt_m = st.selectbox("Velg mappe:", list(db["bygg_mapper"].keys()))
            tittel_dok = st.text_input("Dokumenttittel:")
            opplastet_fil = st.file_uploader("Velg fil:")
            if st.form_submit_button("Lagre dokument"):
                if valgt_m and tittel_dok and opplastet_fil:
                    lagret_navn = lagre_opplastet_fil(opplastet_fil)
                    db["bygg_mapper"][valgt_m].append({"tittel": tittel_dok, "filnavn": lagret_navn})
                    db["vis_last_opp_form"] = False
                    zapisz_dane(db)
                    st.rerun()
                else:
                    st.warning("Fyll ut tittel og velg fil.")
        st.markdown('''</div>''', unsafe_allow_html=True)

    st.write("---")
    for mappe_navn, filer in db["bygg_mapper"].items():
        col_m1, col_m2 = st.columns([4, 1])
        with col_m1:
            st.markdown(f'''<div class="mappe-overskrift">{mappe_navn.upper()}</div>''', unsafe_allow_html=True)
        with col_m2:
            if mappe_navn not in ["Forsikring", "Tegninger & Bygg", "Økonomi & Budsjett", "Møtereferater"]:
                if st.button("Slett mappe", key=f"slett_map_{mappe_navn}"):
                    db["bygg_mapper"].pop(mappe_navn)
                    zapisz_dane(db)
                    st.rerun()

        if not filer:
            st.markdown('''<p style="color: #999999; font-style: italic; font-size: 0.88em; margin-bottom: 16px;">Ingen filer.</p>''', unsafe_allow_html=True)
        else:
            for idx_f, fil in enumerate(filer):
                st.markdown(f'''
                <div style="background-color: #FFFFFF; padding: 18px 22px; border-radius: 5px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03); margin-bottom: 10px; border-left: 3px solid #738269;">
                    <div style="font-family: 'Playfair Display', serif; font-size: 1.05em; color: #1A1A1A; font-weight: 600;">{fil['tittel']}</div>
                    <div style="font-size: 0.8em; color: #777777; margin-bottom: 10px;">{fil['filnavn']}</div>
                ''', unsafe_allow_html=True)
                vis_fil_seksjon(fil['filnavn'], fil['tittel'], f"arkiv_{mappe_navn}_{idx_f}")
                
                if st.button("Slett dokument", key=f"slett_arkiv_dok_{mappe_navn}_{idx_f}"):
                    filer.pop(idx_f)
                    zapisz_dane(db)
                    st.success("Dokument slettet!")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)

# Fane 4
with fane4:
    st.markdown("### Styrets Kalender & Planlegging")
    k_fane1, k_fane2, k_fane3 = st.tabs(["📅 Månedskalender", "📋 Årshjul & Aktiviteter", "➕ Ny hendelse"])
    
    with k_fane1:
        st.write("<br>", unsafe_allow_html=True)
        col_aar, col_maned = st.columns([1, 1])
        with col_aar:
            valgt_aar = st.selectbox("Velg år:", [2026, 2027], index=0)
        with col_maned:
            maned_navn = ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"]
            valgt_maned_navn = st.selectbox("Velg måned:", maned_navn, index=9)
            valgt_maned = maned_navn.index(valgt_maned_navn) + 1

        st.markdown(f'''<h3 style="text-align: center; margin: 15px 0 20px 0; font-family: 'Playfair Display', serif;">{valgt_maned_navn} {valgt_aar}</h3>''', unsafe_allow_html=True)
        forste_ukedag, dager_i_mnd = calendar.monthrange(valgt_aar, valgt_maned)
        ukedager = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
        
        table_html = "<table class='kalender-table'><thead><tr>"
        for d in ukedager: table_html += f"<th>{d}</th>"
        table_html += "</tr></thead><tbody><tr>"
        for _ in range(forste_ukedag): table_html += "<td class='empty'></td>"
            
        gjeldende_dag_i_uke = forste_ukedag
        for dag in range(1, dager_i_mnd + 1):
            if gjeldende_dag_i_uke == 7:
                table_html += "</tr><tr>"
                gjeldende_dag_i_uke = 0
            dato_str = f"{valgt_aar}-{valgt_maned:02d}-{dag:02d}"
            hendelser = [o for o in db["kalender_oppgaver"] if o["dato"] == dato_str]
            td_class = "has-event" if hendelser else ""
            table_html += f"<td class='{td_class}'><strong>{dag}</strong>"
            for h in hendelser:
                tid_visning = f"kl. {h.get('tid', '')} " if h.get('tid') else ""
                table_html += f"<br><span class='event-badge'>{tid_visning}{h['oppgave']}</span>"
            table_html += "</td>"
            gjeldende_dag_i_uke += 1
        while gjeldende_dag_i_uke < 7:
            table_html += "<td class='empty'></td>"
            gjeldende_dag_i_uke += 1
        table_html += "</tr></tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
        
    with k_fane2:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown('''<h4 style="font-family: 'Playfair Display', serif;">Oversikt over alle planlagte styreaktiviteter</h4>''', unsafe_allow_html=True)
        if st.session_state.redigerer_kalender_id is not None:
            red_id = st.session_state.redigerer_kalender_id
            treff = [item for item in db["kalender_oppgaver"] if item["id"] == red_id]
            if treff:
                gjeldende_hendelse = treff[0]
                st.markdown('''<div class="nordic-card">''', unsafe_allow_html=True)
                st.markdown('''<div class="nordic-meta">Rediger Hendelse</div>''', unsafe_allow_html=True)
                with st.form("form_rediger_kalender"):
                    r_kol1, r_kol2, r_kol3 = st.columns([1, 1, 2])
                    with r_kol1:
                        def_date = datetime.datetime.strptime(gjeldende_hendelse["dato"], "%Y-%m-%d").date()
                        red_dato = st.date_input("Dato:", def_date)
                    with r_kol2:
                        red_tid = st.text_input("Klokkeslett:", value=gjeldende_hendelse.get("tid", "18:00"))
                    with r_kol3:
                        red_tittel = st.text_input("Tittel:", value=gjeldende_hendelse["oppgave"])
                    red_detaljer = st.text_area("Beskrivelse:", value=gjeldende_hendelse.get("detaljer", ""))
                    if st.form_submit_button("Lagre oppdatering"):
                        gjeldende_hendelse["dato"] = str(red_dato)
                        gjeldende_hendelse["tid"] = red_tid
                        gjeldende_hendelse["oppgave"] = red_tittel
                        gjeldende_hendelse["detaljer"] = red_detaljer
                        st.session_state.redigerer_kalender_id = None
                        zapisz_dane(db)
                        st.rerun()
                st.markdown('''</div>''', unsafe_allow_html=True)

        for oppg in db["kalender_oppgaver"]:
            tid_tekst = f"kl. {oppg.get('tid', '')} • " if oppg.get('tid') else ""
            c_oppg_tekst, c_oppg_btn = st.columns([4, 1.2])
            with c_oppg_tekst:
                st.markdown(f'''
                <div class="nordic-card" style="padding: 16px 22px; margin-bottom: 10px; border-left: 4px solid #738269; border-top: none;">
                    <div style="font-weight: 700; color: #738269; font-size: 0.9em; text-transform: uppercase;">{oppg['dato']} • {tid_tekst}{oppg['type']}</div>
                    <div style="font-size: 1.1em; font-weight: 600; color: #1A1A1A; margin-top: 2px;">{oppg['oppgave']}</div>
                    <div style="font-size: 0.9em; color: #666666; margin-top: 2px;">{oppg.get('detaljer', '')}</div>
                </div>
                ''', unsafe_allow_html=True)
            with c_oppg_btn:
                st.write("")
                col_sub1, col_sub2 = st.columns(2)
                with col_sub1:
                    if st.button("Rediger", key=f"red_cal_{oppg['id']}"):
                        st.session_state.redigerer_kalender_id = oppg["id"]
                        st.rerun()
                with col_sub2:
                    if st.button("Slett", key=f"slett_cal_{oppg['id']}"):
                        db["kalender_oppgaver"] = [o for o in db["kalender_oppgaver"] if o["id"] != oppg["id"]]
                        if st.session_state.redigerer_kalender_id == oppg["id"]:
                            st.session_state.redigerer_kalender_id = None
                        zapisz_dane(db)
                        st.rerun()
            
    with k_fane3:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown('''<h4 style="font-family: 'Playfair Display', serif;">Legg til ny aktivitet</h4>''', unsafe_allow_html=True)
        with st.form("form_ny_kalender"):
            k1, k2, k3 = st.columns([1, 1, 2])
            with k1: ny_dato = st.date_input("Dato:", datetime.date(2026, 10, 11))
            with k2: ny_tid = st.text_input("Klokkeslett:", value="18:00")
            with k3: ny_tittel = st.text_input("Tittel:")
            ny_detaljer = st.text_input("Beskrivelse:")
            if st.form_submit_button("Lagre hendelse"):
                if ny_tittel:
                    ny_id = max([o["id"] for o in db["kalender_oppgaver"]], default=0) + 1
                    db["kalender_oppgaver"].append({
                        "id": ny_id, "dato": str(ny_dato), "tid": ny_tid, "oppgave": ny_tittel, "detaljer": ny_detaljer, "type": "Møte/Aktivitet"
                    })
                    db["kalender_oppgaver"] = sorted(db["kalender_oppgaver"], key=lambda k: (k['dato'], k.get('tid', '')))
                    zapisz_dane(db)
                    st.rerun()

# Fane 5
with fane5:
    st.markdown("### Juridisk Rådgivning")
    st.write("Hva ønsker du vurdert opp mot lovverket?")
    sporsmal = st.text_input("", placeholder="Skriv inn spørsmålet ditt her...")
    
    if st.button("Innhent Råd", key="jus_knapp_final"):
        if ai_klar and sporsmal:
            with st.spinner("AI-assistenten vurderer saken opp mot Norges lover..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
                fullt_sporsmal = f"Du er styrets juridiske AI-assistent for Sameiet Kirkegata 6. Finn lovhjemler i Norges lover som støtter styrets og sameiets interesser. Svar formelt. Spørsmål: {sporsmal}"
                try:
                    response = requests.post(url, json={"contents": [{"parts": [{"text": fullt_sporsmal}]}]})
                    if response.status_code == 200:
                        st.markdown(f"<div class='nordic-card'>{response.json()['candidates'][0]['content']['parts'][0]['text']}</div>", unsafe_allow_html=True)
                except Exception:
                    st.error("Tjenesten er midlertidig utilgjengelig.")
