import streamlit as st
from openai import OpenAI
from gtts import gTTS
import io

# Configuración de página con icono e interfaz limpia
st.set_page_config(
    page_title="Asistente Virtual", 
    page_icon="✨", 
    layout="centered", 
    initial_sidebar_state="collapsed", 
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# Estilos CSS personalizados (Paleta Cálida y Amigable en Tonos Azul/Violeta)
css_amable = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;} .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;} [data-testid="stStatusWidget"] {display: none;}
    
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #e6eeef 50%, #e0e7ff 100%); 
        max-width: 100%; 
        padding: 0; 
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-family: 'Inter', sans-serif !important; 
        color: #312e81 !important; 
        text-align: center; 
        font-size: 2.2rem !important; 
        font-weight: 700 !important; 
        padding-top: 1.5rem !important; 
        margin-bottom: 0.1rem !important;
    }
    
    .stCaption {
        text-align: center; 
        color: #4f46e5 !important; 
        font-family: 'Inter', sans-serif !important; 
        font-size: 0.95rem !important; 
        margin-bottom: 1.2rem !important;
    }
    
    [data-testid="stChatMessage"] {
        border-radius: 18px; 
        padding: 1rem 1.2rem !important; 
        margin: 0.5rem 0 !important;
    }
    
    /* Mensaje del Asistente */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: #ffffff !important; 
        border: 1px solid rgba(99, 102, 241, 0.15) !important; 
        border-left: 4px solid #6366f1 !important; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }
    
    /* Mensaje del Usuario */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important; 
        border: none !important; 
        box-shadow: 0 3px 14px rgba(79, 70, 229, 0.25);
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] p, 
    [data-testid="stChatMessage"][data-testid*="user"] span, 
    [data-testid="stChatMessage"][data-testid*="user"] div {
        color: #ffffff !important; 
        font-weight: 450;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] p, 
    [data-testid="stChatMessage"][data-testid*="assistant"] span {
        color: #1e1b4b !important; 
        line-height: 1.65; 
        font-size: 0.95rem;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] [data-testid="stAvatar"] {
        background: linear-gradient(135deg, #818cf8, #6366f1) !important; 
        border: 2px solid #fff !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] [data-testid="stAvatar"] {
        background: linear-gradient(135deg, #312e81, #4338ca) !important; 
        border: 2px solid #fff !important;
    }
    
    [data-testid="stChatInputContainer"] {padding: 0.8rem 1rem 1.5rem 1rem !important;}
    [data-testid="stChatInput"] {
        border-radius: 25px !important; 
        border: 2px solid rgba(99, 102, 241, 0.35) !important; 
        background: rgba(255,255,255,0.9) !important; 
        box-shadow: 0 4px 20px rgba(49, 46, 129, 0.06);
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #6366f1 !important; 
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.20) !important;
    }
    [data-testid="stChatInput"]::placeholder {color: #818cf8 !important; font-style: italic;}
    
    .stException {
        background: #fef2f2 !important; 
        border: 1px solid #fca5a5 !important; 
        border-radius: 12px !important; 
        color: #991b1b !important;
    }
    
    ::-webkit-scrollbar {width: 6px;} 
    ::-webkit-scrollbar-track {background: transparent;} 
    ::-webkit-scrollbar-thumb {background: #a5b4fc; border-radius: 10px;}
    
    .sep {text-align: center; margin: 0.5rem 0 1rem 0; font-size: 0.75rem; color: #a5b4fc; letter-spacing: 0.5em;}
    .temas-bar {display: flex; flex-wrap: wrap; justify-content: center; gap: 0.4rem; margin: 0.3rem 1rem 1rem 1rem;}
    .tema-chip {
        padding: 0.25rem 0.75rem; 
        border-radius: 12px; 
        background: rgba(255,255,255,0.7); 
        color: #4338ca; 
        font-size: 0.75rem; 
        font-weight: 500; 
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
</style>
"""
st.markdown(css_amable, unsafe_allow_html=True)

# Encabezado principal
st.markdown('<div class="sep">✦ ✦ ✦ ✦ ✦</div>', unsafe_allow_html=True)
st.title("✨ Asistente Virtual ✨")
st.caption("Tu compañero atento, servicial y siempre listo para ayudarte")

# Etiquetas de sugerencia/capacidades
sugerencias = ["💬 Conversar", "💡 Resolver dudas", "✍️ Redactar ideas", "📚 Aprender algo nuevo"]
chips = '<div class="temas-bar">' + ''.join(f'<span class="tema-chip">{s}</span>' for s in sugerencias) + '</div>'
st.markdown(chips, unsafe_allow_html=True)

# Botón para limpiar el chat
c1, c2, c3 = st.columns([1,1,1])
with c2:
    if st.button("🗑️ Limpiar conversación", key="btn_limpiar"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="sep">· · · · ·</div>', unsafe_allow_html=True)

# Prompt del Sistema enfocado en amabilidad y ayuda general
SYSTEM_PROMPT = """Eres un asistente virtual increíblemente amable, cálido, atento y servicial. Tu objetivo principal es ayudar al usuario de la manera más clara, empática y agradable posible.

Pautas de comportamiento:
1. Tono de voz: Muy respetuoso, amigable, positivo y paciente. Usa un lenguaje claro y acogedor.
2. Formato de respuesta: Sé conciso pero completo. Organiza la información con puntos o párrafos breves cuando sea conveniente para facilitar la lectura.
3. Empatía y disposición: Muestra siempre entusiasmo por ayudar. Si el usuario comete un error o duda, guíalo amablemente sin juzgar.
4. Uso de emojis: Utiliza emojis con moderación pero calidez para mantener una atmósfera cercana (✨😊💡🤝🌸).
5. Versatilidad: Puedes ayudar en tareas creativas, explicaciones, organización de ideas, conversación cotidiana o resolución de dudas cotidianas.
6. Si te preguntan quién te creó, responde con amabilidad que eres un asistente virtual diseñado para ser su compañero de apoyo en lo que necesite."""

# Inicialización de cliente OpenAI (conectado a Groq)
try:
    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=st.secrets["groq"]["api_key"])
except Exception:
    st.error("Error de configuración: Revisa que la clave de la API esté configurada correctamente en los Secrets de Streamlit.")
    st.stop()

# Función para convertir texto a voz
def text_to_speech_web(text):
    try:
        tts = gTTS(text=text, lang='es', slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception:
        return None

# Estado de la sesión para el historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Procesamiento de la entrada del usuario
def procesar_respuesta(user_input):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        try:
            mensajes_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=mensajes_api, 
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Generar y reproducir audio de la respuesta
            if full_response:
                audio_bytes = text_to_speech_web(full_response)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                    
        except Exception as e:
            st.error(f"Ocurrió un pequeño inconveniente: {str(e)}")
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                st.session_state.messages.pop()

# Input del chat
if prompt := st.chat_input("¿En qué te puedo ayudar hoy?..."):
    procesar_respuesta(prompt)
