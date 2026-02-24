import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path

# Configuração da página
st.set_page_config(page_title="Gerador de Assinatura ArcelorMittal", layout="centered")

# Cores
ORANGE = "#F47D30"
WHITE = "#FFFFFF"

# Caminho base
BASE_DIR = Path(__file__).resolve().parent

# Caminhos da logo e das fontes
LOGO_PATH = BASE_DIR / "img" / "logo.png"
FONT_REG = BASE_DIR / "fonts" / "DejaVuSans.ttf"
FONT_BOLD = BASE_DIR / "fonts" / "DejaVuSans-Bold.ttf"

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

    num_andar = st.text_input("Digite o andar em que voce está: ")
    sem_num_andar= st.checkbox("Não quero informar o andar")

    submit = st.form_submit_button("Gerar Assinatura")

# Geração da assinatura
if submit:
    if not nome or not email or not cargo:
        st.error("Por favor, preencha todos os campos obrigatórios (*).")
    elif not telefone and not sem_telefone:
        st.error("Você deve preencher o telefone/ramal ou marcar a opção de não informar.")
    elif not num_andar and not sem_num_andar:
        st.error("Por favor, digite o número do andar ou marque a opção de não informar") 
    else:
        try:
            altura = 260 if telefone and num_andar else 230 

            img = Image.new("RGB", (720, altura), WHITE)
            draw = ImageDraw.Draw(img)

            # Barra lateral laranja
            draw.rectangle([(0, 0), (12, altura)], fill=ORANGE)

            # Logo
            logo = Image.open(LOGO_PATH).convert("RGBA").resize((140, 60))
            img.paste(logo, (30, 25), logo)

            # Fontes
            font_nome = ImageFont.truetype(str(FONT_BOLD), 30)
            font_cargo = ImageFont.truetype(str(FONT_REG), 20)
            font_texto = ImageFont.truetype(str(FONT_REG), 18)
            font_small = ImageFont.truetype(str(FONT_REG), 15)

            # Texto
            draw.text((210, 30), nome, font=font_nome, fill="#1C1C1C")
            draw.text((210, 70), cargo, font=font_cargo, fill="#666666")
            draw.line([(210, 100), (690, 100)], fill="#DDDDDD", width=2)

            draw.text((210, 115), email, font=font_texto, fill="#333333")

            y_pos = 140

            if telefone:
                draw.text((210, y_pos), telefone, font=font_texto, fill="#333333")
                y_pos += 25

            y_pos += 10

            draw.text((210, y_pos), "ArcelorMittal Brasil | www.arcelormittal.com.br", font=font_small, fill="#777777")
            draw.text((210, y_pos + 18), "Av. Carandá, 1115 - {num_andar}° andar", font=font_small, fill="#777777")
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
