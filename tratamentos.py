"""
Informações de manejo para cada classe reconhecida pelo AgroCheck.

As chaves do dicionário TRATAMENTOS são exatamente os nomes da lista
`classes` do app.py. O conteúdo é informativo, baseado em publicações
técnicas (como as da Embrapa Milho e Sorgo e da Embrapa Hortaliças (batata)), e
NÃO cita produtos comerciais nem doses: qualquer uso de defensivo deve
seguir a recomendação de um engenheiro agrônomo e os produtos registrados
no MAPA para a cultura.

Campos de cada classe:
    tipo             -> "saudavel" ou "doenca"
    titulo           -> título do card
    nome_popular     -> nome(s) popular(es) do problema
    nome_cientifico  -> agente causador (None quando não se aplica)
    descricao        -> explicação curta
    sintomas         -> lista com os principais sinais
    manejo           -> lista de recomendações de manejo/prevenção
    fonte            -> referência geral para aprofundar
"""

TRATAMENTOS = {
    # 0
    "Milho - Ferrugem comum": {
        "tipo": "doenca",
        "titulo": "Ferrugem comum do milho",
        "nome_popular": "Ferrugem comum",
        "nome_cientifico": "Puccinia sorghi (fungo)",
        "descricao": (
            "Doença causada por um fungo que se espalha pelo vento. É "
            "favorecida por temperaturas amenas (cerca de 16 a 23 °C) e "
            "umidade alta, com orvalho nas folhas."
        ),
        "sintomas": [
            "Pequenas pústulas (bolinhas) arredondadas a alongadas, de cor "
            "marrom-avermelhada (cor de ferrugem).",
            "Pústulas nas duas faces da folha, que se rompem e liberam um pó "
            "avermelhado.",
            "Com o avanço, as pústulas escurecem e as folhas podem secar.",
        ],
        "manejo": [
            "Use cultivares/híbridos com resistência à ferrugem comum "
            "(principal forma de controle).",
            "Ajuste a época de semeadura para evitar períodos mais frios e "
            "úmidos, quando a doença é mais favorecida na sua região.",
            "Monitore a lavoura com frequência, principalmente antes do "
            "pendoamento, observando as folhas do terço médio e superior.",
            "Elimine plantas voluntárias de milho (tigueras) entre safras.",
            "Se necessário, use fungicidas registrados para a cultura, apenas "
            "com receita e orientação de um engenheiro agrônomo.",
        ],
        "fonte": "Embrapa Milho e Sorgo — doenças do milho",
    },

    # 1
    "Milho - Mancha cinzenta": {
        "tipo": "doenca",
        "titulo": "Mancha cinzenta do milho (cercosporiose)",
        "nome_popular": "Mancha cinzenta / cercosporiose",
        "nome_cientifico": "Cercospora zeae-maydis (fungo)",
        "descricao": (
            "Uma das doenças foliares mais importantes do milho no Brasil. O "
            "fungo sobrevive nos restos de cultura e é favorecido por "
            "umidade relativa alta, temperaturas moderadas a altas e plantios "
            "sucessivos de milho na mesma área."
        ),
        "sintomas": [
            "Manchas retangulares, de cor cinza a palha, com bordas retas.",
            "Lesões limitadas pelas nervuras e paralelas a elas.",
            "Começa nas folhas de baixo e sobe na planta; em ataques fortes, "
            "as manchas se juntam e a folha seca.",
        ],
        "manejo": [
            "Use cultivares/híbridos resistentes ou tolerantes.",
            "Faça rotação de culturas com espécies que não sejam hospedeiras "
            "(por exemplo, soja ou feijão), evitando milho após milho.",
            "Maneje os restos culturais, que são a principal fonte do fungo "
            "para a safra seguinte.",
            "Faça adubação equilibrada e use população de plantas adequada.",
            "Monitore as folhas inferiores desde cedo, principalmente em "
            "períodos úmidos.",
            "Se necessário, use fungicidas registrados para a cultura, apenas "
            "com receita e orientação de um engenheiro agrônomo.",
        ],
        "fonte": "Embrapa Milho e Sorgo — doenças do milho",
    },

    # 2
    "Milho saudável": {
        "tipo": "saudavel",
        "titulo": "Seu milho parece saudável",
        "nome_popular": None,
        "nome_cientifico": None,
        "descricao": (
            "Ótima notícia! O modelo não encontrou sinais das doenças "
            "avaliadas. Continue de olho na lavoura com estas práticas de "
            "prevenção:"
        ),
        "sintomas": [],
        "manejo": [
            "Monitore a lavoura semanalmente, olhando folhas de baixo, do meio "
            "e de cima.",
            "Prefira híbridos com boa resistência às doenças comuns na sua região.",
            "Faça rotação de culturas e evite plantar milho sobre milho.",
            "Maneje os restos culturais e elimine plantas voluntárias (tigueras).",
            "Mantenha adubação equilibrada e população de plantas adequada.",
        ],
        "fonte": "Embrapa Milho e Sorgo — manejo de doenças do milho",
    },

    # 3
    "Milho - Helmintosporiose": {
        "tipo": "doenca",
        "titulo": "Helmintosporiose do milho",
        "nome_popular": "Helmintosporiose / mancha de turcicum / queima de turcicum",
        "nome_cientifico": "Exserohilum turcicum (fungo)",
        "descricao": (
            "Doença foliar causada por um fungo que sobrevive nos restos de "
            "cultura. É favorecida por temperaturas moderadas (cerca de 18 a "
            "27 °C), orvalho e umidade alta. Ataques antes do enchimento de "
            "grãos podem reduzir a produção."
        ),
        "sintomas": [
            "Lesões grandes e alongadas, em forma de \"charuto\" (elípticas), "
            "com vários centímetros de comprimento.",
            "Cor cinza-esverdeada a marrom-clara.",
            "Surge primeiro nas folhas de baixo; em ataques fortes, as lesões "
            "se juntam e a folha parece queimada.",
        ],
        "manejo": [
            "Use cultivares/híbridos resistentes (principal medida de controle).",
            "Faça rotação de culturas com espécies não hospedeiras.",
            "Maneje os restos culturais, que mantêm o fungo de uma safra para "
            "outra.",
            "Evite semeaduras em épocas muito favoráveis à doença na sua região.",
            "Monitore a lavoura, principalmente em períodos frescos e úmidos.",
            "Se necessário, use fungicidas registrados para a cultura, apenas "
            "com receita e orientação de um engenheiro agrônomo.",
        ],
        "fonte": "Embrapa Milho e Sorgo — doenças do milho",
    },

    # 4
    "Batata - Pinta-preta": {
        "tipo": "doenca",
        "titulo": "Pinta-preta da batata",
        "nome_popular": "Pinta-preta / mancha-de-alternária",
        "nome_cientifico": "Alternaria solani (fungo)",
        "descricao": (
            "Doença foliar comum nas lavouras de batata. O fungo sobrevive em "
            "restos de cultura, no solo e em outras plantas da mesma família "
            "(como tomate). É favorecida por temperaturas mais altas (cerca de "
            "20 a 30 °C) alternando períodos úmidos e secos, e ataca mais "
            "plantas estressadas ou mal nutridas."
        ),
        "sintomas": [
            "Manchas marrom-escuras com anéis concêntricos, parecendo um "
            "\"alvo\".",
            "Halo amarelado ao redor das manchas.",
            "Começa nas folhas mais velhas (de baixo) e sobe na planta.",
            "Em ataques fortes, as folhas secam e a planta perde folhagem, "
            "reduzindo a produção.",
        ],
        "manejo": [
            "Use batata-semente sadia e certificada.",
            "Prefira cultivares menos suscetíveis à pinta-preta.",
            "Faça adubação equilibrada: plantas bem nutridas resistem melhor.",
            "Faça rotação com culturas que não sejam da família da batata "
            "(evite tomate, pimentão e berinjela na sequência).",
            "Elimine restos culturais e plantas voluntárias (tigueras) de batata.",
            "Evite longos períodos de folha molhada; prefira irrigar de forma "
            "que as folhas sequem rápido.",
            "Se necessário, use fungicidas registrados para a cultura, apenas "
            "com receita e orientação de um engenheiro agrônomo.",
        ],
        "fonte": "Embrapa Hortaliças — doenças da batata",
    },

    # 5
    "Batata - Requeima": {
        "tipo": "doenca",
        "titulo": "Requeima da batata",
        "nome_popular": "Requeima / mela",
        "nome_cientifico": "Phytophthora infestans (oomiceto, organismo parecido com fungo)",
        "descricao": (
            "É a doença mais destrutiva da batata no mundo e pode destruir uma "
            "lavoura em poucos dias. É favorecida por clima frio e úmido "
            "(temperaturas amenas, chuva, neblina e orvalho por muitas horas). "
            "Também ataca o tomate."
        ),
        "sintomas": [
            "Manchas grandes, de aspecto encharcado, verde-escuras a marrom ou "
            "pretas, muitas vezes começando pelas bordas e pontas das folhas.",
            "Em tempo úmido, aparece um mofo esbranquiçado na parte de baixo "
            "da folha, ao redor das manchas.",
            "A doença avança rápido e as folhas e hastes parecem queimadas.",
            "Os tubérculos podem apresentar manchas marrom-avermelhadas e "
            "podridão.",
        ],
        "manejo": [
            "Plante batata-semente sadia e certificada.",
            "Prefira cultivares com maior resistência à requeima.",
            "Monitore a lavoura com muita frequência em períodos frios e "
            "úmidos; a ação precisa ser rápida.",
            "Evite irrigação por aspersão em excesso e folhas molhadas por "
            "muito tempo; use espaçamento que favoreça a ventilação.",
            "Faça a amontoa bem feita para proteger os tubérculos.",
            "Elimine plantas voluntárias, restos culturais e pilhas de "
            "descarte de batata, e evite plantar perto de tomate doente.",
            "O controle químico costuma ser preventivo: use fungicidas "
            "registrados para a cultura, apenas com receita e orientação de "
            "um engenheiro agrônomo.",
        ],
        "fonte": "Embrapa Hortaliças — doenças da batata",
    },

    # 6
    "Batata saudável": {
        "tipo": "saudavel",
        "titulo": "Sua batata parece saudável",
        "nome_popular": None,
        "nome_cientifico": None,
        "descricao": (
            "Ótima notícia! O modelo não encontrou sinais de pinta-preta nem "
            "de requeima. Continue de olho na lavoura com estas práticas de "
            "prevenção:"
        ),
        "sintomas": [],
        "manejo": [
            "Monitore a lavoura com frequência, principalmente em períodos "
            "úmidos, quando a requeima pode surgir e se espalhar rápido.",
            "Use batata-semente sadia e certificada.",
            "Faça rotação de culturas, evitando plantas da mesma família "
            "(tomate, pimentão, berinjela) na sequência.",
            "Mantenha adubação equilibrada e irrigação que não deixe as folhas "
            "molhadas por muito tempo.",
            "Elimine plantas voluntárias e restos de cultura de batata.",
        ],
        "fonte": "Embrapa Hortaliças — produção de batata",
    },
}
