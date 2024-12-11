import streamlit as st
import requests

# Título de la Aplicación
st.title("Análisis de Imágenes con Llama 3.2 Vision")
st.write(
    "Ingresa un enlace a una imagen para recibir comentarios detallados generados por la API de Llama Vision."
)

# Pedir la clave de la API
api_key = st.text_input("🔑 Ingresa tu API Key de GroqCloud:", type="password")

if api_key:
    # Pedir al usuario que ingrese el enlace de la imagen
    image_url = st.text_input("🔗 Ingresa el enlace (URL) de la imagen:")

    if image_url:
        st.write("Enlace proporcionado:", image_url)

        # Validar que el enlace sea una URL de imagen válida
        if image_url.lower().endswith((".jpg", ".jpeg", ".png")):
            # Mostrar la imagen cargada desde el enlace
            st.image(image_url, caption="Imagen cargada desde el enlace", use_column_width=True)

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
            st.error("Por favor, ingresa un enlace válido a una imagen en formato JPG, JPEG o PNG.")

else:
    st.info("Por favor, ingresa tu API Key para continuar.")


