# -*- coding: utf-8 -*-
"""Baixa as 3 fotos do Pexels para a exibição do documentário."""
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent.parent / "fotos_exibicao"
OUT.mkdir(exist_ok=True)

# URLs diretas das imagens (CDN do Pexels, versão large)
fotos = [
    {
        "nome": "01_descarte_irregular.jpg",
        "url": "https://images.pexels.com/photos/22485721/pexels-photo-22485721.jpeg?auto=compress&cs=tinysrgb&w=1600",
        "credito": "Foto: Pexels (uso livre)"
    },
    {
        "nome": "02_cooperativa_reciclagem.jpg",
        "url": "https://images.pexels.com/photos/39839890/pexels-photo-39839890.jpeg?auto=compress&cs=tinysrgb&w=1600",
        "credito": "Foto: Pexels (uso livre)"
    },
    {
        "nome": "03_celular_mapa.jpg",
        "url": "https://images.pexels.com/photos/4542998/pexels-photo-4542998.jpeg?auto=compress&cs=tinysrgb&w=1600",
        "credito": "Foto: Pexels (uso livre)"
    },
]

headers = {"User-Agent": "Mozilla/5.0"}

for f in fotos:
    dest = OUT / f["nome"]
    req = urllib.request.Request(f["url"], headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as out:
            out.write(r.read())
        print(f"ok: {f['nome']} ({dest.stat().st_size // 1024} KB)")
    except Exception as e:
        print(f"erro: {f['nome']} -> {e}")

print(f"\nFotos salvas em: {OUT}")
