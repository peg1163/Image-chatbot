import streamlit as st
from PIL import Image
import requests
import base64
import io

# Título de la Aplicación
st.title("Análisis de Imágenes con GroqCloud")
st.write(
    "Sube una imagen y recibe comentarios detallados sobre esta, generados por la API de GroqCloud."
)

# Pedir la clave de la API
api_key = st.text_input("🔑 Ingresa tu API Key de GroqCloud:", type="password")

if api_key:
    # Cargar una imagen
    uploaded_file = st.file_uploader("Sube una imagen (formatos permitidos: jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Mostrar la imagen cargada
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_column_width=True)

        # Convertir la imagen a base64
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Configurar el cuerpo de la solicitud
        data = {
            "model": "llama-3.2-90b-vision-preview",  # Asegúrate de que este modelo esté disponible en GroqCloud
            "messages": [
                {"role": "user", "content": "Por favor, analiza esta imagen y proporciona un comentario detallado."}
            ],
            "image": image_base64
        }

        # Enviar solicitud a la API
        st.write("Analizando la imagen...")
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"  # Endpoint de GroqCloud
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=data)

            # Manejar la respuesta
            if response.status_code == 200:
                result = response.json()
                comentario = result["choices"][0]["message"]["content"]
                st.write("**Comentario generado por IA:**")
                st.success(comentario)
            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Ocurrió un error al analizar la imagen: {e}")

else:
    st.info("Por favor, ingresa tu API Key para continuar.")


