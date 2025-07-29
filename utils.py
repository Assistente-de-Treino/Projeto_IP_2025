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

def carregar_dados_exercicios() -> pd.DataFrame:
    dir_base = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(dir_base, config.CAMINHO_ARQUIVO_CSV)
    df = pd.read_csv(caminho_completo)
    return df
    
class GerenciadorDeGifs:
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
        self.label.image = frame_atual
        proximo_indice = (indice_frame + 1) % len(self.frames)
        self.id_animacao = self.master.after(150, self._iniciar_loop_animacao, proximo_indice)

    def parar(self):
        if self.id_animacao:
            self.master.after_cancel(self.id_animacao)
            self.id_animacao = None
        self.frames = []

def gerar_pdf_treino_semanal(plano_semanal: dict, caminho_arquivo: str):
    try:
        c = canvas.Canvas(caminho_arquivo, pagesize=letter)
        largura, altura = letter
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(largura / 2.0, altura - 50, "Seu Plano de Treino Semanal")
        y = altura - 100
        for dia, treino in plano_semanal.items():
            if y < 100:
                c.showPage(); c.setFont("Helvetica-Bold", 18)
                c.drawCentredString(largura / 2.0, altura - 50, "Seu Plano de Treino Semanal (Continuação)")
                y = altura - 100
            c.setFont("Helvetica-Bold", 14); c.drawString(72, y, dia); y -= 25
            c.setFont("Helvetica", 11)
            for exercicio in treino:
                nome, series, reps = exercicio.get("Nome", "N/A"), exercicio.get("Séries", "N/A"), exercicio.get("Repetições", "N/A")
                linha = f"  • {nome}: {series} séries de {reps} repetições"
                if "Descanso" in nome or "Aeróbico" in nome: linha = f"  • {nome}"
                c.drawString(82, y, linha); y -= 20
                if y < 60: c.showPage(); c.setFont("Helvetica", 11); y = altura - 50
            y -= 20
        c.save()
        return True
    except Exception as e:
        messagebox.showerror("Erro ao Gerar PDF", f"Não foi possível gerar o PDF: {e}")
        return False