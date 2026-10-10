import streamlit as st
import pandas as pd

# 1. KONFIGURASJON AV SIDEN
st.set_page_config(page_title="SmartStyre | Kirkegata 6", layout="wide")

# 2. SKANDINAVISK MINIMALISTISK CSS (Kun farger og stil)
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    
    .stButton > button {
        background-color: #1D4ED8;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    
    [data-testid="stSidebar"] { background-color: #0F172A; }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] label { 
        color: #F8FAFC !important; 
    }
</style>
""", unsafe_allow_html=True)

# 3. DATABASE I MINNET (Stabil logikk)
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

# 4. LOGG INN SKJERM (Gammel, pålitelig metode)
if not st.session_state.logged_in:
    st.title("SmartStyre")
    st.write("Vennligst logg inn for å få tilgang til styreportalen.")
    
    brukernavn = st.selectbox("Velg bruker:", ["Weronika B.", "Ine", "Maria"])
    passord = st.text_input("Passord:", type="password")
    
    if st.button("Logg inn"):
        # BYTT UT "ditt_gamle_passord" MED DET PASSORDET DU HADDE I BEGYNNELSEN
        if passord == "ditt_gamle_passord": 
            st.session_state.logged_in = True
            st.session_state.brukernavn = brukernavn
            st.rerun()
        else:
            st.error("Feil passord.")

# 5. HOVEDAPP
else:
    # Brukervelger oppe til høyre
    col1, col2 = st.columns([8, 2])
    with col2:
        st.write(f"Aktiv bruker: **{st.session_state.get('brukernavn', 'Weronika B.')}**")
        if st.button("Logg ut"):
            st.session_state.logged_in = False
            st.rerun()

    # Sidemeny
    st.sidebar.title("SmartStyre")
    menu = st.sidebar.radio(
        "Meny:",
        ["Oversikt", "Innboks", "Beboere", "Regnskap"]
    )

    # Innhold for fanene
    if menu == "Oversikt":
        st.title(f"Velkommen tilbake, {st.session_state.get('brukernavn', 'Weronika B.').split(' ')[0]}!")
        
        colA, colB, colC = st.columns(3)
        colA.metric("Aktive saker", "1", "Krever oppfølging")
        colB.metric("Registrerte beboere", str(len(st.session_state.beboere_db)), "Oppdatert i dag")
        colC.metric("Konto saldo", "245 000 kr", "Stabil")
        
        st.info("💧 Ny henvendelse: Vannlekkasje fra taket (Akram Zalmai, Seksjon 1). Svarutkast er klart i innboksen.")

    elif menu == "Innboks":
        st.title("Innboks")
        st.error("💬 Melding fra: Akram Zalmai (Seksjon 1)\n\nHei, jeg oppdaget i morges at det drypper vann fra taket på badet mitt. Hvem har ansvaret for å fikse dette ifølge loven, og hva gjør jeg nå?")
        
        st.write("Svarutkast:")
        
        # Svaret er formidlet stramt og juridisk korrekt, uten å skryte av at det er AI
        st.text_area("", 
            "Hei Akram,\n\nVi mottok din melding om vannlekkasje. Ifølge eierseksjonsloven § 32 har du ansvar for innvendig vedlikehold i egen branncelle. Før sameiet kan ta stilling til saken, må du bestille en rørlegger for å dokumentere årsaken. Sameiet dekker ingenting før en formell rapport bekrefter at feilen ligger i felles rørføring eller bygningsmasse.\n\nMvh\nStyret, Sameiet Kirkegata 6", 
            height=200)
            
        st.button("Send e-post")

    elif menu == "Beboere":
        st.title("Beboeroversikt")
        st.dataframe(st.session_state.beboere_db
