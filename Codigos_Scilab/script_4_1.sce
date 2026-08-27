// =========================================================================
// PROJETO DE PDS - ITEM 4.1: FILTRO DE ESQUECIMENTO (FILTRO IIR DE 1ª ORDEM)
// =========================================================================

// Limpa o console e as variaveis do Scilab para comecar do zero
clc;
clear;

// Nome do arquivo de audio de entrada (localizado na pasta pai)
arquivo_entrada = "../input_voice.wav";

// Tenta carregar o audio de voz usando o wavread
try
    [x, Fs] = wavread(arquivo_entrada);
catch
    disp("Erro ao usar wavread. Tentando usar a funcao audioread...");
    [x, Fs] = audioread(arquivo_entrada);
end

// Verifica o tamanho do sinal carregado para ver se e estereo ou mono
[linhas, colunas] = size(x);

// Vamos garantir que estamos trabalhando apenas com um canal (sinal mono)
if linhas > 1 then
    sinal_mono = x(1, :);
else
    sinal_mono = x'; // Se for vetor coluna, transformamos em linha
end

// Comprimento total do sinal de voz (numero de amostras)
N = length(sinal_mono);

// Lista com os valores de alpha que o professor pediu para testarmos (incluindo o 0.9)
alphas = [0.98, 0.5, -0.98, -0.5, 0.9];

// Loop para passar por cada valor de alpha da lista
for i = 1:length(alphas)
    alpha = alphas(i);
    disp("Processando para alpha = " + string(alpha) + "...");
    
    // Cria um vetor de zeros para guardar o sinal de saida
    y = zeros(1, N);
    
    // A primeira amostra do sinal filtrado recebe a primeira amostra do sinal de entrada
    y(1) = sinal_mono(1);
    
    // Aplica a equacao de diferencas: y[n] = x[n] + alpha * y[n-1]
    for n = 2:N
        y(n) = sinal_mono(n) + alpha * y(n-1);
    end
    
    // Normalizacao para garantir que o som nao estoure e fique entre -1 e 1
    valor_minimo = min(y);
    valor_maximo = max(y);
    normalix = max(abs(valor_minimo), abs(valor_maximo));
    y_normalizado = y / normalix;
    
    // Monta o nome do arquivo de saida direcionando para a pasta de audios processados
    if alpha < 0 then
        nome_saida = "../Audios_Processados/output_4_1_alpha_menos_" + string(abs(alpha)) + ".wav";
    else
        nome_saida = "../Audios_Processados/output_4_1_alpha_" + string(alpha) + ".wav";
    end
    
    // Salva o audio processado na pasta correta
    try
        wavwrite(y_normalizado, Fs, nome_saida);
    catch
        audiowrite(nome_saida, y_normalizado', Fs);
    end
    
    disp("Arquivo salvo com sucesso: " + nome_saida);
end

disp("Fim do processamento do item 4.1!");
