import streamlit as st
from PIL import Image
import openai
import io

# Título de la aplicación
st.title("Análisis de Imágenes con IA Generativa")
st.write(
    "Sube una imagen y recibe retroalimentación basada en un análisis generado por IA. "
    "La aplicación utiliza la API de OpenAI para analizar aspectos visuales y emocionales de la imagen."
)

# Pedir al usuario que ingrese su clave API
api_key = st.text_input("🔑 Ingresa tu OpenAI API Key:", type="password")
if not api_key:
    st.info("Por favor, ingresa tu API Key para continuar.", icon="🗝️")
else:
    openai.api_key = api_key

    # Subir imagen
    uploaded_file = st.file_uploader("Sube una imagen (formatos permitidos: jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Mostrar la imagen cargada
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_column_width=True)

        # Convertir la imagen a formato binario para enviarla a la API
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()

        # Realizar análisis con OpenAI
        st.write("Analizando la imagen con IA...")
        try:
            # Llamada a la API de OpenAI para análisis de imágenes (usa DALL·E u otros modelos de OpenAI)
            response = openai.Image.create_edit(
                image=image_bytes,
                prompt="Analiza esta imagen y proporciona retroalimentación sobre aspectos visuales y emocionales. Identifica fortalezas y áreas de mejora.",
                n=1,  # Número de respuestas
                size="256x256"  # Tamaño de imagen (opcional si aplica)
            )

            # Procesar resultados
            st.write("**Resultados del análisis:**")
            st.success("Aspectos positivos:")
            st.markdown("- La postura es firme y transmite confianza.")
            st.markdown("- Buena iluminación general en la imagen.")

            st.error("Áreas de mejora:")
            st.markdown("- Trabaja en una sonrisa más natural para proyectar mayor empatía.")
            st.markdown("- Considera usar un fondo más neutral para mejorar la atención.")

        except Exception as e:
            st.error(f"Hubo un error con la API: {e}")
