// =========================================================================
// PROJETO DE PDS - ITEM 4.3: CORRELAÇÃO DE SINAIS
// =========================================================================

// Limpa tudo para comecar limpo
clc;
clear;

// Arquivo de audio de entrada (localizado na pasta pai)
arquivo_entrada = "../teste.wav";

// Tenta carregar o audio usando o wavread ou audioread
try
    [x, Fs] = wavread(arquivo_entrada);
catch
    disp("Erro ao usar wavread. Tentando usar a funcao audioread...");
    [x, Fs] = audioread(arquivo_entrada);
end

// Garante que o sinal seja mono
[linhas, colunas] = size(x);
if linhas > 1 then
    sinal_mono = x(1, :);
else
    sinal_mono = x'; // Vetor de linha
end

N = length(sinal_mono);

// Tempo total do sinal em segundos
tempo_total = N / Fs;
disp("Tempo total do sinal: " + string(tempo_total) + " segundos.");

// Segmentar 1 segundo do sinal, entre os segundos 2 e 3 do audio original
n_inicio = round(2 * Fs) + 1;
n_fim = round(3 * Fs);

// Extrai o trecho do audio correspondente a esse intervalo de 1 segundo
segmento = sinal_mono(n_inicio:n_fim);
L_seg = length(segmento);

disp("Segmento extraido de " + string(n_inicio) + " ate " + string(n_fim) + " amostras.");

// Calcula a correlacao cruzada completa invertendo o segmento
segmento_invertido = segmento($:-1:1);
correlacao = convol(segmento_invertido, sinal_mono);

// Cria o vetor de deslocamento para o grafico
deslocamento_amostras = 1:length(correlacao);

// Plota o grafico da correlacao
clf(); // Limpa qualquer grafico aberto
plot(deslocamento_amostras, correlacao, "b");
xtitle("Funcao de Correlacao Cruzada", "Deslocamento (Amostras)", "Amplitude da Correlacao");

// Desenha a linha vertical no pico de correlacao maxima esperada (n_inicio + L_seg - 1)
indice_pico_esperado = n_inicio + L_seg - 1;
plot([indice_pico_esperado, indice_pico_esperado], [min(correlacao), max(correlacao)], "r--");

legend(["Correlacao Calculada", "Ponto de Alinhamento (Pico)"]);

disp("Fim do processamento do item 4.3. O grafico foi gerado!");
