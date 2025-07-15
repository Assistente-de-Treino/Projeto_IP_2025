import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
<<<<<<< HEAD
from config import CAMINHO_ARQUIVO_CSV, COLUNAS_OBRIGATORIAS

def calcular_imc(peso, altura_cm):
=======
from config import CSV_FILE_PATH, REQUIRED_COLUMNS


def calcular_imc(peso, altura_cm):
    """Calcula o Índice de Massa Corporal."""
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
    if altura_cm <= 0:
        return 0
    altura_m = altura_cm / 100
    return peso / (altura_m ** 2)

<<<<<<< HEAD
def classificar_imc(imc):
=======
def classificacao_imc(imc):
    """Retorna a classificação do IMC."""
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
    if imc < 18.5: return "Abaixo do peso"
    elif 18.5 <= imc < 24.9: return "Peso normal"
    elif 25 <= imc < 29.9: return "Sobrepeso"
    elif 30 <= imc < 34.9: return "Obesidade Grau I"
    elif 35 <= imc < 39.9: return "Obesidade Grau II"
    else: return "Obesidade Grau III (Mórbida)"

<<<<<<< HEAD
def obter_tempo_aerobico(classificacao_imc):
    if "Obesidade" in classificacao_imc or "Sobrepeso" in classificacao_imc:
        return "30-45 min"
    elif "Peso normal" in classificacao_imc:
        return "20-30 min"
    else: 
        return "15-20 min"

def carregar_dados_exercicios():
    try:
        if not os.path.exists(CAMINHO_ARQUIVO_CSV):
            raise FileNotFoundError
        
        df = pd.read_csv(CAMINHO_ARQUIVO_CSV)
=======
def tempo_cardio(imc_classification):
    """Retorna o tempo de aeróbico recomendado."""
    if "Obesidade" in imc_classification or "Sobrepeso" in imc_classification:
        return "30-45 min"
    elif "Peso normal" in imc_classification:
        return "20-30 min"
    else: # Abaixo do peso
        return "15-20 min"

# --- Gerenciamento de Dados ---

def carregar_exercicios():
    """Carrega os exercícios do arquivo CSV e valida os dados."""
    try:
        if not os.path.exists(CSV_FILE_PATH):
            raise FileNotFoundError
        
        df = pd.read_csv(CSV_FILE_PATH)
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        
        if df.empty:
            raise pd.errors.EmptyDataError
            
<<<<<<< HEAD
        if not all(col in df.columns for col in COLUNAS_OBRIGATORIAS):
            colunas_faltantes = [col for col in COLUNAS_OBRIGATORIAS if col not in df.columns]
            messagebox.showerror("Erro de Dados", f"O arquivo 'exercicios.csv' está faltando as colunas: {', '.join(colunas_faltantes)}.")
=======
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            messagebox.showerror("Erro de Dados", f"O arquivo 'exercicios.csv' está faltando as colunas: {', '.join(missing_cols)}.")
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
            return None
            
        return df

    except FileNotFoundError:
<<<<<<< HEAD
        messagebox.showerror("Erro", f"Arquivo '{CAMINHO_ARQUIVO_CSV}' não encontrado.")
        return None
    except pd.errors.EmptyDataError:
        messagebox.showerror("Erro de Dados", f"O arquivo '{CAMINHO_ARQUIVO_CSV}' está vazio.")
        return None
    except Exception as e:
        messagebox.showerror("Erro ao Carregar CSV", f"Erro ao ler '{CAMINHO_ARQUIVO_CSV}': {e}")
        return None

class Configuracoes_de_gifs:
=======
        messagebox.showerror("Erro", f"Arquivo '{CSV_FILE_PATH}' não encontrado.")
        return None
    except pd.errors.EmptyDataError:
        messagebox.showerror("Erro de Dados", f"O arquivo '{CSV_FILE_PATH}' está vazio.")
        return None
    except Exception as e:
        messagebox.showerror("Erro ao Carregar CSV", f"Erro ao ler '{CSV_FILE_PATH}': {e}")
        return None

# --- Gerenciador de Animação de GIF ---

class GifManager:
    """Uma classe para lidar com o carregamento e animação de GIFs em um widget Label."""
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
    def __init__(self, master, label_widget):
        self.master = master
        self.label = label_widget
        self.frames = []
        self.animation_id = None
<<<<<<< HEAD
        self.current_image = None #faz os gifs rodarem

    def carregar_e_iniciar(self, gif_path):
        self.parar()
=======
        self.current_image = None

    def load_and_play(self, gif_path):
        self.stop()
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        if not gif_path or not os.path.exists(gif_path):
            self.label.config(text="GIF não disponível.", image='')
            return

        try:
            gif_info = tk.PhotoImage(file=gif_path)
            num_frames = gif_info.cget("nframes")
            self.frames = [tk.PhotoImage(file=gif_path, format=f"gif -index {i}") for i in range(num_frames)]
<<<<<<< HEAD
            self.loop_da_animacao(0)
=======
            self.animate_loop(0)
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        except Exception as e:
            self.label.config(text=f"Erro ao carregar GIF: {e}", image='')
            self.frames = []

<<<<<<< HEAD
    def loop_da_animacao(self, frame_index):
=======
    def animate_loop(self, frame_index):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        if not self.frames:
            return
            
        frame = self.frames[frame_index]
        self.label.config(image=frame)
<<<<<<< HEAD
        self.current_image = frame 
        next_frame_index = (frame_index + 1) % len(self.frames)
        self.animation_id = self.master.after(100, self.loop_da_animacao, next_frame_index)

    def parar(self):
=======
        self.current_image = frame # Mantém referência para evitar garbage collection
        
        next_frame_index = (frame_index + 1) % len(self.frames)
        self.animation_id = self.master.after(100, self.animate_loop, next_frame_index)

    def stop(self):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        if self.animation_id:
            self.master.after_cancel(self.animation_id)
            self.animation_id = None
        self.frames = []
<<<<<<< HEAD
        self.current_image = None
=======
        self.current_image = None
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
