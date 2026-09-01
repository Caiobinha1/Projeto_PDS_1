# -*- coding: utf-8 -*-
"""
PROJETO DE PDS - SIMULAÇÃO E GERAÇÃO DE GRÁFICOS EM PYTHON
Este script faz todo o processamento de sinais do projeto de forma automatica:
1. Filtro de Esquecimento (IIR)
2. Filtro de Media Movel (FIR)
3. Correlacao Cruzada
4. Alteracao de Taxa (Upsampling e Downsampling)
Ele gera os arquivos de audio e os graficos de espectros para o relatorio.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import lfilter

# Configurando estilo visual dos graficos para ficar moderno e bonito
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['font.size'] = 10

# Caminho do projeto
DIRETORIO_PROJETO = r"D:\Programação\PDS\Projeto1"
ARQUIVO_VOZ = os.path.join(DIRETORIO_PROJETO, "teste.wav")
PASTA_GRAFICOS = os.path.join(DIRETORIO_PROJETO, "Graficos")
PASTA_AUDIOS = os.path.join(DIRETORIO_PROJETO, "Audios_Processados")

# Cria as pastas se nao existirem
for pasta in [PASTA_GRAFICOS, PASTA_AUDIOS]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

def gerar_audio_exemplo():
    """Gera um arquivo de voz sintetico caso o usuario ainda nao tenha gravado o seu"""
    fs = 16000  # Frequencia de amostragem de 16 kHz
    duracao = 5.0  # 5 segundos
    t = np.linspace(0, duracao, int(fs * duracao), endpoint=False)
    
    # Criando um sinal sintetico que imita a voz (soma de senoides com frequencias fundamentais e formantes)
    # 150 Hz (frequencia de voz masculina media) e harmonicos
    sinal = 0.5 * np.sin(2 * np.pi * 150 * t)
    sinal += 0.3 * np.sin(2 * np.pi * 300 * t)
    sinal += 0.2 * np.sin(2 * np.pi * 600 * t)
    # Adicionando uma variacao para parecer fala
    envelope = 0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * t)
    sinal = sinal * envelope
    # Adicionando um pouco de ruido de fundo suave
    sinal += 0.05 * np.random.normal(0, 1, len(t))
    
    # Normalizando entre -1 e 1
    sinal = sinal / np.max(np.abs(sinal))
    # Convertendo para 16-bit PCM
    sinal_int16 = np.int16(sinal * 32767)
    
    wavfile.write(ARQUIVO_VOZ, fs, sinal_int16)
    print("AVISO: Criamos um arquivo de voz de exemplo 'input_voice.wav' para voce testar!")
    print("Grave o seu proprio audio no Audacity e substitua este arquivo quando puder.")

# Verifica se o arquivo de voz existe. Se nao, gera um sintetico.
if not os.path.exists(ARQUIVO_VOZ):
    gerar_audio_exemplo()

# Lendo o arquivo de audio
fs, sinal = wavfile.read(ARQUIVO_VOZ)

# Se o audio for int16, converte para float entre -1 e 1
if sinal.dtype == np.int16:
    sinal = sinal / 32768.0

# Se for estereo (2 canais), pega apenas o primeiro canal
if len(sinal.shape) > 1:
    sinal = sinal[:, 0]

# Remove o componente DC (media do sinal) para evitar pico em 0 Hz no espectro
sinal = sinal - np.mean(sinal)

n_amostras = len(sinal)
tempo = np.arange(n_amostras) / fs

print(f"Audio carregado com sucesso. Taxa de amostragem: {fs} Hz, Total de amostras: {n_amostras} (sem offset DC)")

# =========================================================================
# GERAÇÃO DO GRÁFICO DO SINAL ORIGINAL (TEMPO E FREQUÊNCIA)
# =========================================================================
print("Gerando gráfico do sinal de voz original (onda e espectro)...")
plt.figure(figsize=(10, 8))

# Subplot 1: Formato de onda no domínio do tempo
plt.subplot(2, 1, 1)
plt.plot(tempo, sinal, color='#3182CE', alpha=0.9, linewidth=0.8)
plt.title("Formato de Onda do Sinal de Voz Original (Domínio do Tempo)")
plt.xlabel("Tempo (segundos)")
plt.ylabel("Amplitude")
plt.ylim(-1.1, 1.1)

# Subplot 2: Espectro de frequência no domínio da frequência (0 a 10 kHz)
plt.subplot(2, 1, 2)
N_fft = 8192
n_start_voice = int(2.0 * fs)
trecho_orig = sinal[n_start_voice : n_start_voice + N_fft]
fft_result = np.fft.fft(trecho_orig * np.hanning(N_fft))
fft_freqs = np.fft.fftfreq(N_fft, d=1/fs)
metade = N_fft // 2
f = fft_freqs[:metade]
magnitude = np.abs(fft_result[:metade])
magnitude = magnitude / np.max(magnitude)  # Normaliza
plt.plot(f, magnitude, color='#805AD5', alpha=0.9)
plt.title("Espectro de Frequência do Sinal de Voz Original (0 a 10 kHz)")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude Normalizada")
plt.xlim(0, 10000)

plt.tight_layout()
plt.savefig(os.path.join(PASTA_GRAFICOS, "sinal_original.png"), dpi=150)
plt.close()

# Gráfico adicional para o Sinal Original com Zoom de 0 a 2500 Hz
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(tempo, sinal, color='#3182CE', alpha=0.9, linewidth=0.8)
plt.title("Formato de Onda do Sinal de Voz Original (Domínio do Tempo)")
plt.xlabel("Tempo (segundos)")
plt.ylabel("Amplitude")
plt.ylim(-1.1, 1.1)

plt.subplot(2, 1, 2)
plt.plot(f, magnitude, color='#805AD5', alpha=0.9)
plt.title("Espectro de Frequência do Sinal de Voz Original (Zoom: 0 a 2500 Hz)")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude Normalizada")
plt.xlim(0, 2500)

plt.tight_layout()
plt.savefig(os.path.join(PASTA_GRAFICOS, "sinal_original_zoom.png"), dpi=150)
plt.close()


def salvar_audio(nome, dados_filtrados):
    """Normaliza o audio entre -1 e 1 e salva como wav de 16-bit"""
    # Formula de normalizacao do professor
    normalix = max(np.abs(np.min(dados_filtrados)), np.abs(np.max(dados_filtrados)))
    if normalix > 0:
        dados_norm = dados_filtrados / normalix
    else:
        dados_norm = dados_filtrados
        
    dados_int16 = np.int16(dados_norm * 32767)
    caminho = os.path.join(PASTA_AUDIOS, nome)
    wavfile.write(caminho, fs, dados_int16)
    return dados_norm

def plotar_e_salvar_espectro(sinais_lista, nomes_legendas, titulo, nome_arquivo_plot):
    """Calcula a FFT de cada sinal e plota os espectros em modulo (versao 0-10kHz e versao zoom 0-2500Hz)"""
    n_start_voice = int(2.0 * fs)
    N_fft = 4096

    # 1. Versao 0 a 10 kHz
    plt.figure()
    for sinal_temp, legenda in zip(sinais_lista, nomes_legendas):
        trecho = sinal_temp[n_start_voice : n_start_voice + N_fft]
        fft_result = np.fft.fft(trecho * np.hanning(N_fft))
        fft_freqs = np.fft.fftfreq(N_fft, d=1/fs)
        metade = N_fft // 2
        f = fft_freqs[:metade]
        magnitude = np.abs(fft_result[:metade])
        magnitude = magnitude / np.max(magnitude)
        plt.plot(f, magnitude, label=legenda, alpha=0.8)
        
    plt.title(f"{titulo} (0 a 10 kHz)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude Normalizada")
    plt.xlim(0, 10000)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_GRAFICOS, nome_arquivo_plot), dpi=150)
    plt.close()

    # 2. Versao Zoom (0 a 2500 Hz)
    nome_base, ext = os.path.splitext(nome_arquivo_plot)
    nome_zoom = f"{nome_base}_zoom{ext}"
    plt.figure()
    for sinal_temp, legenda in zip(sinais_lista, nomes_legendas):
        trecho = sinal_temp[n_start_voice : n_start_voice + N_fft]
        fft_result = np.fft.fft(trecho * np.hanning(N_fft))
        fft_freqs = np.fft.fftfreq(N_fft, d=1/fs)
        metade = N_fft // 2
        f = fft_freqs[:metade]
        magnitude = np.abs(fft_result[:metade])
        magnitude = magnitude / np.max(magnitude)
        plt.plot(f, magnitude, label=legenda, alpha=0.8)
        
    plt.title(f"{titulo} (Zoom: 0 a 2500 Hz)")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude Normalizada")
    plt.xlim(0, 2500)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_GRAFICOS, nome_zoom), dpi=150)
    plt.close()

# =========================================================================
# 4.1) FILTRO DE ESQUECIMENTO
# =========================================================================
print("Executando Item 4.1...")
alphas = [0.98, 0.5, -0.98, -0.5, 0.9]
sinais_4_1 = []
legendas_4_1 = []

for alpha in alphas:
    # Equacao de diferencas: y[n] = x[n] + alpha * y[n-1]
    # Coeficientes do filtro: b = [1.0], a = [1.0, -alpha]
    y = lfilter([1.0], [1.0, -alpha], sinal)
    
    # Substitui o caractere '-' por 'menos' para o nome do arquivo
    nome_arq = f"output_4_1_alpha_{'menos_' + str(abs(alpha)) if alpha < 0 else str(alpha)}.wav"
    y_norm = salvar_audio(nome_arq, y)
    
    sinais_4_1.append(y_norm)
    legendas_4_1.append(f"alpha = {alpha}")

# Gera grafico de espectro comparativo do Item 4.1
plotar_e_salvar_espectro(
    [sinal] + sinais_4_1,
    ["Original"] + legendas_4_1,
    "Espectro - Filtro de Esquecimento (Item 4.1)",
    "espectro_4_1_esquecimento.png"
)

# =========================================================================
# 4.2) FILTRO DE MÉDIA MÓVEL
# =========================================================================
print("Executando Item 4.2...")
Ms = [50, 100, 1000, 10]
sinais_4_2 = []
legendas_4_2 = []

for M in Ms:
    # Filtro de media movel de tamanho M
    # Coeficientes: b = [1/M, 1/M, ..., 1/M], a = [1.0]
    b = np.ones(M) / M
    y = lfilter(b, [1.0], sinal)
    
    nome_arq = f"output_4_2_M_{M}.wav"
    y_norm = salvar_audio(nome_arq, y)
    
    sinais_4_2.append(y_norm)
    legendas_4_2.append(f"M = {M}")

# Gera grafico de espectro comparativo do Item 4.2
plotar_e_salvar_espectro(
    [sinal] + sinais_4_2,
    ["Original"] + legendas_4_2,
    "Espectro - Filtro de Média Móvel (Item 4.2)",
    "espectro_4_2_media_movel.png"
)

# =========================================================================
# 4.3) CORRELAÇÃO DE SINAIS
# =========================================================================
print("Executando Item 4.3...")
# Segmentando 1 segundo do meio, entre t = 2s e t = 3s
n_inicio = int(2.0 * fs)
n_fim = int(3.0 * fs)

# Se o audio for muito curto por algum motivo, ajusta as amostras
if n_fim > n_amostras:
    n_inicio = max(0, n_amostras - fs)
    n_fim = n_amostras
    print("Aviso: O audio era menor que 3 segundos. Ajustamos o segmento de 1s para o final do audio.")

segmento = sinal[n_inicio:n_fim]

# Calcula a correlacao cruzada completa entre o segmento e o sinal inteiro usando numpy.convolve
# Para calcular correlacao usando convolucao, invertemos o segmento no tempo
segmento_invertido = segmento[::-1]
correlacao = np.convolve(sinal, segmento_invertido, mode='full')

# Cria o grafico de correlacao cruzada
plt.figure()
plt.plot(correlacao, color='darkblue', label='Correlação Cruzada')

# Pico teorico onde o segmento se encontra perfeitamente
# Na convolucao 'full' com segmento invertido de tamanho L_seg,
# o pico ocorre exatamente em n_inicio + L_seg - 1
L_seg = len(segmento)
indice_pico_esperado = n_inicio + L_seg - 1
plt.axvline(x=indice_pico_esperado, color='red', linestyle='--', label=f'Pico Esperado ({indice_pico_esperado})')

plt.title("Função de Correlação Cruzada (Item 4.3)")
plt.xlabel("Deslocamento (Amostras)")
plt.ylabel("Amplitude")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(PASTA_GRAFICOS, "correlacao_4_3.png"), dpi=150)
plt.close()

# =========================================================================
# 4.4) ALTERAÇÃO DE TAXA
# =========================================================================
print("Executando Item 4.4...")

# PARTE A: Upsampling por 2 (inserir zeros)
y_up = np.zeros(2 * n_amostras)
y_up[::2] = sinal

# Normaliza e salva
normalix_up = max(np.abs(np.min(y_up)), np.abs(np.max(y_up)))
y_up_norm = y_up / normalix_up
wavfile.write(os.path.join(PASTA_AUDIOS, "output_4_4_upsampled.wav"), fs, np.int16(y_up_norm * 32767))

# PARTE B: Downsampling por 2 (eliminar amostras de indice impar, no caso indice 1, 3, 5...)
# Em indexacao 0-based do Python, manter indices pares significa manter sinal[::2],
# o que elimina os indices impares (1, 3, 5...)
y_down = sinal[::2]

# Normaliza e salva
normalix_down = max(np.abs(np.min(y_down)), np.abs(np.max(y_down)))
y_down_norm = y_down / normalix_down
# Notar que a taxa de amostragem no WAV continua fs para podermos escutar a variacao de velocidade
wavfile.write(os.path.join(PASTA_AUDIOS, "output_4_4_downsampled.wav"), fs, np.int16(y_down_norm * 32767))

# Gera grafico de espectro para alteracao de taxa
# Para o upsampling, o espectro repete (espelhamento). Para o downsampling, pode haver aliasing.

# FFT do original, upsampled e downsampled baseados no trecho com voz ativa
N_fft = 4096
n_start_voice = int(2.0 * fs)
trecho_orig = sinal[n_start_voice : n_start_voice + N_fft]
trecho_up = y_up_norm[2 * n_start_voice : 2 * n_start_voice + N_fft]
trecho_down = y_down_norm[n_start_voice // 2 : n_start_voice // 2 + N_fft]

# FFT do original
fft_orig = np.abs(np.fft.fft(trecho_orig * np.hanning(N_fft)))[:N_fft//2]
freq_orig = np.fft.fftfreq(N_fft, d=1/fs)[:N_fft//2]

# FFT do Upsampled
fft_up = np.abs(np.fft.fft(trecho_up * np.hanning(N_fft)))[:N_fft//2]
freq_up = np.fft.fftfreq(N_fft, d=1/(2*fs))[:N_fft//2]

# FFT do Downsampled
fft_down = np.abs(np.fft.fft(trecho_down * np.hanning(N_fft)))[:N_fft//2]
freq_down = np.fft.fftfreq(N_fft, d=1/(fs/2))[:N_fft//2]

# 1. Versao 0 a 10 kHz
plt.figure()
plt.plot(freq_orig, fft_orig / np.max(fft_orig), label="Original", alpha=0.7)
plt.plot(freq_up, fft_up / np.max(fft_up), label="Upsampled (2x Fs)", alpha=0.7, color='green')
plt.plot(freq_down, fft_down / np.max(fft_down), label="Downsampled (0.5x Fs)", alpha=0.7, color='red')
plt.title("Espectro - Alteração de Taxa (Item 4.4 - 0 a 10 kHz)")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude Normalizada")
plt.xlim(0, 10000)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(PASTA_GRAFICOS, "espectro_4_4_taxa.png"), dpi=150)
plt.close()

# 2. Versao Zoom (0 a 2500 Hz)
plt.figure()
plt.plot(freq_orig, fft_orig / np.max(fft_orig), label="Original", alpha=0.7)
plt.plot(freq_up, fft_up / np.max(fft_up), label="Upsampled (2x Fs)", alpha=0.7, color='green')
plt.plot(freq_down, fft_down / np.max(fft_down), label="Downsampled (0.5x Fs)", alpha=0.7, color='red')
plt.title("Espectro - Alteração de Taxa (Item 4.4 - Zoom: 0 a 2500 Hz)")
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude Normalizada")
plt.xlim(0, 2500)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(PASTA_GRAFICOS, "espectro_4_4_taxa_zoom.png"), dpi=150)
plt.close()

print("Simulações concluidas com sucesso! Todos os audios e graficos foram gerados.")
