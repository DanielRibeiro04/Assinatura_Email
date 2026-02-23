#python -m streamlit run app.py

# app.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Gerador de Assinatura ArcelorMittal", layout="centered")

# Cores
ORANGE = "#F47D30"
WHITE = "#FFFFFF"

# Caminho da logo local
LOGO_PATH = "./img/logo.png"

# Título
st.markdown(
    f"<h2 style='color:{ORANGE};text-align:center;'>Gerador de Assinatura de Email - ArcelorMittal</h2>",
    unsafe_allow_html=True,
)

# Formulário
with st.form("assinatura_form"):
    nome = st.text_input("Nome completo*", "")
    email = st.text_input("Email*", "")
    cargo = st.text_input("Cargo*", "")
    telefone = st.text_input("Telefone/Ramal")
    sem_telefone = st.checkbox("Não quero informar telefone/ramal")
    submit = st.form_submit_button("Gerar Assinatura")

# Geração da assinatura
if submit:
    if not nome or not email or not cargo:
        st.error("Por favor, preencha todos os campos obrigatórios (*).")
    elif not telefone and not sem_telefone:
        st.error("Você deve preencher o telefone/ramal ou marcar a opção de não informar.")
    else:
        try:
            # Altura dinâmica
            altura = 240 if telefone else 220

            # Fundo branco (mais profissional)
            img = Image.new("RGB", (720, altura), "#FFFFFF")
            draw = ImageDraw.Draw(img)

            # Barra lateral laranja
            draw.rectangle([(0, 0), (12, altura)], fill=ORANGE)

            # Logo
            logo = Image.open(LOGO_PATH).convert("RGBA").resize((140, 60))
            img.paste(logo, (30, 25), logo)

            # Fontes
            try:
                font_nome = ImageFont.truetype("arialbd.ttf", 30)
                font_cargo = ImageFont.truetype("arial.ttf", 20)
                font_texto = ImageFont.truetype("arial.ttf", 18)
                font_small = ImageFont.truetype("arial.ttf", 15)
            except:
                font_nome = ImageFont.load_default()
                font_cargo = ImageFont.load_default()
                font_texto = ImageFont.load_default()
                font_small = ImageFont.load_default()

            # Nome (mais destaque)
            draw.text((210, 30), nome, font=font_nome, fill="#1C1C1C")

            # Cargo (mais discreto)
            draw.text((210, 70), cargo, font=font_cargo, fill="#666666")

            # Linha divisória elegante
            draw.line([(210, 100), (690, 100)], fill="#DDDDDD", width=2)

            # Email
            draw.text((210, 115), f"{email}", font=font_texto, fill="#333333")

            y_pos = 140

            # Telefone
            if telefone:
                draw.text((210, y_pos), f"{telefone}", font=font_texto, fill="#333333")
                y_pos += 25

            y_pos += 10

            # Informações institucionais (discretas)
            draw.text((210, y_pos), "ArcelorMittal Brasil | www.arcelormittal.com.br", font=font_small, fill="#777777")
            draw.text((210, y_pos + 18), "Av. Carandá, 1115", font=font_small, fill="#777777")
            draw.text((210, y_pos + 36), "Funcionários - MG | CEP 30130-915", font=font_small, fill="#777777")

            # Preview
            st.image(img, caption="Prévia da assinatura", use_column_width=True)

            # Download
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                label="Baixar assinatura",
                data=buf.getvalue(),
                file_name="assinatura.png",
                mime="image/png",
            )

        except Exception as e:
            st.error(f"Erro ao gerar assinatura: {e}")
