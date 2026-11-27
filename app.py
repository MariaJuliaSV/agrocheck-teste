import os
import unicodedata

import streamlit as st
import streamlit.components.v1 as components
import tensorflow as tf
import numpy as np
from PIL import Image

from tratamentos import TRATAMENTOS

# -----------------------------------------
# LOGIN DE DEMONSTRAÇÃO
# -----------------------------------------
# Usuários e senhas fixos, só para a apresentação do trabalho.
# Para adicionar, remover ou trocar, basta mudar o dicionário abaixo
# (à esquerda o nome, como aparece no "Olá", à direita a senha).

USUARIOS_DEMO = {
    "Maria Julia": "12345",
    "Nathalia": "12345",
    "Isadora": "12345",
}

# -----------------------------------------
# CONFIGURAÇÕES
# -----------------------------------------

st.set_page_config(
    page_title="AgroCheck | Milho e Batata",
    page_icon="🌱",
    layout="centered"
)


def html(conteudo):
    """Mostra um trecho de HTML.

    Remove a indentação de cada linha para o Markdown do Streamlit
    não confundir o HTML com um bloco de código.
    """
    linhas = [linha.strip() for linha in conteudo.splitlines()]
    st.markdown(" ".join(l for l in linhas if l), unsafe_allow_html=True)


# -----------------------------------------
# ESTILO VISUAL
# -----------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --verde-escuro: #123d2a;
    --verde: #23734a;
    --verde-claro: #e8f3ec;
    --texto: #1d2b23;
    --texto-suave: #66776d;
    --borda: #e1eae3;
    --fundo: #f5f8f3;
}

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
}

.stApp { background: var(--fundo); }

.block-container {
    max-width: 980px;
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
}

header, #MainMenu, footer { visibility: hidden; }

/* ---------- CABEÇALHO ---------- */

.hero {
    background: linear-gradient(135deg, var(--verde-escuro), var(--verde));
    padding: 28px 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(18, 61, 42, 0.15);
    display: flex;
    align-items: center;
    gap: 20px;
}
.hero-icone {
    font-size: 40px;
    background: rgba(255, 255, 255, 0.12);
    width: 72px;
    height: 72px;
    min-width: 72px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.hero-label {
    color: #b8e4c6;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.5px;
    text-transform: uppercase;
}
.hero h1 {
    color: white;
    font-size: 34px;
    margin: 4px 0 4px 0;
    padding: 0;
    font-weight: 800;
}
.hero p {
    color: #e0eee4;
    font-size: 15px;
    line-height: 1.5;
    margin: 0;
}
.hero-tags { margin-top: 10px; }
.hero-tag {
    display: inline-block;
    background: rgba(255, 255, 255, 0.14);
    color: white;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 999px;
    margin: 4px 6px 0 0;
}

/* ---------- TÍTULOS DE SEÇÃO ---------- */

.section-title {
    color: #173f2c;
    font-size: 20px;
    font-weight: 800;
    margin: 8px 0 2px 0;
}
.section-description {
    color: var(--texto-suave);
    font-size: 14px;
    margin-bottom: 12px;
    line-height: 1.5;
}

/* ---------- UPLOAD ---------- */

[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
    background: white;
    border: 2px dashed #a8c9b1;
    border-radius: 16px;
}
/* Botão "Upload" da área de envio */
[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] {
    background: var(--verde);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}
[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"]:hover {
    background: #174e32;
    color: white;
}
/* Esconde o "chip" com o nome do arquivo enviado
   (versões novas: stFileChip/stFileChips; versões antigas: stFileUploaderFile) */
[data-testid="stFileChip"],
[data-testid="stFileChips"],
[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderPagination"] {
    display: none !important;
}

/* Textos do upload em português (o Streamlit não traduz o file_uploader).
   O texto original fica escondido e o novo entra com ::after. */
[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] [data-testid="stMarkdownContainer"] p {
    display: none;
}
[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"] [data-testid="stMarkdownContainer"]::after {
    content: "Carregar imagem";
}
[data-testid="stFileUploaderDropzoneInstructions"] > div > span,
[data-testid="stFileUploaderDropzoneInstructions"] > div > small {
    display: none;
}
[data-testid="stFileUploaderDropzoneInstructions"] > div::after {
    content: "Até 200 MB • JPG ou PNG";
    color: var(--texto-suave);
    font-size: 14px;
}
/* Versões antigas do Streamlit mostram "Drag and drop file here" */
[data-testid="stFileUploaderDropzoneInstructions"] > div:has(> small)::before {
    content: "Arraste a imagem aqui";
    display: block;
    color: var(--texto);
    font-weight: 600;
}

/* ---------- IMAGEM ENVIADA ---------- */

[data-testid="stImage"] img,
[data-testid="stImageContainer"] img {
    max-height: 300px;
    object-fit: contain;
    border-radius: 14px;
    background: white;
}
[data-testid="stImageCaption"] {
    color: var(--texto-suave);
}

/* ---------- BOTÃO ---------- */

.stButton > button,
[data-testid="stBaseButton-primary"] {
    background: var(--verde);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
    font-size: 16px;
    transition: 0.2s;
}
.stButton > button:hover,
[data-testid="stBaseButton-primary"]:hover {
    background: #174e32;
    color: white;
    border: none;
}
.stButton > button:focus:not(:active) {
    color: white;
    border: none;
}

/* ---------- CARDS ---------- */

.card {
    background: white;
    border: 1px solid var(--borda);
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 4px 16px rgba(30, 70, 45, 0.05);
    margin-bottom: 16px;
}
.card-label {
    color: #6c8875;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.placeholder {
    color: var(--texto-suave);
    font-size: 14px;
    line-height: 1.6;
}
.placeholder ol { margin: 8px 0 0 0; padding-left: 20px; }

/* Resultado principal */
.result-name {
    color: #174e32;
    font-size: 24px;
    font-weight: 800;
    margin: 6px 0 10px 0;
    line-height: 1.25;
}
.badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
}
.badge-saudavel { background: #e3f4e8; color: #1b6b3e; }
.badge-doenca { background: #fdeee6; color: #a2461c; }
.badge-pos_colheita { background: #fff4dc; color: #8a5a00; }

.score-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-top: 16px;
}
.score-value {
    color: var(--verde);
    font-size: 30px;
    font-weight: 800;
}
.score-track {
    background: #edf2ee;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    margin-top: 6px;
}
.score-fill {
    background: linear-gradient(90deg, #2f8f5b, var(--verde));
    height: 100%;
    border-radius: 999px;
}
.low-score {
    margin-top: 12px;
    font-size: 13px;
    color: #8a5a00;
    background: #fff8e6;
    border-radius: 10px;
    padding: 8px 12px;
    line-height: 1.5;
}

/* Barras de probabilidade */
.prob-item { margin-bottom: 12px; }
.prob-item:last-child { margin-bottom: 0; }
.prob-head {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: var(--texto-suave);
    margin-bottom: 4px;
    gap: 12px;
}
.prob-track {
    background: #eef2ef;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}
.prob-fill {
    background: #c3cec7;
    height: 100%;
    border-radius: 999px;
}
.prob-item.vencedora .prob-head {
    color: var(--texto);
    font-weight: 700;
}
.prob-item.vencedora .prob-fill {
    background: linear-gradient(90deg, #2f8f5b, var(--verde));
}

/* Card de tratamento */
.trat-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 14px;
}
.trat-icone {
    font-size: 24px;
    width: 48px;
    height: 48px;
    min-width: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--verde-claro);
}
.trat-titulo {
    color: #173f2c;
    font-size: 20px;
    font-weight: 800;
    line-height: 1.25;
}
.trat-sub {
    color: var(--texto-suave);
    font-size: 13px;
    margin-top: 2px;
}
.trat-sub em { color: var(--texto); }
.trat-desc {
    color: var(--texto);
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 6px;
}
.trat-bloco-titulo {
    color: #173f2c;
    font-size: 15px;
    font-weight: 800;
    margin: 14px 0 6px 0;
}
.trat-lista {
    margin: 0;
    padding-left: 20px;
    color: var(--texto);
    font-size: 14px;
    line-height: 1.6;
}
.trat-lista li { margin-bottom: 4px; }
.trat-fonte {
    color: var(--texto-suave);
    font-size: 12px;
    margin-top: 14px;
    padding-top: 10px;
    border-top: 1px solid var(--borda);
}
.card-saudavel { border-left: 5px solid #2f8f5b; }
.card-doenca { border-left: 5px solid #d9773f; }
.card-pos_colheita { border-left: 5px solid #d9a521; }

/* ---------- AVISO ---------- */

.notice {
    background: #edf4ed;
    border: 1px solid #dce9dd;
    border-left: 4px solid #43865a;
    padding: 14px 18px;
    border-radius: 12px;
    color: #496451;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 8px;
}

/* ---------- RODAPÉ ---------- */

.footer {
    text-align: center;
    color: #91a197;
    font-size: 12px;
    margin-top: 36px;
    padding-top: 18px;
    border-top: 1px solid #e1e9e1;
    line-height: 1.6;
}

/* ---------- LOGIN ---------- */

.login-topo {
    text-align: center;
    margin: 24px 0 18px 0;
}
.login-logo {
    font-size: 34px;
    width: 68px;
    height: 68px;
    margin: 0 auto 10px auto;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, var(--verde-escuro), var(--verde));
    box-shadow: 0 8px 22px rgba(18, 61, 42, 0.18);
}
.login-nome {
    color: #173f2c;
    font-size: 30px;
    font-weight: 800;
}
.login-sub {
    color: var(--texto-suave);
    font-size: 14px;
    margin-top: 2px;
}
[data-testid="stForm"] {
    background: white;
    border: 1px solid var(--borda);
    border-radius: 18px;
    padding: 24px 24px 20px 24px;
    box-shadow: 0 8px 26px rgba(30, 70, 45, 0.07);
}
.login-form-titulo {
    color: #173f2c;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 4px;
}
[data-testid="stFormSubmitButton"] button {
    background: var(--verde);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 46px;
    font-weight: 700;
    font-size: 16px;
}
[data-testid="stFormSubmitButton"] button:hover {
    background: #174e32;
    color: white;
    border: none;
}
.login-dica {
    text-align: center;
    color: #91a197;
    font-size: 12px;
    margin-top: 12px;
}

/* Campo de senha: esconde "Press Enter to submit form" e o olho nativo do Edge,
   deixando só o olho do Streamlit */
[data-testid="InputInstructions"] {
    display: none !important;
}
input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear {
    display: none;
}

/* Saudação + botão Sair (depois do login), na mesma linha */
.st-key-barra_usuario {
    margin-bottom: 4px;
}
.saudacao {
    color: var(--texto-suave);
    font-size: 17px;
    line-height: 1.3;
}
.saudacao strong { color: #173f2c; font-weight: 800; }
.st-key-barra_usuario [data-testid="stMarkdownContainer"] {
    margin-bottom: 0;  /* o Streamlit põe uma margem negativa que desalinha */
}

/* Botões secundários compactos (Sair e Trocar imagem) */
.st-key-botao_sair .stButton > button,
.st-key-botao_sair .stButton > button:focus:not(:active),
.st-key-botao_trocar .stButton > button,
.st-key-botao_trocar .stButton > button:focus:not(:active) {
    background: white;
    color: var(--verde);
    border: 1px solid #b9d3c1;
    border-radius: 10px;
    min-height: 34px;
    height: 34px;
    padding: 0 14px;
    font-size: 14px;
    font-weight: 700;
}
.st-key-botao_sair .stButton > button:hover,
.st-key-botao_trocar .stButton > button:hover {
    background: var(--verde-claro);
    color: #174e32;
    border: 1px solid #9cc2a8;
}

/* ---------- CELULAR ---------- */

@media (max-width: 640px) {
    .block-container { padding-top: 1rem; }
    .hero { padding: 20px; gap: 14px; border-radius: 16px; }
    .hero-icone { display: none; }
    .hero-label { letter-spacing: 1.5px; }
    .hero h1 { font-size: 26px; }
    .hero p { font-size: 14px; }
    .card { padding: 16px; }
    .result-name { font-size: 20px; }
    .score-value { font-size: 26px; }
    .trat-titulo { font-size: 18px; }
    [data-testid="stImage"] img,
    [data-testid="stImageContainer"] img { max-height: 240px; }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# TELA DE LOGIN
# -----------------------------------------

def normalizar(texto):
    """Deixa o texto em minúsculas, sem acentos e sem espaços nas pontas.

    Assim "Maria Julia", "maria julia" e "Maria Júlia" ficam iguais.
    """
    texto = unicodedata.normalize("NFKD", texto.strip().lower())
    sem_acento = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(sem_acento.split())  # junta espaços repetidos no meio


# Número que vai no "key" do uploader. Quando ele muda, o Streamlit cria
# um uploader novo, vazio (é assim que "esquecemos" a imagem enviada).
if "uploader_id" not in st.session_state:
    st.session_state.uploader_id = 0


def limpar_imagem():
    """Esquece a imagem enviada e o resultado da análise."""
    st.session_state.uploader_id += 1
    st.session_state.pop("resultado_analise", None)
    st.session_state.pop("arquivo_analisado", None)


def sair():
    """Faz logout e limpa tudo da sessão (imagem, resultado e uploader)."""
    limpar_imagem()
    st.session_state.logado = False
    st.session_state.pop("usuario_nome", None)


def conferir_login(usuario_digitado, senha_digitada):
    """Devolve o nome do usuário se o login estiver certo, ou None se não."""
    for nome, senha_certa in USUARIOS_DEMO.items():
        if normalizar(usuario_digitado) == normalizar(nome) and senha_digitada == senha_certa:
            return nome
    return None


# Enter no campo "Usuário" passa para o campo "Senha" (em vez de tentar entrar).
# O código fica preso só no campo Usuário e só reage à tecla Enter.
# Se algo der errado, ele não faz nada (o login continua funcionando normal).
SCRIPT_ENTER_PROXIMO_CAMPO = """
<script>
(function () {
    try {
        const doc = window.parent.document;
        function ligar(tentativas) {
            const usuario = doc.querySelector('input[aria-label="Usuário"]');
            const senha = doc.querySelector('input[aria-label="Senha"]');
            if (!usuario || !senha) {
                if (tentativas > 0) { setTimeout(function () { ligar(tentativas - 1); }, 200); }
                return;
            }
            usuario.setAttribute("enterkeyhint", "next");
            if (usuario.dataset.agroEnter === "1") { return; }
            usuario.dataset.agroEnter = "1";
            usuario.addEventListener("keydown", function (evento) {
                if (evento.key === "Enter" && !evento.isComposing) {
                    evento.preventDefault();
                    evento.stopPropagation();
                    senha.focus();
                }
            });
        }
        ligar(25);
    } catch (erro) {
        console.log("AgroCheck (Enter -> Senha):", erro);
    }
})();
</script>
"""


if not st.session_state.get("logado", False):

    html("""
    <div class="login-topo">
        <div class="login-logo">🌱</div>
        <div class="login-nome">AgroCheck</div>
        <div class="login-sub">Identificação de doenças em folhas de milho e batata</div>
    </div>
    """)

    _, col_login, _ = st.columns([1, 2, 1])

    with col_login:
        with st.form("form_login"):
            html('<div class="login-form-titulo">Entrar</div>')

            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")

            entrar = st.form_submit_button(
                "Entrar",
                icon=":material/login:",
                type="primary",
                width="stretch"
            )

        if entrar:
            nome_logado = conferir_login(usuario, senha)
            if nome_logado:
                st.session_state.logado = True
                st.session_state.usuario_nome = nome_logado
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos. Tente novamente.", icon="🔒")

        html('<div class="login-dica">Acesso de demonstração do projeto AgroCheck.</div>')

    components.html(SCRIPT_ENTER_PROXIMO_CAMPO, height=0)

    # Enquanto não houver login, nada abaixo é executado (nem o modelo é carregado)
    st.stop()


# Saudação + botão Sair, na mesma linha (o botão fica à direita)
with st.container(
    key="barra_usuario",
    horizontal=True,
    horizontal_alignment="distribute",
    vertical_alignment="center"
):
    st.markdown(
        f'<div class="saudacao">👋 Olá, <strong>{st.session_state.get("usuario_nome", "")}</strong></div>',
        unsafe_allow_html=True,
        width="content"
    )
    st.button(
        "Sair",
        key="botao_sair",
        icon=":material/logout:",
        on_click=sair,
        width="content"
    )


# -----------------------------------------
# CARREGAR MODELO
# -----------------------------------------

ARQUIVO_MODELO = "agrocheck_turbinado.keras"


@st.cache_resource
def carregar_modelo():
    return tf.keras.models.load_model(ARQUIVO_MODELO)


if not os.path.exists(ARQUIVO_MODELO):
    st.error(
        f"O arquivo do modelo ({ARQUIVO_MODELO}) não foi encontrado. "
        "Coloque-o na mesma pasta do app.py e recarregue a página."
    )
    st.stop()


with st.spinner("Preparando o AgroCheck..."):
    modelo = carregar_modelo()


# -----------------------------------------
# CLASSES
# -----------------------------------------

# A ordem precisa ser IGUAL à do treino (caderno AgroCheck_Treino_Milho_Batata):
# 0 Corn___Common_Rust_Leaf, 1 Corn___Gray_Leaf_Spot_Leaf, 2 Corn___Healthy_Leaf,
# 3 Corn___Northern_Leaf_Blight_Leaf, 4 Potato___Early_blight_Leaf,
# 5 Potato___Late_Blight_Leaf, 6 Potato__Healthy_Leaf
classes = [
    "Milho - Ferrugem comum",
    "Milho - Mancha cinzenta",
    "Milho saudável",
    "Milho - Helmintosporiose",
    "Batata - Pinta-preta",
    "Batata - Requeima",
    "Batata saudável"
]

# Proteção: confere se o modelo tem o mesmo número de classes da lista acima
saidas_modelo = modelo.output_shape[-1]
if saidas_modelo != len(classes):
    st.error(
        f"O modelo carregado tem {saidas_modelo} classes, mas o site espera "
        f"{len(classes)}. Verifique se o arquivo agrocheck_turbinado.keras está na pasta."
    )
    st.stop()


# Textos e ícones de cada tipo de resultado
TIPOS = {
    "saudavel": {"icone": "✅", "badge": "Planta saudável"},
    "doenca": {"icone": "🦠", "badge": "Doença identificada"},
    "pos_colheita": {"icone": "📦", "badge": "Problema pós-colheita"},
}

# Abaixo desta pontuação, sugerimos tirar outra foto
LIMITE_CONFIANCA = 0.60


# -----------------------------------------
# FUNÇÕES DE EXIBIÇÃO
# -----------------------------------------

def mostrar_resultado(indice, confianca):
    """Card com a identificação e a pontuação da classe vencedora."""
    info = TRATAMENTOS.get(classes[indice], {})
    tipo = info.get("tipo", "doenca")
    aviso_baixo = ""
    if confianca < LIMITE_CONFIANCA:
        aviso_baixo = (
            '<div class="low-score">💡 Pontuação baixa: o modelo ficou em dúvida. '
            'Tente outra foto, com boa luz e a folha ou raiz bem enquadrada.</div>'
        )

    html(f"""
    <div class="card">
        <div class="card-label">🍃 Possível identificação</div>
        <div class="result-name">{classes[indice]}</div>
        <span class="badge badge-{tipo}">{TIPOS[tipo]["icone"]} {TIPOS[tipo]["badge"]}</span>
        <div class="score-row">
            <div class="card-label">📊 Pontuação do modelo</div>
            <div class="score-value">{confianca:.1%}</div>
        </div>
        <div class="score-track">
            <div class="score-fill" style="width: {confianca * 100:.1f}%"></div>
        </div>
        {aviso_baixo}
    </div>
    """)


def mostrar_probabilidades(previsoes, indice):
    """Barras com a pontuação de cada classe; destaque só na vencedora."""
    ranking = np.argsort(previsoes)[::-1]
    itens = []
    for i in ranking:
        valor = float(previsoes[i]) * 100
        classe_css = "prob-item vencedora" if i == indice else "prob-item"
        itens.append(f"""
        <div class="{classe_css}">
            <div class="prob-head">
                <span>{classes[i]}</span>
                <span>{valor:.1f}%</span>
            </div>
            <div class="prob-track">
                <div class="prob-fill" style="width: {valor:.1f}%"></div>
            </div>
        </div>
        """)

    html(f"""
    <div class="card">
        <div class="card-label" style="margin-bottom: 14px;">📊 Probabilidade por categoria</div>
        {"".join(itens)}
    </div>
    """)


def lista_html(itens):
    return "<ul class='trat-lista'>" + "".join(f"<li>{item}</li>" for item in itens) + "</ul>"


def mostrar_tratamento(nome_classe):
    """Card com informações e recomendações de manejo da classe."""
    info = TRATAMENTOS.get(nome_classe)
    if info is None:
        return

    tipo = info["tipo"]

    subtitulo = ""
    if info.get("nome_popular"):
        subtitulo += f"<div class='trat-sub'>Nome popular: {info['nome_popular']}</div>"
    if info.get("nome_cientifico"):
        subtitulo += f"<div class='trat-sub'>Agente causador: <em>{info['nome_cientifico']}</em></div>"

    sintomas = ""
    if info.get("sintomas"):
        sintomas = (
            "<div class='trat-bloco-titulo'>🔎 Principais sintomas</div>"
            + lista_html(info["sintomas"])
        )

    if tipo == "saudavel":
        titulo_manejo = "🌿 Dicas de prevenção"
    elif tipo == "pos_colheita":
        titulo_manejo = "🧺 Cuidados na pós-colheita e no armazenamento"
    else:
        titulo_manejo = "🛠️ Recomendações de manejo"

    html(f"""
    <div class="card card-{tipo}">
        <div class="trat-header">
            <div class="trat-icone">{TIPOS[tipo]["icone"]}</div>
            <div>
                <div class="card-label">Possíveis tratamentos e manejo</div>
                <div class="trat-titulo">{info["titulo"]}</div>
                {subtitulo}
            </div>
        </div>
        <div class="trat-desc">{info["descricao"]}</div>
        {sintomas}
        <div class="trat-bloco-titulo">{titulo_manejo}</div>
        {lista_html(info["manejo"])}
        <div class="trat-fonte">📚 Para saber mais: {info["fonte"]}</div>
    </div>
    """)


# -----------------------------------------
# CABEÇALHO
# -----------------------------------------

html("""
<div class="hero">
    <div class="hero-icone">🌱</div>
    <div>
        <div class="hero-label">Inteligência artificial no campo</div>
        <h1>AgroCheck</h1>
        <p>Envie a foto de uma folha de milho ou de batata e descubra
        em segundos se há sinais de doença.</p>
        <div class="hero-tags">
            <span class="hero-tag">🌽 Milho</span>
            <span class="hero-tag">🥔 Batata</span>
            <span class="hero-tag">7 categorias</span>
        </div>
    </div>
</div>
""")


# -----------------------------------------
# ÁREA DE ANÁLISE
# -----------------------------------------

html("""
<div class="section-title">📷 Análise de imagem</div>
<div class="section-description">
Envie uma foto nítida de uma folha de milho ou de batata (JPG ou PNG).
</div>
""")

with st.container(key="area_upload"):
    imagem = st.file_uploader(
        "Selecione uma imagem de folha de milho ou batata",
        type=["jpg", "jpeg", "png"],
        help="Formatos aceitos: JPG, JPEG e PNG.",
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_id}"
    )

resultado = None

if imagem is not None:

    # Com uma imagem carregada, a área de upload some
    # (para trocar, usa-se o botão "Trocar imagem" abaixo da foto)
    st.markdown(
        "<style>.st-key-area_upload { display: none; }</style>",
        unsafe_allow_html=True
    )

    foto = Image.open(imagem).convert("RGB")

    arquivo_atual = (imagem.name, imagem.size)

    if st.session_state.get("arquivo_analisado") != arquivo_atual:
        st.session_state.pop("resultado_analise", None)

    col_foto, col_resultado = st.columns([2, 3], gap="large")

    with col_foto:
        st.image(
            foto,
            caption="Imagem enviada",
            width="stretch"
        )
        st.button(
            "Trocar imagem",
            key="botao_trocar",
            icon=":material/swap_horiz:",
            on_click=limpar_imagem,
            width="stretch"
        )

    with col_resultado:

        clicou = st.button(
            "Analisar imagem",
            icon=":material/search:",
            type="primary",
            width="stretch"
        )

        if clicou:
            with st.spinner("A inteligência artificial está analisando a imagem..."):

                imagem_processada = foto.resize((224, 224))

                imagem_array = np.array(
                    imagem_processada,
                    dtype=np.float32
                )

                imagem_array = np.expand_dims(
                    imagem_array,
                    axis=0
                )

                previsoes = modelo.predict(
                    imagem_array,
                    verbose=0
                )[0]

                ranking = np.argsort(previsoes)[::-1]

                indice = int(ranking[0])
                confianca = float(previsoes[indice])

                st.session_state.resultado_analise = {
                    "previsoes": previsoes,
                    "indice": indice,
                    "confianca": confianca
                }

                st.session_state.arquivo_analisado = arquivo_atual

        resultado = st.session_state.get("resultado_analise")

        if resultado is not None:
            mostrar_resultado(resultado["indice"], resultado["confianca"])
        else:
            html("""
            <div class="card placeholder">
                <div class="card-label">Pronto para analisar</div>
                <ol>
                    <li>Confira se a foto ao lado está nítida.</li>
                    <li>Clique em <strong>Analisar imagem</strong>.</li>
                    <li>Veja a identificação, as pontuações e as dicas de manejo.</li>
                </ol>
            </div>
            """)


# -----------------------------------------
# DETALHES DO RESULTADO (largura total)
# -----------------------------------------

if resultado is not None:

    mostrar_probabilidades(resultado["previsoes"], resultado["indice"])

    mostrar_tratamento(classes[resultado["indice"]])

    html("""
    <div class="notice">
        <strong>⚠️ Importante:</strong>
        esta análise é uma estimativa gerada por inteligência artificial,
        baseada nas imagens usadas no treinamento do modelo.
        O resultado e as recomendações são apenas informativos e
        <strong>não substituem a avaliação de um engenheiro agrônomo</strong>,
        que deve ser consultado antes de qualquer aplicação de produtos.
    </div>
    """)


# -----------------------------------------
# RODAPÉ
# -----------------------------------------

html("""
<div class="footer">
    🌱 <strong>AGROCHECK</strong><br>
    Inteligência artificial aplicada à agricultura · milho e batata
</div>
""")
