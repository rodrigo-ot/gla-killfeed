# GLA Killfeed
O GLA Killfeed é uma ferramenta externa desenvolvida para auxiliar no controle e monitoramento das informações de renascimento dos jogadores durante as partidas GvG no Grand Line Adventures.

## Funcionalidade
**Captura de tela**: A ferramenta captura a tela em uma região específica, onde são exibidas as informações relevantes sobre os jogadores renascidos    
**Reconhecimento de texto**: Utilizando técnicas de processamento de imagem e OCR (Optical Character Recognition), o GLA Killfeed realiza a leitura das informações contidas na captura de tela.    
**Filtro de texto**: O texto capturado passa por um filtro para garantir que apenas as informações desejadas sejam consideradas, descartando possíveis ruídos ou informações irrelevantes.  
**Monitoramento em tempo real**: O GLA Killfeed atualiza continuamente as informações capturadas e exibe os dados em uma interface gráfica intuitiva.    
**Contagem regressiva**: A ferramenta conta o tempo desde o renascimento de cada jogador e exibe uma barra de progresso, indicando o tempo restante até o próximo renascimento.
## Como usar
Execute o código fornecido no ambiente de execução apropriado, com todas as dependências instaladas.    
Ajuste as coordenadas da área de captura de tela conforme necessário, para garantir que apenas as informações relevantes sejam capturadas.
## Requisitos
Python 3.x  
Bibliotecas: tkinter, pyautogui, pytesseract, cv2, numpy, time, re, fuzzywuzzy, PIL
## Limitações
O GLA Killfeed foi projetado para funcionar em um ambiente específico e para um determinado jogo.   
É necessário ajustar as coordenadas da área de captura de tela para que a ferramenta funcione corretamente.     
A precisão do reconhecimento de texto pode variar, causando registros errôneos.   
A ferramenta pode consumir recursos do sistema, devido a captura contínua da tela e o processamento de imagens.  
## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue relatando problemas, sugestões ou melhorias. Você também pode enviar um pull request com suas contribuições.

## Licença
Este projeto está licenciado sob a MIT License.
