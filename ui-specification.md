# Especificação UX/UI — Painel DC-e Responsivo

**Data:** 26/03/2026  
**Versão:** 1.0  
**Escopo:** Painel de triagem e consulta sem edição de regras (read-only)  
**Público:** Analistas operacionais, auditores, suporte DC-e

---

## 1. Objetivos e Princípios

### Objetivos
1. **Clareza operacional** — usuário identifica categoria e regra aplicada sem ambiguidade
2. **Ação rápida** — filtros e atalhos acessíveis em < 3 cliques
3. **Visual diferenciado** — design autoral que não pareça padrão ServiceNow
4. **Responsivo total** — uso pleno em celular (< 390px) até desktop (> 1366px)
5. **Sem dependência JS** — funciona 100% em HTML/CSS no Rich Text; JS é enhancement opcional

### Princípios de Design
- **Mobile-first** — layout estruturado para celular, escala para deixtop
- **Hierarquia visual clara** — usuário lê por ordem: título > KPI > contexto > detalhe
- **Affordance imediata** — claro o que é clicável (cards com hover, chips com cor)
- **Acessibilidade nativa** — contraste WCAG AA, foco visível, ordem de leitura sensata

---

## 2. Arquitetura de Seções

### 2.1 Estrutura Geral (Top-Down)

```
┌─────────────────────────────────────────────────────────┐
│  HEADER: Logo + Títu lo "Painel de Triagem DC-e"       │
│  Subtítulo: "Classificação inteligente por camadas"     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  BLOCO 1: ALERTAS REGULATÓRIOS (sticky no scroll)       │
│  ⚠️ Obrigatoriedade em 06/04/2026 | ℹ️ Autorização pre│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  BLOCO 2: KPI — Totais por Categoria                    │
│  [Card: 245 Total] [Card: 189 Emissão] [Card: 56 Ou...]│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  BLOCO 3: FILTROS POR CAMADA (Abas ou Accordions)      │
│  [Âncora] [Intenção] [Contexto] [Complemento]           │
│  └─ Listagem filtrada abaixo                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  BLOCO 4: GRÁFICOS DE VISÃO (Sankey + Heatmap)         │
│  Fluxo de camadas | Matriz categoria x status           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  BLOCO 5: CATEGORIA + ATALHOS                           │
│  [Card Emissão/Ativação] [Card CNPJ/PDI] [...]         │
│  └─ Link ServiceNow + ícone clicável para cada         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  BLOCO 6: MATRIZ DE REGRAS (Read-only)                 │
│  Tabela ou accordion: Se X + Y → Categoria Z           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  FOOTER: Versão, data da última atualização, crédito    │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Componentes Detalhados

### 3.1 Header

```
┌───────────────────────────────────────────────────┐
│                                                   │
│  DC-e  Painel de Triagem                         │
│        Classificação inteligente por camadas      │
│        Versão 1.0 | Atualizado em 26/03/2026    │
│                                                   │
└───────────────────────────────────────────────────┘

Especificação:
- Logotipo (mini): ícone ou símbolo "DC-e" | 32px
- Título H1: "Painel de Triagem DC-e" | 2.5rem, bold
- Subtítulo: "Classificação inteligente por camadas" | 1rem, medium
- Metadados: versão + data | 0.75rem, gray

Estilo: Background com gradiente sutil (branco → cinza claro), bordinha inferior 4px na cor primária
```

### 3.2 Alertas Regulatórios (Sticky Block)

```
┌─ ⚠️  PONTOS OBRIGATÓRIOS ─────────────────────────┐
│                                                   │
│ 🔴 Data de Obrigatoriedade: 06/04/2026           │
│    Exigência nacional via Ajuste SINIEF 22/2025  │
│                                                   │
│ ℹ️  Autorização Pré-Transporte (Obrigatória)     │
│    DC-e deve ser autorizada ANTES do início do   │
│    transporte                                     │
│                                                   │
│ ℹ️  Uso Exclusivo: Sem emissão de NF-e          │
│    Uso somente para operações SEM Nota Fiscal    │
│                                                   │
└─────────────────────────────────────────────────┘

Especificação:
- Container: padding 1rem | border-left 4px vermelho | background rgba(244, 67, 54, 0.05)
- Ícone: 24px, alinhado à esquerda
- Texto: 0.9rem | cor dark (/212121)
- Posição: sticky top 0 (scroll mantém visível)
- Responsivo mobile: font-size 0.85rem
```

### 3.3 KPI Cards

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│    245   │  │    189   │  │     44   │  │     12   │
│  TOTAL   │  │ EMISSÃO  │  │ REEMISSÃO│  │ CANCEL.  │
│ ITEMS    │  │ /ATIVAÇÃO│  │          │  │   /SLA   │
└──────────┘  └──────────┘  └──────────┘  └──────────┘

Especificação:
- Cada Card: width 100% mobile (stacked), 25% em grid de 4 no desktop
- Altura: 120px
- Border-left: 4px na cor da categoria
- Número grande: 2.5rem, bold, cor primária
- Label: 0.9rem, uppercase, gray + 50%

Cores por categoria:
  - Total: #0066cc (azul)
  - Emissão: #0066cc
  - Reemissão: #FF5722
  - Cancelamento: #F44336
  - CNPJ/PDI: #FF9800
  - VE Leves: #9C27B0
  - TraaS: #00BCD4
  - Pesados: #3F51B5
  - Desativação: #757575

Interação:
  - Hover: box-shadow 0 8px 20px rgba(0,0,0,0.15)
  - Cursor: pointer (clicável para filtrar por categoria)
```

### 3.4 Filtros por Camada (Tabs/Accordions)

**Desktop (> 640px)**: Abas horizontais  
**Mobile (< 640px)**: Accordions empilhados

```
┌─────────────────────────────────────────────────┐
│  [Âncora ✓]  [Intenção ↓]  [Contexto ↓]  [+]   │
├─────────────────────────────────────────────────┤
│  Palavras-chave encontradas:                    │
│  🔹 ativação    🔹 emitir     🔹 gerar         │
│  🔹 emissão     🔹 cancelada  🔹 reemissão      │
│                                                 │
│  Listagem de itens matchando essa intenção:    │
│  • Item 1: emissão CNPJ    → Categoria: X     │
│  • Item 2: ativação LVE    → Categoria: Y     │
│                                                 │
└─────────────────────────────────────────────────┘

Especificação:
- Tab/Summary: 1rem, bold, cor primária hover
- Conteúdo aberto: padding 1rem | background #f5f5f5
- Chips de palavras-chave: display inline-block, background color-light, margin 0.5rem
- Listagem: ul com item-style none, padding left 2rem

Comportamento:
- Desktop: tabs mutualmente exclusivas
- Mobile: accordions com <details>/<summary> (sem JS)
```

### 3.5 Gráficos (Sankey + Heatmap)

#### 3.5.1 Sankey Diagram — Fluxo de Camadas

```
ÂNCORA          INTENÇÃO        CONTEXTO        COMPLEMENTO
  245 ────→    ┌─ 189 Emissão ──→ ┌─ 120 CNPJ ──→ 85 tributário
  DC-e         │  44 Reemissão ──→ │  64 TraaS ──→ 44 XML
               │  12 Cancelamento  │  21 Pesados   ...
               └─ ...

Especificação:
- Responsivo: 100% width no mobile, fixo 800px desktop
- SVG inline com viewBox preservado
- Cores por camada: azul (âncora) → cores por intenção → cinza complemento
- Hover em paths: opacity 1, non-hovered → 0.3
- Sem clique; visual only
```

#### 3.5.2 Heatmap — Categoria x Status

```
           Processando  Em Fila   Concluído  Bloqueado
Emissão       ████        ██        ██         —
Reemissão     ██          ████      ②         —
CNPJ/PDI      —           ④         ⑩         ②
TraaS         ③           ②         ④         —
Pesados       —           —         ③         —

Especificação:
- Grid: categorias no eixo Y, status no eixo X
- Cada célula: cor verde (⑤+) → amarelo (②-④) → vermelho (<②)
- Hover: tooltip com número exato + percentual
- Responsive: rotação 45° de labels em mobile, mantém cores
```

### 3.6 Categorias + Atalhos (Card Grid)

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  01             │  │  02             │  │  03             │
│  Emissão /      │  │  CNPJ / PDI /   │  │  Reemissão /    │
│  Ativação       │  │  Cadastro       │  │  Cancelada      │
│                 │  │                 │  │                 │
│  Ativar emissão │  │  Validar origem │  │  Reemitir com   │
│  de DC-e        │  │  de identidade  │  │  novo destino   │
│                 │  │                 │  │                 │
│  🔗 Emissões    │  │  🔗 CNPJ        │  │  🔗 Canceladas  │
│     sem NF-e    │  │     Específicos │  │     c/ novo est │
└─────────────────┘  └─────────────────┘  └─────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  04             │  │  05             │  │  06             │
│  VE Leves       │  │  TraaS / Frete  │  │  Pesados /      │
│  / LVE          │  │  / Realocação   │  │  Caminhões      │
│  ...            │  │  ...            │  │  ...            │
└─────────────────┘  └─────────────────┘  └─────────────────┘

Especificação:
- Grid: 1 coluna mobile | 2 colunas tablet | 3 colunas desktop
- Card size: mínimo 220px | máximo 300px
- Conteúdo:
  - Número (01-09): pequeno, cinza, topo-direita
  - Título H3: 1.25rem, bold, cor categoria
  - Descrição: 0.9rem, gray-600, 2-3 linhas
  - Atalho (link): 📎 "Abrir no ServiceNow" com href dinâmico
  - Ícone: emoji relevante (📤 emit, 🏷️ CNPJ, ♻️ reemis, etc.)

Interação:
- Hover: elevação (+8px drop-shadow), cor mais intensa
- Clique em atalho: abre em nova aba com query filtrada
- Sem clique em card: apenas visual

Cores: cada card tem cor de fundo rgba(categoria-color, 0.1)
Border-left: 4px na cor da categoria
```

### 3.7 Matriz de Regras (Accordion Read-Only)

```
<details>
  <summary>📋 Matriz de Decisão — Como a Classificação Funciona</summary>
  
  Tabela ou cards mostrando:
  
  SE CONTÉM...             ENTÃO CATEGORIA...                  EXEMPLOS
  ─────────────────────────────────────────────────────────────────────
  "ativação" + contexto    Emissão / Ativação                  "ativação VE leves"
  "gerar" + contexto       Emissão / Ativação                  "gerar DC-e para CNPJ"
  "cancelada" + "novo..."  Reemissão / Cancelada               "cancelada com novo dest."
  "cancelamento" + "24h"   Cancelamento / SLA ⚠️ ALERTA        "cancelamento em 24h"
  ...
  
</details>

Especificação:
- Summary: 1rem, bold, pode ser expandido clicando
- Conteúdo: padding 1rem | background #fafafa
- Tabela ou cards: max-width 100%, responsivo
```

---

## 4. Design System

### 4.1 Paleta de Cores

```css
--primary: #0066cc;           /* Azul corporativo */
--success: #4CAF50;           /* Verde (emissão OK) */
--warning: #FF9800;           /* Laranja (em análise) */
--danger: #F44336;            /* Vermelho (bloqueado) */
--info: #00BCD4;              /* Ciano (info/neutral) */
--neutral: #757575;           /* Cinza (não aplicável) */
--bg-light: #f5f5f5;          /* Fundo claro */
--bg-white: #ffffff;          /* Fundo branco */
--text-primary: #212121;      /* Texto principal */
--text-secondary: #666;       /* Texto secundário */
--border: #e0e0e0;            /* Borda */

Cores por Categoria:
--cat-emissao: #0066cc;
--cat-cnpj: #FF9800;
--cat-reemissao: #FF5722;
--cat-leves: #9C27B0;
--cat-valor: #4CAF50;
--cat-cancelamento: #F44336;
--cat-desativacao: #757575;
--cat-traas: #00BCD4;
--cat-pesados: #3F51B5;
```

### 4.2 Tipografia

```css
--font-primary: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
--font-mono: "Courier New", monospace;

H1: 2.5rem | 700 (bold) | letter-spacing: -0.02em | line-height: 1.2
H2: 1.875rem | 600 (semibold) | line-height: 1.3
H3: 1.25rem | 600 (semibold) | line-height: 1.4
H4: 1rem | 600 (semibold) | line-height: 1.5

Body: 0.9rem | 400 | line-height: 1.6 | letter-spacing: 0.005em
Small: 0.75rem | 400 | line-height: 1.5
Label: 0.85rem | 500 (medium) | text-transform: uppercase | letter-spacing: 0.1em
Code: 0.8rem | 400 | font-family: var(--font-mono) | background #f0f0f0 | padding 0.25rem

Responsive:
Mobile:     H1 2rem   | Body 0.9rem
Tablet:     H1 2.25rem | Body 0.95rem
Desktop:    H1 2.5rem | Body 1rem
```

### 4.3 Espaçamento (8px base)

```css
--spacing-xs: 0.25rem (4px)   /* padding mínimo em chips */
--spacing-sm: 0.5rem  (8px)   /* padding em botões pequenos */
--spacing-md: 1rem    (16px)  /* padding standard em cards */
--spacing-lg: 1.5rem  (24px)  /* margin entre seções */
--spacing-xl: 2rem    (32px)  /* margin entre blocos principais */
--spacing-xxl: 3rem   (48px)  /* top/bottom do painel */
```

### 4.4 Border Radius

```css
--radius-sm: 4px    /* cards pequenos, chips */
--radius-md: 8px    /* cards padrão */
--radius-lg: 12px   /* cards principais, gráficos */
```

### 4.5 Sombras (Material Design)

```css
--shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
--shadow-md: 0 4px 8px rgba(0,0,0,0.12);
--shadow-lg: 0 8px 20px rgba(0,0,0,0.15);
--shadow-xl: 0 16px 32px rgba(0,0,0,0.18);

Aplicação:
Cards (normal):   --shadow-md
Cards (hover):    --shadow-lg
Alert blocks:     --shadow-sm
Modal/overlay:    --shadow-xl
```

---

## 5. Responsividade

### 5.1 Breakpoints

```css
Mobile:     < 640px   (default, mobile-first)
Tablet:     640px - 1024px
Desktop:    >= 1024px
```

### 5.2 Mudanças por Breakpoint

| Elemento | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| **Header** | H1 2rem | H1 2.25rem | H1 2.5rem |
| **KPI Cards** | 1 col (100%) | 2 cols | 4 cols |
| **Filtros** | Accordions | Abas | Abas |
| **Gráficos** | Scaled 90% | Scaled 95% | Scaled 100% |
| **Categorias Grid** | 1 col | 2 cols | 3 cols |
| **Padding global** | 1rem | 1.5rem | 2rem |
| **Font-size body** | 0.9rem | 0.95rem | 1rem |

### 5.3 Viewport Meta

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

---

## 6. Estados Interativos (Sem JS Obrigatório)

### 6.1 Estados Visual

```
DEFAULT
  └─ background: --bg-white
  └─ color: --text-primary
  └─ box-shadow: --shadow-sm

HOVER (desktop)
  └─ background: rgba(var(--primary), 0.05)
  └─ transform: translateY(-2px)
  └─ box-shadow: --shadow-lg
  └─ transition: all 0.3s ease

FOCUS (keyboard naveg.)
  └─ outline: 2px solid var(--primary)
  └─ outline-offset: 2px

ACTIVE (clique)
  └─ transform: scale(0.98)
  └─ box-shadow: --shadow-md

DISABLED
  └─ opacity: 0.6
  └─ cursor: not-allowed
  └─ color: --text-secondary
```

### 6.2 Interatividade sem JS

**Abas:** usar `<input type="radio">`+ labels formatadas  
**Accordions:** usar `<details>` + `<summary>`  
**Hover effects:** CSS `:hover`, `:focus`, `:active`  
**Cores dinâmicas:** CSS custom properties `--color` passadas via atributo `style`

---

## 7. Acessibilidade

### 7.1 Contraste

- Texto preto (#212121) sobre fundo branco: 18:1 ✅ AAA
- Texto cinza (#666) sobre fundo branco: 7:1 ✅ AA
- Links: cor diferente + underline no hover

### 7.2 Foco Visível

```css
:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-radius: 4px;
}
```

### 7.3 Hierarquia de Títulos

- H1: Título principal do painel (1 apenas)
- H2: Blocos principais (Header, KPI, Filtros, Gráficos, Categorias)
- H3: Subcategorias ou cards de categoria
- H4: Dentro de cards (se houver)

### 7.4 Labels e WAI-ARIA

```html
<!-- Para chips/filtros -->
<span role="pill" aria-label="Intenção: ativação">ativação</span>

<!-- Para alerts obrigatórios -->
<div role="alert" aria-live="assertive">
  ⚠️ ...
</div>

<!-- Para tabs/accordions -->
<button aria-expanded="false" aria-controls="panel-intenção">
  Intenção
</button>
<div id="panel-intenção" hidden>
  ...
</div>
```

### 7.5 Ordem de Leitura

1. Header (logo, título, subtítulo)
2. Alertas regulatórios (role="alert")
3. KPI summary
4. Filtros e busca
5. Gráficos (descrição textual antes/depois)
6. Categorias grid
7. Matriz de regras
8. Footer

---

## 8. Comportamento por Tela

### 8.1 Mobile (< 390px)

- Header: compacto, sem subtítulo em scroll
- Alerta: sticky, altura mínima
- KPI cards: 1 coluna, scrollável horizontalmente
- Filtros: accordions empilhados
- Gráficos: escala 90%, scrollável horizontalmente
- Categorias: 1 coluna
- Padding global: 1rem
- Font mínima: 14px (0.875rem)

### 8.2 Tablet (640px - 1024px)

- Header: normal
- KPI cards: 2 colunas
- Filtros: abas com wrap se necessário
- Gráficos: escala 95%
- Categorias: 2 colunas
- Padding: 1.5rem

### 8.3 Desktop (> 1024px)

- Todos os elementos na config padrão
- KPI cards: 4 colunas (ou grid automático)
- Gráficos: 100% com sidebar opcional
- Categorias: 3 colunas
- Padding: 2rem

---

## 9. Estrutura de Arquivo HTML (Referência)

```html
<div class="dce-panel" lang="pt-BR">
  
  <!-- Header -->
  <header class="dce-header">...</header>
  
  <!-- Alerts Block -->
  <section class="dce-alerts" role="alert">...</section>
  
  <!-- KPI Cards -->
  <section class="dce-kpis">...</section>
  
  <!-- Filters by Layer -->
  <section class="dce-filters">...</section>
  
  <!-- Visuals (Sankey + Heatmap) -->
  <section class="dce-visuals">...</section>
  
  <!-- Category Cards -->
  <section class="dce-categories">...</section>
  
  <!-- Decision Matrix -->
  <section class="dce-matrix">...</section>
  
  <!-- Footer -->
  <footer class="dce-footer">...</footer>
  
</div>
```

---

## 10. Notas para Implementação

1. **CSS Namespace:** sempre usar `.dce-*` para evitar conflitos com estilos globais ServiceNow
2. **Responsive Images:** usar `viewBox` em SVG inline; não usar `<img>` para gráficos
3. **Data Attributes:** usar `data-category`, `data-flag`, etc. para estilo dinâmico sem JS
4. **Print-friendly:** considerar `@media print { display: none; }` para seções não relevantes
5. **Dark Mode:** preparar fallback ou versão dark se ServiceNow suportar

