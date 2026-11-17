# Arquitetura e plano de desenvolvimento

## Objetivo e limites da Fase 1

Criar uma fundação executável para um laboratório acadêmico local. Nesta entrega, a navegação, o editor inicial, a persistência do rascunho, a leitura da API e a inspeção do exemplo são reais. Não há resultados matemáticos simulados apresentados como cálculos. As fases 2 a 5 continuam pendentes.

## Separação de responsabilidades

O navegador envia JSON para a camada HTTP em `matrixlab/api/`. A API deve validar o contrato, chamar funções puras em `matrixlab/domain/` e transformar os resultados em JSON. O domínio não deve importar Flask. Templates e assets são servidos pelo próprio Flask, na mesma origem, sem CORS ou serviços obrigatórios.

O padrão application factory permite instanciar aplicações isoladas para testes. A base segue a [documentação oficial do Flask](https://flask.palletsprojects.com/en/stable/patterns/appfactories/).

Na Fase 2, acrescentar `domain/matrices.py`, `api/matrices.py` e `tests/test_matrices.py`. Na Fase 3, acrescentar `domain/graph.py`, `domain/dijkstra.py`, `api/graphs.py` e testes correspondentes. Separar arquivos quando a responsabilidade concreta surgir, evitando camadas vazias.

## Modelo do grafo

O contrato versionado usa `schema_version: 1`, `directed: false`, uma lista ordenada de nós `{id, x, y}`, `adjacency`, `source` e `target`. Os índices da matriz correspondem à ordem dos nós. IDs são letras únicas. A fase inicial mostra A, B, C e D. O resultado `reference` pertence apenas ao exemplo de demonstração e não será aceito como resultado de uma execução.

Invariantes a implementar na Fase 3:

- Matriz quadrada, dimensão igual ao total de nós e simetria exata.
- Zero na diagonal; `null` fora dela significa ausência de aresta.
- Todo peso de aresta deve ser um número finito estritamente positivo; rejeitar booleanos, strings, negativos, zero fora da diagonal, NaN e infinito.
- Origem e destino devem existir; podem ser iguais.
- Coordenadas são exclusivamente visuais e nunca alteram pesos.
- Remover um nó remove simultaneamente sua linha e coluna e ajusta seleções.

Na Fase 4, um único store JavaScript guardará esse modelo. Ações semânticas (`setWeight`, `addNode`, `removeNode`, `moveNode`) atualizarão o store; SVG e tabela serão projeções dele. Alterar um peso escreverá simultaneamente `[i][j]` e `[j][i]`. Nenhum componente manterá uma cópia editável própria. Importar JSON exigirá validação antes de substituir o estado. O servidor continuará sendo a autoridade de validação para cálculos.

## Cálculos e passos futuros

Operações matriciais usarão listas e laços em Python. Soma e subtração exigem dimensões iguais; multiplicação exige compatibilidade interna. Determinantes estarão limitados a 2×2 e 3×3. A geração de identidade exigirá ordem quadrada; a nula aceitará linhas e colunas. Erros terão mensagem legível e código estável. A dimensão inicial máxima de 8 mantém a UI e os históricos utilizáveis; limites do servidor deverão ser definidos e testados ao criar os endpoints.

Dijkstra utilizará busca manual do menor nó não visitado (O(V²)), relaxamento e reconstrução via predecessores. Cada evento conterá cópias independentes das distâncias, visitados e predecessores, além de nó atual, aresta examinada e descrição da atualização. A API representará distância infinita por `null` acompanhado do estado apropriado, porque infinito não é JSON válido. Empates serão resolvidos pela ordem dos nós para uma demonstração determinística. Destino inalcançável e origem igual ao destino terão respostas explícitas.

O frontend apenas reproduzirá os eventos retornados pelo Python. Nenhuma segunda implementação de Dijkstra será criada em JavaScript. Editar o grafo invalidará uma execução anterior; arrastar posições poderá preservar o histórico porque não altera a conectividade ou os pesos.

## Design system

Tokens CSS para fundo grafite, superfícies, bordas, texto secundário e violeta. Fontes nativas para execução sem downloads. Componentes reutilizáveis: painel, botão, título, navegação e estados de formulário. Ícones SVG locais. A revisão 0.1.1 abre diretamente em Matrizes e usa três abas visíveis em todas as larguras: Matrizes, Grafos e Guia. Não há sidebar nem menu recolhido. A antiga rota `#overview` redireciona para Matrizes; `#roadmap`, para o Guia. O planejamento completo permanece na documentação.

O layout usa grid/flex, foco visível, teclado nos nós e link para pular ao conteúdo. Transições em botões e campos e uma animação breve de entrada das telas são desativadas por `prefers-reduced-motion`. Explicações detalhadas ficam em elementos `details`/`summary` acessíveis por teclado.

O estado de servidor é verificado em `/api/health` na inicialização e na nova tentativa de carregamento; não é monitoramento contínuo. O rascunho da matriz é local ao navegador/origem e não sincroniza entre computadores. A importação/exportação JSON completa é trabalho da Fase 4.

## Plano e critérios de aceitação

1. **Fundação:** iniciar Flask, servir todos os assets localmente, navegar entre áreas, editar rascunho e visualizar o exemplo sem erros. Testes da API e contrato e inspeção responsiva.
2. **Matrizes:** validar operações válidas e inválidas, dimensões incompatíveis, resultados e passos em Python. Exemplos de propriedades deverão declarar condições e verificar ambos os lados.
3. **Grafos e Dijkstra:** validar modelo, caminhos alternativos, nós isolados, origem=destino, pesos inválidos, reconstrução e snapshots independentes. Exemplo A→B→C→D com custo 9 deve ser calculado pelo algoritmo.
4. **Editor:** verificar sincronização nos dois sentidos, remoção de linha/coluna, simetria, invariância do peso ao arrastar, importação inválida e round-trip JSON.
5. **Aprendizagem:** avançar/recuar/reiniciar eventos sem recalcular no JS, destacar arestas e rota, enriquecer a teoria, executar regressão e validar apresentação e acessibilidade em navegador.

Cada fase deve deixar o aplicativo executável. Os testes entregues agora são da fundação e do contrato do exemplo; não substituem os testes das funcionalidades futuras.
