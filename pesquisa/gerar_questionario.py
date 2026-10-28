# -*- coding: utf-8 -*-
"""Gera o questionario de mapeamento em PDF profissional."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from pathlib import Path

OUT = Path(__file__).parent / "04_Questionario_Mapeamento_EcoMapa_Suzano.pdf"

verde = HexColor("#166534")
verde_claro = HexColor("#f0fdf4")
cinza = HexColor("#334155")
cinza_claro = HexColor("#f1f5f9")
amarelo_claro = HexColor("#fef3c7")

styles = getSampleStyleSheet()

st_titulo = ParagraphStyle("t", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=20, textColor=verde, spaceAfter=4, leading=24)
st_sub = ParagraphStyle("s", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10.5, textColor=cinza, spaceAfter=18, leading=14)
st_h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
    fontSize=13, textColor=verde, spaceBefore=12, spaceAfter=6)
st_body = ParagraphStyle("b", parent=styles["BodyText"], fontName="Helvetica",
    fontSize=10, leading=14, textColor=cinza, spaceAfter=6, alignment=TA_JUSTIFY)
st_q = ParagraphStyle("q", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=10.5, textColor=cinza, spaceBefore=10, spaceAfter=4, leading=14)
st_opt = ParagraphStyle("o", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, textColor=cinza, leading=14, leftIndent=16, spaceAfter=2)
st_linha = ParagraphStyle("l", parent=styles["Normal"], fontName="Helvetica",
    fontSize=10, textColor=cinza, leading=14, spaceAfter=4)
st_info = ParagraphStyle("i", parent=st_body, backColor=verde_claro,
    borderPadding=10, borderColor=verde, borderWidth=0.5, spaceAfter=12)

def cab(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(verde)
    canvas.rect(0, A4[1]-1.3*cm, A4[0], 1.3*cm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#ffffff"))
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(2*cm, A4[1]-0.85*cm, "EcoMapa Suzano — Questionario de Mapeamento")
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(A4[0]-2*cm, A4[1]-0.85*cm, "Projeto de Extensao")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(cinza)
    canvas.drawCentredString(A4[0]/2, 1*cm, f"Pagina {doc.page}")
    canvas.restoreState()

def opt(letra, texto):
    return Paragraph(f"( ) <b>{letra})</b> {texto}", st_opt)

def linhas(n=3):
    return Paragraph("_" * 90 + "<br/>" * (n-1) + ("_" * 90 + "<br/>") * (n-1), st_linha)

def escala_likert():
    data = [["Afirmacao", "1", "2", "3", "4", "5"]]
    afirmacoes = [
        "Eu sei onde ficam os ecopontos de Suzano.",
        "Eu descarto corretamente oleo de cozinha.",
        "Eu descarto corretamente pilhas e baterias.",
        "Eu descarto corretamente eletronicos antigos.",
        "Eu descarto corretamente medicamentos vencidos.",
        "A Prefeitura divulga bem onde descartar.",
        "Eu usaria um site que mostre onde descartar perto de mim.",
    ]
    for a in afirmacoes:
        data.append([a, "( )", "( )", "( )", "( )", "( )"])
    t = Table(data, colWidths=[9*cm, 1.3*cm, 1.3*cm, 1.3*cm, 1.3*cm, 1.3*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), verde),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), cinza_claro]),
        ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#cbd5e1")),
    ]))
    return t

doc = SimpleDocTemplate(str(OUT), pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

E = []
E.append(Paragraph("Questionario de Mapeamento", st_titulo))
E.append(Paragraph("Projeto EcoMapa Suzano — Descarte correto de residuos em Suzano/SP",
                   st_sub))

# Introducao
E.append(Paragraph("Ola! Meu nome e Rafael Calixto de Oliveira, sou aluno de Ciencia da "
    "Computacao e estou desenvolvendo um projeto de extensao universitaria chamado "
    "EcoMapa Suzano, que pretende criar um site gratuito mostrando onde descartar "
    "corretamente diferentes tipos de residuos na cidade. "
    "Este questionario leva cerca de 5 minutos. As respostas sao anonimas e serao "
    "usadas apenas para a pesquisa academica. Obrigado por participar!",
    st_info))

# =============================================================
# SECAO 1 - PERFIL
# =============================================================
E.append(Paragraph("SECAO 1 — Perfil do entrevistado", st_h2))

E.append(Paragraph("1. Em qual bairro de Suzano voce mora?", st_q))
E.append(linhas(1))

E.append(Paragraph("2. Qual sua faixa etaria?", st_q))
E.append(opt("a", "18 a 24 anos"))
E.append(opt("b", "25 a 39 anos"))
E.append(opt("c", "40 a 59 anos"))
E.append(opt("d", "60 anos ou mais"))

E.append(Paragraph("3. Ha quanto tempo voce mora em Suzano?", st_q))
E.append(opt("a", "Menos de 1 ano"))
E.append(opt("b", "1 a 5 anos"))
E.append(opt("c", "6 a 15 anos"))
E.append(opt("d", "Mais de 15 anos"))

E.append(Paragraph("4. Voce usa smartphone com internet no dia a dia?", st_q))
E.append(opt("a", "Sim, todos os dias"))
E.append(opt("b", "Sim, com frequencia"))
E.append(opt("c", "As vezes"))
E.append(opt("d", "Nao uso"))

E.append(PageBreak())

# =============================================================
# SECAO 2 - CONHECIMENTO
# =============================================================
E.append(Paragraph("SECAO 2 — Conhecimento sobre descarte", st_h2))

E.append(Paragraph("5. Voce sabe o que e um ecoponto?", st_q))
E.append(opt("a", "Sim, sei exatamente o que e"))
E.append(opt("b", "Ja ouvi falar, mas nao tenho certeza"))
E.append(opt("c", "Nao sei"))

E.append(Paragraph("6. Voce conhece algum ecoponto ou ponto de coleta em Suzano? "
                   "Se sim, qual(is)?", st_q))
E.append(linhas(2))

E.append(Paragraph("7. Onde voce buscaria informacao se precisasse descartar algo "
                   "que nao sabe onde levar? (pode marcar mais de uma)", st_q))
E.append(opt("a", "Google / internet"))
E.append(opt("b", "Site da Prefeitura"))
E.append(opt("c", "Redes sociais (Facebook, Instagram)"))
E.append(opt("d", "Perguntaria a um vizinho ou familiar"))
E.append(opt("e", "Nao buscaria — jogaria no lixo comum"))

# =============================================================
# SECAO 3 - HABITOS
# =============================================================
E.append(Paragraph("SECAO 3 — Habitos de descarte", st_h2))

E.append(Paragraph("8. O que voce faz com o <b>oleo de cozinha</b> usado?", st_q))
E.append(opt("a", "Jogo na pia / vaso sanitario"))
E.append(opt("b", "Guardo em garrafa e levo a um ponto de coleta"))
E.append(opt("c", "Guardo em garrafa e jogo no lixo comum"))
E.append(opt("d", "Reutilizo (sabao, por exemplo)"))
E.append(opt("e", "Outro:_______________________________________________________"))

E.append(Paragraph("9. O que voce faz com <b>pilhas, baterias e eletronicos</b> velhos?", st_q))
E.append(opt("a", "Jogo no lixo comum"))
E.append(opt("b", "Guardo em casa (nao sei onde descartar)"))
E.append(opt("c", "Levo a um ponto de coleta especifico"))
E.append(opt("d", "Doo / vendo para quem reusa"))
E.append(opt("e", "Outro:_______________________________________________________"))

E.append(Paragraph("10. O que voce faz com <b>medicamentos vencidos</b>?", st_q))
E.append(opt("a", "Jogo no lixo comum"))
E.append(opt("b", "Jogo no vaso sanitario"))
E.append(opt("c", "Levo a uma farmacia / UBS"))
E.append(opt("d", "Guardo em casa"))
E.append(opt("e", "Outro:_______________________________________________________"))

E.append(Paragraph("11. O que voce faz com <b>entulho</b> de pequenas reformas "
                   "ou moveis velhos?", st_q))
E.append(opt("a", "Contrato caminhao particular"))
E.append(opt("b", "Levo a um ecoponto municipal"))
E.append(opt("c", "Deixo na calcada / terreno baldio"))
E.append(opt("d", "Doo / dou para alguem"))
E.append(opt("e", "Outro:_______________________________________________________"))

E.append(PageBreak())

# =============================================================
# SECAO 4 - LIKERT
# =============================================================
E.append(Paragraph("SECAO 4 — Percepcoes", st_h2))
E.append(Paragraph("Marque com um X: 1 = Discordo totalmente | 2 = Discordo | "
    "3 = Nem concordo nem discordo | 4 = Concordo | 5 = Concordo totalmente", st_body))
E.append(escala_likert())
E.append(Spacer(1, 10))

# =============================================================
# SECAO 5 - BARREIRAS
# =============================================================
E.append(Paragraph("SECAO 5 — Barreiras", st_h2))

E.append(Paragraph("12. Qual a maior dificuldade que voce enfrenta para descartar "
                   "residuos corretamente? (marque ate 2)", st_q))
E.append(opt("a", "Nao sei onde ficam os pontos"))
E.append(opt("b", "Os pontos sao muito distantes"))
E.append(opt("c", "Nao tenho tempo"))
E.append(opt("d", "Nao confio no destino final"))
E.append(opt("e", "Nao vejo necessidade"))
E.append(opt("f", "Outro:_______________________________________________________"))

# =============================================================
# SECAO 6 - RECEPTIVIDADE
# =============================================================
E.append(Paragraph("SECAO 6 — Interesse em uma solucao digital", st_h2))

E.append(Paragraph("13. Voce usaria um site gratuito que, em poucos cliques, "
                   "mostrasse o ponto de descarte mais proximo da sua casa "
                   "para cada tipo de residuo?", st_q))
E.append(opt("a", "Com certeza usaria"))
E.append(opt("b", "Talvez usaria"))
E.append(opt("c", "Provavelmente nao usaria"))
E.append(opt("d", "Nao usaria"))

E.append(Paragraph("14. Como voce gostaria de ser avisado sobre pontos de descarte? "
                   "(pode marcar mais de uma)", st_q))
E.append(opt("a", "WhatsApp"))
E.append(opt("b", "Instagram / Facebook"))
E.append(opt("c", "Site da Prefeitura"))
E.append(opt("d", "Cartaz ou folder em locais publicos"))
E.append(opt("e", "QR Code em comercios"))

E.append(Paragraph("15. (Aberta) O que mais te motivaria a descartar corretamente "
                   "o lixo de casa?", st_q))
E.append(linhas(3))

E.append(Paragraph("16. (Aberta) Alguma sugestao para o projeto EcoMapa Suzano?", st_q))
E.append(linhas(3))

E.append(Spacer(1, 20))
E.append(Paragraph("Obrigado pela sua participacao! As respostas vao ajudar a "
    "construir uma ferramenta util para toda a cidade.", st_info))

doc.build(E, onFirstPage=cab, onLaterPages=cab)
print(f"ok: {OUT.name}")
