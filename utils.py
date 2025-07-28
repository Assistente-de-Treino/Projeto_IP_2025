import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from typing import Optional

from PIL import Image, ImageTk, ImageSequence
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import config


def calcular_imc(peso: float, altura_cm: float) -> float: 
    if altura_cm <= 0: return 0.0
    altura_m = altura_cm / 100
    return peso / (altura_m ** 2)

    
def classificar_imc(imc: float) -> str:
    if imc < 18.5: return "Abaixo do peso"
    if imc < 25: return "Peso normal"
    if imc < 30: return "Sobrepeso"
    if imc < 35: return "Obesidade Grau I"
    if imc < 40: return "Obesidade Grau II"
    return "Obesidade Grau III (Mórbida)"

def obter_tempo_aerobico(classificacao_imc: str) -> str:
    
    if "Obesidade" in classificacao_imc or "Sobrepeso" in classificacao_imc: return "30-45 min"
    if "Peso normal" in classificacao_imc: return "20-30 min"
    return "15-20 min"

def carregar_dados_exercicios() -> Optional[pd.DataFrame]: # <-- carrega os exercícios dentro do arquivo CSV, 
                                                                #validando se ele está bem estruturado
    try:
        dir_base = os.path.dirname(os.path.abspath(__file__)) # <-- verifica onde o arquivo está dentro do computador, 
        caminho_completo = os.path.join(dir_base, config.CAMINHO_ARQUIVO_CSV) #<-- monta o caminho completo pra chegar no CSV

        if not os.path.exists(caminho_completo): raise FileNotFoundError(f"O arquivo '{config.CAMINHO_ARQUIVO_CSV}' não foi encontrado.")
        df = pd.read_csv(caminho_completo) # <--confirma que o arquivo existe e ele é lido pelo pandas
                                            # transformando numa tabela

        if df.empty: raise ValueError(f"O arquivo '{config.CAMINHO_ARQUIVO_CSV}' está vazio.")
        colunas_faltantes = [col for col in config.COLUNAS_OBRIGATORIAS if col not in df.columns]

        if colunas_faltantes: raise ValueError(f"Faltam as seguintes colunas no arquivo: {', '.join(colunas_faltantes)}")
        return df
    except (FileNotFoundError, ValueError) as e:
        messagebox.showerror("Erro de Dados", str(e))
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao carregar os dados: {e}")
    return None
    
# A classe que faz os GIFs dançarem na tela
# Cada vez que a gente precisa de um GIF, a gente cria um "gerenciador" desses
class GerenciadorDeGifs:
    """Controla o carregamento e animação de GIFs usando Pillow."""
    def __init__(self, master_widget: tk.Widget, label_widget: tk.Label):
        self.master = master_widget
        self.label = label_widget
        self.frames = []
        self.id_animacao = None

    def carregar_e_iniciar(self, caminho_gif: str):
        self.parar()
        if not caminho_gif or not os.path.exists(caminho_gif):
            self.label.config(text="GIF não disponível.", image='')
            return
        try:
            gif = Image.open(caminho_gif)
            self.frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
            self._iniciar_loop_animacao(0)
        except Exception:
            self.label.config(text="Erro ao carregar GIF.", image='')
            self.frames = []

    def _iniciar_loop_animacao(self, indice_frame: int):
        if not self.frames: return
        frame_atual = self.frames[indice_frame]
        self.label.config(image=frame_atual)
        proximo_indice = (indice_frame + 1) % len(self.frames)
        # o '150' aqui é o tempo em milissegundos entre cada frame. Quanto maior, mais lento o GIF.
        self.id_animacao = self.master.after(150, self._iniciar_loop_animacao, proximo_indice)

    def parar(self):
        if self.id_animacao:
            self.master.after_cancel(self.id_animacao)
            self.id_animacao = None
        self.frames = []

