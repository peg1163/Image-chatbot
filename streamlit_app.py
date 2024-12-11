import streamlit as st
from PIL import Image
import requests
import io

# Título de la Aplicación
st.title("Análisis de Imágenes con Llama 3.2 Vision")
st.write(
    "Sube una imagen y recibe comentarios detallados sobre esta, generados por Llama Vision."
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

        # Subir la imagen a un almacenamiento público (puedes usar un servicio como Imgur o tu propio servidor)
        st.write("Subiendo imagen a un servidor público...")
        try:
            # Simulación de subida a un servidor público (reemplaza esta sección con tu solución de almacenamiento)
            files = {"image": uploaded_file.getvalue()}
            upload_response = requests.post("https://api.imgbb.com/1/upload?key=YOUR_IMGBB_API_KEY", files=files)
            upload_result = upload_response.json()

            if upload_response.status_code == 200:
                image_url = upload_result["data"]["url"]  # URL pública de la imagen

                # Configurar el cuerpo de la solicitud
                data = {
                    "model": "llama-3.2-90b-vision-preview",  # Asegúrate de que este modelo esté disponible
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Por favor analiza esta imagen y proporciona un comentario detallado."},
                                {"type": "image_url", "image_url": {"url": image_url}}
                            ]
                        }
                    ],
                    "temperature": 1,
                    "max_tokens": 1024,
                    "top_p": 1
                }

                # Enviar solicitud a la API
                st.write("Analizando la imagen...")
                url = "https://api.groq.com/openai/v1/chat/completions"
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

            else:
                st.error("Error al subir la imagen. Intenta con otra o revisa el servidor de almacenamiento.")

        except Exception as e:
            st.error(f"Ocurrió un error al analizar la imagen: {e}")

else:
    st.info("Por favor, ingresa tu API Key para continuar.")



