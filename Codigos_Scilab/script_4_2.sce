// =========================================================================
// PROJETO DE PDS - ITEM 4.2: FILTRO DE MÉDIA MÓVEL (FILTRO FIR)
// =========================================================================

// Limpa o console e as variaveis para comecar limpo
clc;
clear;

// Nome do arquivo de audio de entrada (localizado na pasta pai)
arquivo_entrada = "../teste.wav";

// Tenta carregar o audio usando o wavread
try
    [x, Fs] = wavread(arquivo_entrada);
catch
    disp("Erro ao usar wavread. Tentando usar a funcao audioread...");
    [x, Fs] = audioread(arquivo_entrada);
end

// Pega apenas um canal de audio (mono)
[linhas, colunas] = size(x);
if linhas > 1 then
    sinal_mono = x(1, :);
else
    sinal_mono = x'; // Garante que seja um vetor de linha
end

N = length(sinal_mono);

// Valores de M (incluindo o valor extra 10 para refletir os outros valores de M)
Ms = [50, 100, 1000, 10];

// Loop para rodar o filtro para cada valor de M
for i = 1:length(Ms)
    M = Ms(i);
    disp("Processando filtro de media movel para M = " + string(M) + "...");
    
    // Filtro h e um vetor de 1s de tamanho M, dividido por M (calcula a media)
    h = ones(1, M) / M;
    
    // Faz a convolucao do sinal de voz com o nosso filtro h
    y_completo = convol(h, sinal_mono);
    
    // Cortamos para ficar com o mesmo tamanho original N de amostras
    y = y_completo(1:N);
    
    // Normalizacao antes de salvar (faixa de -1 a 1)
    valor_minimo = min(y);
    valor_maximo = max(y);
    normalix = max(abs(valor_minimo), abs(valor_maximo));
    y_normalizado = y / normalix;
    
    // Nome do arquivo direcionando para a pasta de audios processados
    nome_saida = "../Audios_Processados/output_4_2_M_" + string(M) + ".wav";
    
    // Salva o audio processado
    try
        wavwrite(y_normalizado, Fs, nome_saida);
    catch
        audiowrite(nome_saida, y_normalizado', Fs);
    end
    
    disp("Arquivo salvo com sucesso: " + nome_saida);
end

disp("Fim do processamento do item 4.2!");
