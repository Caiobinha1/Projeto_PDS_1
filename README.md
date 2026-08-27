# Projeto 1: Processamento de Voz

Este repositório contém o código-fonte, dados e resultados do Projeto 1 da disciplina de Processamento Digital de Sinais (EEL7522) da Universidade Federal de Santa Catarina (UFSC).

## Integrantes
- Caio Missfeld Carlos (Matrícula: 22202674)
- Miguel Sória da Luz (Matrícula: 22100860)

## Estrutura do Projeto

O projeto está organizado da seguinte forma na pasta de trabalho:

- **input_voice.wav**: Arquivo de áudio original gravado (5.9 segundos, 48 kHz, mono) usado como entrada.
- **process_voice.py**: Script Python para processamento de sinais que lê o áudio original, gera as versões filtradas e salva as figuras dos gráficos.
- **relatorio_pds.pdf**: Relatório final em PDF contendo as explicações e os gráficos.
- **Codigos_Scilab/**: Pasta com os scripts Scilab (.sce) para rodar na ferramenta oficial:
  - **script_4_1.sce**: Filtro de Esquecimento (IIR) com diferentes valores de alpha.
  - **script_4_2.sce**: Filtro de Média Móvel (FIR) com diferentes tamanhos de janela M.
  - **script_4_3.sce**: Correlação Cruzada entre um trecho de 1 segundo e o áudio completo.
  - **script_4_4.sce**: Alteração de Taxa de Amostragem (Upsampling e Downsampling por fator 2).
- **Audios_Processados/**: Pasta contendo todos os áudios processados no formato WAV.
- **Graficos/**: Pasta com as imagens de espectros de frequência e de correlação.

## Como Funciona

Os algoritmos de processamento de sinais de áudio realizam as seguintes etapas:

1. **Filtragem de Esquecimento:** Aplica a equação recursiva $y[n] = x[n] + \alpha \cdot y[n-1]$. Valores positivos de $\alpha$ atenuam agudos (passa-baixas) abafando a voz, e valores negativos atenuam graves (passa-altas) deixando o som sussurrado e sibilante.
2. **Filtro de Média Móvel:** Calcula a média de uma janela de $M$ amostras, atenuando as altas frequências. Janelas pequenas ($M=10$) quase não alteram o som, enquanto janelas grandes ($M=1000$) removem a maior parte do sinal deixando apenas um zumbido grave.
3. **Correlação Cruzada:** Mede a semelhança do trecho extraído no intervalo de 2 a 3 segundos com o restante do sinal. O pico no gráfico demonstra o alinhamento de tempo exato onde o trecho original ocorreu.
4. **Alteração de Taxa:** Modifica a amostragem do sinal. O upsampling (inserção de zeros) dobra a quantidade de amostras e causa espelhamento no espectro, fazendo a voz tocar na metade da velocidade e mais grave. O downsampling (eliminação de amostras ímpares) reduz o sinal pela metade, fazendo a voz tocar acelerada (efeito esquilo) e gerando o efeito de aliasing (mascaramento espectral).
