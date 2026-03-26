# Sistema Declaração de Conteúdo eletrônica (DC-e)

**Manual de Orientação – Visão Geral**  
**Versão 1.0 – Outubro/2021**

> **Fonte**: conteúdo integral extraído do arquivo PDF fornecido pelo usuário ("Manual DC-e – Visão Geral.pdf"). Este .md é uma organização fiel, em texto, do manual original, com ajustes de formatação para Markdown. Ilustrações do PDF são referenciadas, mas não incorporadas como imagens. 
  

---

## Sumário

- [Acrônimos](#acrônimos)
    
- [1. Introdução](#1-introdução)
    
- [2. Considerações Iniciais](#2-considerações-iniciais)
    
    - [2.1. Objetivos do Projeto](#21-objetivos-do-projeto)
        
    - [2.2. Conceito da DCe](#22-conceito-da-dce)
        
        - [2.2.1. DACE](#221-dace)
            
        - [2.2.2. Modelo Conceitual da DCe](#222-modelo-conceitual-da-dce)
            
        - [2.2.3. Modelos de emissão da DCe](#223-modelos-de-emissão-da-dce)
            
        - [2.2.4. Chave de Acesso](#224-chave-de-acesso)
            
            - [2.2.4.1. Cálculo do Dígito Verificador (DV)](#2241-cálculo-do-dígito-verificador-dv)
                
    - [2.3. Descrição Simplificada do Modelo Operacional](#23-descrição-simplificada-do-modelo-operacional)
        
        - [2.3.1. Autorização de Uso](#231-autorização-de-uso)
            
- [3. Eventos](#3-eventos)
    
    - [3.1. Tipos de Evento](#31-tipos-de-evento)
        
- [4. Arquitetura de Comunicação](#4-arquitetura-de-comunicação)
    
    - [4.1. Modelo Conceitual](#41-modelo-conceitual)
        
    - [4.2. Padrões Técnicos](#42-padrões-técnicos)
        
        - [4.2.1. Padrão de Documento XML](#421-padrão-de-documento-xml)
            
        - [4.2.2. Padrão de Comunicação](#422-padrão-de-comunicação)
            
        - [4.2.3. Padrão de Certificado Digital](#423-padrão-de-certificado-digital)
            
        - [4.2.4. Padrão de Assinatura Digital](#424-padrão-de-assinatura-digital)
            
        - [4.2.5. Resumo dos Padrões Técnicos](#425-resumo-dos-padrões-técnicos)
            
        - [4.2.6. Colunas das Tabelas de Leiaute](#426-colunas-das-tabelas-de-leiaute)
            
    - [4.3. Modelo Operacional](#43-modelo-operacional)
        
        - [4.3.1. Número do Protocolo](#431-número-do-protocolo)
            
        - [4.3.2. Ambientes de Homologação e de Produção](#432-ambientes-de-homologação-e-de-produção)
            
        - [4.3.3. Validação da Estrutura XML](#433-validação-da-estrutura-xml)
            
        - [4.3.4. Schemas XML](#434-schemas-xml)
            
    - [4.4. Versão dos Schemas](#44-versão-dos-schemas)
        
        - [4.4.1. Controle de Versão](#441-controle-de-versão)
            
        - [4.4.2. Liberação de Versões](#442-liberação-de-versões)
            
- [5. Web Services (WS)](#5-web-services-ws)
    
    - [5.1. DCeAutorizacao](#51-dceautorizacao)
        
    - [5.2. DCeConsultaProtocolo](#52-dceconsultaprotocolo)
        
    - [5.3. DCeStatusServico](#53-dcestatusservico)
        
    - [5.4. DCeRecepcaoEvento – Parte Geral](#54-dcerecepcaoevento-–-parte-geral)
        
    - [5.5. DCeRecepcaoEvento – Cancelamento](#55-dcerecepcaoevento-–-cancelamento)
        
- [6. Consulta Pública da DCe](#6-consulta-pública-da-dce)
    
    - [6.1. Consulta da DCe](#61-consulta-da-dce)
        
    - [6.2. Consulta via QR-Code](#62-consulta-via-qr-code)
        
- [7. Contingência offline da DCe](#7-contingência-offline-da-dce)
    
    - [7.1. Detalhes técnicos da contingência](#71-detalhes-técnicos-da-contingência)
        
- [8. Tabelas e Códigos](#8-tabelas-e-códigos)
    
    - [8.1. Tabela de Código de UF do IBGE](#81-tabela-de-código-de-uf-do-ibge)
        
    - [8.2. Tabela de Código de Município do IBGE (Capitais)](#82-tabela-de-código-de-município-do-ibge-capitais)
        

---

## Acrônimos

**BACEN**: Banco Central do Brasil  
**CNPJ**: Cadastro Nacional de Pessoas Jurídicas  
**CONFAZ**: Conselho Nacional de Política Fazendária  
**COTEPE**: Comissão Técnica Permanente do ICMS  
**CPF**: Cadastro de Pessoas Físicas  
**CT-e**: Conhecimento de Transporte Eletrônico  
**DACE**: Declaração Auxiliar de Conteúdo eletrônica  
**DF**: Distrito Federal  
**DV**: Dígito Verificador  
**ENAT**: Encontro Nacional de Administradores Tributários  
**ENCAT**: Encontro Nacional de Coordenadores e Administradores Tributários Estaduais  
**HTTPS**: Hypertext Transfer Protocol Secure  
**IBGE**: Instituto Brasileiro de Geografia e Estatística  
**ICMS**: Imposto sobre Operações relativas à Circulação de Mercadorias e Prestação de Serviços  
**ICP-Brasil**: Infraestrutura de Chaves Pública Brasileira  
**GNU Gzip**: Protocolo de compactação  
**LCR**: Lista de Certificados (digitais) Revogados  
**NCM**: Nomenclatura Comum do Mercosul  
**NSU**: Número Sequencial Único  
**Procergs**: Companhia de Processamento de Dados do Rio Grande do Sul  
**PRODEB**: Companhia de Processamento de Dados da Bahia  
**QR-Code**: Quick Response Code  
**RFB**: Receita Federal do Brasil  
**RSA**: Rivest-Shamir-Adleman  
**SEFAZ**: Secretaria de Fazenda/Finanças/Tributação  
**SHA1**: Secure Hash Algorithm 1  
**SINIEF**: Sistema Nacional de Informações Econômico-Fiscais  
**SOAP**: Simple Object Access Protocol  
**SSL**: Secure Socket Layer  
**SRE**: Sistema de Registro de Eventos  
**SVBA**: Sefaz Virtual da Bahia  
**SVRS**: Sefaz Virtual do Rio Grande do Sul  
**TLS**: Transport Layer Security  
**UF**: Unidade Federada  
**URI**: Uniform Resource Identifier  
**XML**: Extensible Markup Language  
**XSD**: XML Schema Definition  
**W3C**: World Wide Web Consortium  
**WS**: Web Service  
**WSDL**: Web Services Description Language

---

## 1\. Introdução

Define as especificações e os critérios técnicos para integração entre Portais das SEFAZ estaduais e os sistemas dos emissores na emissão da **Declaração de Conteúdo eletrônica (DC-e)**. O conjunto de documentação é composto por: Visão Geral (este manual), Anexo I (Leiaute DC-e e Regras de Validação), Anexo II (Especificações Técnicas da DACE e QR-Code) e Anexo III (Credenciamento). Ao longo do manual, o acrônimo **DCe** é utilizado para todas as situações aplicáveis.

---

## 2\. Considerações Iniciais

A DCe é desenvolvida de forma integrada pelas SEFAZ e instituída pelo **Ajuste SINIEF 05/2021**, em substituição à declaração de conteúdo em papel (Protocolo ICMS 32/2001).

### 2.1. Objetivos do Projeto

Implantar um **modelo nacional** de declaração de conteúdo **eletrônica**, substituindo o papel, com maior visibilidade e acompanhamento **em tempo real**.

### 2.2. Conceito da DCe

Documento **exclusivamente digital**, emitido e armazenado eletronicamente, para **operações sem exigência de documento fiscal**, com validade jurídica garantida por **autorização de uso** e **assinatura digital** pela Administração Tributária, Marketplace, usuário emitente ou transportadora **antes do início do transporte**.

#### 2.2.1. DACE

A **Declaração Auxiliar de Conteúdo eletrônica (DACE)** é a representação simplificada (papel ou eletrônico) **apenas para consulta**. Contém **chave de acesso** e **QR-Code**, permitindo confirmar a existência e a autorização da DCe no portal da SEFAZ. O QR-Code e o código de barras devem estar **visíveis na embalagem** do produto.

#### 2.2.2. Modelo Conceitual da DCe

1. O usuário emitente gera a DCe (XML) e envia para **autorização**.
    
2. Após autorizada, apresenta a **DACE** para a transportadora, que valida a DCe e inicia o transporte.
    
3. Durante o transporte, a fiscalização pode ler a DACE e verificar a **validade da DCe**.
    

#### 2.2.3. Modelos de emissão da DCe

1. **Aplicativo do Fisco** – Emissão pelo app da SEFAZ; assinatura digital pelo **certificado da SEFAZ**.
    
2. **Marketplace** – Emissão para clientes (CPF/CNPJ não contribuinte); assinatura pelo **certificado do Marketplace**.
    
3. **Emissão Própria** – Usuário emitente (CNPJ não contribuinte) integra seu sistema; assinatura pelo **certificado do próprio emitente (CNPJ)**.
    
4. **Transportadora** – Emissão para clientes (CPF/CNPJ não contribuinte); assinatura pelo **certificado da Transportadora**.
    

#### 2.2.4. Chave de Acesso

A **Chave de Acesso** da DCe possui **44 dígitos**, formada por:

| Posição | Informação | Tam | Campo | Id |
| --- | --- | --- | --- | --- |
| 1 | Código da UF do emitente | 02 | cUF | B02 |
| 2 | Ano e mês de emissão | 04 | AAMM | (de B09) |
| 3 | CNPJ (SEFAZ/Marketplace/Transportadora/Emitente) | 14 | CNPJ | C02 |
| 4 | Modelo da Declaração | 02 | mod (99) | B06 |
| 5 | Série | 03 | serie | B07 |
| 6 | Número | 09 | nDC | B08 |
| 7 | Forma de emissão | 01 | tpEmis | B22 |
| 8 | Tipo do emitente (0 App Fisco / 1 Market / 2 Próprio / 3 Transp.) | 01 | tpEmit | B08a |
| 9 | Site Autorizador | 01 | nSiteAutoriz | B08b |
| 10 | Código Numérico | 06 | cDC | B03 |
| 11 | Dígito Verificador | 01 | cDV | B23 |

> O **DV** garante a integridade da chave. O **cDC** deve ser **aleatório**. 
  

##### 2.2.4.1. Cálculo do Dígito Verificador (DV)

- Baseado em **módulo 11**.
    
- Multiplicar cada dígito pela sequência: 2,3,4,5,6,7,8,9,2,3,... (da direita para a esquerda).
    
- Somar os produtos, dividir por 11 e calcular **DV = 11 – resto**.
    
- Se **resto = 0 ou 1**, então **DV = 0**.
    
- O manual apresenta um **exemplo completo** cuja soma ponderada é 644; 644 ÷ 11 = 58 resto 6; DV = 5.
    

### 2.3. Descrição Simplificada do Modelo Operacional

- Usuário (CPF) deve estar **cadastrado no gov.br**.
    
- Acessa o portal/aplicativo e **gera a DCe (XML)**.
    
- Transmite o XML à SEFAZ da **UF do emitente**.
    
- Recebe protocolo de **Autorização de Uso** (validade jurídica).
    
- A SEFAZ disponibiliza **consulta** pública (chave de acesso).
    
- Para o trânsito: imprimir **DACE** (chave, QR-Code, código de barras e **protocolo de autorização**).
    
- O sistema DCe implementa o conceito de **Evento** (ex.: cancelamento).
    

#### 2.3.1. Autorização de Uso

- Arquivo eletrônico é **assinado** e **transmitido**.
    
- A SEFAZ valida e devolve **Autorização de Uso**.
    
- **A DCe não desobriga** a emissão de NF-e, NFC-e ou outros **DF-e** e **não os substitui**.
    

---

## 3\. Eventos

Evento = registro de ocorrência relacionada à DCe após a autorização (p. ex., **cancelamento**).

- Mensagens **XML** enviadas por WS específico (modelo genérico, parte **comum + específica**).
    
- Conteúdo mínimo: **autor**, **identificação do evento**, **chave da DCe**, **dados específicos** e **assinatura digital**.
    

### 3.1. Tipos de Evento

A DCe **possui apenas** o evento **Cancelamento**, conforme **Cláusula 11 do Ajuste SINIEF 05/2021**.

---

## 4\. Arquitetura de Comunicação

### 4.1. Modelo Conceitual

Serviços disponibilizados pelas SEFAZ:

- Software/Aplicativo emissor da DCe
    
- WS **Autorização**
    
- WS **Consulta** situação
    
- WS **Status do Serviço**
    
- WS **Registro de Eventos**
    
- **Consulta Pública** da DCe
    

Todos os serviços são **síncronos**.

### 4.2. Padrões Técnicos

#### 4.2.1. Padrão de Documento XML

- XML 1.0 (W3C) e **UTF-8**; declaração única .
    
- Um **único namespace** no elemento raiz, **sem prefixos**. Ex.: .
    
- **Otimização**: não incluir tags vazias, zeros não significativos, comentários, anotações, formatação/whitespace entre tags, nem prefixos de namespace.
    
- **Validação por XSD** obrigatória.
    
- **Caracteres especiais** no texto XML devem usar _escape_ (`<`, `>`, `&`, `"`, `'`).
    

#### 4.2.2. Padrão de Comunicação

- **Web Services** com **SOAP 1.2**, estilo **Document/Literal**.
    
- **TLS 1.2+** com **autenticação mútua** (certificados cliente/servidor).
    
- Mensagens trafegam no parâmetro **`dceDadosMsg`** (ou `dceDadosMsgZip` para compactado).
    

#### 4.2.3. Padrão de Certificado Digital

- Certificado **ICP-Brasil** (A1 ou A3), contendo o **CNPJ** do titular no OID `2.16.76.1.3.3`.
    

#### 4.2.4. Padrão de Assinatura Digital

- Padrão **XML Digital Signature** (_enveloped_).
    
- Evitar incluir elementos redundantes do certificado dentro do XML (ex.: `X509IssuerSerial`, `RSAKeyValue`, etc.).
    
- Assinatura aplicada ao elemento **`infDCe`** (atributo `Id` = `DCe` + **chave de acesso**). O atributo `URI` de `Reference` deve conter `#DCe...`.
    
- Parâmetros principais:
    
    - **RSA + SHA-1**; **Base64**; **Transforms**: `enveloped-signature` + **C14N**.
        
    - Cadeia de certificação: **EndCertOnly** (somente certificado do usuário final).
        
- **QR-Code** em emissões **offline** deve ser **assinado** com o mesmo certificado utilizado na DCe.
    

#### 4.2.5. Resumo dos Padrões Técnicos

- WS conforme **WS-I Basic Profile 1.1**.
    
- Transporte: **Internet + TLS 1.2** (mútua).
    
- Padrão de mensagem: **SOAP 1.2** + **XML Doc/Lit**.
    
- Certificado: **X.509 v3** (ICP-Brasil; A1/A3; com CNPJ).
    
- Assinatura: **XMLDSIG** (RSA + SHA-1; `enveloped`; `C14N`).
    
- Validação de assinatura: integridade, autoria e **cadeia** (com **LCR**).
    
- Preenchimento XML: suprimir tags opcionais sem conteúdo; máscaras de números/datas definidas nos XSD; **ponto** como separador decimal.
    

#### 4.2.6. Colunas das Tabelas de Leiaute

- **#** (referência), **Campo** (tag), **Ele** (A/Id/G/CG/E/CE), **Pai**, **Tipo** (C/N/D/DH), **Ocor.** (cardinalidade), **Tam.** (formato), **Descrição/Observação**.
    
- Notações de tamanho: `x`, `x-y`, `xvn`, `xv(n-m)`, `(x-y)v(n-m)`, lista de valores fixos.
    

### 4.3. Modelo Operacional

Serviços **síncronos**.

#### 4.3.1. Número do Protocolo

Formado por: **Tipo Autorizador (1/3)** + **UF (2)** + **Ano (2)** + **Site (1)** + **Sequencial (10)** = **16 dígitos**.

- Tipo Autorizador: `1=SEFAZ Estadual`, `3=SVRS`.
    

#### 4.3.2. Ambientes de Homologação e de Produção

Dois ambientes (Homologação e Produção). O uso exige **credenciamento prévio** na UF.

#### 4.3.3. Validação da Estrutura XML

- Controle por **versão** de leiaute.
    
- Aplicativo deve **gerar** mensagens válidas e **informar a versão** no cabeçalho (`versaoDados`).
    

#### 4.3.4. Schemas XML

- Toda mudança de leiaute implica **atualização** do XSD.
    
- Versões identificadas com sufixo `_v` (ex.: `DCe_v1.03.xsd`).
    
- **Tipos básicos** em XSDs comuns (ex.: `tiposBasico_v1.00.xsd`); alterações **propagam** versão.
    

### 4.4. Versão dos Schemas

#### 4.4.1. Controle de Versão

Definição nacional da **versão vigente** e das **anteriores suportadas**.

#### 4.4.2. Liberação de Versões

Schemas da DCe são publicados no **Portal Nacional** via **Pacotes de Liberação (PL_###.zip)**, numerados sequencialmente.

---

## 5\. Web Services (WS)

### 5.1. DCeAutorizacao

- **Função**: recepção da DCe.
    
- **Processo**: **síncrono**. Método: `dceAutorizacao` (e `DCeAutorizacaoZip` para compactado GZip + Base64 em `dceDadosMsgZip`).
    
- **Entrada**: XML da DCe (até **1 DCe** por envio).
    
- **Retorno**: XML `retDCe` com: ambiente, versão, app, **cStat/xMotivo**, UF, **dhRecbto** e, quando cabível, **protDCe**.
    
- **Validações**: Certificado de Transmissão, validações iniciais, área de dados, **Certificado de Assinatura**, **Assinatura Digital** (regras específicas no Anexo I).
    
- **Resultados possíveis**: **Rejeição** (descarta; pode reenviar corrigido) ou **Autorização de Uso** (armazenada em BD).
    

### 5.2. DCeConsultaProtocolo

- **Função**: consultar situação **atual** da DCe.
    
- **Processo**: **síncrono**. Método: `dceConsulta`.
    
- **Entrada**: `consSitDCe` com **chave de acesso (44)**.
    
- **Retorno**: `retConsSitDCe` com ambiente, versão, app, **cStat/xMotivo**, UF, **dhRecbto**, **chDCe** e, quando aplicável: **protDCe**, **procEventoDCe**, e os XML **DCe/eventos** (se o certificado pertencer ao **mesmo CNPJ base** de ator legítimo ou transportadora habilitada **no prazo de 3 meses** da autorização).
    
- **Validações**: ambiente/site/UF, **formação da chave** (modelo 99, DV, UF, CNPJ/CPF, mês/ano, tipo de emissão/emitente), **antiguidade** (até 6 meses, a critério da UF), **existência** na base.
    
- **Final**: `cStat` como “100 – Autorizado o uso” ou “101 – Cancelamento homologado”, entre outros.
    

### 5.3. DCeStatusServico

- **Função**: consultar **status** do serviço do Portal da SEFAZ.
    
- **Processo**: **síncrono**. Método: `dceStatusServico`.
    
- **Entrada**: `consStatServ` com **tpAmb**, **cUF** e `xServ=STATUS`.
    
- **Retorno**: `retConsStatServ` com ambiente, versão, app, **cStat/xMotivo**, UF, **dhRecbto**, **tMed**, **dhRetorno**, **xObs**.
    
- **Códigos**: “**107 – Serviço em Operação**”, “108 – Paralisado Temporariamente” e “109 – Paralisado sem Previsão”.
    

### 5.4. DCeRecepcaoEvento – Parte Geral

- **Função**: recepção de **eventos** da DCe (lotes de **1 a 20** eventos).
    
- **Estrutura (entrada)**: `evento` (versão) > `infEvento` (Id, cOrgao, tpAmb, **tpEmit**, **CNPJAutor**, CNPJ/CPF/Id do **Usuário Emitente**, **chDCe**, **dhEvento**, **tpEvento**, **nSeqEvento**, **verEvento**, `detEvento` com XML **específico**).
    
- **Assinatura**: sobre **`infEvento`**, e o certificado deve ser do **mesmo CNPJ base do CNPJAutor**.
    
- **Retorno**: `retEvento` com dados do processamento, incluindo **cStat/xMotivo**, **dhRegEvento**, **nProt** (quando aplicável) e assinatura opcional do órgão.
    
- **Validações genéricas**: Id consistente (`ID` + `tpEvento` + `chDCe` + `nSeqEvento`), UF/ambiente/site coerentes, chave válida (estrutura e DV), **autor = emissor** da DCe, data do evento não futura (tolerância 5 min), habilitação do emissor, existência da DCe, **duplicidade** de evento (mesmo tipo + chave + sequência), etc.
    

### 5.5. DCeRecepcaoEvento – Cancelamento

- **Autor**: **emissor** da DCe; DCe deve **existir** no BD; assina com **certificado do emissor** (CNPJ matriz ou qualquer filial – mesmo **CNPJ base**).
    
- **Código do evento**: **110111 – Cancelamento**.
    
- **Entrada (parte específica)**: `versao` (igual a `verEvento`), `descEvento`, `nProt` (protocolo de autorização da DCe), `xJust` (justificativa **15-255** caracteres).
    
- **Retorno**: `retEvento` (xEvento: **“Cancelamento homologado”** quando sucesso).
    
- **Validações específicas** (exemplos): UF coerente; autor = emissor; **nSeqEvento = 1**; órgão autor = UF da chave; tipo do autor compatível; emissor habilitado; **chave existe**; prazo de **24h** para cancelamento **normal** (UF pode homologar **fora do prazo** com `cStat=155`); data do evento ≥ emissão/autorização (tolerância **5 min**); **nProt** confere; não pode cancelar **já cancelada**; impedir **duplicidade**.
    

---

## 6\. Consulta Pública da DCe

### 6.1. Consulta da DCe

No portal das Administrações Tributárias: digitar a **chave de 44 dígitos** ou ler o **QR-Code** da DACE.

### 6.2. Consulta via QR-Code

A aplicação verifica consistência entre parâmetros do **QR-Code** e o conteúdo da **DCe**. Resultados/avisos exemplares:

| Código | Regra/Condição | Mensagem |
| --- | --- | --- |
| 201 | Chave de Acesso ausente ou < 44 dígitos | Problemas no preenchimento da Chave de Acesso |
| 202 | DV inválido | Problemas na Chave de Acesso (dígito verificador inválido) |
| 203 | Modelo ≠ 99 **ou** CNPJ inválido **ou** UF divergente | Problemas na Chave de Acesso (modelo/CNPJ/UF inválido) |
| 204 | `tpAmb` ausente ou ≠ 1/2 | Inconsistência no QR-Code (tipo ambiente) |
| 205 | `tpEmis=1` e DCe inexiste na base | DCe inexistente |
| 206 | `tpEmis=2` e DCe não encontrada **mas assinatura do QR-Code válida** | DCe emitida em contingência e assinatura do QR-Code **VÁLIDA**; consulte novamente após 24h |
| 207 | `tpEmis=2` e assinatura do QR-Code **inválida** | DCe inválida (assinatura do QR-Code inválida) |
| 208 | DCe possui evento de **cancelamento** | DCe foi Cancelada – Documento Inválido |

---

## 7\. Contingência offline da DCe

Modalidade para **exceção** (problemas técnicos).

- Emitente pode **emitir em contingência**, imprimir a **DACE** e **transportar**; deve **transmitir** a DCe para autorização até o **final do primeiro dia útil subsequente**.
    
- Recomenda-se priorizar emissão **em tempo real**. UF pode **restringir** uso indevido.
    

### 7.1. Detalhes técnicos da contingência

- Indicar **`tpEmis = 9`** (contingência offline).
    
- DACE deve conter a expressão **“EMITIDO EM CONTINGÊNCIA”**.
    
- **QR-Code** deve conter o parâmetro **`sign`**, com **assinatura digital da chave de acesso** usando o **mesmo certificado** da DCe (garante autoria e permite informar prazo para constar na base).
    

---

## 8\. Tabelas e Códigos

### 8.1. Tabela de Código de UF do IBGE

| Região Norte | Região Nordeste | Região Sudeste | Região Sul | Região Centro-Oeste |
| --- | --- | --- | --- | --- |
| 11-RO · 12-AC · 13-AM · 14-RR · 15-PA · 16-AP · 17-TO | 21-MA · 22-PI · 23-CE · 24-RN · 25-PB · 26-PE · 27-AL · 28-SE · 29-BA | 31-MG · 32-ES · 33-RJ · 35-SP | 41-PR · 42-SC · 43-RS | 50-MS · 51-MT · 52-GO · 53-DF |

### 8.2. Tabela de Código de Município do IBGE (Capitais)

| Município | Código | Estado | UF |
| --- | --- | --- | --- |
| Aracaju | 2800308 | Sergipe | 28 |
| Belém | 1501402 | Pará | 15 |
| **Belo Horizonte** | **3106200** | **Minas Gerais** | **31** |
| Boa Vista | 1400100 | Roraima | 14 |
| Brasília | 5300108 | Distrito Federal | 53 |
| Campo Grande | 5002704 | Mato Grosso do Sul | 50 |
| Cuiabá | 5103403 | Mato Grosso | 51 |
| Curitiba | 4106902 | Paraná | 41 |
| Florianópolis | 4205407 | Santa Catarina | 42 |
| Fortaleza | 2304400 | Ceará | 23 |
| Goiânia | 5208707 | Goiás | 52 |
| João Pessoa | 2507507 | Paraíba | 25 |
| Macapá | 1600303 | Amapá | 16 |
| Maceió | 2704302 | Alagoas | 27 |
| Manaus | 1302603 | Amazonas | 13 |
| Natal | 2408102 | Rio Grande do Norte | 24 |
| Palmas | 1721000 | Tocantins | 17 |
| Porto Alegre | 4314902 | Rio Grande do Sul | 43 |
| Porto Velho | 1100205 | Rondônia | 11 |
| Recife | 2611606 | Pernambuco | 26 |
| Rio Branco | 1200401 | Acre | 12 |
| Rio de Janeiro | 3304557 | Rio de Janeiro | 33 |
| Salvador | 2927408 | Bahia | 29 |
| São Luís | 2111300 | Maranhão | 21 |
| São Paulo | 3550308 | São Paulo | 35 |
| Teresina | 2211001 | Piauí | 22 |
| Vitória | 3205309 | Espírito Santo | 32 |

> Para operações com **exterior**, utilizar **código 9999999** e município “EXTERIOR”. Em regiões administrativas (ex.: cidades-satélites do DF), considerar o **município sede**. 
  

---

## Apêndices (referências a esquemas citados)

- **DCe_v1.00.xsd**, **retDCe_v1.00.xsd**
    
- **consSitDCe_1.00.xsd**, **retConsSitDCe_v1.00.xsd**
    
- **consStatServ_v1.00.xsd**, **retConsStatServ_1.00.xsd**
    
- **Evento_v1.00.xsd**, **retEvento_v1.00.xsd**
    
- **envEventoCancDCe_v1.00.xsd** (tpEvento=110111)
    

---

### Observações Finais

- Este Markdown reflete fielmente o conteúdo do **Manual DC-e – Visão Geral – v1.0 (Out/2021)**, organizado para leitura técnica e implementação.
    
- Tabelas, regras e estruturas foram mantidas; figuras mencionadas no PDF foram **omitidas**.