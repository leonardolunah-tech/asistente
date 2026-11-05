import io
import re
from gtts import gTTS
from openai import OpenAI
import streamlit as st

# Configuración de página con icono e interfaz limpia
st.set_page_config(
    page_title="El Maestro Virtual",
    page_icon="👨‍🏫",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# Estilos CSS personalizados (Paleta cálida y didáctica)
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
    
    /* Mensaje del Asistente (Maestro) */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: #ffffff !important; 
        border: 1px solid rgba(99, 102, 241, 0.15) !important; 
        border-left: 4px solid #6366f1 !important; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    }
    
    /* Mensaje del Estudiante (Usuario) */
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
st.title("👨‍🏫 El Maestro Virtual")
st.caption("Tu tutor interactivo para aprender, resolver dudas y guiarte paso a paso")

# Etiquetas de sugerencia/capacidades didácticas
sugerencias = ["📖 Explicar temas", "✍️ Corregir tareas", "💡 Resolver dudas", "🧪 Ejemplos prácticos"]
chips = '<div class="temas-bar">' + ''.join(f'<span class="tema-chip">{s}</span>' for s in sugerencias) + '</div>'
st.markdown(chips, unsafe_allow_html=True)

# Botón para reiniciar el chat
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("🗑️ Reiniciar clase", key="btn_limpiar"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="sep">· · · · ·</div>', unsafe_allow_html=True)

# Prompt del Sistema enfocado en rol de Profesor / Maestro
SYSTEM_PROMPT = """Eres un maestro y tutor altamente preparado, paciente, empático y dedicado. Tu objetivo es ayudar a los estudiantes a comprender cualquier concepto, resolver dudas académicas o prácticas y fomentar el pensamiento crítico.

Pautas didácticas:
1. Tono pedagógico: Amable, motivador, formal pero cercano. Trata al usuario como a un alumno con ganas de aprender.
2. Estructura clara: Explica de lo general a lo particular. Usa listas, viñetas y negritas para resaltar puntos clave.
3. Ejemplos sencillos: Acompaña las explicaciones complejas con analogías o ejemplos cotidianos de la vida real.
4. Verificación de aprendizaje: Al final de una explicación extensa, puedes hacer una pregunta breve o proponer un pequeño ejercicio para confirmar la comprensión.
5. Corrección constructiva: Si el alumno comete un error, felicítalo por el intento, explica amablemente dónde estuvo el fallo y cómo corregirlo sin juzgar.
6. Uso de emojis didácticos: Usa iconos con moderación para organizar la lectura (📚, 💡, ✏️, 🎯, 🔍)."""

# Obtención segura de la clave API
groq_key = None
if "groq" in st.secrets and "api_key" in st.secrets["groq"]:
    groq_key = st.secrets["groq"]["api_key"]
elif "GROQ_API_KEY" in st.secrets:
    groq_key = st.secrets["GROQ_API_KEY"]

if not groq_key:
    st.error("⚠️ Configuración requerida: Define 'api_key' dentro del bloque [groq] en los Secrets de Streamlit.")
    st.stop()

try:
    client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key)
except Exception as e:
    st.error(f"Error al conectar con el servidor: {e}")
    st.stop()

# Función para limpiar sintaxis Markdown antes de sintetizar voz
def limpiar_texto_para_tts(texto):
    texto = re.sub(r'[\*\#\`\_]', '', texto)
    texto = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', texto)
    return texto.strip()

# Función para convertir texto a voz
def text_to_speech_web(text):
    try:
        texto_limpio = limpiar_texto_para_tts(text)
        if not texto_limpio:
            return None
        tts = gTTS(text=texto_limpio, lang='es', slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception:
        return None

# Estado de la sesión para el historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de conversación
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
            st.error(f"Ocurrió un inconveniente al procesar la respuesta: {str(e)}")
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                st.session_state.messages.pop()

# Chat input
if prompt := st.chat_input("Escribe tu pregunta o tema a repasar..."):
    procesar_respuesta(prompt)
