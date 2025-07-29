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

def carregar_dados_exercicios() -> pd.DataFrame: # <-- o DataFrame identifica que as colunas do CSV
                                                # são separadas por vírgulas e organiza toda a estrutura
                                                # da tabela e depois guarda na variável df  
    
    dir_base = os.path.dirname(os.path.abspath(__file__)) # <-- monta o caminho para o arquivo, garantindo que funcione em qualquer PC
    caminho_completo = os.path.join(dir_base, config.CAMINHO_ARQUIVO_CSV) # <-- 
    
    df = pd.read_csv(caminho_completo) # <-- lê o CSV
    
    return df # <-- retorna a tabela com os dados
    
    
class GerenciadorDeGifs:
    
    def __init__(self, master_widget: tk.Widget, label_widget: tk.Label): # <-- função init cria a 
        self.master = master_widget # <-- aqui ele guarda a janela onde o GIF vai aparecer
        self.label = label_widget    # <-- e aqui o espaço exato (o Label) que vai mostrar a imagem
        self.frames = []             # <-- uma lista vazia pra guardar todos os frames do GIF
        self.id_animacao = None      # <-- uma variável pra gente ter o "controle remoto" da animação e poder parar ela

    # esse é o método que a gente chama de fora pra fazer a mágica acontecer.
    # ele para qualquer GIF que já tava rodando e começa um novo.
    def carregar_e_iniciar(self, caminho_gif: str):
        self.parar() # <-- por segurança, primeiro ele manda parar qualquer animação que já exista

        # <-- se o caminho do GIF não existir, ele só avisa no label e encerra a função
        if not caminho_gif or not os.path.exists(caminho_gif):
            self.label.config(text="GIF não disponível.", image='')
            return

        # <-- aqui ele tenta carregar o GIF, usando um try..except pra não quebrar o programa se o arquivo for inválido
        try:
            gif = Image.open(caminho_gif) # <-- usa a biblioteca Pillow pra abrir o arquivo do GIF
            # <-- aqui tá o pulo do gato: ele passa por cada frame do GIF, converte pra um formato que o Tkinter entende, e guarda na nossa lista
            self.frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]
            # <-- se deu tudo certo, ele chama a função que começa o loop da animação, começando pelo primeiro frame (índice 0)
            self._iniciar_loop_animacao(0)
        except Exception:
            # <-- se der qualquer erro ao tentar carregar, ele avisa no label e limpa a lista de frames
            self.label.config(text="Erro ao carregar GIF.", image='')
            self.frames = []

    # essa é a função que fica rodando em loop pra dar a impressão de movimento.
    # ela é "privada" (começa com _) porque só a própria classe deveria chamar ela.
    def _iniciar_loop_animacao(self, indice_frame: int):
        if not self.frames: return # <-- se por algum motivo a lista de frames estiver vazia, ele para

        frame_atual = self.frames[indice_frame]
        self.label.config(image=frame_atual)    # <-- coloca o frame no nosso label na tela
        self.label.image = frame_atual
        proximo_indice = (indice_frame + 1) % len(self.frames) # <-- aqui ele descobre qual é o próximo frame. se chegar no último, o '%' faz ele voltar pro primeiro

        self.id_animacao = self.master.after(150, self._iniciar_loop_animacao, proximo_indice)

    # um método simples pra parar a animação quando a gente não precisar mais dela (ex: quando fecha a janela do GIF)
    def parar(self):
        if self.id_animacao: # <-- se tiver uma animação agendada...
            self.master.after_cancel(self.id_animacao) # <-- ...a gente usa o "controle remoto" (o ID) pra cancelar ela
            self.id_animacao = None
        self.frames = [] # <-- e limpa a lista de frames pra liberar memória