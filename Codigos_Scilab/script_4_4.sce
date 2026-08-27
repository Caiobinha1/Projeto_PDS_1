// =========================================================================
// PROJETO DE PDS - ITEM 4.4: ALTERAÇÃO DE TAXA (REAMOSTRAGEM POR FATOR 2)
// =========================================================================

// Limpa tudo para comecar limpo
clc;
clear;

// Arquivo de audio de entrada (localizado na pasta pai)
arquivo_entrada = "../input_voice.wav";

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

// =========================================================================
// PARTE A: DOBRAR A TAXA (UPSAMPLING / EXPANSÃO POR FATOR 2)
// =========================================================================
disp("Processando Upsampling (insercao de zeros)...");

// Criamos um novo vetor de zeros com o dobro do tamanho do sinal original
y_up = zeros(1, 2 * N);

// Colocamos as amostras originais nas posicoes impares (1, 3, 5, ...)
y_up(1:2:$) = sinal_mono;

// Normalizacao antes de salvar (faixa de -1 a 1)
normalix_up = max(abs(min(y_up)), abs(max(y_up)));
y_up_normalizado = y_up / normalix_up;

// Salva o audio processado na pasta correta
nome_saida_up = "../Audios_Processados/output_4_4_upsampled.wav";
try
    wavwrite(y_up_normalizado, Fs, nome_saida_up);
catch
    audiowrite(nome_saida_up, y_up_normalizado', Fs);
end
disp("Arquivo de upsampling salvo: " + nome_saida_up);


// =========================================================================
// PARTE B: REDUZIR A TAXA (DOWNSAMPLING / DECIMAÇÃO POR FATOR 2)
// =========================================================================
disp("Processando Downsampling (remocao de amostras impares)...");

// Mantemos apenas as amostras de indices pares (2, 4, 6, ...), eliminando as impares.
y_down = sinal_mono(2:2:$);

// Normalizacao antes de salvar (faixa de -1 a 1)
normalix_down = max(abs(min(y_down)), abs(max(y_down)));
y_down_normalizado = y_down / normalix_down;

// Salva o audio processado na pasta correta
nome_saida_down = "../Audios_Processados/output_4_4_downsampled.wav";
try
    wavwrite(y_down_normalizado, Fs, nome_saida_down);
catch
    audiowrite(nome_saida_down, y_down_normalizado', Fs);
end
disp("Arquivo de downsampling salvo: " + nome_saida_down);

disp("Fim do processamento do item 4.4!");
