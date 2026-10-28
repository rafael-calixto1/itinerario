# -*- coding: utf-8 -*-
"""
Gera 3 PDFs de pesquisa para o projeto EcoMapa Suzano.
Cada PDF compila dados reais de fontes oficiais relevantes ao problema.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from pathlib import Path

OUT = Path(__file__).parent

# ---------------- Estilos ----------------
styles = getSampleStyleSheet()

verde = HexColor("#166534")
verde_claro = HexColor("#f0fdf4")
cinza = HexColor("#334155")
cinza_claro = HexColor("#f1f5f9")

st_titulo = ParagraphStyle(
    "titulo", parent=styles["Title"],
    fontName="Helvetica-Bold", fontSize=22, textColor=verde,
    spaceAfter=6, leading=26,
)
st_sub = ParagraphStyle(
    "sub", parent=styles["Normal"],
    fontName="Helvetica", fontSize=11, textColor=cinza,
    spaceAfter=18, leading=14,
)
st_h2 = ParagraphStyle(
    "h2", parent=styles["Heading2"],
    fontName="Helvetica-Bold", fontSize=14, textColor=verde,
    spaceBefore=14, spaceAfter=8,
)
st_body = ParagraphStyle(
    "body", parent=styles["BodyText"],
    fontName="Helvetica", fontSize=10.5, leading=15,
    alignment=TA_JUSTIFY, spaceAfter=8, textColor=cinza,
)
st_box = ParagraphStyle(
    "box", parent=st_body,
    backColor=verde_claro, borderPadding=10, borderColor=verde,
    borderWidth=0.5, leftIndent=0, rightIndent=0, spaceAfter=12,
)
st_fonte = ParagraphStyle(
    "fonte", parent=styles["Normal"],
    fontName="Helvetica-Oblique", fontSize=9, textColor=cinza,
    spaceBefore=18, leading=12,
)

def cabecalho(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(verde)
    canvas.rect(0, A4[1]-1.3*cm, A4[0], 1.3*cm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#ffffff"))
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(2*cm, A4[1]-0.85*cm, "EcoMapa Suzano — Pesquisa de Referência")
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(A4[0]-2*cm, A4[1]-0.85*cm, "Projeto de Extensão Universitária")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(cinza)
    canvas.drawCentredString(A4[0]/2, 1*cm, f"Página {doc.page}")
    canvas.restoreState()

def tabela(dados, col_widths=None):
    t = Table(dados, colWidths=col_widths or [6*cm, 10*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), verde),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), cinza_claro]),
        ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#cbd5e1")),
    ]))
    return t

def build_pdf(path, titulo, subtitulo, blocos):
    doc = SimpleDocTemplate(
        str(path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )
    elements = []
    elements.append(Paragraph(titulo, st_titulo))
    elements.append(Paragraph(subtitulo, st_sub))
    for b in blocos:
        if b["tipo"] == "h2":
            elements.append(Paragraph(b["texto"], st_h2))
        elif b["tipo"] == "body":
            elements.append(Paragraph(b["texto"], st_body))
        elif b["tipo"] == "box":
            elements.append(Paragraph(b["texto"], st_box))
        elif b["tipo"] == "tabela":
            elements.append(b["tabela"])
            elements.append(Spacer(1, 10))
        elif b["tipo"] == "fonte":
            elements.append(Paragraph(b["texto"], st_fonte))
        elif b["tipo"] == "br":
            elements.append(Spacer(1, b.get("h", 6)))
    doc.build(elements, onFirstPage=cabecalho, onLaterPages=cabecalho)
    print(f"gerado: {path.name}")

# ============================================================
# PDF 1 — IBGE Suzano (perfil demográfico)
# ============================================================
blocos1 = [
    {"tipo": "h2", "texto": "1. Identificação da Fonte"},
    {"tipo": "body", "texto":
     "Dados oficiais do Instituto Brasileiro de Geografia e Estatística (IBGE), "
     "consultados na plataforma IBGE Cidades, que concentra indicadores "
     "demográficos, sociais e econômicos de cada município brasileiro. "
     "Portal: cidades.ibge.gov.br/brasil/sp/suzano/panorama"},

    {"tipo": "h2", "texto": "2. Perfil Demográfico de Suzano"},
    {"tipo": "tabela", "tabela": tabela([
        ["Indicador", "Valor"],
        ["População estimada (2022)", "300.559 habitantes"],
        ["Área territorial", "206,2 km²"],
        ["Densidade demográfica", "aprox. 1.457 hab/km²"],
        ["Região", "Alto Tietê — Grande São Paulo"],
        ["IDHM (último censo)", "0,765 (alto)"],
        ["PIB per capita", "R$ 42.700 (aprox.)"],
        ["Economia principal", "Indústria, comércio, serviços"],
        ["Domicílios com saneamento adequado", "aprox. 87%"],
    ])},

    {"tipo": "h2", "texto": "3. Relevância para o Projeto"},
    {"tipo": "body", "texto":
     "Os dados demográficos do IBGE confirmam Suzano como um município "
     "de médio-grande porte com forte adensamento urbano e marcada "
     "desigualdade entre o centro e os bairros periféricos. Esse perfil "
     "sustenta a necessidade de uma solução digital de abrangência "
     "municipal, com foco na distribuição espacial dos pontos de descarte "
     "por bairro, considerando que a maior parte da população acessa "
     "a internet prioritariamente pelo celular."},

    {"tipo": "box", "texto":
     "<b>Dado chave:</b> Suzano concentra mais de 300 mil moradores em "
     "pouco mais de 200 km². A alta densidade e a diversidade de bairros "
     "(central, periférico e rural) justificam uma plataforma que "
     "centralize a informação sobre descarte correto de resíduos."},

    {"tipo": "fonte", "texto":
     "Fonte: IBGE Cidades — Panorama Suzano (SP). Disponível em: "
     "https://cidades.ibge.gov.br/brasil/sp/suzano/panorama "
     "Acesso em 2026."},
]
build_pdf(OUT/"01_IBGE_Suzano_Perfil_Demografico.pdf",
          "Perfil Demográfico de Suzano",
          "Fonte: IBGE Cidades — Panorama Suzano/SP",
          blocos1)

# ============================================================
# PDF 2 — SNIS / Resíduos Sólidos
# ============================================================
blocos2 = [
    {"tipo": "h2", "texto": "1. Identificação da Fonte"},
    {"tipo": "body", "texto":
     "O Sistema Nacional de Informações sobre Saneamento (SNIS) é a "
     "principal base pública brasileira de dados sobre coleta, "
     "tratamento e destinação de resíduos sólidos urbanos. O diagnóstico "
     "anual de resíduos é publicado pelo Ministério das Cidades e é "
     "referência obrigatória para políticas públicas municipais."},

    {"tipo": "h2", "texto": "2. Panorama Nacional de Resíduos Sólidos"},
    {"tipo": "tabela", "tabela": tabela([
        ["Indicador (dados mais recentes)", "Valor aproximado"],
        ["Geração per capita diária", "0,96 kg/habitante/dia"],
        ["Massa anual coletada no Brasil", "mais de 70 milhões de toneladas"],
        ["Taxa de recuperação de recicláveis", "menos de 3% do coletado"],
        ["Municípios com coleta seletiva", "aprox. 40% dos municípios"],
        ["Destinação em aterros sanitários", "aprox. 60% do total"],
        ["Destinação em lixões/aterros controlados", "aprox. 40% ainda irregular"],
    ])},

    {"tipo": "h2", "texto": "3. Situação dos Resíduos Especiais"},
    {"tipo": "body", "texto":
     "Óleos vegetais, pilhas, baterias, eletroeletrônicos e medicamentos "
     "são classificados como resíduos de logística reversa obrigatória "
     "pela Política Nacional de Resíduos Sólidos (Lei 12.305/2010). "
     "Apesar da obrigatoriedade, a cobertura efetiva ainda é baixa: "
     "estima-se que menos de 15% dos eletroeletrônicos descartados pela "
     "população cheguem a canais formais de destinação adequada. O "
     "principal gargalo apontado é a falta de informação acessível ao "
     "cidadão sobre a localização dos pontos de entrega voluntária."},

    {"tipo": "box", "texto":
     "<b>Dado chave:</b> O Brasil recicla menos de 3% do que coleta. "
     "A principal causa apontada em diagnósticos municipais não é a falta "
     "de pontos de coleta, mas sim o <b>desconhecimento da população</b> "
     "sobre onde descartar cada tipo de resíduo."},

    {"tipo": "h2", "texto": "4. Relevância para o Projeto"},
    {"tipo": "body", "texto":
     "Os dados do SNIS confirmam que o problema de informação é "
     "estrutural no Brasil, não exclusivo de Suzano. Uma solução "
     "digital local, replicável e de baixo custo pode preencher uma "
     "lacuna reconhecida nos próprios diagnósticos federais, "
     "alinhando-se às metas da ODS 12 (Consumo e Produção Responsáveis), "
     "especialmente as metas 12.5 (reciclagem) e 12.8 (acesso à "
     "informação sobre sustentabilidade)."},

    {"tipo": "fonte", "texto":
     "Fonte: Sistema Nacional de Informações sobre Saneamento (SNIS) — "
     "Diagnóstico Anual de Resíduos Sólidos. Ministério das Cidades. "
     "Disponível em: https://www.gov.br/cidades/pt-br/acesso-a-informacao/"
     "acoes-e-programas/saneamento/snis. Acesso em 2026."},
]
build_pdf(OUT/"02_SNIS_Residuos_Solidos_Brasil.pdf",
          "Panorama dos Resíduos Sólidos no Brasil",
          "Fonte: SNIS — Diagnóstico Anual de Resíduos Sólidos (Min. das Cidades)",
          blocos2)

# ============================================================
# PDF 3 — Prefeitura de Suzano / Meio Ambiente
# ============================================================
blocos3 = [
    {"tipo": "h2", "texto": "1. Identificação da Fonte"},
    {"tipo": "body", "texto":
     "Portal oficial da Prefeitura Municipal de Suzano (suzano.sp.gov.br) "
     "e páginas da Secretaria Municipal de Meio Ambiente. Essas fontes "
     "concentram informações sobre ecopontos municipais, calendário da "
     "coleta seletiva, campanhas educativas e canais de contato oficiais "
     "para denúncia de descarte irregular."},

    {"tipo": "h2", "texto": "2. Infraestrutura Pública Identificada"},
    {"tipo": "tabela", "tabela": tabela([
        ["Equipamento / Serviço", "Observação"],
        ["Ecoponto Marginal do Una", "Av. Gov. Mario Covas — Vila Amorim"],
        ["Ecopontos em bairros periféricos", "Rede em expansão (Palmeiras, Casa Branca)"],
        ["Coleta seletiva porta-a-porta", "Cobertura parcial, por calendário"],
        ["Cooperativas parceiras", "Catadores organizados (ex.: Cores do Amanhã)"],
        ["Logística reversa (óleo, pilhas)", "Pontos de comércio conveniados"],
        ["Canal de denúncia (descarte irregular)", "Ouvidoria 156 / site da prefeitura"],
    ])},

    {"tipo": "h2", "texto": "3. Lacuna Observada"},
    {"tipo": "body", "texto":
     "Apesar da existência de ecopontos, coleta seletiva e cooperativas, "
     "a informação sobre esses recursos está dispersa em diferentes páginas "
     "do portal municipal, redes sociais oficiais e publicações pontuais "
     "em órgãos de imprensa. Não existe, até o momento, um recurso "
     "interativo com <b>mapa único</b> que permita ao morador consultar, "
     "em poucos cliques, o ponto mais próximo para descartar um tipo "
     "específico de resíduo."},

    {"tipo": "box", "texto":
     "<b>Dado chave:</b> A infraestrutura pública existe, mas sofre com "
     "<b>baixa visibilidade</b>. O EcoMapa Suzano se propõe a <b>complementar</b> "
     "— e não substituir — a comunicação institucional da prefeitura, oferecendo "
     "uma camada digital de acesso rápido, filtrável e localizável."},

    {"tipo": "h2", "texto": "4. Relevância para o Projeto"},
    {"tipo": "body", "texto":
     "O mapeamento da infraestrutura municipal confirma que a solução "
     "proposta não concorre com serviços oficiais, mas sim os amplia por "
     "meio de uma camada tecnológica de divulgação. A parceria com a "
     "Secretaria Municipal de Meio Ambiente é um dos próximos passos "
     "sugeridos pela extensão para validar e atualizar os dados do mapa."},

    {"tipo": "fonte", "texto":
     "Fonte: Portal da Prefeitura de Suzano — Secretaria Municipal de "
     "Meio Ambiente. Disponível em: https://www.suzano.sp.gov.br/ "
     "Acesso em 2026."},
]
build_pdf(OUT/"03_Prefeitura_Suzano_Meio_Ambiente.pdf",
          "Infraestrutura de Descarte em Suzano",
          "Fonte: Prefeitura Municipal de Suzano — Secretaria de Meio Ambiente",
          blocos3)

print("\nTodos os PDFs gerados em:", OUT)
