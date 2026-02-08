import streamlit as st
import openai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Répondeur Avis IA", page_icon="⭐", layout="centered")

# --- TON LIEN STRIPE ---
STRIPE_LINK = "https://buy.stripe.com/eVq5kEgsV3cJ5gdbAd1B603"

# --- GESTION DE LA CLÉ API ---
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    # Si pas de clé, on affiche une erreur propre
    st.warning("⚠️ Clé API manquante. Veuillez la configurer dans Streamlit Cloud.")
    st.stop()

# --- INITIALISATION DU COMPTEUR ---
if 'count' not in st.session_state:
    st.session_state.count = 0

# --- INTERFACE ---
st.title("⭐ Répondeur Avis Clients Pro")
st.write("Transformez vos avis négatifs en opportunités commerciales.")

# Zone de texte
review = st.text_area("Copiez l'avis du client ici :", height=150)

# Choix du ton
tone = st.selectbox("Ton de la réponse :", ["Professionnel & Diplomate", "Empathique", "Commercial"])

# --- LOGIQUE ---
if st.button("✨ Générer la réponse"):
    if not review:
        st.warning("Collez un avis d'abord !")
    else:
        # Vérification quota (3 essais)
        if st.session_state.count >= 3:
            st.error("🔒 Version Gratuite Terminée")
            st.markdown(f"👉 **[CLIQUEZ ICI POUR DÉBLOQUER L'ACCÈS À VIE (29€)]({STRIPE_LINK})**")
        else:
            # Appel IA
            try:
                with st.spinner("Rédaction..."):
                    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": f"Tu es un expert service client. Réponds sur un ton {tone}. Sois bref et pro."},
                            {"role": "user", "content": review}
                        ]
                    )
                    reply = response.choices[0].message.content
                    st.success("✅ Réponse générée :")
                    st.code(reply, language='text')
                    
                    st.session_state.count += 1
                    st.info(f"Essais restants : {3 - st.session_state.count}/3")
            except Exception as e:
                st.error(f"Erreur : {e}")
