import streamlit as st
import pandas as pd
import numpy as np

# 1. KONFIGURACJA STRONY (Zawsze na samej górze)
st.set_page_config(page_title="SmartStyre | Kirkegata 6", layout="wide", initial_sidebar_state="expanded")

# 2. PAMIĘĆ SESJI (Baza danych, logowanie, sprawy)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'beboere_db' not in st.session_state:
    st.session_state.beboere_db = pd.DataFrame({
        "Seksjon": ["1", "2", "3"],
        "Navn": ["Akram Zalmai", "Ola Nordmann", "Kari Hansen"],
        "E-post": ["akram@example.com", "ola@example.com", "kari@example.com"],
        "Telefon": ["99887766", "11223344", "55443322"],
        "Rolle": ["Eier", "Leietaker", "Eier"]
    })

if 'active_cases' not in st.session_state:
    st.session_state.active_cases = 1

# 3. WSTRZYKNIĘCIE NOWOCZESNEGO STYLU CSS (Naprawione - bez ukrywania headera)
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp { background-color: #F8FAFC; }
    
    .stButton>button {
        background-color: #1D4ED8;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1E40AF;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A;
    }
    
    .legal-shield-box {
        background-color: #F1F5F9;
        border-left: 4px solid #475569;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        font-size: 0.9em;
        color: #334155;
    }
    
    .login-box {
        max-width: 400px;
        margin: 0 auto;
        padding: 40px;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 10vh;
    }
</style>
""", unsafe_allow_html=True)

# 4. EKRAN LOGOWANIA
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("SmartStyre")
    st.caption("Sameiet Kirkegata 6 - Styreportal")
    st.write("Vennligst logg inn for å fortsette.")
    
    password = st.text_input("Passord:", type="password")
    if st.button("Logg inn"):
        if password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Feil passord. Prøv igjen.")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. GŁÓWNA APLIKACJA (Pokazuje się tylko po zalogowaniu)
else:
    # Górny pasek - przełącznik użytkowników
    col1, col2, col3 = st.columns([6, 2, 2])
    with col3:
        st.write("")
        active_user = st.selectbox(
            "Aktiv bruker:",
            ["Weronika B. (Styremedlem)", "Ine (Styremedlem)", "Maria (Styreleder)"]
        )

    # Lewy pasek nawigacyjny
    st.sidebar.title("SmartStyre")
    st.sidebar.caption("Sameiet Kirkegata 6")
    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "Meny:",
        ["Oversikt (Panel)", "Innboks (Wiadomości)", "Beboere (Mieszkańcy)", "Regnskap (Księgowość AI)", "E-post & Dokumenter"]
    )

    st.sidebar.markdown("---")
    st.sidebar.success("🛡️ AI Legal Shield: Aktywny")
    
    # Przycisk wylogowania
    if st.sidebar.button("Logg ut"):
        st.session_state.logged_in = False
        st.rerun()

    # Logika zakładek
    if menu == "Oversikt (Panel)":
        st.title("Oversikt")
        st.write(f"Velkommen tilbake, **{active_user.split(' ')[0]}**!")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Aktive saker (W toku)", str(st.session_state.active_cases), "Wymaga uwagi")
        m2.metric("Beboere registrert", str(len(st.session_state.beboere_db)), "Zaktualizowano dzisiaj")
        m3.metric("Konto saldo", "245 000 kr", "Stabilne")
        
        st.markdown("### Siste Aktivitet")
        st.info("💧 **Zgłoszenie:** Wyciek wody z dachu (Akram Zalmai, Seksjon 1). AI przygotowało bezpieczną odpowiedź prawną.")

    elif menu == "Innboks (Wiadomości)":
        st.title("Innboks & AI Assistent")
        st.markdown("Zarządzanie korespondencją z aktywnym pancerzem prawnym.")
        
        st.markdown("#### Sprawa #001: Vannlekkasje fra taket på badet (Akram Zalmai)")
        st.error("💬 **Wiadomość od mieszkańca:**\n\n*Hei, jeg oppdaget i morges at det drypper vann fra taket på badet mitt. Hvem har ansvaret for å fikse dette ifølge loven, og hva gjør jeg nå?*")
        
        st.markdown("### 🛡️ Odpowiedź wygenerowana przez AI Legal Shield")
        st.markdown("""
        <div class="legal-shield-box">
        <b>CEL STRATEGICZNY AI:</b> Uniknięcie przyznania odpowiedzialności finansowej før ekspertyzą techniczną, wskazanie obowiązków mieszkańca. Brak informacji, że pismo pisało AI.
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area("Gotowa odpowiedź do wysłania (Edytowalna):", 
            "Hei Akram,\n\nStyret bekrefter mottak av din henvendelse vedrørende vannlekkasje på badet i seksjon 1.\n\nVi minner om at seksjonseier i henhold til eierseksjonsloven § 32 har et selvstendig vedlikeholdsansvar for innvendige flater, inkludert rør og installasjoner i egen branncelle. \n\nFor at styret skal kunne vurdere om dette faller inn under sameiets utvendige/strukturelle vedlikeholdsplikt, ber vi deg umiddelbart kontakte rørlegger for en faglig skaderapport. Sameiet påtar seg ikke økonomisk ansvar for utbedring før det foreligger dokumentasjon på at årsaken ligger i felles rørføring eller bygningsmasse.\n\nVennligst send skaderapporten til styret så snart den foreligger.\n\nMed vennlig hilsen,\nStyret, Sameiet Kirkegata 6", 
            height=300)
        
        st.button("Send E-post (Wymaga integracji API)")

    elif menu == "Beboere (Mieszkańcy)":
        st.title("Beboeroversikt")
        st.markdown("Lista mieszkańców chroniona i zapisana w sesji.")
        
        st.dataframe(st.session_state.beboere_db, use_container_width=True)
        
        st.markdown("### Dodaj nowego mieszkańca")
        with st.form("add_beboer_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            new_seksjon = c1.text_input("Seksjonsnummer")
            new_navn = c2.text_input("Fullt navn")
            new_epost = c1.text_input("E-post")
            new_tlf = c2.text_input("Telefonnummer")
            new_rolle = st.selectbox("Rolle", ["Eier", "Leietaker"])
            
            submitted = st.form_submit_button("Legg til beboer")
            if submitted and new_navn != "":
                new_row = pd.DataFrame({
                    "Seksjon": [new_seksjon], "Navn": [new_navn], 
                    "E-post": [new_epost], "Telefon": [new_tlf], "Rolle": [new_rolle]
                })
                st.session_state.beboere_db = pd.concat([st.session_state.beboere_db, new_row], ignore_index=True)
                st.success(f"Dodano mieszkańca: {new_navn}")
                st.rerun()

    elif menu == "Regnskap (Księgowość AI)":
        st.title("Regnskap i Budżet")
        st.success("🤖 **AI Analiza:** Finanse są bezpieczne. Brak niezapłaconych faktur (felleskostnader) za ubiegły miesiąc.")
        
        tab1, tab2, tab3 = st.tabs(["📊 Oversikt", "🧾 Faktura-skanner AI", "⚠️ Purringer (Zaległości)"])
        with tab1:
            st.markdown("### Zużycie budżetu")
            chart_data = pd.DataFrame(np.random.randn(12, 2) * 5000 + 20000, columns=['Wpływy', 'Wydatki (Konserwacja)'])
            st.line_chart(chart_data)
        with tab2:
            st.markdown("### Automatyczny skanner dokumentów")
            st.file_uploader("Przeciągnij plik faktury (PDF/JPG)", type=["pdf", "jpg", "png"])
        with tab3:
            st.markdown("### Autopilot opłat wspólnych")
            st.dataframe(pd.DataFrame({
                "Mieszkaniec": ["Akram Zalmai", "Ola Nordmann"],
                "Status": ["Opłacono", "Opłacono"],
                "Akcja": ["-", "-"]
            }), use_container_width=True)

    elif menu == "E-post & Dokumenter":
        st.title("Infrastruktura Danych")
        st.info("Oczekujemy na dane dostępowe do skrzynek e-mail oraz Supabase w celu trwałej integracji.")
        
