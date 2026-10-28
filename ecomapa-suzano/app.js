// ============================================================
// EcoMapa Suzano - app principal
// ============================================================

const TIPOS = {
  reciclaveis:  { label: "Recicláveis",  cor: "#22c55e", icone: "♻️" },
  oleo:         { label: "Óleo de cozinha", cor: "#eab308", icone: "🛢️" },
  eletronicos:  { label: "Eletrônicos",  cor: "#ef4444", icone: "🔌" },
  pilhas:       { label: "Pilhas e baterias", cor: "#a855f7", icone: "🔋" },
  medicamentos: { label: "Medicamentos", cor: "#0ea5e9", icone: "💊" },
  entulho:      { label: "Entulho",      cor: "#a16207", icone: "🧱" },
  podas:        { label: "Podas e galhos", cor: "#15803d", icone: "🌿" },
};

const SUZANO_CENTRO = [-23.5425, -46.3108];

let mapa;
let pontos = [];
let marcadores = {};               // id -> L.marker
let filtrosAtivos = new Set();     // vazio = mostrar todos
let marcadorUsuario = null;

// ---------------- Inicialização ----------------

document.addEventListener("DOMContentLoaded", () => {
  inicializarMapa();
  renderizarChips();
  pontos = window.PONTOS_DESCARTE || [];
  renderizarListaEMarcadores();
  configurarBotoes();
});

function inicializarMapa() {
  mapa = L.map("map", {
    zoomControl: true,
    scrollWheelZoom: true,
  }).setView(SUZANO_CENTRO, 13);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(mapa);
}

// ---------------- Filtros (chips) ----------------

function renderizarChips() {
  const container = document.getElementById("chips");
  container.innerHTML = "";
  Object.entries(TIPOS).forEach(([chave, info]) => {
    const chip = document.createElement("button");
    chip.className = "chip";
    chip.dataset.tipo = chave;
    chip.innerHTML = `<span class="dot" style="background:${info.cor}"></span> ${info.icone} ${info.label}`;
    chip.addEventListener("click", () => alternarFiltro(chave, chip));
    container.appendChild(chip);
  });
}

function alternarFiltro(tipo, chipEl) {
  if (filtrosAtivos.has(tipo)) {
    filtrosAtivos.delete(tipo);
    chipEl.classList.remove("ativo");
  } else {
    filtrosAtivos.add(tipo);
    chipEl.classList.add("ativo");
  }
  renderizarListaEMarcadores();
}

function limparFiltros() {
  filtrosAtivos.clear();
  document.querySelectorAll(".chip").forEach(c => c.classList.remove("ativo"));
  renderizarListaEMarcadores();
}

// ---------------- Lista + marcadores ----------------

function pontoCorresponde(ponto) {
  if (filtrosAtivos.size === 0) return true;
  return ponto.tipos.some(t => filtrosAtivos.has(t));
}

function renderizarListaEMarcadores() {
  // Limpa marcadores anteriores
  Object.values(marcadores).forEach(m => mapa.removeLayer(m));
  marcadores = {};

  const visiveis = pontos.filter(pontoCorresponde);

  // Lista lateral
  const lista = document.getElementById("listaPontos");
  lista.innerHTML = "";
  document.getElementById("contador").textContent = visiveis.length;

  if (visiveis.length === 0) {
    lista.innerHTML = `<li style="color:var(--cinza-500);font-size:.85rem;padding:1rem 0;">
      Nenhum ponto encontrado com os filtros selecionados.
    </li>`;
    return;
  }

  visiveis.forEach(ponto => {
    // Card na lista
    const li = document.createElement("li");
    li.className = "ponto-card";
    li.innerHTML = `
      <h3>${ponto.nome}</h3>
      <p class="end">${ponto.endereco}</p>
      <div class="tags">
        ${ponto.tipos.map(t => `
          <span class="tag">
            <span class="dot" style="background:${TIPOS[t]?.cor || '#999'}"></span>
            ${TIPOS[t]?.label || t}
          </span>`).join("")}
      </div>
    `;
    li.addEventListener("click", () => focarPonto(ponto));
    lista.appendChild(li);

    // Marcador no mapa
    const cor = TIPOS[ponto.tipos[0]]?.cor || "#22c55e";
    const icone = TIPOS[ponto.tipos[0]]?.icone || "📍";
    const marker = L.marker([ponto.lat, ponto.lng], {
      icon: criarIcone(cor, icone),
    });
    marker.bindPopup(construirPopup(ponto), { maxWidth: 300 });
    marker.addTo(mapa);
    marcadores[ponto.id] = marker;
  });
}

function criarIcone(cor, emoji) {
  return L.divIcon({
    className: "",
    html: `
      <div class="marker-pin" style="--pin-cor:${cor}">
        <style>.marker-pin::before{background:${cor} !important;}</style>
        <span>${emoji}</span>
      </div>`,
    iconSize: [32, 42],
    iconAnchor: [16, 42],
    popupAnchor: [0, -40],
  });
}

function construirPopup(ponto) {
  return `
    <div class="popup">
      <h3>${ponto.nome}</h3>
      <p><strong>📍</strong> ${ponto.endereco}</p>
      <p><strong>🕒</strong> ${ponto.horario}</p>
      <p><strong>📞</strong> ${ponto.telefone}</p>
      <div class="popup-tags">
        ${ponto.tipos.map(t => `
          <span class="tag">
            <span class="dot" style="background:${TIPOS[t]?.cor || '#999'}"></span>
            ${TIPOS[t]?.label || t}
          </span>`).join("")}
      </div>
      ${ponto.observacao ? `<p class="obs">💡 ${ponto.observacao}</p>` : ""}
    </div>`;
}

function focarPonto(ponto) {
  mapa.setView([ponto.lat, ponto.lng], 16, { animate: true });
  const m = marcadores[ponto.id];
  if (m) m.openPopup();
}

// ---------------- Botões ----------------

function configurarBotoes() {
  document.getElementById("btnTodos").addEventListener("click", () => {
    limparFiltros();
    mapa.setView(SUZANO_CENTRO, 13);
  });

  document.getElementById("btnLimpar").addEventListener("click", limparFiltros);

  document.getElementById("btnLocalizar").addEventListener("click", localizarUsuario);
}

function localizarUsuario() {
  if (!("geolocation" in navigator)) {
    alert("Seu navegador não suporta geolocalização.");
    return;
  }
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const { latitude, longitude } = pos.coords;
      if (marcadorUsuario) mapa.removeLayer(marcadorUsuario);
      marcadorUsuario = L.circleMarker([latitude, longitude], {
        radius: 10,
        color: "#1d4ed8",
        fillColor: "#3b82f6",
        fillOpacity: 0.6,
        weight: 3,
      }).addTo(mapa).bindPopup("Você está aqui");
      mapa.setView([latitude, longitude], 14);
    },
    (err) => {
      alert("Não foi possível obter sua localização: " + err.message);
    }
  );
}
