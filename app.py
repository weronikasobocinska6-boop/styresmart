import streamlit as st
import pandas as pd

# 1. KONFIGURASJON AV SIDEN
st.set_page_config(page_title="SmartStyre | Kirkegata 6", layout="wide")

# 2. SIKKER CSS
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

# 4. LOGG INN SKJERM (100% Norsk, Med Brukernavn)
if not st.session_state.logged_in:
    st.title("SmartStyre")
    st.write("Vennligst logg inn for å få tilgang til styreportalen.")
    
    # Dodane pole loginu (Brukernavn)
    brukernavn = st.selectbox("Velg bruker:", ["Weronika B.", "Ine", "Maria"])
    passord = st.text_input("Passord (tast 1234):", type="password")
    
    # Prosty, niezawodny przycisk
    if st.button("Logg inn"):
        if passord == "1234":
            st.session_state.logged_in = True
            st.session_state.brukernavn = brukernavn
            st.rerun()
        else:
            st.error("Feil passord. Vennligst prøv igjen.")

# 5. HOVEDAPP
else:
    # Brukervelger oppe til høyre
    col1, col2 = st.columns([8, 2])
    with col2:
        st.write(f"Aktiv bruker: **{st.session_state.get('brukernavn', 'Weronika B.')}**")
        if st.button("Logg ut"):
            st.session_state.logged_in = False
            st.rerun()

    # Sidemeny (Venstre)
    st.sidebar.title("SmartStyre")
    menu = st.sidebar.radio(
        "Meny:",
        ["Oversikt", "Innboks", "Beboere", "Regnskap"]
    )

    st.sidebar.markdown("---")
    st.sidebar.success("🛡️ AI Legal Shield: Aktiv")

    # Innhold for fanene
    if menu == "Oversikt":
        st.title(f"Velkommen tilbake, {st.session_state.get('brukernavn', 'Weronika B.').split(' ')[0]}!")
        
        colA, colB, colC = st.columns(3)
        colA.metric("Aktive saker", "1", "Krever oppfølging")
        colB.metric("Registrerte beboere", str(len(st.session_state.beboere_db)), "Oppdatert i dag")
        colC.metric("Konto saldo", "245 000 kr", "Stabil")
        
        st.info("💧 Ny henvendelse: Vannlekkasje fra taket (Akram Zalmai, Seksjon 1). AI har forberedt et utkast til svar.")

    elif menu == "Innboks":
        st.title("Innboks & AI Assistent")
        st.error("💬 Melding fra: Akram Zalmai (Seksjon 1)\n\nHei, jeg oppdaget i morges at det drypper vann fra taket på badet mitt. Hvem har ansvaret for å fikse dette ifølge loven, og hva gjør jeg nå?")
        
        st.warning("🛡️ AI-strategi: Beskytte sameiets økonomi. Avvise automatisk ansvar. Kreve rørleggerrapport.")
        
        st.text_area("Svarutkast forberedt av AI:", 
            "Hei Akram,\n\nVi mottok din melding om vannlekkasje. Ifølge eierseksjonsloven § 32 har du ansvar for innvendig vedlikehold i egen branncelle. Før sameiet kan ta stilling til saken, må du bestille en rørlegger for å dokumentere årsaken. Sameiet dekker ingenting før en formell rapport bekrefter at feilen ligger i felles rørføring eller bygningsmasse.\n\nMvh\nStyret, Sameiet Kirkegata 6", 
            height=200)

    elif menu == "Beboere":
        st.title("Beboeroversikt")
        st.dataframe(st.session_state.beboere_db, use_container_width=True)
        
        st.markdown("### Legg til ny beboer")
        with st.form("legg_til_beboer", clear_on_submit=True):
            s = st.text_input("Seksjon")
            n = st.text_input("Navn")
            e = st.text_input("E-post")
            t = st.text_input("Telefon")
            r = st.selectbox("Rolle", ["Eier", "Leietaker"])
            
            if st.form_submit_button("Legg til"):
                if n != "":
                    ny_beboer = pd.DataFrame({"Seksjon": [s], "Navn": [n], "E-post": [e], "Telefon": [t], "Rolle": [r]})
                    st.session_state.beboere_db = pd.concat([st.session_state.beboere_db, ny_beboer], ignore_index=True)
                    st.success("Beboer lagt til!")
                    st.rerun()

    elif menu == "Regnskap":
        st.title("Regnskap og Budsjett")
        st.success("🤖 AI Analyse: Økonomien er sikker. Ingen ubetalte felleskostnader registrert.")
        st.write("Her vil modul for intelligent fakturaskanner integreres etter hvert.")
