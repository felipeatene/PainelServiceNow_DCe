# Matriz de Decisão — Triagem DC-e

**Data:** 26/03/2026  
**Versão:** 1.0  
**Precedência:** Intenção > Contexto > Complemento  
**Estrutura:** Baseada em `taxonomy.json`

---

## 1. Pré-requisito Absoluto: Camada 1 (Âncora)

Antes de qualquer classificação, verificar se o item contém **uma variação de âncora DC-e**:

```
✓ Contém: "dce" OU "dc-e" OU "dc e" OU "declaração de conteúdo" OU "declaração de conteúdo eletrônica"
✗ Não contém nenhuma: → FILTRAR FORA (não é DC-e)
```

**Se não passar aqui, parar. Sem âncora, sem classificação.**

---

## 2. Fluxo de Classificação (Camadas 2, 3, 4)

### Passo 1: Procurar por Intenção (Camada 2)

Varrer o texto procurando por qualquer palavra-chave de Intenção:

| Intenção | Palavras-chave | Categoria Primária |
|----------|----------------|-------------------|
| **ativação** | ativação, ativar, ativando | Emissão / Ativação |
| **emissão** | emissão, emitir, emitindo, gerar, gerar uma dce | Emissão / Ativação |
| **cancelamento** | cancelamento, cancelada, cancelado, cancelar | Cancelamento / SLA |
| **reemissão** | reemissão, reemitir, novo destino, a partir de uma dce cancelada | Reemissão / Cancelada / Novo destino |
| **desativação** | desativação, operação desativação, desativar | Desativação / Não emissão |
| **não emissão** | não emissão, não gerar dc-e, bloqueado | Desativação / Não emissão |

**Resultado esperado:** Se encontrar uma intenção → atribuir sua `primary_category` (isso é a lógica de precedência).

---

### Passo 2: Se Nenhuma Intenção, Procurar por Contexto (Camada 3)

Se o Passo 1 não encontrou nada, procurar por palavras-chave de Contexto:

| Contexto | Palavras-chave | Categoria Primária | Weight |
|----------|--|---|---|
| **CNPJ_PDI** | cnpj, pdi, cd, cadastro de cnpj, fornecedor, rac, gf, 42, 44 | CNPJ / PDI / Cadastro | 2 |
| **VE_Leves** | lve, leves, ve leves, locavia | VE Leves / LVE | 2 |
| **Valor** | abaixo de R$ 100.000,00, 100.000, 100000, 100 mil, pabaixo, limite | Regra de Valor | 1 |
| **TraaS_Frete** | traas, frete, realocação, realocação frota, realocação seminovos, sn, seminovos | TraaS / Frete / Realocação | 2 |
| **Pesados** | pesados, caminhões, gateway, ativação pesados | Pesados / Caminhões | 2 |

**Resultado esperado:** Se encontrar contexto → atribuir sua `primary_category`. Se múltiplos contextos com mesmo weight, usar primeiro encontrado no texto.

---

### Passo 3: Complementar com Complementos (Camada 4)

Independentemente de ter Intenção ou Contexto, procurar por palavras-chave de Complemento para adicionar flags:

| Complemento | Palavras-chave | Flag | Risk Level |
|---|---|---|---|
| **tributário** | tributário | `tributario` | info |
| **piloto** | piloto | `piloto` | info |
| **homologação** | hml, homologação, teste | `hml` | info |
| **contingência** | contingência, contingencia, offline, emitido em contingência | `contingencia` | ⚠️ warning |
| **XML** | xml, estrutura, validação xml | `xml` | info |
| **bug** | bug, defeito, erro | `bug` | 🔴 alert |
| **documentos validados** | documentos validados | `documentos_validados` | ✅ success |
| **documentos disponíveis** | documentos disponíveis | `documentos_disponiveis` | ✅ success |
| **SLA 24h** | 24 horas, sla, dentro do sla, após 24 horas | `sla_24h` | ⚠️ warning |

**Resultado esperado:** Adicionar flags a um array `flags[]` sem alterar a categoria primária.

---

## 3. Regras de Desempate

### Caso A: Múltiplas Intenções Encontradas

**Exemplo:** "gerar um cancelamento"

```
Intenções encontradas:
  - "gerar" → Emissão / Ativação
  - "cancelamento" → Cancelamento / SLA

Regra: Usar a primeira encontrada no texto
→ Categoria: Emissão / Ativação
```

**Por quê:** Intenção tem peso 3, contexto tem peso 2. Não há desempate entre intenções, então segue ordem de aparição.

---

### Caso B: Uma Intenção + Múltiplos Contextos

**Exemplo:** "ativação VE leves CNPJ"

```
Intenção encontrada:
  - "ativação" → Emissão / Ativação

Contextos encontrados:
  - "leves" (weight 2)
  - "cnpj" (weight 2)

Regra de Precedência: Intenção > Contexto
→ Categoria: Emissão / Ativação
→ Contexto descartado (não entra na categoria)
```

**Por quê:** Intenção tem precedência absoluta por regra estabelecida.

---

### Caso C: Nenhuma Intenção, Múltiplos Contextos com Mesmo Weight

**Exemplo:** "DC-e TraaS Frete RAC Realocação"

```
Contextos encontrados:
  - "traas" (weight 2) → TraaS / Frete / Realocação
  - "frete" (weight 2) → TraaS / Frete / Realocação
  - "rac" (weight 2) → CNPJ / PDI / Cadastro
  - "realocação" (weight 2) → TraaS / Frete / Realocação

Regra: Primeiro encontrado no texto
→ "traas" aparece primeiro
→ Categoria: TraaS / Frete / Realocação
```

---

## 4. Exemplos Passo-a-Passo

### Exemplo 1: "DC-e cancelada com novo destino"

```
Entrada: "DC-e cancelada com novo destino"

Passo 1 - Âncora
✓ Contém "DC-e" → continua

Passo 2 - Intenção
✓ Contém "cancelada" → Cancelamento / SLA
  Contém "novo destino" → Reemissão / Cancelada / Novo destino
  Ambas são Intenção; primeira → "cancelada"
  → Categoria = Cancelamento / SLA

Passo 3 - Complemento
✗ Nenhum complemento encontrado
  → flags = []

RESULTADO: Categoria = "Cancelamento / SLA", Flags = []
```

---

### Exemplo 2: "ativação VE leves com contingência"

```
Entrada: "ativação VE leves com contingência"

Passo 1 - Âncora
✓ Contém variação de "dce" (implícito) → continua

Passo 2 - Intenção
✓ Contém "ativação" → Emissão / Ativação
  Há também contexto "leves", mas Intenção prevalece
  → Categoria = Emissão / Ativação

Passo 3 - Complemento
✓ Contém "contingência" → flags.push("contingencia")
  → flags = ["contingencia"]

RESULTADO: Categoria = "Emissão / Ativação", Flags = ["contingencia"]
```

---

### Exemplo 3: "gerar DC-e para cada CNPJ PDI"

```
Entrada: "gerar DC-e para cada CNPJ PDI"

Passo 1 - Âncora
✓ Contém "DC-e" → continua

Passo 2 - Intenção
✓ Contém "gerar" → Emissão / Ativação
  → Categoria = Emissão / Ativação

(Contexto "CNPJ" e "PDI" encontrados, mas Intenção prevalece)

Passo 3 - Complemento
✗ Nenhum complemento encontrado
  → flags = []

RESULTADO: Categoria = "Emissão / Ativação", Flags = []
```

---

### Exemplo 4: "DC-e TraaS Frete RAC Realocação (bug em produção)"

```
Entrada: "DC-e TraaS Frete RAC Realocação (bug em produção)"

Passo 1 - Âncora
✓ Contém "DC-e" → continua

Passo 2 - Intenção
✗ Nenhuma intenção encontrada
  → passa para Passo 3 (Contexto)

Passo 3 - Contexto
✓ Encontrados: "traas", "frete", "rac", "realocação"
  Todos têm weight 2
  Primeira no texto: "traas"
  → Categoria = TraaS / Frete / Realocação

Passo 4 - Complemento
✓ Contém "bug"
  → flags.push("bug")
  → flags = ["bug"]

RESULTADO: Categoria = "TraaS / Frete / Realocação", Flags = ["bug"]
```

---

## 5. Validações Obrigatórias Após Classificação

Após atribuir Categoria e Flags, sempre validar:

| Validação | Ação |
|-----------|------|
| Se Categoria = "Cancelamento / SLA" E Flag = "sla_24h" | ⚠️ Avisar: Prazo de 24h obrigatório |
| Se Categoria = "Desativação / Não emissão" | 🔴 Avisar: Bloqueio de emissão; validar regra |
| Se Categoria = "Reemissão..." E Flag = "contingencia" | ⚠️ Avisar: Emissão em contingência; prazo até fim do 1º dia útil |
| Se Categoria = "CNPJ / PDI / Cadastro" | Avisar: Validar CNPJ em base |
| Se Categoria = qualquer AND Flag = "bug" | 🔴 Prioridade Alta |

---

## 6. Integração no Painel

### Output para o Painel

Cada item classificado retorna:

```json
{
  "input_text": "...",
  "anchor_found": true,
  "primary_category": "nome da categoria",
  "category_color": "#color",
  "category_description": "...",
  "flags": ["flag1", "flag2"],
  "alerts": ["alerta 1", "alerta 2"],
  "confidence": 0.95,
  "logic_trace": "..." (para auditoria)
}
```

### Estrutura de Componentes no Painel

1. **Card Principal** — exibe `primary_category` com cor e ícone
2. **Tags de Contexto** — exibe cada flag com cor de risco
3. **Alertas** — exibição de avisos regulatórios associados
4. **Matriz Interativa** — widget mostrando qual camada (Âncora/Intenção/Contexto/Complemento) foi acionada

---

## 7. Notas Operacionais

### Palavras-chave Próximas de Falso Positivo

Investigar em implementação:
- "cancelada" vs "reemissão": ambas são intenções diferentes; usar ordem de aparição
- "100.000" vs "abaixo de R$ 100.000,00": normalizar variações antes de buscar
- "CNPJ" + contexto de "TraaS": ambos são contextos; qual prevalece? → Resposta: primeiro encontrado

### Manutenção Futura

Quando adicionar:
1. Novas palavras-chave: adicionar em `taxonomy.json` na categoria apropriada
2. Novas categorias principais: adicionar em `layer_2_intention` ou `layer_3_context`
3. Novos complementos: adicionar em `layer_4_complement.flags`

Sempre manter `examples` atualizado com novos casos.

