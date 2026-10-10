import streamlit as st
import pandas as pd

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="SmartStyre | Kirkegata 6", layout="wide")

# 2. BEZPIECZNY CSS (TYLKO KOLORY - bez ingerencji w strukturę kodu)
st.markdown("""
<style>
    /* Nowoczesne jasne tło strony */
    .stApp { background-color: #F8FAFC; }
    
    /* Kolor głównych przycisków */
    .stButton > button {
        background-color: #1D4ED8;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    
    /* Ciemny elegancki pasek boczny (Fjord Blue) */
    [data-testid="stSidebar"] { background-color: #0F172A; }
    
    /* Wymuszenie białego tekstu na ciemnym pasku bocznym */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] label { 
        color: #F8FAFC !important; 
    }
</style>
""", unsafe_allow_html=True)

# 3. PAMIĘĆ SESJI (Stara, niezawodna logika)
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

# 4. STARY EKRAN LOGOWANIA (Standardowy, działający)
if not st.session_state.logged_in:
    st.title("SmartStyre - Logowanie")
    st.write("Wprowadź hasło, aby uzyskać dostęp do panelu zarządu.")
    
    password = st.text_input("Hasło (wpisz 1234):", type="password")
    
    if st.button("Logg inn"):
        if password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Błędne hasło!")

# 5. GŁÓWNA APLIKACJA (Działa w 100% po zalogowaniu)
else:
    # Górny przełącznik użytkownika
    col1, col2 = st.columns([8, 2])
    with col2:
        active_user = st.selectbox("Aktiv bruker:", ["Weronika B.", "Ine", "Maria"])
        if st.button("Wyloguj"):
            st.session_state.logged_in = False
            st.rerun()

    # Lewe menu
    st.sidebar.title("SmartStyre")
    menu = st.sidebar.radio(
        "Nawigacja:",
        ["Oversikt (Panel)", "Innboks (Wiadomości)", "Beboere (Mieszkańcy)", "Regnskap (Księgowość)"]
    )

    st.sidebar.markdown("---")
    st.sidebar.success("🛡️ AI Legal Shield: Aktywny")

    # Zakładki
    if menu == "Oversikt (Panel)":
        st.title(f"Velkommen tilbake, {active_user}!")
        
        colA, colB, colC = st.columns(3)
        colA.metric("Aktive saker", "1", "Wymaga uwagi")
        colB.metric("Beboere registrert", str(len(st.session_state.beboere_db)), "Aktualne")
        colC.metric("Konto saldo", "245 000 kr", "Stabilne")
        
        st.info("💧 Zgłoszenie: Wyciek wody z dachu (Akram Zalmai, Seksjon 1). AI przygotowało odpowiedź.")

    elif menu == "Innboks (Wiadomości)":
        st.title("Innboks & AI Assistent")
        st.error("💬 Wiadomość od: Akram Zalmai (Seksjon 1)\n\nZalanie dachu w łazience. Kto ma to naprawić?")
        
        st.warning("🛡️ Cel AI: Ochrona finansów wspólnoty. Odrzucenie automatycznej winy. Zlecenie rzeczoznawcy.")
        
        st.text_area("Odpowiedź przygotowana przez AI:", 
            "Hei Akram,\n\nVi mottok din melding om vannlekkasje. Ifølge eierseksjonsloven § 32 har du ansvar for innvendig vedlikehold. Før sameiet kan ta stilling til saken, må du bestille en rørlegger for å dokumentere årsaken. Sameiet dekker ingenting før en formell rapport bekrefter feil på fellesrør.\n\nMvh Styret", 
            height=200)

    elif menu == "Beboere (Mieszkańcy)":
        st.title("Lista mieszkańców")
        st.dataframe(st.session_state.beboere_db, use_container_width=True)
        
        st.markdown("### Dodaj nowego mieszkańca")
        with st.form("dodaj_mieszkanca", clear_on_submit=True):
            s = st.text_input("Seksjon")
            n = st.text_input("Navn")
            e = st.text_input("E-post")
            t = st.text_input("Telefon")
            r = st.selectbox("Rolle", ["Eier", "Leietaker"])
            
            if st.form_submit_button("Legg til"):
                if n != "":
                    nowy = pd.DataFrame({"Seksjon": [s], "Navn": [n], "E-post": [e], "Telefon": [t], "Rolle": [r]})
                    st.session_state.beboere_db = pd.concat([st.session_state.beboere_db, nowy], ignore_index=True)
                    st.success("Dodano!")
                    st.rerun()

    elif menu == "Regnskap (Księgowość)":
        st.title("Regnskap i Budżet")
        st.success("🤖 Analiza: Finanse są bezpieczne. Brak niezapłaconych opłat.")
        st.write("Tutaj podepniemy inteligentny skaner faktur i zestawienie budżetu.")
