<div align="center">

<img src="matrixlab/static/favicon.svg" width="64" height="64" alt="Símbolo do MatrixLab">

# MatrixLab

**Da teoria à descoberta.**

Um laboratório interativo de Matemática Computacional Aplicada.<br>
Matrizes, grafos e os caminhos entre conceitos e prática.

![Versão](https://img.shields.io/badge/vers%C3%A3o-0.1.2--alpha-8b7cf8?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.2-252a3b?style=flat-square&logo=flask&logoColor=white)
![Status](https://img.shields.io/badge/entrega-fase%201%20de%205-7386ff?style=flat-square)

[Começar](#executar-localmente) · [Funcionalidades](#o-que-já-funciona) · [Arquitetura](docs/ARCHITECTURE.md) · [Próximas fases](#próximas-fases)

</div>

![MatrixLab: editor de matrizes minimalista com três abas no topo](docs/images/desktop.png)

## Sobre o projeto

O MatrixLab é um projeto acadêmico da disciplina de **Matemática Computacional Aplicada**, desenvolvido para aproximar teoria e experimentação. A proposta é permitir que o estudante edite matrizes, explore grafos ponderados e acompanhe a resolução dos problemas passo a passo.

A aplicação combina **Python e Flask** no backend com **HTML, CSS, JavaScript e SVG** no frontend. Os algoritmos matemáticos serão implementados manualmente em Python, sem NumPy, NetworkX ou bibliotecas que resolvam os cálculos.

> **Versão atual · v0.1.2-alpha — estrutura pronta para implementar os algoritmos**
>
> A fundação da Fase 1 está pronta e a integração das matrizes da Fase 2 já está preparada: editores A/B, sete operações, API validada, resultados e passos. **Os algoritmos ficam a cargo dos estudantes em `matrixlab/domain/matrizes.py`.** As funções pendentes mostram “Em desenvolvimento”. Dijkstra, edição sincronizada do grafo e importação/exportação JSON continuam pendentes.

**Vai programar as resoluções? Comece pelo [guia de implementação das matrizes](docs/IMPLEMENTAR_MATRIZES.md).** Ele explica os argumentos, os retornos e os testes. Basta preencher as sete funções no arquivo indicado; a ligação com a tela já existe.

### Uma interface mais simples

A versão 0.1.1 abre diretamente no editor de matrizes. São apenas três abas — **Matrizes, Grafos e Guia** — visíveis também no celular. A interface usa transições discretas, cores suaves e explicações que podem ser expandidas no guia. As animações respeitam a preferência por movimento reduzido.

## O que já funciona

- **Interface responsiva:** tema escuro, três abas no topo, animações suaves, estados de foco e navegação por teclado.
- **Editores A e B:** matrizes de 1×1 a 8×8, dimensões independentes, valores editáveis e restauração dos exemplos. B aparece apenas nas operações que precisam dela.
- **Operações conectadas:** adição, subtração, multiplicação, transposta, determinante, identidade e nula encaminham os dados às respectivas funções Python, ainda pendentes de resolução.
- **Resultado e passos:** apresentação de matriz ou número, resolução opcional, carregamento, mensagens de erro e cancelamento de respostas antigas após uma edição.
- **Rascunho local:** A, B e a operação são salvas no navegador. O rascunho antigo da matriz A é preservado na migração.
- **Grafo de demonstração:** explore quatro nós e cinco arestas em SVG; selecione um nó para consultar suas conexões.
- **Matriz de adjacência:** representação simétrica, somente leitura, gerada a partir dos mesmos dados do grafo.
- **Guia introdutório:** conceitos de matrizes, grafos, condições das operações e funcionamento de Dijkstra.
- **Base Flask:** API JSON, indicador de conexão, tratamento de falhas e página 404.
- **Testes Python:** cobertura da estrutura, dos endpoints e do contrato do exemplo.

Os recursos da aplicação são locais: sem CDN, fontes remotas ou serviços externos obrigatórios durante o uso. Não é necessário instalar Node.js. Os badges acima são apenas elementos do README no GitHub.

<details>
<summary><strong>Ver a interface em dispositivos menores</strong></summary>
<br>
<img src="docs/images/mobile.png" width="320" alt="MatrixLab em tela de celular, com os módulos organizados verticalmente">
</details>

## Executar localmente

**Pré-requisitos:** Python 3.10 ou superior com `pip`, Git para clonar e um navegador moderno. A instalação inicial das dependências precisa de internet; depois disso, a aplicação funciona localmente.

### 1. Obtenha o projeto

```bash
git clone https://github.com/vicenteedu/A3_matrixLab.git
cd A3_matrixLab
```

Também é possível usar **Code → Download ZIP** no GitHub, extrair o arquivo e abrir um terminal na pasta que contém `run.py`.

### 2. Instale e execute

**Windows / PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run.py
```

Se o Python estiver disponível como `python`, substitua `py` por `python` no primeiro comando. Não é necessário ativar o ambiente virtual nem alterar a política de execução do PowerShell.

**macOS / Linux**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run.py
```

### 3. Abra o laboratório

Acesse **[http://127.0.0.1:5000](http://127.0.0.1:5000)** no navegador. Para encerrar o servidor, pressione `Ctrl+C` no terminal.

<details>
<summary><strong>Solução de problemas de instalação</strong></summary>

- **Python não encontrado:** instale pelo [site oficial](https://www.python.org/downloads/), habilite a opção de adicionar ao PATH e reabra o terminal.
- **`venv` indisponível no Linux:** instale o pacote `venv` correspondente à versão do Python da sua distribuição.
- **Porta 5000 ocupada:** escolha outra porta com o comando abaixo e abra o endereço indicado no terminal.

```powershell
.\.venv\Scripts\python.exe -m flask --app matrixlab run --port 5001
```

No macOS/Linux, substitua o executável por `.venv/bin/python`.

</details>

O servidor inicia sem debug e atende somente no computador local. Esta configuração é destinada ao desenvolvimento e à apresentação acadêmica; publicação em produção exige uma configuração própria.

## Exemplo de demonstração

O grafo inicial é **não direcionado**, com pesos estritamente positivos:

```text
          B
       4 /|\ 8
        / | \
       A  2  D
        \ | /
      10 \|/ 3
          C
```

Para origem **A** e destino **D**, a referência do enunciado é:

```text
Caminho:   A → B → C → D
Distância: 4 + 2 + 3 = 9
```

**Nesta versão, esse resultado é uma referência exibida para a futura validação do algoritmo. Dijkstra ainda não é executado.** As coordenadas dos nós são apenas visuais e não determinam os pesos das arestas.

## Testes e validação

Execute os testes a partir da raiz do repositório:

**Windows / PowerShell**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**macOS / Linux**

```bash
.venv/bin/python -m unittest discover -s tests -v
```

São **31 testes: 21 aprovados e 10 pulados enquanto os algoritmos estão pendentes**. Nove verificam a base e o grafo; doze verificam a API matricial, validações, encaminhamento e tratamento de retornos; dez são casos de aceitação das resoluções. Estes últimos deixam de ser pulados quando a função correspondente é implementada.

A interface também foi verificada em Chrome com automação de navegador: navegação, persistência, validações do editor, teclado, recuperação de falha da API e cinco larguras de tela. Consulte o [registro de validação](docs/VALIDATION.md) para os cenários e limites dessa verificação.

Os testes de transporte usam funções simuladas; eles não comprovam os algoritmos. Os casos reais em `tests/test_matrizes.py` devem passar após a implementação de vocês. Dijkstra e edição sincronizada ainda terão seus próprios testes.

## Organização do código

```text
A3_matrixLab/
├── run.py                     # Inicialização do servidor local
├── requirements.txt           # Dependências Python
├── .gitignore
├── .gitattributes
├── README.md
├── matrixlab/
│   ├── __init__.py             # Application factory e rotas de página
│   ├── api/
│   │   ├── __init__.py        # Registro dos endpoints REST
│   │   └── matrices.py        # Recebe JSON e devolve resultado/erro
│   ├── domain/
│   │   ├── examples.py         # Grafo de demonstração
│   │   ├── matrix_service.py   # Validação e ligação com as funções
│   │   └── matrizes.py         # IMPLEMENTEM AS RESOLUÇÕES AQUI
│   ├── templates/             # Páginas HTML
│   └── static/
│       ├── css/app.css         # Design system e responsividade
│       ├── js/                 # Navegação, editor e visualização SVG
│       └── favicon.svg
├── tests/                     # Base, API e aceitação das resoluções
└── docs/
    ├── IMPLEMENTAR_MATRIZES.md # Guia para os estudantes
    ├── ARCHITECTURE.md         # Decisões, contratos e plano técnico
    ├── VALIDATION.md           # Evidências e checklist de validação
    └── images/                # Capturas usadas neste README
```

**Separação de responsabilidades:** Flask cuida do HTTP; o domínio Python concentrará os cálculos; JavaScript apresenta os dados e controla a interação. O histórico de Dijkstra será produzido exclusivamente pelo Python.

### API disponível

- `GET /api/health` — informa aplicação, estado e fase atual.
- `GET /api/graph/example` — retorna nós, posições, matriz de adjacência, origem, destino e referência do enunciado.
- `POST /api/matrices/calculate` — recebe `operacao` e seus argumentos, valida e chama `matrizes.py`. Devolve `resultado` e `passos`, ou erro explícito. Funções pendentes retornam HTTP 501.

No contrato JSON do grafo, `null` representa ausência de aresta e `0` é reservado à diagonal. A ordem dos nós define as linhas e colunas da matriz. O contrato matricial está detalhado no guia de implementação.

## Próximas fases

- [x] **Fase 1 — Fundação:** Flask, layout, design system, editor inicial, grafo de referência e testes da base.
- [ ] **Fase 2 — Matrizes:** adição, subtração, multiplicação, transposta, determinantes 2×2/3×3, identidade, matriz nula e resolução passo a passo em Python.
- [ ] **Fase 3 — Dijkstra:** validação do modelo, algoritmo manual, predecessores, histórico de execução e tratamento de destinos inalcançáveis.
- [ ] **Fase 4 — Editor de grafos:** criação e remoção de nós/arestas, arraste, edição de pesos, sincronização bidirecional e importação/exportação JSON.
- [ ] **Fase 5 — Aprendizagem e refinamento:** reprodução das etapas, propriedades com exemplos verificados, conteúdo educativo ampliado e testes integrados.

Veja o [plano de arquitetura](docs/ARCHITECTURE.md) para os critérios de aceitação de cada fase.

## Observações da versão alpha

- O rascunho pertence ao navegador e à origem usados; não há sincronização entre computadores.
- Reduzir uma matriz descarta as células fora das novas dimensões.
- O grafo e sua matriz de adjacência são somente leitura nesta entrega.
- O indicador de servidor é atualizado ao abrir a aplicação e ao tentar novamente um carregamento; não é monitoramento contínuo.

## Referências

- [Flask — Application factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)
- [Flask — Testes de aplicações](https://flask.palletsprojects.com/en/stable/testing/)
- [Flask — Instalação](https://flask.palletsprojects.com/en/stable/installation/)

---

<div align="center">
Projeto acadêmico de Matemática Computacional Aplicada · <a href="https://github.com/vicenteedu">vicenteedu</a><br>
<sub>MatrixLab · Pense. Conecte. Descubra.</sub>
</div>
