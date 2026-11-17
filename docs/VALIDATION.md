# Validação da Fase 1 — interface simplificada 0.1.1

Data: 17 de novembro de 2026.

## Execução confirmada

- Python 3.12 no Windows, Flask 3.1.2 instalado em ambiente virtual isolado.
- Servidor iniciado em loopback, resposta HTTP 200 para a página principal.
- 9 testes automatizados de Python aprovados, incluindo respostas da API, assets locais, erros e contrato do exemplo.
- Navegador Chrome automatizado com Playwright: navegação entre páginas, edição e restauração de matriz, redimensionamento com preservação de células, persistência após recarga e recusa de célula vazia ao redimensionar.
- Grafo: 4 nós, 5 arestas, 16 células na tabela, seleção de nó por Enter e descrição das conexões correta.
- Três abas visíveis em desktop e celular; abertura direta no editor. Guia expansível operável com Enter. Link de pular ao conteúdo preserva o módulo atual.
- Links antigos `#overview` e `#roadmap` redirecionam para Matrizes e Guia, respectivamente. Rota desconhecida retorna ao editor.
- Animação de entrada presente na preferência padrão e desativada com movimento reduzido.
- Rascunho corrompido: recuperação do exemplo com mensagem. Falha HTTP do grafo: aviso e nova tentativa bem-sucedida.
- Sem exceções JavaScript na sequência de verificação.
- Sem transbordamento horizontal da página em 15 combinações: três telas em larguras de 1440, 1024, 768, 390 e 320 px. Matriz 8×8 também verificada a 390 px com rolagem restrita ao editor.
- Capturas do editor em desktop/celular e do grafo em desktop revisadas visualmente.

## Checklist manual reproduzível

1. Inicie o aplicativo seguindo o README e confirme o indicador de conexão.
2. Navegue pelas três abas e use voltar/avançar do navegador.
3. Em Matrizes, altere A₁₁ para 12,5 (ou 12.5 conforme o navegador) e recarregue. Confirme a persistência.
4. Mude para 2×4; confira preservação das células existentes e zeros nas novas. Apague uma célula e tente alterar a dimensão: o erro deve permanecer visível. Restaure o exemplo.
5. Em Grafos, use Tab e Enter nos nós. Confira A–B=4, A–C=10, B–C=2, B–D=8 e C–D=3 na figura e na tabela simétrica.
6. Em uma janela estreita, confira as três abas visíveis. Percorra os controles com Tab, abra um tópico do Guia com Enter e confirme o foco visível.
7. Verifique que a referência A→B→C→D, distância 9, está rotulada como referência do enunciado.

## Limites desta verificação

A automação de navegador foi executada no ambiente de desenvolvimento; não há dependência de Node.js/Playwright para usar a aplicação. Os testes Python entregues são executáveis somente com as dependências do projeto e a biblioteca padrão.

Não foram realizados testes em dispositivos físicos, auditoria completa com leitor de tela nem execução em Firefox/Safari. Os testes de matemática, Dijkstra, importação/exportação e sincronização editável serão adicionados nas fases correspondentes. A inspeção do exemplo não demonstra a correção de algoritmos ainda ausentes.
