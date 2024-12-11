import streamlit as st
from PIL import Image
import openai
import io

# Configurar la API Key de OpenAI
st.title("Análisis de Imágenes con GPT-4 Vision")
api_key = st.text_input("🔑 Ingresa tu OpenAI API Key:", type="password")

if api_key:
    openai.api_key = api_key

    # Subir imagen
    uploaded_file = st.file_uploader("Sube una imagen para analizar", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Mostrar la imagen cargada
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_column_width=True)

        # Convertir imagen a bytes para enviarla a la API
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()

        # Enviar imagen a GPT-4 Vision
        st.write("Analizando la imagen con GPT-4 Vision...")
        try:
            # Llamada al modelo GPT-4 (asegúrate de que tu cuenta tenga acceso)
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un asistente que analiza imágenes y proporciona retroalimentación detallada."},
                    {"role": "user", "content": "Por favor analiza esta imagen y proporciona comentarios."}
                ]
            )

            # Procesar y mostrar los resultados
            analysis = response['choices'][0]['message']['content']
            st.write("**Resultados del análisis:**")
            st.write(analysis)

        except openai.OpenAIError as e:
            st.error(f"Error en la API de OpenAI: {e}")

        except Exception as e:
            st.error(f"Error inesperado: {e}")
