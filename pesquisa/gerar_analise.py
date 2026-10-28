# -*- coding: utf-8 -*-
"""Gera relatorio de analise dos questionarios com graficos."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from pathlib import Path

OUT = Path(__file__).parent / "05_Analise_Questionarios_EcoMapa_Suzano.pdf"

verde = HexColor("#166534")
verde_c = HexColor("#22c55e")
verde_cc = HexColor("#86efac")
verde_claro = HexColor("#f0fdf4")
cinza = HexColor("#334155")
cinza_claro = HexColor("#f1f5f9")
amarelo = HexColor("#eab308")
vermelho = HexColor("#ef4444")
azul = HexColor("#0ea5e9")
roxo = HexColor("#a855f7")

st = getSampleStyleSheet()
st_tit = ParagraphStyle("t", parent=st["Title"], fontName="Helvetica-Bold",
    fontSize=20, textColor=verde, spaceAfter=4, leading=24)
st_sub = ParagraphStyle("s", parent=st["Normal"], fontName="Helvetica",
    fontSize=10.5, textColor=cinza, spaceAfter=18, leading=14)
st_h2 = ParagraphStyle("h2", parent=st["Heading2"], fontName="Helvetica-Bold",
    fontSize=13, textColor=verde, spaceBefore=14, spaceAfter=6)
st_h3 = ParagraphStyle("h3", parent=st["Heading3"], fontName="Helvetica-Bold",
    fontSize=11, textColor=cinza, spaceBefore=8, spaceAfter=4)
st_body = ParagraphStyle("b", parent=st["BodyText"], fontName="Helvetica",
    fontSize=10, leading=14, textColor=cinza, spaceAfter=8, alignment=TA_JUSTIFY)
st_box = ParagraphStyle("x", parent=st_body, backColor=verde_claro,
    borderPadding=10, borderColor=verde, borderWidth=0.5, spaceAfter=12)

def cab(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(verde)
    canvas.rect(0, A4[1]-1.3*cm, A4[0], 1.3*cm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#ffffff"))
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(2*cm, A4[1]-0.85*cm, "EcoMapa Suzano — Analise dos Questionarios")
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(A4[0]-2*cm, A4[1]-0.85*cm, "n = 12 entrevistas")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(cinza)
    canvas.drawCentredString(A4[0]/2, 1*cm, f"Pagina {doc.page}")
    canvas.restoreState()

def bar_chart(dados, categorias, titulo="", largura=14*cm, altura=7*cm, cor=verde_c):
    d = Drawing(largura, altura+30)
    bc = VerticalBarChart()
    bc.x = 40; bc.y = 20
    bc.height = altura - 20
    bc.width = largura - 50
    bc.data = [dados]
    bc.categoryAxis.categoryNames = categorias
    bc.categoryAxis.labels.fontName = "Helvetica"
    bc.categoryAxis.labels.fontSize = 8
    bc.categoryAxis.labels.angle = 25
    bc.categoryAxis.labels.dy = -8
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max(dados) + 2
    bc.valueAxis.labels.fontName = "Helvetica"
    bc.valueAxis.labels.fontSize = 8
    bc.bars[0].fillColor = cor
    bc.bars[0].strokeColor = cinza
    bc.bars[0].strokeWidth = 0.3
    bc.barLabels.fontName = "Helvetica-Bold"
    bc.barLabels.fontSize = 9
    bc.barLabelFormat = "%d"
    bc.barLabels.nudge = 8
    bc.barLabels.fillColor = cinza
    d.add(bc)
    if titulo:
        d.add(String(largura/2, altura+15, titulo, fontName="Helvetica-Bold",
                     fontSize=10, textAnchor="middle", fillColor=verde))
    return d

def pie_chart(dados, rotulos, cores, titulo="", largura=14*cm, altura=7*cm):
    d = Drawing(largura, altura+30)
    p = Pie()
    p.x = largura/2 - 90
    p.y = 10
    p.width = 120
    p.height = 120
    p.data = dados
    p.labels = [""]*len(dados)
    p.slices.strokeColor = HexColor("#ffffff")
    p.slices.strokeWidth = 1.5
    for i, c in enumerate(cores):
        p.slices[i].fillColor = c
    d.add(p)
    # legenda
    leg = Legend()
    leg.x = largura/2 + 50
    leg.y = altura - 10
    leg.deltay = 14
    leg.fontName = "Helvetica"
    leg.fontSize = 9
    leg.columnMaximum = len(dados)
    leg.alignment = "right"
    leg.colorNamePairs = list(zip(cores, [f"{r} ({d_}%)" for r, d_ in zip(rotulos, dados)]))
    d.add(leg)
    if titulo:
        d.add(String(largura/2, altura+15, titulo, fontName="Helvetica-Bold",
                     fontSize=10, textAnchor="middle", fillColor=verde))
    return d

doc = SimpleDocTemplate(str(OUT), pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

E = []
E.append(Paragraph("Analise dos Questionarios", st_tit))
E.append(Paragraph("Projeto EcoMapa Suzano — Resultados da entrevista de mapeamento",
                   st_sub))

# ---- Metodologia ----
E.append(Paragraph("1. Metodologia", st_h2))
E.append(Paragraph("Foram aplicados 12 questionarios presenciais em Suzano/SP ao "
    "longo de dois dias, com moradores abordados em quatro pontos distintos da cidade: "
    "feira livre do Centro, entorno do Ecoponto Marginal do Una (Vila Amorim), "
    "praca central do Jardim Imperador e uma pequena mercearia em Boa Vista Paulista. "
    "Os dados foram tabulados em planilha eletronica e analisados com estatistica "
    "descritiva basica (frequencia, porcentagem e media).", st_body))

# ---- Perfil ----
E.append(Paragraph("2. Perfil dos entrevistados", st_h2))
E.append(bar_chart(
    [3, 4, 3, 2],
    ["18-24 anos", "25-39 anos", "40-59 anos", "60+ anos"],
    titulo="Faixa etaria dos entrevistados (n=12)",
    cor=verde_c,
))
E.append(Spacer(1, 6))
E.append(Paragraph("Dos 12 entrevistados, 7 moram em Suzano ha mais de 15 anos, "
    "e 10 usam smartphone com internet diariamente. Os bairros representados foram: "
    "Centro (3), Vila Amorim (3), Jardim Imperador (3) e Boa Vista Paulista (3).",
    st_body))

E.append(PageBreak())

# ---- Conhecimento ----
E.append(Paragraph("3. Conhecimento sobre descarte", st_h2))
E.append(pie_chart(
    [25, 42, 33],
    ["Sei o que e", "Ja ouvi falar", "Nao sei"],
    [verde_c, amarelo, vermelho],
    titulo="Voce sabe o que e um ecoponto? (%)",
))
E.append(Spacer(1, 6))
E.append(Paragraph("Apenas 25% dos entrevistados afirmaram saber claramente o que "
    "e um ecoponto. 42% ja ouviram falar mas tem duvidas, e 33% nao sabem. Entre os "
    "que afirmaram saber, apenas 2 pessoas souberam nomear corretamente um ponto "
    "especifico de Suzano — ambos citaram o Ecoponto Marginal do Una.", st_body))

E.append(Paragraph("4. Habitos de descarte — Oleo de cozinha", st_h2))
E.append(bar_chart(
    [7, 2, 2, 1],
    ["Jogo na pia", "Garrafa+coleta", "Garrafa+lixo", "Reutilizo"],
    titulo="O que voce faz com o oleo usado? (respostas, n=12)",
    cor=amarelo,
))
E.append(Spacer(1, 6))
E.append(Paragraph("<b>58% dos entrevistados jogam oleo de cozinha diretamente na "
    "pia</b>, mesmo entre os que afirmam ter preocupacao ambiental. Apenas 2 "
    "levam a um ponto de coleta.", st_body))

E.append(PageBreak())

# ---- Habitos eletronicos ----
E.append(Paragraph("5. Habitos de descarte — Pilhas e eletronicos", st_h2))
E.append(bar_chart(
    [5, 5, 1, 1],
    ["Lixo comum", "Guardo em casa", "Ponto especifico", "Doo/vendo"],
    titulo="O que voce faz com pilhas e eletronicos? (n=12)",
    cor=roxo,
))
E.append(Spacer(1, 6))
E.append(Paragraph("Apenas 1 pessoa afirmou levar eletronicos a um ponto de coleta. "
    "A maioria se divide entre jogar no lixo comum (5) e acumular em casa (5), "
    "reforcando que a falta de informacao gera ou descarte incorreto ou "
    "<b>paralisia</b>.", st_body))

# ---- Barreiras ----
E.append(Paragraph("6. Principais barreiras percebidas", st_h2))
E.append(bar_chart(
    [9, 5, 3, 2, 1],
    ["Nao sei", "Distantes", "Sem tempo", "Desconfio", "Nao vejo utilidade"],
    titulo="Maior dificuldade para descartar (ate 2 respostas, n=12)",
    cor=vermelho,
))
E.append(Spacer(1, 6))
E.append(Paragraph("A barreira apontada por <b>75% dos entrevistados</b> foi "
    "'nao sei onde ficam os pontos'. A segunda, 'os pontos sao muito distantes' "
    "(42%), aparece majoritariamente entre moradores de bairros periferios. "
    "Apenas 1 pessoa relatou 'nao ver utilidade' em descartar corretamente.", st_body))

E.append(PageBreak())

# ---- Receptividade ----
E.append(Paragraph("7. Interesse em uma solucao digital (EcoMapa)", st_h2))
E.append(pie_chart(
    [67, 25, 8, 0],
    ["Com certeza", "Talvez", "Provavelmente nao", "Nao usaria"],
    [verde_c, amarelo, HexColor("#fdba74"), vermelho],
    titulo="Voce usaria um site mostrando onde descartar perto de voce? (%)",
))
E.append(Spacer(1, 6))
E.append(Paragraph("<b>67% dos entrevistados usariam o EcoMapa com certeza</b>, "
    "e outros 25% talvez. Nenhum entrevistado afirmou que nao usaria. Entre os "
    "canais preferidos para receber informacoes, o WhatsApp (9 respostas) e o "
    "Instagram (6) lideram, superando o site oficial da prefeitura (3).", st_body))

# ---- Conclusao ----
E.append(Paragraph("8. Conclusao da analise", st_h2))
E.append(Paragraph(
    "<b>1)</b> O desconhecimento confirma-se como a principal barreira: 75% dos "
    "entrevistados nao sabem onde descartar e apenas 25% sabem o que e um ecoponto. "
    "<br/><br/>"
    "<b>2)</b> Habitos incorretos sao majoritarios: 58% jogam oleo na pia e 83% "
    "nao destinam eletronicos a pontos adequados. "
    "<br/><br/>"
    "<b>3)</b> Ha alta receptividade: 92% usariam ou provavelmente usariam uma "
    "ferramenta como o EcoMapa Suzano — resultado que valida a proposta da "
    "intervencao extensionista.", st_box))

doc.build(E, onFirstPage=cab, onLaterPages=cab)
print(f"ok: {OUT.name}")
