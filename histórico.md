Contexto para continuidade — Construção da triagem de DC-e no ServiceNow
Objetivo geral

Estou construindo uma lógica de triagem por palavras-chave e contexto para itens relacionados a DC-e (Declaração de Conteúdo Eletrônica) dentro do ServiceNow, com foco em:

melhorar a identificação de chamados/cenários relacionados a DC-e;
separar os itens por tipo de contexto operacional;
criar uma classificação em camadas;
gerar links prontos do próprio ServiceNow com filtros aplicados via sysparm_query;
usar essa lógica depois em um Painel AI / painel de apoio à triagem.
Contexto do negócio

Os cenários analisados são relacionados ao projeto de DC-e dentro da operação da Localiza, com vários contextos de emissão e não emissão, incluindo:

ativação;
emissão;
cancelamento;
reemissão;
novo destino;
desativação;
não emissão;
CNPJ / PDI / CD;
RAC / GF / 42 / 44;
VE Leves / LVE / Locavia;
TraaS / Frete / Realocação;
Pesados / Caminhões / Gateway;
contextos complementares como:
tributário;
piloto;
HML;
contingência;
XML;
bug;
fornecedor.

Também foram trazidas regras e definições de negócio como:

DC-e só deve ser emitida em situações específicas;
há cenários em que o fornecedor/transportadora deve emitir;
carta frete será substituída por DC-e em certos fluxos;
CTe / Nota Fiscal não substituem DC-e;
há contingência de CNPJ em alguns contextos;
existem cenários de ativação, cancelamento, reemissão e desativação.
Problema que estou resolvendo

Quero sair de uma busca simples por "dce" e passar para uma triagem mais inteligente, baseada em:

1. Âncora

Palavras que identificam o domínio DC-e:

dce
dc-e
dc e
declaração de conteúdo
declaração de conteúdo eletrônica
2. Intenção

Palavras que mostram o que está acontecendo no cenário:

ativação
emissão
gerar
emitir
cancelamento
cancelada
reemissão
novo destino
desativação
não emissão
3. Contexto

Palavras que mostram em qual tipo de cenário aquilo acontece:

CNPJ
PDI
fornecedor
RAC
GF
42
44
LVE
leves
locavia
TraaS
frete
realocação
seminovos
pesados
caminhões
gateway
4. Complemento

Palavras que não definem a categoria principal, mas ajudam a enriquecer a triagem:

tributário
piloto
HML
bug
contingência
XML
montadora
desenvolvimento
testes unitários
testes integrados
documentos validados
documentos disponíveis
Lógica de classificação definida

A lógica principal da triagem ficou assim:

Âncora + Intenção + Contexto + Complemento

Exemplo:

DC-e + cancelada + novo destino → cenário de Reemissão
DC-e + ativação + CNPJ + PDI → cenário de Emissão / Ativação com CNPJ/PDI
DC-e + desativação + não emissão → cenário de Desativação / Não emissão
DC-e + TraaS + frete + RAC → cenário de TraaS / Frete / Realocação
DC-e + LVE + 24 horas → cenário de VE Leves / Cancelamento / SLA
DC-e + pesados + caminhões → cenário de Pesados / Caminhões
Categorias principais da classificação
1) Emissão / Ativação

Usada quando o cenário fala em:

gerar DC-e;
emitir DC-e;
ativar processo de emissão.

Palavras fortes:

ativação
emitir
emissão
gerar
gerar uma dce
2) CNPJ / PDI / Cadastro

Usada quando o foco do cenário está em:

CNPJ utilizado;
cadastro de CNPJ;
origem do documento;
PDI / CD / localidade.

Palavras fortes:

cnpj
pdi
cadastro de cnpj
fornecedor
rac
gf
42
44
3) Reemissão / Cancelada / Novo destino

Usada quando há:

DC-e cancelada;
novo destino;
necessidade de gerar novamente.

Palavras fortes:

cancelada
cancelamento
novo destino
reemissão
a partir de uma dce cancelada
4) VE Leves / LVE

Usada quando o cenário pertence claramente ao universo de:

VE Leves;
LVE;
Locavia.

Palavras fortes:

lve
leves
ve leves
locavia
5) Regra de valor

Usada quando o cenário depende de limite/faixa de valor.

Palavras fortes:

abaixo de R$ 100.000,00
100.000
100000
abaixo de 100 mil

Também considerar variações digitadas incorretamente como pabaixo.

6) Cancelamento / SLA

Usada quando o foco é o cancelamento da DC-e, especialmente por prazo.

Palavras fortes:

cancelamento de dc-e
dentro do SLA de 24 horas
após 24 horas
24 horas
7) Desativação / Não emissão

Usada quando o cenário trata de:

operação desativação;
fluxo que não deve emitir;
regra de não emissão.

Palavras fortes:

desativação
operação desativação
não emissão
não gerar dc-e
bloqueado
8) TraaS / Frete / Realocação

Usada para operação de transporte/frete.

Palavras fortes:

traas
frete
realocação
realocação frota
realocação seminovos
rac
sn
seminovos
9) Pesados / Caminhões

Usada para a linha específica de pesados.

Palavras fortes:

pesados
caminhões
gateway
ativação pesados
10) Complementares / Apoio

Não definem a categoria principal, mas ajudam a explicar o cenário:

tributário
piloto
hml
xml
bug
contingência
testes integrados
testes unitários
documentos validados
documentos disponíveis
Cenários analisados

Foram analisados cenários reais como:

gerar uma DC-e para cada CNPJ utilizado pelos PDI’s;
gerar DC-e da GF com pedidos para 42 / 44;
gerar DC-e RAC a partir de uma DC-e cancelada com novo destino;
ativação VE leves;
gerar DC-e abaixo de R$ 100.000,00;
cancelamento de DC-e dentro e após 24 horas;
desativação VE Leves;
DC-e TraaS (Frete): RAC - Realocação Frota;
DC-e TraaS (Frete): SN - Realocação Frota;
DC-e TraaS (Frete): Operações - Desativação;
ativação - emissão de DC-e Caminhões.

A partir disso, os cenários foram agrupados em blocos principais:

Ativação + CNPJ/PDI
Reemissão / cancelada / novo destino
VE Leves + valor / SLA
Desativação / não emissão
TraaS / Frete / Realocação
Pesados / Caminhões
Estratégia de filtro em camadas

A construção da triagem foi pensada em camadas, e não em uma única palavra.

Camada 1 — identificar o universo DC-e

Base para saber se o item pertence ao assunto:

dce
dc-e
dc e
declaração de conteúdo
declaração de conteúdo eletrônica
Camada 2 — identificar intenção

Refina pelo que está acontecendo:

ativação
emissão
gerar
emitir
cancelamento
cancelada
reemissão
desativação
não emissão
Camada 3 — identificar contexto operacional

Refina pela área / linha / tipo de cenário:

cnpj
pdi
fornecedor
rac
gf
42
44
lve
leves
locavia
traas
frete
realocação
seminovos
pesados
caminhões
gateway
Camada 4 — enriquecer a leitura

Ajuda a entender o estágio ou impedimento:

tributário
piloto
hml
bug
contingência
xml
montadora
testes
Implementação no ServiceNow

A triagem passou a ser pensada com links do próprio ServiceNow usando:

incident_list.do
sysparm_query
123TEXTQUERY321 para busca textual
filtro por data usando opened_at
javascript:gs.dateGenerate(...)
Instância utilizada

https://ibmlocaliza.service-now.com/

Exemplo da estrutura usada

https://ibmlocaliza.service-now.com/incident_list.do?sysparm_query=...

Estratégia usada no filtro
uma busca textual base com 123TEXTQUERY321;
somada a um filtro de data em opened_at;
somada a uma camada de contexto adicional.
Link base construído

Foi construída uma URL base para buscar itens de DC-e a partir de uma data:

Base conceitual
busca por:
dce
dc-e
dc e
declaração de conteúdo
declaração de conteúdo eletrônica
e restringe para:
opened_at > 01/03/2026 23:59:59
Links de camadas construídos

Foram montados links separados para cada contexto principal:

Base DC-e
Emissão / Ativação
CNPJ / PDI
Cancelamento / Reemissão
VE Leves / LVE
TraaS / Frete / Realocação
Pesados / Caminhões
Desativação / Não emissão

Esses links foram pensados para serem usados:

manualmente;
no painel AI;
como ponto de partida para navegação operacional.
HTML já criado

Também foi criado um HTML explicativo para uso no Painel AI, contendo:

explicação visual da lógica de classificação;
descrição das categorias;
exemplos práticos;
estrutura de leitura da triagem;
organização visual em cards.

Arquivo gerado: painel_ai_classificacao_dce.html

O que já ficou decidido
Decisões principais
A triagem não será baseada só em “dce”.
A classificação será feita por:
Âncora
Intenção
Contexto
Complemento
O melhor formato de busca é por camadas.
O ServiceNow será usado com links prontos com sysparm_query.
A lógica deve servir tanto para:
triagem manual;
quanto painel AI / apoio operacional.
O que ainda pode ser evoluído
Próximos passos sugeridos
Revisar se a busca com 123TEXTQUERY321 está retornando corretamente na instância.
Validar se vale a pena usar:
busca textual global (123TEXTQUERY321)
ou campo específico adicional (caso exista outro campo mais preciso).
Criar um painel HTML com:
botões clicáveis para cada camada;
agrupamento por tipo de consulta;
separação entre consulta ampla e consulta específica.
Criar uma matriz de regra automática, por exemplo:
se contém cancelada + novo destino → Reemissão
se contém lve + 24 horas → Cancelamento VE Leves
se contém traas + frete + rac → TraaS RAC
Refinar os filtros para reduzir falso positivo.
Se necessário, transformar essa lógica em:
regras de classificação;
JSON;
documentação funcional;
conteúdo para painel AI.
Como eu gostaria que a conversa continuasse no próximo chat

No próximo chat, quero continuar exatamente daqui, com ajuda para:

refinar a lógica de triagem;
melhorar os filtros em camadas;
otimizar as buscas do ServiceNow;
organizar as categorias de DC-e;
criar um painel mais prático para consulta;
e, se possível, transformar isso em uma estrutura mais operacional.
O foco principal da continuidade é:
tornar a triagem mais assertiva;
reduzir ruído;
melhorar a consulta de cenários relacionados a DC-e;
estruturar melhor a classificação por contexto.
Pedido para o próximo chat

Considere todo esse contexto acima como base da conversa e me ajude a continuar a construção da triagem de DC-e no ServiceNow, com foco em:

filtros por camadas;
classificação por contexto;
melhoria das palavras-chave;
organização operacional das consultas;
e evolução do painel AI.

Se você quiser, eu também posso te entregar isso agora em uma versão ainda mais limpa, tipo:

opção 1 — resumo executivo

mais curto, para colar rápido em outro chat;

opção 2 — resumo técnico

mais focado em sysparm_query, camadas e lógica de busca;

opção 3 — prompt pronto

já escrito como um comando para colar direto no outro chat.

Se quiser, eu já faço a opção 3: prompt pronto para copiar e colar.