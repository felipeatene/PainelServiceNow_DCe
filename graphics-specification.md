# Especificação de Gráficos — Painel DC-e

**Data:** 26/03/2026  
**Versão:** 1.0  
**Tecnologia:** SVG Inline com CSS Animations  
**Suporte:** Fallback estático para ambientes restritivos

---

## 1. Visão Geral dos 3 Gráficos

| Gráfico | Objetivo | Dados | Interação | Responsivo |
|---------|----------|-------|-----------|-----------|
| **Sankey** | Visualizar fluxo de camadas (Âncora → Intenção → Contexto → Complemento) | Contadores por camada | Hover em paths | SVG viewBox |
| **Heatmap** | Matriz: categorias x status (Processando, Fila, Concluído, Bloqueado) | Grid 9x4 com valores | Tooltip on hover | CSS Grid + Scale |
| **Anéis de Progresso** | KPIs resumidos (total, sucesso %, falha %, pendente %) | 4 anéis + label central | Animação ao load | SVG viewBox |

---

## 2. Gráfico 1: Sankey Diagram (Fluxo de Camadas)

### 2.1 Objetivo

Visualizar a jornada de classificação: quantos itens passam por cada camada e qual categoria final é atribuída.

```
ENTRADA:
┌──────────────────┐
│  245 itens       │  ← Camada 1: Âncora
│  com "dce"       │     (245 encontrados)
└──────────────────┘
        ↓
┌──────────────────────────────────────────┐
│  Camada 2: Intenção                      │
│  ├── 189 Emissão / Ativação              │  ← Maior fluxo
│  ├── 44 Reemissão                        │
│  ├── 12 Cancelamento                     │
│  └── [outros]                            │
└──────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────┐
│  Camada 3: Contexto (se sem intenção)     │
│  ├── 56 CNPJ/PDI                         │
│  ├── 23 VE Leves                         │
│  └── [outros]                            │
└──────────────────────────────────────────┘
        ↓
┌──────────────────────────────────────────┐
│  Camada 4: Complemento (flags)            │
│  ├── 34 tributário                       │
│  ├── 21 contingência                     │
│  └── [outros]                            │
└──────────────────────────────────────────┘
```

### 2.2 Estrutura SVG

```html
<svg class="dce-sankey" viewBox="0 0 1000 400" preserveAspectRatio="xMidYMid meet">
  
  <!-- Coluna 1: Âncora -->
  <g class="sankey-column column-1" data-layer="anchor">
    <rect x="20" y="150" width="80" height="100" class="sankey-node" data-value="245"/>
    <text x="60" y="205" class="sankey-label">245</text>
    <text x="60" y="225" class="sankey-label-sm">DC-e</text>
  </g>
  
  <!-- Coluna 2: Intenção -->
  <g class="sankey-column column-2" data-layer="intention">
    <rect x="200" y="50" width="80" height="65" class="sankey-node intention-emissao" data-value="189"/>
    <text x="240" y="88" class="sankey-label">189</text>
    
    <rect x="200" y="130" width="80" height="35" class="sankey-node intention-reemissao" data-value="44"/>
    <text x="240" y="153" class="sankey-label">44</text>
    
    <rect x="200" y="175" width="80" height="20" class="sankey-node intention-cancelamento" data-value="12"/>
    <text x="240" y="186" class="sankey-label">12</text>
  </g>
  
  <!-- Conexões (paths) -->
  <g class="sankey-connections">
    <path class="sankey-flow flow-emissao" 
          d="M 100 200 L 200 88 Z" 
          data-value="189" 
          stroke="#0066cc" 
          fill="rgba(0, 102, 204, 0.3)"/>
    
    <path class="sankey-flow flow-reemissao" 
          d="M 100 200 L 200 153 Z" 
          data-value="44" 
          stroke="#FF5722" 
          fill="rgba(255, 87, 34, 0.3)"/>
    
    <!-- ... mais paths ... -->
  </g>
  
  <!-- Coluna 3 e 4 com mesma estrutura -->
  <!-- ... -->
  
</svg>

<style>
  .dce-sankey {
    width: 100%;
    height: auto;
    min-height: 300px;
    max-width: 1000px;
  }
  
  .sankey-node {
    fill: white;
    stroke: #e0e0e0;
    stroke-width: 2;
    transition: fill 0.3s ease;
  }
  
  .sankey-node:hover {
    fill: rgba(0, 102, 204, 0.1);
    stroke: #0066cc;
    stroke-width: 3;
  }
  
  .sankey-flow {
    opacity: 0.6;
    transition: all 0.3s ease;
  }
  
  .sankey-flow:hover {
    opacity: 1;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  }
  
  .sankey-label {
    font-size: 1.25rem;
    font-weight: 600;
    text-anchor: middle;
    fill: #212121;
  }
  
  .sankey-label-sm {
    font-size: 0.75rem;
    font-weight: 400;
    text-anchor: middle;
    fill: #666;
    text-transform: uppercase;
  }
  
  /* Animação ao carregar */
  @keyframes sankey-flow-pulse {
    0% { opacity: 0.3; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
  }
  
  .sankey-flow {
    animation: sankey-flow-pulse 2s ease-in-out infinite;
  }
</style>
```

### 2.3 Dados Esperados (JSON)

```json
{
  "sankey": {
    "columns": [
      {
        "layer": "anchor",
        "name": "Âncora",
        "total": 245,
        "items": [
          {
            "key": "dce",
            "label": "dce, dc-e, etc.",
            "count": 245,
            "percentage": 100
          }
        ]
      },
      {
        "layer": "intention",
        "name": "Intenção",
        "total": 245,
        "items": [
          {
            "key": "emissao",
            "label": "Emissão / Ativação",
            "count": 189,
            "percentage": 77,
            "color": "#0066cc"
          },
          {
            "key": "reemissao",
            "label": "Reemissão",
            "count": 44,
            "percentage": 18,
            "color": "#FF5722"
          },
          {
            "key": "cancelamento",
            "label": "Cancelamento",
            "count": 12,
            "percentage": 5,
            "color": "#F44336"
          }
        ]
      },
      {
        "layer": "context",
        "name": "Contexto",
        "total": 56,
        "items": [/*...*/]
      },
      {
        "layer": "complement",
        "name": "Complemento",
        "total": 78,
        "items": [/*...*/]
      }
    ],
    "connections": [
      {
        "source_layer": "anchor",
        "source_key": "dce",
        "target_layer": "intention",
        "target_key": "emissao",
        "flow": 189,
        "color": "#0066cc"
      }
      /*...*/
    ]
  }
}
```

### 2.4 Responsividade

- **Mobile** (< 640px): Altura reduzida (200px), rotula abrevisada
- **Desktop** (>= 1024px): Altura normal (400px), rótulos completos
- Sempre usar `viewBox` + `preserveAspectRatio` para scaling automático

### 2.5 Fallback Estático (Sem SVG)

```html
<div class="dce-sankey-fallback">
  <h3>Fluxo de Classificação</h3>
  <div class="fallback-flow">
    <div class="flow-step">
      <span class="step-label">Âncora</span>
      <span class="step-count">245</span>
    </div>
    <span class="flow-arrow">→</span>
    <div class="flow-step">
      <span class="step-label">Intenção</span>
      <span class="step-count">189 Emissão</span>
    </div>
    <!-- ... -->
  </div>
</div>

<style>
  .dce-sankey-fallback {
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
  }
  
  .fallback-flow {
    display: flex;
    align-items: center;
    gap: 1rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .flow-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 100px;
    padding: 0.75rem;
    background: white;
    border-radius: 4px;
    border-left: 4px solid #0066cc;
  }
  
  .flow-arrow {
    font-size: 1.5rem;
    color: #999;
    flex-shrink: 0;
  }
</style>
```

---

## 3. Gráfico 2: Heatmap (Categorias × Status)

### 3.1 Objetivo

Matriz visual mostrando distribuição de categorias por status (Processando, Fila, Concluído, Bloqueado).

```
           Processando  Fila   Concluído  Bloqueado
Emissão       ████       ██       ②         —
Reemissão     ②          ④        ⑩         —
CNPJ/PDI      —          ④        ⑩         ②
TraaS         ③          ②        ④         —
Pesados       —          —        ③         —

Cor:  🟢 verde (alto) → 🟡 amarelo (médio) → 🔴 vermelho (baixo)
```

### 3.2 Estrutura SVG

```html
<svg class="dce-heatmap" viewBox="0 0 600 400">
  
  <!-- Eixo Y (Categorias) -->
  <g class="heatmap-labels-y">
    <text x="10" y="30">Emissão</text>
    <text x="10" y="100">Reemissão</text>
    <text x="10" y="170">CNPJ/PDI</text>
    <text x="10" y="240">TraaS</text>
    <text x="10" y="310">Pesados</text>
  </g>
  
  <!-- Eixo X (Status) -->
  <g class="heatmap-labels-x">
    <text x="130" y="15" text-anchor="middle">Processando</text>
    <text x="230" y="15" text-anchor="middle">Fila</text>
    <text x="330" y="15" text-anchor="middle">Concluído</text>
    <text x="430" y="15" text-anchor="middle">Bloqueado</text>
  </g>
  
  <!-- Grid de células -->
  <g class="heatmap-cells">
    <!-- Linha 1: Emissão -->
    <rect class="heatmap-cell cell-high" x="100" y="20" width="80" height="50" 
          data-value="89" data-category="emissao" data-status="processando"/>
    <text class="heatmap-value" x="140" y="50">89</text>
    
    <rect class="heatmap-cell cell-medium" x="190" y="20" width="80" height="50" 
          data-value="45" data-category="emissao" data-status="fila"/>
    <text class="heatmap-value" x="230" y="50">45</text>
    
    <rect class="heatmap-cell cell-low" x="280" y="20" width="80" height="50" 
          data-value="12" data-category="emissao" data-status="concluido"/>
    <text class="heatmap-value" x="320" y="50">12</text>
    
    <!-- ... mais células ... -->
  </g>
  
</svg>

<style>
  .dce-heatmap {
    width: 100%;
    height: auto;
    max-width: 600px;
  }
  
  .heatmap-cell {
    stroke: white;
    stroke-width: 2;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .cell-high {
    fill: #4CAF50;  /* Verde */
  }
  
  .cell-medium {
    fill: #FF9800;  /* Laranja */
  }
  
  .cell-low {
    fill: #F44336;  /* Vermelho */
  }
  
  .cell-empty {
    fill: #f0f0f0;  /* Cinza claro */
  }
  
  .heatmap-cell:hover {
    stroke: #212121;
    stroke-width: 3;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  }
  
  .heatmap-value {
    fill: white;
    font-size: 1.25rem;
    font-weight: 600;
    text-anchor: middle;
    dominant-baseline: middle;
  }
  
  .heatmap-labels-y text,
  .heatmap-labels-x text {
    font-size: 0.9rem;
    font-weight: 500;
    fill: #212121;
  }
</style>
```

### 3.3 Dados Esperados

```json
{
  "heatmap": {
    "categories": ["Emissão", "Reemissão", "CNPJ/PDI", "TraaS", "Pesados"],
    "statuses": ["Processando", "Fila", "Concluído", "Bloqueado"],
    "data": [
      ["emissao", [89, 45, 12, 0]],
      ["reemissao", [2, 4, 10, 0]],
      ["cnpj_pdi", [0, 4, 10, 2]],
      ["traas", [3, 2, 4, 0]],
      ["pesados", [0, 0, 3, 0]]
    ]
  }
}
```

### 3.4 Fallback Estático

```html
<table class="dce-heatmap-table">
  <thead>
    <tr>
      <td></td>
      <th>Processando</th>
      <th>Fila</th>
      <th>Concluído</th>
      <th>Bloqueado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Emissão</th>
      <td class="cell-high">89</td>
      <td class="cell-medium">45</td>
      <td class="cell-low">12</td>
      <td class="cell-empty">—</td>
    </tr>
    <!-- ... -->
  </tbody>
</table>

<style>
  .dce-heatmap-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }
  
  .dce-heatmap-table th {
    background: #f5f5f5;
    padding: 0.75rem;
    text-align: center;
    font-weight: 600;
  }
  
  .dce-heatmap-table td {
    padding: 0.75rem;
    text-align: center;
    border: 1px solid #e0e0e0;
  }
  
  .dce-heatmap-table .cell-high {
    background: #4CAF50;
    color: white;
  }
  
  .dce-heatmap-table .cell-medium {
    background: #FF9800;
    color: white;
  }
  
  .dce-heatmap-table .cell-low {
    background: #F44336;
    color: white;
  }
</style>
```

---

## 4. Gráfico 3: Anéis de Progresso (KPI Radial)

### 4.1 Objetivo

Representação visual circular de progresso: Total, Sucesso %, Falha %, Pendente %.

```
       ◐████◑            (189 Sucesso)
       │ 77% │
       └────┘

Cada anel:
- Anel externo: total (gris背景)
- Anel colorido: progresso
- Centro: número + percentual
```

### 4.2 Estrutura SVG

```html
<svg class="dce-progress-rings" viewBox="0 0 180 180">
  
  <!-- Anel 1: Total (245 itens) -->
  <g class="progress-ring" data-label="Total" data-value="245" data-percentage="100">
    
    <!-- Background circle (gris) -->
    <circle cx="90" cy="90" r="60" class="progress-ring-background"/>
    
    <!-- Progress circle (animado) -->
    <circle cx="90" cy="90" r="60" class="progress-ring-progress" 
            style="--progress: 100%; --color: #0066cc;"/>
    
    <!-- Texto central -->
    <text x="90" y="85" class="progress-value">245</text>
    <text x="90" y="105" class="progress-label">Total</text>
    
  </g>
  
  <!-- Anel 2: Sucesso (189 = 77%) -->
  <g class="progress-ring" data-label="Sucesso" data-value="189" data-percentage="77" transform="translate(300, 0)">
    <circle cx="90" cy="90" r="60" class="progress-ring-background"/>
    <circle cx="90" cy="90" r="60" class="progress-ring-progress" 
            style="--progress: 77%; --color: #4CAF50;"/>
    <text x="90" y="85" class="progress-value">77%</text>
    <text x="90" y="105" class="progress-label">Sucesso</text>
  </g>
  
  <!-- Anel 3: Falha (12 = 5%) -->
  <g class="progress-ring" data-label="Falha" data-value="12" data-percentage="5" transform="translate(600, 0)">
    <circle cx="90" cy="90" r="60" class="progress-ring-background"/>
    <circle cx="90" cy="90" r="60" class="progress-ring-progress" 
            style="--progress: 5%; --color: #F44336;"/>
    <text x="90" y="85" class="progress-value">5%</text>
    <text x="90" y="105" class="progress-label">Falha</text>
  </g>
  
  <!-- Anel 4: Pendente (44 = 18%) -->
  <g class="progress-ring" data-label="Pendente" data-value="44" data-percentage="18" transform="translate(900, 0)">
    <circle cx="90" cy="90" r="60" class="progress-ring-background"/>
    <circle cx="90" cy="90" r="60" class="progress-ring-progress" 
            style="--progress: 18%; --color: #FF9800;"/>
    <text x="90" y="85" class="progress-value">18%</text>
    <text x="90" y="105" class="progress-label">Pendente</text>
  </g>
  
</svg>

<style>
  .dce-progress-rings {
    width: 100%;
    height: auto;
    max-width: 100%;
  }
  
  .progress-ring-background {
    fill: none;
    stroke: #e0e0e0;
    stroke-width: 8;
  }
  
  .progress-ring-progress {
    fill: none;
    stroke: var(--color, #0066cc);
    stroke-width: 8;
    stroke-linecap: round;
    stroke-dasharray: 377;  /* 2π × 60 ≈ 377 */
    stroke-dashoffset: calc(377 - (377 * var(--progress) / 100));
    transition: stroke-dashoffset 1s ease-in-out;
  }
  
  .progress-ring-progress {
    animation: ring-load 1.5s ease-out forwards;
  }
  
  @keyframes ring-load {
    from {
      stroke-dashoffset: 377;
      opacity: 0;
    }
    to {
      stroke-dashoffset: calc(377 - (377 * var(--progress) / 100));
      opacity: 1;
    }
  }
  
  .progress-value {
    font-size: 1.5rem;
    font-weight: 700;
    text-anchor: middle;
    fill: #212121;
  }
  
  .progress-label {
    font-size: 0.85rem;
    font-weight: 500;
    text-anchor: middle;
    text-transform: uppercase;
    fill: #666;
  }
  
  /* Responsivo: reduzir tamanho em mobile -->
  @media (max-width: 640px) {
    .progress-ring {
      transform: scale(0.75) !important;
    }
  }
</style>
```

### 4.3 Dados Esperados

```json
{
  "kpi_rings": [
    {
      "label": "Total",
      "value": 245,
      "percentage": 100,
      "color": "#0066cc"
    },
    {
      "label": "Sucesso",
      "value": 189,
      "percentage": 77,
      "color": "#4CAF50"
    },
    {
      "label": "Falha",
      "value": 12,
      "percentage": 5,
      "color": "#F44336"
    },
    {
      "label": "Pendente",
      "value": 44,
      "percentage": 18,
      "color": "#FF9800"
    }
  ]
}
```

### 4.4 Fallback Estático

```html
<div class="dce-progress-rings-fallback">
  <div class="ring-card">
    <div class="ring-stat">245</div>
    <div class="ring-label">Total</div>
    <div class="ring-bar" style="width: 100%; background: #0066cc;"></div>
  </div>
  
  <div class="ring-card">
    <div class="ring-stat">77%</div>
    <div class="ring-label">Sucesso</div>
    <div class="ring-bar" style="width: 77%; background: #4CAF50;"></div>
  </div>
  
  <!-- ... mais cards ... -->
</div>

<style>
  .dce-progress-rings-fallback {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }
  
  .ring-card {
    text-align: center;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
  }
  
  .ring-stat {
    font-size: 1.75rem;
    font-weight: 700;
    color: #212121;
  }
  
  .ring-label {
    font-size: 0.85rem;
    text-transform: uppercase;
    color: #666;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
  }
  
  .ring-bar {
    height: 4px;
    border-radius: 2px;
    margin: 0 auto;
  }
</style>
```

---

## 5. Arquivo de Dados Unificado (JSON)

```json
{
  "version": "1.0",
  "last_updated": "2026-03-26T10:30:00Z",
  "kpi_summary": {
    "total_items": 245,
    "success_count": 189,
    "success_percentage": 77,
    "failure_count": 12,
    "failure_percentage": 5,
    "pending_count": 44,
    "pending_percentage": 18
  },
  "sankey": {
    /* ... */
  },
  "heatmap": {
    /* ... */
  },
  "kpi_rings": {
    /* ... */
  }
}
```

---

## 6. Integração no HTML

```html
<!-- Arquivo único com dados embutidos -->
<script type="application/json" id="dce-graph-data">
{
  "version": "1.0",
  "last_updated": "2026-03-26T10:30:00Z",
  /* ... dados JSON ... */
}
</script>

<!-- Seção de gráficos -->
<section class="dce-visuals">
  
  <div class="visual-block">
    <h2>Sankey: Fluxo de Classificação</h2>
    <svg class="dce-sankey" viewBox="0 0 1000 400">
      <!-- SVG gerado -->
    </svg>
    <p class="visual-description">
      Este gráfico mostra como os 245 itens DC-e foram classificados ao passar por cada camada.
    </p>
  </div>
  
  <div class="visual-block">
    <h2>Heatmap: Categorias por Status</h2>
    <svg class="dce-heatmap" viewBox="0 0 600 400">
      <!-- SVG gerado -->
    </svg>
  </div>
  
  <div class="visual-block">
    <h2>KPI: Progresso</h2>
    <svg class="dce-progress-rings" viewBox="0 0 900 180">
      <!-- SVG gerado -->
    </svg>
  </div>
  
</section>
```

---

## 7. Considerações de Performance

1. **Tamanho**: Manter SVG inline < 50KB total (incluindo todos 3 gráficos)
2. **Animações**: Usar `will-change: transform` em elementos animados
3. **Responsividade**: Usar `viewBox` + `preserveAspectRatio` sempre
4. **Fallback**: Se SVG falhar, mostrar versão HTML/CSS estática

---

## 8. Testes Necessários

- ✅ Renderização em Chrome, Edge, Safari, Firefox
- ✅ Mobile: iOS Safari, Chrome Android
- ✅ Acessibilidade: screen readers (título + descrição textual antes/depois de cada SVG)
- ✅ Performance: tempo de render < 200ms em 4G
- ✅ Zoom: 200% zoom mantém clareza

