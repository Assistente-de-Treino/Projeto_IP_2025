import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import pandas as pd
from PIL import Image, ImageTk

import config
import utils 
from logica_de_treinos import GeradorDeTreinos 

class AppAssistenteDeTreinos:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Assistente de Treinos")
        master.geometry("1200x800")
        master.bind("<Escape>", lambda e: master.attributes('-fullscreen', False))
        self.style = ttk.Style()
        config.configurar_estilos_globais(self.style)
        
        self.style.configure('Welcome.TButton', font=('Arial', 16, 'bold'))

        self.df_exercicios = utils.carregar_dados_exercicios()
        if self.df_exercicios is None:
            master.destroy()
            return

        self.ficha_semanal = {}
        self.imc_label = None 
        self.original_image = None
        self.background_photo = None
        self.canvas_inicial = None
        self.botao_iniciar_widget = None

        self.mostrar_tela_inicial()

    def limpar_interface(self):
        self.master.unbind('<Configure>')
        for componente in self.master.winfo_children(): componente.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_interface()
        
        self.canvas_inicial = tk.Canvas(self.master, highlightthickness=0)
        self.canvas_inicial.pack(expand=True, fill=tk.BOTH)

        try:
            caminho_imagem = os.path.join(os.path.dirname(__file__), "assets", "fundo.jpg")
            self.original_image = Image.open(caminho_imagem)
        except FileNotFoundError:
            self.original_image = None

        self.botao_iniciar_widget = ttk.Button(
            self.master, 
            text="Iniciar", 
            command=self.mostrar_interface_principal, 
            style='Welcome.TButton'
        )

        self.master.bind('<Configure>', self._atualizar_tela_inicial)
        self.master.after(10, self._atualizar_tela_inicial)

    def _atualizar_tela_inicial(self, event=None):
        if not hasattr(self, 'canvas_inicial') or not self.canvas_inicial: return
        
        largura_janela = self.master.winfo_width()
        altura_janela = self.master.winfo_height()
        
        self.canvas_inicial.delete("all")
        
        if self.original_image:
            imagem_redimensionada = self.original_image.resize((largura_janela, altura_janela), Image.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(imagem_redimensionada)
            self.canvas_inicial.create_image(0, 0, image=self.background_photo, anchor='nw')
        else:
            self.canvas_inicial.config(bg=config.CORES['CABECALHO_TABELA'])

        self.canvas_inicial.create_text(
            largura_janela / 2, 
            altura_janela * 0.4,
            text="Assistente de Treinos",
            font=('Helvetica', 52, 'bold'),
            fill="white"
        )

        self.canvas_inicial.create_window(
            largura_janela / 2, 
            altura_janela * 0.6,
            window=self.botao_iniciar_widget, 
            width=220,
            height=50
        )

    def mostrar_interface_principal(self):
        self.limpar_interface()
        frame_principal = ttk.Frame(self.master, padding="20")
        frame_principal.pack(expand=True, fill=tk.BOTH)
        self._criar_widgets_principais(frame_principal)

    def _criar_widgets_principais(self, container_pai):
        frame_superior = ttk.Frame(container_pai)
        frame_superior.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        frame_entradas = ttk.Frame(frame_superior)
        frame_entradas.pack(pady=10, fill=tk.X, anchor='n')
        self.entrada_idade = self._criar_campo_de_entrada(frame_entradas, "Idade:")
        self.entrada_altura = self._criar_campo_de_entrada(frame_entradas, "Altura (cm):")
        self.entrada_peso = self._criar_campo_de_entrada(frame_entradas, "Peso (kg):")
        self.nivel_var, _ = self._criar_campo_combobox(frame_entradas, "Nível de treino:", config.NIVEIS_DE_TREINO)

        ttk.Button(frame_superior, text="Gerar Fichas de Treino", command=self.gerar_fichas).pack(pady=10, fill=tk.X, ipady=10)
        self.imc_label = ttk.Label(frame_superior, text="Preencha os dados para calcular o IMC", font=('Arial', 12, 'bold'))
        self.imc_label.pack(pady=5)

        frame_inferior = ttk.Frame(container_pai)
        frame_inferior.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        botao_pdf = ttk.Button(frame_inferior, text="Gerar PDF dos exercícios", command=self._acao_gerar_pdf)
        botao_pdf.pack(side=tk.RIGHT, padx=5, ipady=5)

        self.notebook = ttk.Notebook(container_pai)
        self.notebook.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=10)
        
        self.daily_trees = {}
        for i in range(5):
            nome_dia = f"Dia {i+1}"; aba_frame = ttk.Frame(self.notebook); self.notebook.add(aba_frame, text=nome_dia)
            tabela_treino = self._criar_visualizador_de_treino(aba_frame)
            tabela_treino.bind("<Double-1>", self.ao_clicar_no_exercicio)
            self.daily_trees[nome_dia] = tabela_treino

    def _criar_campo_de_entrada(self, container_pai, texto_rotulo):
        frame_campo = ttk.Frame(container_pai); frame_campo.pack(pady=4, fill=tk.X)
        ttk.Label(frame_campo, text=texto_rotulo, width=15).pack(side=tk.LEFT, padx=5)
        campo_entrada = ttk.Entry(frame_campo); campo_entrada.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        return campo_entrada

    def _criar_campo_combobox(self, container_pai, texto_rotulo, valores):
        frame_campo = ttk.Frame(container_pai); frame_campo.pack(pady=4, fill=tk.X)
        ttk.Label(frame_campo, text=texto_rotulo, width=15).pack(side=tk.LEFT, padx=5)
        variavel_selecao = tk.StringVar(); caixa_selecao = ttk.Combobox(frame_campo, textvariable=variavel_selecao, values=valores, state="readonly")
        caixa_selecao.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        if valores: caixa_selecao.set(valores[0])
        return variavel_selecao, caixa_selecao

    def _criar_visualizador_de_treino(self, container_pai):
        colunas = ["Exercício", "Grupo Muscular", "Séries", "Repetições", "Tipo"]
        tabela = ttk.Treeview(container_pai, columns=colunas, show="headings")
        for coluna in colunas: tabela.heading(coluna, text=coluna)
        tabela.column("Exercício", width=300, anchor=tk.W); tabela.column("Séries", width=80, anchor=tk.CENTER); tabela.column("Repetições", width=100, anchor=tk.CENTER)
        tabela.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        return tabela

    def gerar_fichas(self):
        try:
            idade_str, altura_str, peso_str, nivel = self.entrada_idade.get(), self.entrada_altura.get(), self.entrada_peso.get(), self.nivel_var.get()
            if not all([idade_str, altura_str, peso_str, nivel]):
                messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")
                return
            idade, altura, peso = int(idade_str), float(altura_str.replace(',', '.')), float(peso_str.replace(',', '.'))
            imc = utils.calcular_imc(peso, altura)
            classificacao = utils.classificar_imc(imc)
            tempo_aerobico = utils.obter_tempo_aerobico(classificacao)
            self.imc_label.config(text=f"IMC: {imc:.2f} ({classificacao})")
            gerador = GeradorDeTreinos(self.df_exercicios)
            self.ficha_semanal = gerador.gerar_plano_semanal(nivel, classificacao, tempo_aerobico)
            self._preencher_tabelas_treino()
        except (ValueError, TypeError): messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        except Exception as e: messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def _preencher_tabelas_treino(self):
        for nome_dia, tabela in self.daily_trees.items():
            tabela.delete(*tabela.get_children())
            for exercicio in self.ficha_semanal.get(nome_dia, []):
                valores_linha = (exercicio.get("Nome", "N/A"), exercicio.get("Grupo", "N/A"), exercicio.get("Séries", "3"), exercicio.get("Repetições", "8-12"), exercicio.get("Tipo", "N/A"))
                tabela.insert("", "end", values=valores_linha)
    
    def ao_clicar_no_exercicio(self, event):
        tabela = event.widget;
        if not tabela.selection(): return
        id_do_item = tabela.selection()[0]; nome_exercicio = tabela.item(id_do_item, 'values')[0]
        detalhes_exercicio = self.df_exercicios[self.df_exercicios["Nome"] == nome_exercicio]
        if not detalhes_exercicio.empty: self._mostrar_detalhes_exercicio(detalhes_exercicio.iloc[0])

    def _mostrar_detalhes_exercicio(self, detalhes: pd.Series):
        janela_popup = tk.Toplevel(self.master); janela_popup.title(detalhes["Nome"]); janela_popup.geometry("700x600"); janela_popup.transient(self.master); janela_popup.grab_set()
        frame_conteudo = ttk.Frame(janela_popup, padding="15"); frame_conteudo.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame_conteudo, text=detalhes["Nome"], font=('Helvetica', 18, 'bold')).pack(pady=10)
        
        frame_detalhes = ttk.Frame(frame_conteudo); frame_detalhes.pack(pady=10, fill=tk.BOTH, expand=True)
        
        frame_descricao = ttk.Frame(frame_detalhes, width=350); frame_descricao.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        texto_descricao = tk.Text(frame_descricao, wrap=tk.WORD, relief=tk.FLAT, bg=config.CORES['FUNDO']); texto_descricao.insert(tk.END, detalhes.get("DescricaoDetalhada", "Descrição não disponível."))
        texto_descricao.config(state=tk.DISABLED); texto_descricao.pack(fill=tk.BOTH, expand=True)
        
        gif_frame = ttk.Frame(frame_detalhes); gif_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        gif_label = ttk.Label(gif_frame); gif_label.pack(pady=10)
        
        gerenciador_gif = utils.GerenciadorDeGifs(janela_popup, gif_label)
        janela_popup.gerenciador_gif = gerenciador_gif
        
        caminho_gif_relativo = detalhes["GifURL"]
        caminho_gif_completo = os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho_gif_relativo)
        
        gerenciador_gif.carregar_e_iniciar(caminho_gif_completo)
        
        janela_popup.bind("<Destroy>", lambda e: gerenciador_gif.parar())

    def _acao_gerar_pdf(self):
        if not self.ficha_semanal:
            messagebox.showwarning("Atenção", "Você precisa gerar uma ficha de treino antes de exportar para PDF.")
            return
        caminho_arquivo = filedialog.asksaveasfilename(title="Salvar PDF do Treino", defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho_arquivo:
            sucesso = utils.gerar_pdf_treino_semanal(self.ficha_semanal, caminho_arquivo)
            if sucesso: messagebox.showinfo("Sucesso", f"PDF do treino salvo com sucesso em:\n{caminho_arquivo}")