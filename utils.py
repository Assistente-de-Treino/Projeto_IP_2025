import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from config import CAMINHO_ARQUIVO_CSV, COLUNAS_OBRIGATORIAS
from PIL import Image, ImageTk, ImageSequence  
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


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
            gif = Image.open(gif_path)

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

def gerar_pdf_treino_semanal(plano_semanal: dict, caminho_arquivo: str): #<-- a função de gerar o PDf, usando a biblioteca reportlab
    try:
        c = canvas.Canvas(caminho_arquivo, pagesize=letter) #<-- objeto em branco, já é passado o argumento de onde é preciso que o arquivo seja salvo,
                                                            #nesse caso, é no "caminho_arquivo" e o tamanho da "folha de papel" #tamanho da "folha de papel"
                                                            # aqui o "letter" significa que ele está em formato de carta
        largura, altura = letter
        c.setFont("Helvetica-Bold", 18) #<-- fonte em negrito e tamanho da fonte do título
        c.drawCentredString(largura / 2.0, altura - 50, "Seu Plano de Treino Semanal") #<-- indica que o texto "Seu plano de treino semanal" fique centralizado, 
                                                                                        #com base nas coordenadas de largura e altura 
        y = altura - 100 # <-- serve como um 'cursor', começa do topo e vai descendo
        for dia, treino in plano_semanal.items():
            #antes de escrever o dia, o código verifica se tem espaço suficiente na página atual
            if y < 100:
                c.showPage();  c.setFont("Helvetica-Bold", 18) # <--se não tiver espaço, o "showpage" muda para a página seguinte
                c.drawCentredString(largura / 2.0, altura - 50, "Seu Plano de Treino Semanal (continuação)")
                y = altura - 100
            c.setFont("Helvetica-Bold", 14); c.drawString(72, y, dia); y -= 25
            c.setFont("Helvetica", 11) # } esse bloco todo faz com que, se necessário, o pdf quebra para a próxima página
                                        #no caso de não haver espaço na atual e na próxima ele não começa do topo, 
                                        #dá uma formatação e adaptada para que fique mais legível e organizado
            for exercicio in treino:
                nome, series, repeticoes = exercicio.get("Nome", "N/A"), exercicio.get("Séries", "N/A"), exercicio.get("Repetições", "N/A")
                linha = f"  • {nome}: {series} séries de {repeticoes} repetições" #esse laço for escreve cada exercício do dia
                if "Descanso" in nome or "Aeróbico" in nome: linha = f"  • {nome}"
                c.drawString(82, y, linha); #<-- desenha a linha do exercício e move o cursor para baixo
                y -= 20 #<-- adiciona um espaço entre um dia e outro
                if y < 60: c.showPage(); c.setFont("Helvetica", 11); y = altura - 50 
            y -= 20 # }esse segundo laço for, dentro do principal, é o que faz o processo de gerar os textos pro pdf 
        c.save() #<-- salva dentro da memória da máquina
        return True
    except Exception as e:
        messagebox.showerror("Erro ao Gerar PDF", f"Não foi possível gerar o PDF: {e}")
        return False