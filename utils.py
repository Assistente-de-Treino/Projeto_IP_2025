import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from config import CAMINHO_ARQUIVO_CSV, COLUNAS_OBRIGATORIAS
from PIL import Image, ImageTk, ImageSequence  # Adicionado para GIFs animados


def calcular_imc(peso, altura_cm):
    if altura_cm <= 0:
        return 0
    altura_m = altura_cm / 100
    return peso / (altura_m ** 2)


def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    elif 30 <= imc < 35:
        return "Obesidade Grau I"
    elif 35 <= imc < 40:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III (Mórbida)"


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

        if df.empty:
            raise pd.errors.EmptyDataError

        if not all(col in df.columns for col in COLUNAS_OBRIGATORIAS):
            colunas_faltantes = [col for col in COLUNAS_OBRIGATORIAS if col not in df.columns]
            messagebox.showerror("Erro de Dados",
                                 f"O arquivo 'exercicios.csv' está faltando as colunas: {', '.join(colunas_faltantes)}.")
            return None

        return df

    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo '{CAMINHO_ARQUIVO_CSV}' não encontrado.")
        return None
    except pd.errors.EmptyDataError:
        messagebox.showerror("Erro de Dados", f"O arquivo '{CAMINHO_ARQUIVO_CSV}' está vazio.")
        return None
    except Exception as e:
        messagebox.showerror("Erro ao Carregar CSV", f"Erro ao ler '{CAMINHO_ARQUIVO_CSV}': {e}")
        return None


class Configuracoes_de_gifs:
    def __init__(self, master, label_widget):
        self.master = master
        self.label = label_widget
        self.frames = []
        self.animation_id = None
        self.current_image = None
        self.frame_index = 0

    def carregar_e_iniciar(self, gif_path):
        self.parar()
        if not gif_path or not os.path.exists(gif_path):
            self.label.config(text="GIF não disponível.", image='')
            return

        try:
            # Carrega o GIF usando Pillow
            gif = Image.open(gif_path)

            # Extrai todos os frames e converte para formato compatível com Tkinter
            self.frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

            self.frame_index = 0
            self.loop_da_animacao()
        except Exception as e:
            self.label.config(text=f"Erro ao carregar GIF: {e}", image='')
            self.frames = []

    def loop_da_animacao(self):
        if not self.frames:
            return

        self.label.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.animation_id = self.master.after(50, self.loop_da_animacao)

    def parar(self):
        if self.animation_id:
            self.master.after_cancel(self.animation_id)
            self.animation_id = None
        self.frames = []
        self.current_image = None
