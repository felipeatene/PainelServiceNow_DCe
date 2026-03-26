# Guia Operacional — Painel de Triagem DC-e

**Data:** 26/03/2026  
**Versão:** 1.0  
**Público:** Analistas operacionais, auditores, equipe de triagem DC-e  
**Referência:** `painel-triagem-dce.html`

---

## 1. O que é o Painel de Triagem DC-e

Ferramenta de consulta **read-only** que classifica automaticamente itens relacionados a DC-e (Declaração de Conteúdo Eletrônica) em categorias operacionais, facilitando a identificação rápida, a triagem eficiente e a atuação regulatória informada.

### Objetivo Operacional

1. **Reduzir ruído:** Filtrar itens realmente relevantes para DC-e
2. **Classificar por contexto:** Separar por intenção, contexto operacional e complementos
3. **Gerar ação rápida:** Links prontos para ServiceNow com query filtrada
4. **Informar decisões:** Gráficos visuais e matriz de regras para consulta

### Não é para...

- ❌ Editar regras de classificação (use `taxonomy.json` e `decision-matrix.md`)
- ❌ Gerenciar incidents diretamente (painel é consulta, não execução)
- ❌ Repostar dados em tempo real (atualização periódica a cada 5 minutos em evolução futura)

---

## 2. Navegação Básica do Painel

### 2.1 Header (Topo)

```
📋 Painel de Triagem DC-e
Classificação inteligente por camadas — Visão geral operacional
Versão 1.0 | Atualizado em 26/03/2026
```

**O que fazer:** Ler o título para confirmar que está no painel certo. Timestamp mostra última atualização.

---

### 2.2 Bloco de Alertas Obrigatórios (Sticky)

```
⚠️ Pontos Obrigatórios
├─ 06/04/2026: Data oficial de obrigatoriedade nacional
├─ Autorização Pré-Transporte: Autorizar ANTES do início do transporte
└─ Uso Exclusivo: Apenas para operações SEM NF-e
```

**O que fazer:**
- **Sempre ler** cada vez que abrir o painel (fica no topo ao scroll)
- **Usar como checklist:** Validar se o item em questão atende esses 3 pontos
- **Alertar escalação se:** Item menciona NF-e + DC-e juntos (conflito regulatório)

**Impacto operacional:**
- Se hoje é ≥ 06/04/2026 e há itens SEM autorização: **CRÍTICO — validar urgentemente**
- Se item diz "contingência": **ATENÇÃO — prazo de 24h/1º dia útil para transmitir**
- Se item diz "NF-e + DC-e": **ERRO — DC-e não substitui NF-e**

---

### 2.3 Resumo de Classificações (KPI Cards)

```
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│  245   │ │  189   │ │   44   │ │   12   │
│ TOTAL  │ │EMISSÃO │ │REEMIS. │ │CANCEL. │
└────────┘ └────────┘ └────────┘ └────────┘
```

**Como ler:**
- **245 Total:** Todos os itens DC-e encontrados
- **189 Emissão/Ativação:** Maior volume — foco em gerar/emitir/ativar
- **44 Reemissão:** Segundo maior — atenção a "novo destino" + "cancelamento"
- **12 Cancelamento/SLA:** Menor, mas **crítico** — validar prazo de 24h

**O que fazer:**
- Clique em um card para filtrar itens dessa categoria (evolução futura)
- Use para **priorizar:** Se "Emissão" tem 189 itens, investir lá traz mais impacto
- Use para **dashboard executivo:** Reportar esses números para acompanhamento

---

### 2.4 Filtros por Camada

**Abas disponíveis:**
1. **✓ Âncora** (sempre encontrada) — 245 itens com variações de "DC-e"
2. **Intenção ↓** — ativação, emissão, cancelamento, etc.
3. **Contexto ↓** — CNPJ, PDI, VE Leves, TraaS, Pesados, etc.
4. **Complemento +** — tributário, HML, contingência, bug, XML, etc.

**Como usar:**
- Clique numa aba para expandir e ver distribuição
- Use para **entender composição:** Ex., "189 Emissão" é formado por "120 ativação + 89 emissão"
- Use para **drill-down:** Se problema com "LVE", clique em "Contexto" e veja os 34 itens LVE
- Use para **rastrear impacto:** Se temos 21 itens com "contingência", planejar ação em 24h

---

### 2.5 Gráficos — Visão Geral Analítica

#### Sankey: Fluxo de Classificação

```
Âncora    →    Intenção    →    Contexto    →    Complemento
 245     →    189+44+12     →    67+45+34     →    34+21+...
```

**Como ler:**
- **Largura das linhas:** Quanto maior, mais itens fluem por aquele caminho
- **Cores:** Identificam categoria
- **Top path (azul):** 189 itens em Emissão — fluxo principal

**O que fazer:**
- Usar para **comunicar status:** "190/245 itens com intenção identificada" = 77% clareza
- Usar para **encontrar desvios:** Se um path tem espessura inesperada, investigar

#### Heatmap: Categorias × Status

```
              Processando | Fila | Concluído | Bloqueado
Emissão          89       | 45   |    12     |    —
Reemissão        2        | 4    |    10     |    —
CNPJ/PDI         —        | 4    |    10     |    2
```

**Como ler:**
- **Verde:** Alto valor de itens concluídos (sucesso)
- **Amarelo:** Valor médio, em fila ou processando
- **Vermelho:** Valor baixo, precisa atenção
- **Cinza:** Sem dados/não aplicável

**O que fazer:**
- Usar para **identificar gargalo:** Ex., "CNPJ/PDI tem 2 bloqueados" → investigar validação de CNPJ
- Usar para **priorizar triagem:** Foco em status "Processando" (em progresso, precisa ação)
- Usar para **reporting:** "77 de 245 itens concluídos (31%)" = status executivo

#### Progress Rings: KPI Radial

```
245 Total | 77% Sucesso | 5% Falha | 18% Pendente
```

**Como ler:**
- Cada anel mostra percentual de progresso
- Cor indica saúde (verde = bom, vermelho = atender)

**O que fazer:**
- Usar para **health check rápido:** Abrir painel, olhar o 77% sucesso = OK
- Usar para **meta acompanhamento:** Se meta é 85% sucesso, está abaixo — escalar
- Usar para **tendência:** Se semana passada era 72% e hoje é 77%, mostrar melhoria

---

### 2.6 Categorias Operacionais (Cards)

8 cards mostrando cada categoria principal:

```
01 — Emissão / Ativação
     Iniciar emissão de DC-e ou ativar processo
     🔗 Abrir Consulta

02 — CNPJ / PDI / Cadastro
     Resolver problema de origem/identidade
     🔗 Abrir Consulta

[... 6 cards adicionais ...]
```

**Como usar:**
- **Ler descrição:** Identifica rápido o foco de cada categoria
- **Clicar em atalho:** Link de consulta abre ServiceNow com query pré-filtrada (evolução futura)
- **Usar em training:** Mostrar equipe que DC-e tem 8 cenários bem definidos, não é genérico

---

### 2.7 Matriz de Decisão (Expandível)

Clique em "📋 Matriz de Decisão" para ver como a classificação funciona:

```
SE CONTÉM              | ENTÃO CATEGORIA                | EXEMPLO
"ativação"             | Emissão / Ativação            | "ativação VE leves"
"cancelada" + "novo..." | Reemissão / Cancelada         | "cancelada com novo destino"
"cancelamento" + "24h" | Cancelamento / SLA ⚠️         | "cancelamento em 24h"
```

**O que fazer:**
- Usar para **entender por que** um item foi classificado assim
- Usar para **contestar classificação:** "Meu item tem palavra X, por que não categoria Y?" → Consultar matriz
- Usar em **auditorias:** Comprovar que regras estão sendo aplicadas consistentemente

---

## 3. Alertas Obrigatórios e Regulatórios

### 3.1 Alerta 1: Data de Obrigatoriedade (06/04/2026)

**Quando ativar:**
- Qualquer item DC-e aberto em ou após 06/04/2026
- Item sem autorização em data ≥ 06/04/2026

**Ação obrigatória:**
- ✅ Certificar que DC-e foi **autorizada** antes da data
- ✅ Se não autorizada: escalação imediata à equipe de homologação
- ✅ Documentar motivo de atraso (se houver)

**Onde documentar:**
- Campo "Observações" do incident: "⚠️ DC-e obrigatória desde 06/04/2026. Status: [autorizada/não autorizada]"

---

### 3.2 Alerta 2: Autorização Pré-Transporte

**Quando ativar:**
- Item menciona "transporte iniciado" SEM protocolo de autorização
- Item menciona "DACE impressa e enviada" SEM autorização prévia

**Ação obrigatória:**
- ✅ Validar que **protocolo de autorização existe** antes de qualquer transporte
- ✅ Se DACE foi emitida sem autorização: é contingência (tpEmis=9) → prazo de 24h para transmitir

**Onde documentar:**
- Campo de "Status": "Aguardando autorização SEFAZ" ou "Autorizada em [data/hora]"

---

### 3.3 Alerta 3: Uso Exclusivo (Sem NF-e)

**Quando ativar:**
- Item menciona: "NF-e + DC-e" ou "Nota Fiscal e DC-e juntas"
- Item sugere que DC-e substitui NF-e

**Ação obrigatória:**
- ✅ **PARAR triagem** desse item
- ✅ Questionar: "Este transporte tem emissão de NF-e prevista?"
  - SIM → DC-e NÃO é aplicável; é erro de entrada
  - NÃO → DC-e é obrigatória; prosseguir com triagem

**Onde documentar:**
- Comentário: "❌ ERRO: Item menciona NF-e + DC-e. Regra: DC-e APENAS para operações SEM NF-e."

---

## 4. Fluxo de Decisão Prático

### Cenário 1: Analista  recebe um incident com "gerar DC-e para CNPJ X"

```
Step 1 — Abrir painel DC-e
  ↓
Step 2 — Ler alertas (âncora, autorização, uso exclusivo)
  └─ ✓ Contém "DC-e" (âncora OK)
  └─ ✓ Sem menção a NF-e (uso OK) 
  └─ ? Não menciona autorização → verificar em paralelo com SEFAZ
  ↓
Step 3 — Clicar em aba "INTENÇÃO"
  └─ Vê: "gerar" = Emissão / Ativação
  ↓
Step 4 — Clicar em aba "CONTEXTO"
  └─ Vê: "CNPJ" = CNPJ / PDI / Cadastro
  ↓
Step 5 — Consultar Matriz de Decisão
  └─ Encontra: IF "gerar" + "CNPJ" THEN Emissão/Ativação (intenção > contexto)
  ↓
Step 6 — Categoria Final: **Emissão / Ativação**
  ├─ Ação: Validar CNPJ em base de dados
  ├─ Link: Abrir consulta de "Emissão" no ServiceNow
  └─ Escalação: Se CNPJ não existe, escalate para preenchimento de cadastro
```

---

### Cenário 2: Analista recebe "DC-e cancelada em 23 de março"

```
Step 1 — Abrir painel, ler alertas
  └─ ✓ Âncora: "DC-e" encontrada
  └─ ⚠️ Data: 23/03/2026 (antes de 06/04, ainda em período de adaptação, OK)
  ↓
Step 2 — Clicar em aba "INTENÇÃO"
  └─ Vê: "cancelada" + data = pode ser Cancelamento/SLA ou Reemissão
  ↓
Step 3 — Consultar Matriz de Decisão
  └─ Encontra: IF "cancelada" THEN Cancelamento/SLA (primeira correspondência)
  ↓
Step 4 — Categoria Final: **Cancelamento / SLA**
  ├─ Alerta: ⚠️ Prazo de 24h para cancelamento obrigatório
  ├─ Ação: Validar data de cancelamento vs. data de autorização
  │  └─ Se <= 24h: ✓ dentro do SLA
  │  └─ Se > 24h: ⚠️ Fora do SLA, requer análise SEFAZ (cStat=155)
  └─ Escalação: Se fora do SLA, documentar justificativa
```

---

## 5. Links do ServiceNow e Queries

### 5.1 Estrutura Base

```
https://ibmlocaliza.service-now.com/incident_list.do?sysparm_query=...
```

### 5.2 Query por Categoria (Templates)

**Emissão/Ativação:**
```
description contains dce,dc-e,dc e AND description contains ativacao,emitir,gerar AND opened_at >= [DATA]
```

**CNPJ/PDI/Cadastro:**
```
description contains dce AND (description contains cnpj OR description contains pdi) AND opened_at >= [DATA]
```

**Reemissão:**
```
description contains dce AND description contains cancelada,novo destino,reemissao AND opened_at >= [DATA]
```

**Cancelamento/SLA:**
```
description contains dce AND description contains cancelamento AND opened_at >= [DATA-24h]
```

**VE Leves:**
```
description contains dce AND (description contains lve OR description contains locavia OR description contains "ve leves") AND opened_at >= [DATA]
```

### 5.3 Como Usar no Painel

Botões "🔗 Abrir Consulta" em cada card de categoria abrirão a query acima em nova aba (funcionalidade integrada em evolução futura).

**Até lá, uso manual:**
1. Copiar template acima
2. Substituir `[DATA]` pela data desejada
3. Abrir link no navegador

---

## 6. Validação e Testes

### 6.1 Teste de Âncora

**Input:** "Sistema de gestão de transporte com alertas de contingência"  
**Esperado:** Sem âncora → Filtro fora  
**Verificação:** ✓ Pass (não aparece no painel)

**Input:** "DC-E emitida em contingência para frota"  
**Esperado:** Âncora "DC-E" encontrada → continua triagem  
**Verificação:** ✓ Pass (aparece no painel)

---

### 6.2 Teste de Intenção

**Input:** "ativação de DC-e para VE Leves"  
**Esperado:** Categoria = Emissão/Ativação (intenção "ativação")  
**Verificação:** ✓ Pass

**Input:** "DC-e cancelada com novo destino RAC"  
**Esperado:** Categoria = Reemissão/Cancelada (intenção "cancelada" + "novo destino")  
**Verificação:** ✓ Pass

---

### 6.3 Teste de Contexto (Sem Intenção)

**Input:** "Problema na geração de DC-e para CNPJ 12.345.678/0001-90"  
(Sem intenção clara, mas tem "CNPJ")  
**Esperado:** Categoria = CNPJ/PDI/Cadastro  
**Verificação:** ✓ Pass

---

### 6.4 Teste de Complemento

**Input:** "DC-e em contingência para validação HML"  
**Esperado:** 
- Categoria = Emissão/Ativação (se houver intenção como "gerar") OU
- Categoria = padrão se sem intenção clara
- Flags = ["contingencia", "hml"]  
**Verificação:** ✓ Pass

---

## 7. Troubleshooting Comum

### P1: "Abri o painel e não sei por onde começar"

**R:** Leia primeiro os 3 alertas obrigatórios no topo (sticky). Depois olhe os KPI cards — use as cores para encontrar a categoria mais relevante.

### P2: "Item foi classificado errado"

**R:** Consulte a Matriz de Decisão (expandir ao final). Se encontrar que as regras estão sendo aplicadas corretamente mas discorda da classificação, documente em `decision-matrix.md` como caso de exceção.

### P3: "Preciso filtrar itens de uma categoria específica"

**R:** Clique no card da categoria e use o botão "🔗 Abrir Consulta" (evolução futura). Enquanto isso, copie o template de query e adapte no ServiceNow manualmente.

### P4: "Painel não está atualizado"

**R:** Painel é snapshot (atualização manual agora, periódica em 5 min no futuro). Recarregue a página. Se ainda desatualizado, verifique a timestamp no header. Para dados real-time, consulte tickets diretamente no ServiceNow.

---

## 8. Responsabilidades por Papel

### Analista de Triagem DC-e
- Usar o painel para **classificar** itens por categoria
- Validar **alertas obrigatórios** antes de qualquer ação
- Documentar **observações** sobre discrepâncias de classificação
- Abrir **escalações** para casos fora da política

### Auditor
- Usar painel para **verificar** se regras estão sendo aplicadas
- Validar **amostra** de itens contra matriz de decisão
- Reportar **desvios** encontrados
- Certificar **conformidade** regulatória

### Dev/Admin ServiceNow
- **Evoluir** painel para widget com atualização em 5 minutos
- Integrar **queries filtradas** no botão de consulta
- Manter **taxonomy.json** + **decision-matrix.md** sincronizados
- Monitorar **performance** do painel em produção

---

## 9. Próximos Passos

- [ ] **Semana 1:** Treinar equipe com este guia + painel ao vivo
- [ ] **Semana 2:** Executar 10 testes de classificação + validar 100% acerto
- [ ] **Semana 3:** Implementar widget ServiceNow com atualização automática
- [ ] **Semana 4:** Go live em produção; monitorar métrica de acerto

---

**Dúvidas?** Consulte:
- `taxonomy.json` — Dicionário de palavras-chave
- `decision-matrix.md` — Fluxo completo de regras
- `ui-specification.md` — Especificação visual

