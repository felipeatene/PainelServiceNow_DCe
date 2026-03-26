# Plano de Validação — Painel de Triagem DC-e

**Data:** 26/03/2026  
**Versão:** 1.0  
**Status:** ⏳ Not Started (Fase 6)

---

## Resumo Executivo

Checklist de validação final antes do go-live do Painel de Triagem DC-e em produção.

**Escopo:**
- ✅ Validação técnica (browsers, responsividade, CSP)
- ✅ Validação de acessibilidade (WCAG 2.1 AA)
- ✅ Validação de negócio (regras, alertas, categorias)
- ✅ Validação de performance (carga, scroll, gráficos)

**Timeline:** 2-3 dias (execução em paralelo)  
**Aprovação necessária:** Arquiteto Tech + PM + Usuário Final

---

## Fase 6.1 — Validação Técnica

### 6.1.1 Compatibilidade de Browsers

**Objetivo:** Confirmar que `painel-triagem-dce.html` renderiza identicamente em todos os browsers alvo.

**Browsers Testados:**

| Browser | Desktop | Mobile | Status | Notas |
|---------|---------|--------|--------|-------|
| Chrome 120+ | ✓ | ✓ | [ ] | Flexbox, Grid, CSS custom properties suportadas |
| Edge 120+ | ✓ | ✓ | [ ] | Baseado em Chromium; compatibilidade esperada |
| Safari 16+ | ✓ | ✓ | [ ] | ⚠️ Verificar `detail`/`summary` native (suportado desde Safari 16) |
| Firefox 120+ | ✓ | ✓ | [ ] | SVG esperado funcionar; gráficos renderizar |
| Safari iOS 16+ | — | ✓ | [ ] | ⚠️ Verificar sticky alerts em scroll |
| Chrome Android 120+ | — | ✓ | [ ] | Viewport mobile <390px deve reflow corretamente |

**Procedure:**
1. Abrir `painel-triagem-dce.html` em cada browser
2. Verificar renderização:
   - [ ] CSS carrega (cores aparecem)
   - [ ] Layout não tem gaps/overflow
   - [ ] Fonts renderizam (se usando system fonts, sem CDN)
3. Testar interatividade:
   - [ ] Clicar em alertas (expandir/recolher se details/summary)
   - [ ] Clicar em abas de filtros (tabs devem ser CSS-only com radio input)
   - [ ] Scroll horizontal em gráficos (se necessário em mobile)
   - [ ] SVG gráficos renderizam sem garrar
4. Validar responsividade:
   - [ ] Abrir DevTools (F12)
   - [ ] Testar viewports: 390px, 640px, 768px, 1024px, 1366px, 1920px
   - [ ] Verificar quebras de linha, overflow

**Critério de Sucesso:**
- ✅ Painel é 100% funcional em todos os 6 browsers listados
- ✅ Nenhum erro no console (F12 → Console tab)
- ✅ Sem overflow horizontal em viewport ≥ 390px

**Log de Teste:**
```
Chrome 120 — [✓ PASS] CSS OK, SVG OK, responsividade OK
Edge 120 — [✓ PASS] Idêntico ao Chrome
Safari 16 — [? PENDING] Testar details/summary
...
```

---

### 6.1.2 Validação de CSP (Content Security Policy)

**Objetivo:** Confirmar que painel não viola CSP do ServiceNow Rich Text field.

**CSP Restrictions Esperadas (ServiceNow Rich Text):**
- ❌ `<script>` tags (inline ou external) bloqueadas
- ❌ `onclick`, `onload`, event handlers bloqueados
- ❌ Imports CSS externas (CDN) podem ser bloqueadas
- ✅ `<style>` inline permitido
- ✅ SVG inline permitido
- ✅ HTML tags semânticas permitidas

**Procedure:**
1. Verificar arquivo `painel-triagem-dce.html`:
   - [ ] Nenhum `<script type="text/javascript">` ou `<script src="...">` (exceto JSON-safe scripts)
   - [ ] Nenhum `onclick`, `onload` attributes
   - [ ] Nenhum `<link rel="stylesheet" href="...">` para CSS externa
   - [ ] Todos os styles em `<style>` inline no `<head>`
2. Validar SVG:
   - [ ] SVG é `<svg>...</svg>` inline (não `<img src="...">` ou `<object>`)
   - [ ] SVG não contém `<script>` embarcado
   - [ ] SVG não tem `onload` handlers
3. Simular isolamento CSP:
   - [ ] Abrir painel em SandBox/iframe (se browser permitir)
   - [ ] Verificar que estilos e interatividade funcionam sem acesso ao `window` global

**Critério de Sucesso:**
- ✅ Relatório de CSP lint mostra 0 violations
- ✅ Painel funciona identicamente quando wrapped em iframe com `sandbox="allow-same-origin"`

**Tools Recomendados:**
- CSP Header Evaluator (https://csp-evaluator.withgoogle.com/)
- Mozilla Observatory (https://observatory.mozilla.org/)
- Manual: Inspecionar cada tag com F12

---

### 6.1.3 Performance e Carga

**Objetivo:** Confirmar que painel carrega rápido em 4G/3G e não causa lag.

**Métricas Alvo:**
- ⏱️ Tempo total de download: < 500 KB
- ⏱️ Tempo de renderização HTML: < 500 ms
- ⏱️ Tempo de CSS parsing: < 200 ms
- ⏱️ Animações SVG: 60 FPS (sem frame drops)
- ⏱️ Scroll performance: 60 FPS (nenhum jank)

**Procedure:**
1. Medir tamanho do arquivo:
   ```
   ls -lh painel-triagem-dce.html
   # Output: 123 KB (exemplo) — < 500 KB ✓
   ```

2. Testar carregamento em 4G (DevTools Network):
   - [ ] Abrir painel em Chrome
   - [ ] F12 → Network tab → Throttle: "Fast 4G"
   - [ ] Reload (Ctrl+Shift+R para cache bypass)
   - [ ] Verificar: DOMContentLoaded < 1000 ms

3. Testar animações:
   - [ ] F12 → Performance tab
   - [ ] Recording durante 3 segundos de painel aberto
   - [ ] Verificar: FPS 60 contínuo (sem queda abaixo de 45 FPS)

4. Testar scroll:
   - [ ] Scroll lentamente do topo ao final do painel
   - [ ] Scroll rápido (verificar jank)
   - [ ] Usar F12 → Performance → Frame rate durante scroll

**Critério de Sucesso:**
- ✅ Arquivo < 500 KB
- ✅ Renderização < 500 ms em 4G
- ✅ Zero frame drops detectados em Performance trace

---

## Fase 6.2 — Validação de Acessibilidade (WCAG 2.1 AA)

**Objetivo:** Confirmar conformidade com WCAG 2.1 nível AA (obrigatório para portais públicos, recomendado para intranet).

### 6.2.1 Validação Automatizada

**Ferramenta:** axe DevTools ou WAVE (https://wave.webaim.org/)

**Procedure:**
1. Abrir painel em Chrome
2. Instalar axe DevTools extension (chrome web store)
3. Clicar "Scan NEW page" (ícone axe no toolbar)
4. Revisor relatório:
   - [ ] Violations: 0
   - [ ] Best Practices: < 5
   - [ ] Alerts: documentadas

**Critério de Sucesso:**
- ✅ 0 Violations encontradas
- ✅ 100% de elementos com contrast ratio ≥ 7:1 (normal text), ≥ 4.5:1 (large text)

**Log:**
```
Axe Scan Results:
✓ Critical: 0
✓ Serious: 0
✓ Moderate: 0
⚠ Minor: 2 (known: empty H3 in SVG title, acceptable redundancy in labels)
```

---

### 6.2.2 Validação Manual — Navegação por Teclado

**Objetivo:** Confirmar que painel é 100% navegável via teclado (Tab, Shift+Tab, Enter, Space).

**Procedure:**
1. Ligar **Keyboard only mode:**
   - Desconectar mouse (ou usar Windows Accessibility → Keyboard Only)
2. Começar do topo da página (Tab para primeiro elemento)
3. Seguir fluxo de navegação:
   - [ ] Tab navega por: Header → Alertas → KPIs → Filtros → Gráficos → Categorias → Matriz → Footer
   - [ ] Nenhum elemento fica "preso" (Tab saindo do elemento correto)
   - [ ] Nenhum elemento focável está escondido (visibility, display, z-index)

4. Testar interatividade:
   - [ ] Alertas: Tab até foco visível; Enter/Space expande (se details/summary)
   - [ ] Filtros (radio tabs): Tab até foco; Space para selecionar; vê conteúdo filtrado
   - [ ] Matriz (accordion): Tab até summary; Enter/Space expande detalhe
   - [ ] Cards: Tab navega cada card; visual focus presente

5. Verificar **focus visibility:**
   - [ ] :focus-visible outline aparece em TODOS os elementos focáveis (2px solid primary color, min)
   - [ ] Nenhum elemento com `outline: none` sem substituição visual
   - [ ] Contraste entre focus outline e background ≥ 3:1

**Critério de Sucesso:**
- ✅ Navegação completa do painel usando APENAS teclado
- ✅ Todos os elementos focáveis têm focus indicator visível
- ✅ Ordem de navegação é lógica (top to bottom, left to right)

**Log:**
```
Keyboard Navigation Test:
Header ✓ → Alerts [✓ focusable] → KPIs [✓ focusable x4] → Filters [✓ radio], etc.

Focus Indicator Check:
✓ 2px solid #0066cc outline em :focus-visible
✓ No outline: none without replacement
```

---

### 6.2.3 Validação de Heading Hierarchy

**Objetivo:** Confirmar que H1→H4 não têm gaps e que estrutura é semântica.

**Procedure:**
1. Abrir DevTools (F12) → Elements tab
2. Procurar por `<h1>`, `<h2>`, `<h3>`, `<h4>` tags
3. Verificar estrutura esperada:
   ```
   <h1>Painel de Triagem DC-e</h1>
   <section>
     <h2>Resumo de Classificações</h2>
     <h3>Emissão / Ativação</h3>
   </section>
   <section>
     <h2>Gráficos Analíticos</h2>
     <h3>Sankey: Fluxo...</h3>
   </section>
   ```

4. Validar:
   - [ ] H1 aparece exatamente uma vez (painel title)
   - [ ] H2 nunca salta para H4 (sem H3 no meio)
   - [ ] Cada H2 agrupa logicamente H3s subordinadas
   - [ ] Nenhum H5/H6 (usar H1-H4)

**Critério de Sucesso:**
- ✅ Heading hierarchy sem gaps
- ✅ Estrutura é lógica e reflete conteúdo

---

### 6.2.4 Validação com Screen Reader

**Objetivo:** Confirmar que painel é navigável com screen reader (NVDA/JAWS).

**Procedure (usando NVDA — gratuito):**
1. Download: https://www.nvaccess.org/
2. Instalar e abrir NVDA
3. Navegar painel:
   - [ ] NVDA anúncia: "Painel de Triagem DC-e" (H1)
   - [ ] Apertar H para pular por headings; verifica structure
   - [ ] Apertar T para pular por table; verifica matriz é lida corretamente
   - [ ] Navegadores diz labels de buttons/links (ex., "Abrir Consulta button")
4. Testar gráficos:
   - [ ] SVG tenho `<title>` e `<desc>` descrevendo conteúdo
   - [ ] NVDA consegue ler alt text (se não há, marcar como falha)

**Critério de Sucesso:**
- ✅ NVDA consegue navegar painel estruturadamente
- ✅ Gráficos têm alt text descritivo (não apenas "chart")
- ✅ Nenhuma informação importante está disponível apenas visualmente

---

## Fase 6.3 — Validação de Regras de Negócio

**Objetivo:** Confirmar que painel implementa corretamente `taxonomy.json` e `decision-matrix.md`.

### 6.3.1 Teste de Casos de Uso (10 Cenários)

**Cenário 1: Âncora OK**

```
Input: "Sistema de DC-e para frota em contingência"
Esperado: Âncora "DC-e" encontrada ✓
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Cenário 2: Âncora Missante**

```
Input: "Transporte de carga pesada sem DC-e"
Esperado: Nenhuma âncora; fora do painel
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Cenário 3: Intenção > Contexto**

```
Input: "ativação de VE Leves para CNPJ 12.345"
Esperado: Categoria = Emissão/Ativação (intenção "ativação" > contexto "CNPJ")
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
Notes: Verificar que intenção toma precedência
```

**Cenário 4: Contexto (sem Intenção)**

```
Input: "Problema com CNPJ na DC-e"
Esperado: Categoria = CNPJ/PDI/Cadastro (contexto, sem intenção clara)
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Cenário 5: Complementos (não criam categoria)**

```
Input: "DC-e em contingência HML para teste"
Esperado: Complementos "contingencia, hml" adicionados; categoria continua de intenção/contexto
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Cenário 6: Reemissão vs Cancelamento**

```
Input: "cancelada com novo destino"
Esperado: Categoria = Reemissão/Cancelada (não Cancelamento/SLA)
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
Notes: Precedência intenção > contexto decide (cancelada + novo destino = Reemissão)
```

**Cenário 7: Cancelamento/SLA**

```
Input: "cancelamento em 24 horas por descumprimento de contrato"
Esperado: Categoria = Cancelamento/SLA + Alerta: ⚠️ Prazo de 24h
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Cenário 8: Erro — NF-e + DC-e**

```
Input: "emissão de NF-e e DC-e para o mesmo transporte"
Esperado: Alerta 🔴 ERRO: "DC-e NÃO pode ser usada com NF-e"
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Cenário 9: LVE (Ves Leves)**

```
Input: "triagem de DC-e para VE Leves em região HML"
Esperado: Categoria = Emissão/Ativação + Contexto: VE Leves + Complemento: HML
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Cenário 10: TraaS (Transporte como Serviço)**

```
Input: "DC-e para operação de TraaS com frete incluído"
Esperado: Categoria = TraaS/Frete Incluído (ou Emissão com contexto TraaS)
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Log:**
```
Cenário 1: ✓ PASS
Cenário 2: ✓ PASS
...
Cenário 10: ⚠ WARN — "FretaS" foi convertido para "TraaS" manualmente; sem stemming automático
```

---

### 6.3.2 Validação de Alertas Obrigatórios

**Alerta 1: Data de Obrigatoriedade**

```
Teste: Abrir painel em data >= 06/04/2026
Esperado: Alerta "06/04/2026: Data oficial de obrigatoriedade nacional" aparece
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Alerta 2: Autorização Pré-Transporte**

```
Teste: Input item com "transporte iniciado" SEM "protocolo" ou "autorizado"
Esperado: Alerta aparece sugerindo validação de autorização
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

**Alerta 3: Uso Exclusivo**

```
Teste: Input item com "NF-e" + "DC-e" juntas
Esperado: Alerta 🔴 crítico: "DC-e APENAS para operações SEM NF-e"
Status: [✓ PASS / ⚠ WARN / ❌ FAIL]
```

---

### 6.3.3 Validação de Categorias (8 cards)

**Procedure:**
- [ ] 01 Emissão/Ativação: descrição correta, ícone, cor azul (#0066cc)
- [ ] 02 CNPJ/PDI/Cadastro: descrição correta, ícone, cor laranja (#FF9800)
- [ ] 03 Reemissão: descrição correta, ícone, cor vermelho (#FF5722)
- [ ] 04 VE Leves: descrição correta, ícone, cor roxa (#9C27B0)
- [ ] 05 Valor/Pesados: descrição correta, ícone, cor cinza (#757575)
- [ ] 06 Cancelamento: descrição correta, ícone, cor vermelho escuro (#F44336)
- [ ] 07 TraaS/Frete: descrição correta, ícone, cor cyan (#00BCD4)
- [ ] 08 Desativação: descrição correta, ícone, cor index (#3F51B5)

**Critério de Sucesso:**
- ✅ Todos os 8 cards aparecem
- ✅ Cada card tem: ícone + nome + descrição + cor única
- ✅ Descrições alinham com `taxonomy.json`

---

## Fase 6.4 — Validação de Dados Reais

**Objetivo:** Confirmar que painel funciona com dataset real (não apenas synthetic data).

### 6.4.1 Substituição de Dados Sintéticos

**Dados Atuais (Synthetic):**
```json
{
  "kpi_summary": {
    "total_items": 245,
    "success_count": 189,
    "success_percentage": 77,
    "failure_count": 12,
    "pending_count": 44
  }
}
```

**Dados Esperados (Real):**
- Extrair de ServiceNow: incidents com descrição contendo "DC-e" dos últimos 30 dias
- Contagem por categoria: 
  - [ ] Total itens: [?]
  - [ ] Emissão/Ativação: [?]
  - [ ] Reemissão: [?]
  - [ ] Cancelamento: [?]

**Procedure:**
1. Executar query ServiceNow:
   ```sql
   SELECT COUNT(*), category_derived 
   FROM incident 
   WHERE description LIKE '%DC-e%' 
   AND created >= DATE_SUB(NOW(), INTERVAL 30 DAY)
   GROUP BY category_derived
   ```

2. Substituir JSON em `painel-triagem-dce.html` com resultados reais
3. Verificar:
   - [ ] Gráficos reescalam (Sankey, Heatmap, Rings)
   - [ ] Nenhum overflow em números grandes
   - [ ] Proporções são visualmente sensatas

---

### 6.4.2 Teste de Escala

**Procedimento:**
- Testar com 10x dados (2,450 itens ao invés de 245)
- Verificar:
  - [ ] Painel ainda carrega em < 2s
  - [ ] Gráficos não garram
  - [ ] Scroll performance mantém 60 FPS

---

## Fase 6.5 — Teste de User Acceptance (UAT)

**Objetivo:** Validar que painel atende requisitos do usuário final.

### 6.5.1 Teste Funcional com Usuário

**Participants:**
- 1 Analista de Triagem DC-e
- 1 Auditor
- 1 PM

**Procedure:**
1. Preparar 5 incidents reais (não sanitizados)
2. Pedir ao analista: "Classifique esses 5 incidents usando o painel"
3. Observar:
   - [ ] Analista consegue abrir painel e entender interface (< 2 min aprendizado)
   - [ ] Classificação via painel leva menos tempo que manual
   - [ ] Analista consegue encontrar categoria correta
   - [ ] Nenhum frustração ou confusão

**Critério de Sucesso:**
- ✅ 5/5 classificações corretas
- ✅ Feedback positivo: "Interface clara", "Regras fazem sentido"
- ✅ Tempo decrescente por item (aprendizado curto)

### 6.5.2 Feedback Form

```
Escala 1-5 (1=Strongly Disagree, 5=Strongly Agree):

1. Interface é intuitiva: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
2. Alertas são claros: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
3. Classificação é precisa: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
4. Gráficos adicionam valor: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5
5. Usaria novamente: [ ] 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5

Sugestões:
________________
```

---

## Criterios de Aprovação Global

| Critério | Status | Assinado Por |
|----------|--------|--------------|
| Compatibilidade browsers (6/6) | [ ] | QA Lead |
| CSP Validation (0 violations) | [ ] | Security |
| Performance (< 500ms load) | [ ] | DevOps |
| Acessibilidade WCAG AA (0 violations) | [ ] | Accessibility |
| Validação de Regras (10/10 cenários) | [ ] | BA |
| Dados Reais (teste escala OK) | [ ] | Data Team |
| UAT (5/5 testes, 4+ feedback) | [ ] | PM + User |
| Documentação completa | [ ] | Tech Writer |

**Assinatura para Go-Live:**

- [ ] **Arquiteto Tech:** _________________ Data: ___/___/______
- [ ] **PM:** _________________ Data: ___/___/______
- [ ] **Usuário Final:** _________________ Data: ___/___/______

---

## Rollback Plan (Se necessário)

**Cenário 1: Painel está offline**
- Action: Desativar widget/link no ServiceNow; triagem volta ao manual
- Time to Recover: 5 minutos

**Cenário 2: Painel retorna categoria errada**
- Action: Desativar; revisar `decision-matrix.md`; corrigir e redeployer
- Time to Recover: 2-4 horas

**Cenário 3: Performance degradação**
- Action: Limitar dataset a últimos 7 dias (ao invés de 30); redeploy
- Time to Recover: 30 minutos

---

## Sign-Off

**Documento aprovado por:**

- [ ] **QA Analyst:** _________________ Data: ___/___/______
- [ ] **Tech Lead:** _________________ Data: ___/___/______
- [ ] **Product Manager:** _________________ Data: ___/___/______

