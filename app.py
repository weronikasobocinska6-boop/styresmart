import streamlit as st
import requests
import datetime
import calendar

# ==========================================
# 1. DESIGN OG OPPSETT (Nordisk stil)
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

    .stButton > button {
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
    }
    .stButton > button:hover { 
        background-color: #1A2429 !important; 
        transform: translateY(-1px) !important; 
        box-shadow: 0 6px 16px rgba(0,0,0,0.12) !important; 
    }
    .stButton button p { color: #FFFFFF !important; }

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
    
    /* Kalendertabell */
    .kalender-table { width: 100%; border-collapse: separate; border-spacing: 6px; table-layout: fixed; }
    .kalender-table th { background-color: #EFECE5; color: #555555; font-family: 'Playfair Display', serif; padding: 10px; text-align: center; font-weight: 600; border-radius: 4px; font-size: 0.95em; }
    .kalender-table td { background-color: #FFFFFF; border: 1px solid #E5E2D9; height: 75px; vertical-align: top; padding: 8px; border-radius: 4px; font-size: 0.85em; }
    .kalender-table td.empty { background-color: transparent; border: none; }
    .kalender-table td.has-event { background-color: #F1F3ED; border-left: 4px solid #738269; }
    .event-badge { background-color: #738269; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.78em; font-weight: 600; display: inline-block; margin-top: 4px; }
    
    /* Mappestil */
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
    .dok-kort {
        background-color: #FFFFFF;
        padding: 16px 22px;
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 3px solid #738269;
    }
    .dok-knapp {
        color: #2B3A41;
        font-size: 0.78em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        border: 1px solid #D1C7B7;
        padding: 6px 14px;
        border-radius: 4px;
        background-color: #FAF9F6;
        cursor: pointer;
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
# 2. SYSTEMMINNE
# ==========================================
api_key = st.secrets.get("GEMINI_API_KEY", "")
ai_klar = bool(api_key)

if "epost_utkast" not in st.session_state: st.session_state.epost_utkast = ""
if "fellesmelding_utkast" not in st.session_state: st.session_state.fellesmelding_utkast = ""

if "vis_ny_mappe_form" not in st.session_state: st.session_state.vis_ny_mappe_form = False
if "vis_last_opp_form" not in st.session_state: st.session_state.vis_last_opp_form = False

if "valgt_beboer_index" not in st.session_state: st.session_state.valgt_beboer_index = None
if "redigerer_beboer" not in st.session_state: st.session_state.redigerer_beboer = False

if "redigerer_kalender_id" not in st.session_state: st.session_state.redigerer_kalender_id = None

if "alle_beboere" not in st.session_state:
    st.session_state.alle_beboere = [
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
    ]

if "beboer_data" not in st.session_state:
    st.session_state.beboer_data = {
        "zalmai44@gmail.com": {
            "dokumenter": [
                {"tittel": "Tidligere klage på vannlekkasje", "filnavn": "Klage_Vannlekkasje_2024.pdf"},
                {"tittel": "Foto av baderomstak", "filnavn": "Bilde_av_tak_bad.jpg"}
            ],
            "korrespondanse": [
                {"dato": "09.10.2026", "emne": "Vannlekkasje fra taket på badet", "innhold": "Rapportert drypping fra overliggende leilighet (etasje oppgang B). Styret har avvist ansvar jf. eierseksjonsloven."},
                {"dato": "14.02.2025", "emne": "Spørsmål om fellesutgifter", "innhold": "Avklart fakturaspørsmål vedrørende kabel-TV og a-konto."}
            ]
        }
    }

if "bygg_mapper" not in st.session_state:
    st.session_state.bygg_mapper = {
        "Forsikring": [
            {"tittel": "Forsikringsavtale If", "filnavn": "Forsikringsavtale_If_2026.pdf"}
        ],
        "Tegninger & Bygg": [
            {"tittel": "Plantegninger 1. etg", "filnavn": "Plantegninger_Kirkegata_6.pdf"}
        ],
        "Økonomi & Budsjett": [
            {"tittel": "Nytt budsjett 2027", "filnavn": "Nytt_budsjett_2027_Sameiet_K6.xlsx"},
            {"tittel": "Budsjett 2027 Sameiet K6", "filnavn": "Budsjett_2027_Sameiet_K6.pdf"},
            {"tittel": "507 - Årsregnskap 2025", "filnavn": "507_Aarsregnskap_2025.pdf"},
            {"tittel": "507 - Økonomirapport pr. Q3 2026", "filnavn": "507_Oekonomirapport_pr_Q3_2026.pdf"}
        ],
        "Møtereferater": []
    }

if "kalender_oppgaver" not in st.session_state:
    st.session_state.kalender_oppgaver = [
        {"id": 1, "dato": "2026-10-11", "tid": "18:00", "oppgave": "Styremøte", "detaljer": "Gjennomgang av budsjett for 2027", "type": "Møte"},
        {"id": 2, "dato": "2026-10-20", "tid": "18:00", "oppgave": "Ekstraordinært Årsmøte", "detaljer": "Behandling av budsjett og økning av felleskostnader", "type": "Møte"},
        {"id": 3, "dato": "2026-11-01", "tid": "10:00", "oppgave": "Snømåkeavtale", "detaljer": "Inngå avtale om snømåking og strøing", "type": "Generell"}
    ]

# ==========================================
# 3. SIDEBAR MENY
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-top: 15px; color: #1A1A1A;'>StyreSmart</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.85em; letter-spacing: 2px; color: #666;'>KIRKEGATA 6</p>", unsafe_allow_html=True)
    st.write("---")
    if ai_klar:
        st.markdown("<div style='background-color: #E8EDE1; padding: 10px; border-radius: 4px; border-left: 4px solid #738269; text-align: center;'><span style='color: #4A5D3E; font-weight: 700; font-size: 0.85em;'>✓ AI-ASSISTENT TILKOBLET</span></div>", unsafe_allow_html=True)
    else:
        st.error("Mangler API-nøkkel")
    st.write("---")
    st.markdown('''<p style="font-family: 'Playfair Display', serif; font-size: 1.15em; border-bottom: 1px solid #DCDCDC; padding-bottom: 5px;">Aktive i styret</p>''', unsafe_allow_html=True)
    st.write("Weronika Bhatti")
    st.write("<span style='color: #888888;'>Ine Foss (Frakoblet)</span>", unsafe_allow_html=True)
    st.write("<span style='color: #888888;'>Maria Frang (Frakoblet)</span>", unsafe_allow_html=True)

# ==========================================
# 4. HOVEDSKJERM OG FANER
# ==========================================
st.title("Styreportal")
fane1, fane2, fane3, fane4, fane5 = st.tabs(["Innboks", "Beboere", "Arkiv", "Kalender", "Jus"])

# ----------------- FANE 1: INNBOKS -----------------
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
                    prompt = "Du er en bestemt juridisk AI-assistent for styret i Sameiet Kirkegt. 6. Beboer Akram Zalmai klager på lekkasje fra etasjen over. Skriv et formelt svar fra styret. Argumenter med Eierseksjonsloven for at innvendig vedlikehold er seksjonseierens ansvar. Avslutt KUN med 'Med vennlig hilsen, Styret i Sameiet Kirkegt. 6'."
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
                st.success("Sendt og arkivert.")
                st.balloons()
                
    with kol2:
        st.markdown('''<div class="nordic-card"><div class="nordic-meta">Fellesmelding</div><h3 style="margin-top: 0; font-size: 1.4em;">Oppslagstavle</h3><div class="nordic-text" style="font-size: 0.95em;">Bruk assistenten til å utforme en velskrevet melding til alle 16 seksjoner.</div></div>''', unsafe_allow_html=True)
        stikkord_felles = st.text_area("", placeholder="Hva gjelder meldingen?", height=100)
        if st.button("Lag utkast", key="lag_utkast_1"):
            if ai_klar and stikkord_felles:
                with st.spinner("Skriver..."):
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
                    prompt = f"Du er styret i Sameiet Kirkegt. 6. Skriv en kort, høflig felles e-post til beboere basert på: {stikkord_felles}. Avslutt med 'Hilsen Styret i Sameiet Kirkegt. 6'."
                    try:
                        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                        if response.status_code == 200: 
                            st.session_state.fellesmelding_utkast = response.json()['candidates'][0]['content']['parts'][0]['text']
                    except Exception:
                        pass
        if st.session_state.fellesmelding_utkast:
            st.session_state.fellesmelding_utkast = st.text_area("Utkast:", value=st.session_state.fellesmelding_utkast, height=200)
            if st.button("Publiser til beboere", key="publiser_1"): 
                st.success("Fellesmelding publisert.")

# ----------------- FANE 2: BEBOERE -----------------
with fane2:
    st.markdown("### Personregister")
    st.write("Klikk på **Åpne profil** på en beboer for å se samlet korrespondanse, dokumenter eller redigere opplysninger.")
    st.write("<br>", unsafe_allow_html=True)
    
    if st.session_state.valgt_beboer_index is not None and st.session_state.valgt_beboer_index < len(st.session_state.alle_beboere):
        idx = st.session_state.valgt_beboer_index
        akt_beboer = st.session_state.alle_beboere[idx]
        b_epost = akt_beboer["E-post"]
        
        if b_epost not in st.session_state.beboer_data:
            st.session_state.beboer_data[b_epost] = {"dokumenter": [], "korrespondanse": []}
        data_profil = st.session_state.beboer_data[b_epost]

        st.markdown(f'''
        <div class="nordic-card" style="border-top: 3px solid #738269;">
            <div class="nordic-meta">Valgt Beboerprofil</div>
            <h3 style="margin-top: 0; color: #1A1A1A;">👤 {akt_beboer['Navn']} — {akt_beboer['Seksjon']}</h3>
            <p style="color: #666666; font-size: 0.95em;">E-post: <strong>{akt_beboer['E-post']}</strong></p>
        </div>
        ''', unsafe_allow_html=True)
        
        k_rad1, k_rad2, _ = st.columns([1.2, 1.2, 3])
        with k_rad1:
            if st.button("Rediger opplysninger", key="btn_toggle_edit"):
                st.session_state.redigerer_beboer = not st.session_state.redigerer_beboer
        with k_rad2:
            if st.button("Lukk profil", key="btn_lukk_profil"):
                st.session_state.valgt_beboer_index = None
                st.session_state.redigerer_beboer = False
                st.rerun()

        if st.session_state.redigerer_beboer:
            st.markdown('''<div class="nordic-card">''', unsafe_allow_html=True)
            st.markdown('''<div class="nordic-meta">Rediger Beboeropplysninger</div>''', unsafe_allow_html=True)
            with st.form("form_rediger_beboer"):
                nytt_navn = st.text_input("Fullt navn:", value=akt_beboer["Navn"])
                ny_epost = st.text_input("E-postadresse:", value=akt_beboer["E-post"])
                ny_seksjon = st.text_input("Seksjon / Leilighet:", value=akt_beboer["Seksjon"])
                
                c_save, _ = st.columns([1, 4])
                with c_save:
                    if st.form_submit_button("Lagre endringer"):
                        if ny_epost != b_epost:
                            st.session_state.beboer_data[ny_epost] = st.session_state.beboer_data.pop(b_epost, {"dokumenter": [], "korrespondanse": []})
                        st.session_state.alle_beboere[idx] = {
                            "Navn": nytt_navn,
                            "E-post": ny_epost,
                            "Seksjon": ny_seksjon
                        }
                        st.session_state.redigerer_beboer = False
                        st.success("Opplysningene er oppdatert!")
                        st.rerun()
            st.markdown('''</div>''', unsafe_allow_html=True)

        c_dok, c_korr = st.columns(2)
        
        with c_dok:
            st.markdown('''<h4 style="color: #1A1A1A; margin-top: 15px;">Tilknyttede Dokumenter</h4>''', unsafe_allow_html=True)
            if not data_profil["dokumenter"]:
                st.markdown('''<p style="color: #888888; font-style: italic; font-size: 0.9em;">Ingen dokumenter lagret på denne beboeren ennå.</p>''', unsafe_allow_html=True)
            else:
                for d in data_profil["dokumenter"]:
                    st.markdown(f'''
                    <div class="dok-kort">
                        <div>
                            <span style="font-weight: 600; color: #1A1A1A;">{d['tittel']}</span><br>
                            <span style="color: #777; font-size: 0.8em;">{d['filnavn']}</span>
                        </div>
                        <span class="dok-knapp">LAST NED</span>
                    </div>
                    ''', unsafe_allow_html=True)
                    
            with st.expander("Last opp dokument til denne personen"):
                with st.form("form_last_opp_person", clear_on_submit=True):
                    pers_dok_tittel = st.text_input("Tittel på fil:", placeholder="F.eks: Avtale om fasadeendring")
                    pers_fil = st.file_uploader("Velg dokument:")
                    if st.form_submit_button("Lagre på beboer"):
                        if pers_dok_tittel and pers_fil:
                            data_profil["dokumenter"].append({"tittel": pers_dok_tittel, "filnavn": pers_fil.name})
                            st.success(f"Lagret på {akt_beboer['Navn']}!")
                            st.rerun()

        with c_korr:
            st.markdown('''<h4 style="color: #1A1A1A; margin-top: 15px;">Samtalehistorikk & E-poster</h4>''', unsafe_allow_html=True)
            if not data_profil["korrespondanse"]:
                st.markdown('''<p style="color: #888888; font-style: italic; font-size: 0.9em;">Ingen loggført korrespondanse ennå.</p>''', unsafe_allow_html=True)
            else:
                for k in data_profil["korrespondanse"]:
                    st.markdown(f'''
                    <div style="background-color: #FFFFFF; padding: 14px 18px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); margin-bottom: 10px; border-left: 3px solid #738269;">
                        <div style="font-size: 0.78em; color: #738269; font-weight: 700; text-transform: uppercase;">{k['dato']}</div>
                        <div style="font-weight: 700; color: #1A1A1A; font-size: 0.98em; margin-top: 2px;">{k['emne']}</div>
                        <div style="color: #444; font-size: 0.9em; margin-top: 4px; line-height: 1.5;">{k['innhold']}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
            with st.expander("Loggfør nytt notat / samtale"):
                with st.form("form_ny_korr", clear_on_submit=True):
                    ny_emne = st.text_input("Emne:", placeholder="F.eks: Telefonsamtale om støy")
                    ny_tekst = st.text_area("Innhold / referat:")
                    if st.form_submit_button("Legg til i historikk"):
                        if ny_emne and ny_tekst:
                            data_profil["korrespondanse"].append({
                                "dato": datetime.date.today().strftime("%d.%m.%Y"),
                                "emne": ny_emne,
                                "innhold": ny_tekst
                            })
                            st.success("Loggført!")
                            st.rerun()

        st.write("---")

    col_v, col_h = st.columns(2)
    for i, b in enumerate(st.session_state.alle_beboere):
        target_col = col_v if i % 2 == 0 else col_h
        with target_col:
            is_active = (st.session_state.valgt_beboer_index == i)
            css_class = "beboer-boks beboer-boks-valgt" if is_active else "beboer-boks"
            
            st.markdown(f'''
            <div class="{css_class}">
                <div style="font-weight: 700; color: #1A1A1A; font-size: 1.05em;">{b['Navn']} <span style="font-weight: 400; color: #888888; font-size: 0.9em;">({b['Seksjon']})</span></div>
                <div style="color: #555555; font-size: 0.9em; margin-top: 4px;">{b['E-post']}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            btn_tekst = "Lukk profil" if is_active else "Åpne profil & historikk"
            if st.button(btn_tekst, key=f"btn_beboer_{i}"):
                if is_active:
                    st.session_state.valgt_beboer_index = None
                    st.session_state.redigerer_beboer = False
                else:
                    st.session_state.valgt_beboer_index = i
                    st.session_state.redigerer_beboer = False
                st.rerun()
            st.write("<br>", unsafe_allow_html=True)

# ----------------- FANE 3: ARKIV -----------------
with fane3:
    st.markdown("### Sentralt Dokumentarkiv")
    st.write("Felles dokumenter og mapper for bygget.")
    st.write("<br>", unsafe_allow_html=True)
    
    col_knapp1, col_knapp2, _ = st.columns([1, 1.2, 2])
    with col_knapp1:
        if st.button("Lag ny mappe"):
            st.session_state.vis_ny_mappe_form = not st.session_state.vis_ny_mappe_form
            st.session_state.vis_last_opp_form = False
    with col_knapp2:
        if st.button("Last opp dokument"):
            st.session_state.vis_last_opp_form = not st.session_state.vis_last_opp_form
            st.session_state.vis_ny_mappe_form = False

    if st.session_state.vis_ny_mappe_form:
        st.markdown('''<div class="nordic-card">''', unsafe_allow_html=True)
        st.markdown('''<div class="nordic-meta">Ny Mappe</div>''', unsafe_allow_html=True)
        ny_mappe_navn = st.text_input("Navn på mappen:", placeholder="F.eks: Vedlikehold 2026")
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("Opprett"):
                if ny_mappe_navn and ny_mappe_navn not in st.session_state.bygg_mapper:
                    st.session_state.bygg_mapper[ny_mappe_navn] = []
                    st.session_state.vis_ny_mappe_form = False
                    st.success(f"Mappen '{ny_mappe_navn}' er opprettet!")
                    st.rerun()
        with c2:
            if st.button("Avbryt", key="avbryt_ny_mappe"):
                st.session_state.vis_ny_mappe_form = False
                st.rerun()
        st.markdown('''</div>''', unsafe_allow_html=True)

    if st.session_state.vis_last_opp_form:
        st.markdown('''<div class="nordic-card">''', unsafe_allow_html=True)
        st.markdown('''<div class="nordic-meta">Last opp dokument</div>''', unsafe_allow_html=True)
        valgt_m = st.selectbox("Velg mappe:", list(st.session_state.bygg_mapper.keys()))
        tittel_dok = st.text_input("Dokumenttittel:", placeholder="F.eks: Brannvernrapport 2026")
        opplastet_fil = st.file_uploader("Velg fil (PDF, Word, Excel, bilde):")
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("Lagre"):
                if valgt_m and tittel_dok and opplastet_fil:
                    st.session_state.bygg_mapper[valgt_m].append({"tittel": tittel_dok, "filnavn": opplastet_fil.name})
                    st.session_state.vis_last_opp_form = False
                    st.success(f"Lagret i {valgt_m}!")
                    st.rerun()
        with c2:
            if st.button("Avbryt", key="avbryt_last_opp"):
                st.session_state.vis_last_opp_form = False
                st.rerun()
        st.markdown('''</div>''', unsafe_allow_html=True)

    st.write("---")
    
    for mappe_navn, filer in st.session_state.bygg_mapper.items():
        st.markdown(f'''<div class="mappe-overskrift">{mappe_navn.upper()}</div>''', unsafe_allow_html=True)
        if not filer:
            st.markdown('''<p style="color: #999999; font-style: italic; font-size: 0.88em; margin-bottom: 16px;">Ingen dokumenter i denne mappen ennå.</p>''', unsafe_allow_html=True)
        else:
            for fil in filer:
                st.markdown(f'''
                <div class="dok-kort">
                    <div>
                        <span style="font-family: 'Playfair Display', serif; font-size: 1.05em; color: #1A1A1A; font-weight: 600;">{fil['tittel']}</span><br>
                        <span style="font-size: 0.8em; color: #777777;">{fil['filnavn']}</span>
                    </div>
                    <span class="dok-knapp">LAST NED</span>
                </div>
                ''', unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)

# ----------------- FANE 4: KALENDER -----------------
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
        for d in ukedager:
            table_html += f"<th>{d}</th>"
        table_html += "</tr></thead><tbody><tr>"
        
        for _ in range(forste_ukedag):
            table_html += "<td class='empty'></td>"
            
        gjeldende_dag_i_uke = forste_ukedag
        for dag in range(1, dager_i_mnd + 1):
            if gjeldende_dag_i_uke == 7:
                table_html += "</tr><tr>"
                gjeldende_dag_i_uke = 0
                
            dato_str = f"{valgt_aar}-{valgt_maned:02d}-{dag:02d}"
            hendelser = [o for o in st.session_state.kalender_oppgaver if o["dato"] == dato_str]
            
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
        st.write("Her kan du se, redigere eller slette oppføringer.")
        st.write("<br>", unsafe_allow_html=True)

        if st.session_state.redigerer_kalender_id is not None:
            red_id = st.session_state.redigerer_kalender_id
            treff = [item for item in st.session_state.kalender_oppgaver if item["id"] == red_id]
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
                        red_tid = st.text_input("Klokkeslett (f.eks. 18:00):", value=gjeldende_hendelse.get("tid", "18:00"))
                    with r_kol3:
                        red_tittel = st.text_input("Tittel:", value=gjeldende_hendelse["oppgave"])
                    red_detaljer = st.text_area("Beskrivelse / agenda:", value=gjeldende_hendelse.get("detaljer", ""))

                    c_save_k, c_cancel_k = st.columns([1, 4])
                    with c_save_k:
                        if st.form_submit_button("Lagre oppdatering"):
                            gjeldende_hendelse["dato"] = str(red_dato)
                            gjeldende_hendelse["tid"] = red_tid
                            gjeldende_hendelse["oppgave"] = red_tittel
                            gjeldende_hendelse["detaljer"] = red_detaljer
                            st.session_state.redigerer_kalender_id = None
                            st.success("Hendelsen er oppdatert!")
                            st.rerun()
                    with c_cancel_k:
                        if st.form_submit_button("Avbryt"):
                            st.session_state.redigerer_kalender_id = None
                            st.rerun()
                st.markdown('''</div>''', unsafe_allow_html=True)

        for oppg in st.session_state.kalender_oppgaver:
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
                        st.session_state.kalender_oppgaver = [o for o in st.session_state.kalender_oppgaver if o["id"] != oppg["id"]]
                        if st.session_state.redigerer_kalender_id == oppg["id"]:
                            st.session_state.redigerer_kalender_id = None
                        st.success("Hendelsen ble slettet!")
                        st.rerun()
            
    with k_fane3:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown('''<h4 style="font-family: 'Playfair Display', serif;">Legg til ny aktivitet</h4>''', unsafe_allow_html=True)
        with st.form("form_ny_kalender"):
            k1, k2, k3 = st.columns([1, 1, 2])
            with k1: ny_dato = st.date_input("Dato:", datetime.date(2026, 10, 11))
            with k2: ny_tid = st.text_input("Klokkeslett (f.eks. 18:00):", value="18:00")
            with k3: ny_tittel = st.text_input("Tittel på hendelse:", placeholder="F.eks: Styremøte")
            ny_detaljer = st.text_input("Beskrivelse / agenda:", placeholder="Gjennomgang av budsjett")
            
            if st.form_submit_button("Lagre hendelse"):
                if ny_tittel:
                    ny_id = max([o["id"] for o in st.session_state.kalender_oppgaver], default=0) + 1
                    st.session_state.kalender_oppgaver.append({
                        "id": ny_id,
                        "dato": str(ny_dato),
                        "tid": ny_tid,
                        "oppgave": ny_tittel,
                        "detaljer": ny_detaljer,
                        "type": "Møte/Aktivitet"
                    })
                    st.session_state.kalender_oppgaver = sorted(st.session_state.kalender_oppgaver, key=lambda k: (k['dato'], k.get('tid', '')))
                    st.success("Hendelsen er lagt til i kalenderen!")
                    st.rerun()

# ----------------- FANE 5: JUS -----------------
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