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

        self.df_exercicios = utils.carregar_dados_exercicios()
        if self.df_exercicios is None:
            master.destroy()
            return

        self.ficha_semanal = {}
        self.imc_label = None 
        self.original_image = None
        self.background_photo = None
        self.background_label = None

        self.mostrar_tela_inicial()

    def limpar_interface(self):
        for widget in self.master.winfo_children(): widget.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_interface()
        self.background_label = tk.Label(self.master)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        try:
            caminho_imagem = os.path.join(os.path.dirname(__file__), "assets", "fundo.jpg")
            self.original_image = Image.open(caminho_imagem)
        except FileNotFoundError:
            self.background_label.config(bg=config.CORES['CABECALHO_TABELA'])
            self.original_image = None

        ttk.Label(self.master, text="Assistente de Treinos", font=('Helvetica', 52, 'bold'), foreground=config.CORES['TEXTO_BOTAO'], background=self.background_label.cget('bg')).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        ttk.Button(self.master, text="Iniciar", command=self.mostrar_interface_principal, style='TButton').place(relx=0.5, rely=0.6, anchor=tk.CENTER, width=200, height=50)
        self.master.bind('<Configure>', self._redimensionar_fundo)
    
    def _redimensionar_fundo(self, event):
        if not self.original_image: return
        imagem_redimensionada = self.original_image.resize((event.width, event.height), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(imagem_redimensionada)
        self.background_label.config(image=self.background_photo)

    def mostrar_interface_principal(self):
        self.master.unbind('<Configure>')
        self.limpar_interface()
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)
        self._criar_widgets_principais(main_frame)

    def _criar_widgets_principais(self, parent):
        top_frame = ttk.Frame(parent)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        input_frame = ttk.Frame(top_frame)
        input_frame.pack(pady=10, fill=tk.X, anchor='n')
        self.entrada_idade = self._criar_campo_de_entrada(input_frame, "Idade:")
        self.entrada_altura = self._criar_campo_de_entrada(input_frame, "Altura (cm):")
        self.entrada_peso = self._criar_campo_de_entrada(input_frame, "Peso (kg):")
        self.nivel_var, _ = self._criar_campo_combobox(input_frame, "Nível de treino:", config.NIVEIS_DE_TREINO)

        ttk.Button(top_frame, text="Gerar Fichas de Treino", command=self.gerar_fichas).pack(pady=10, fill=tk.X, ipady=10)
        self.imc_label = ttk.Label(top_frame, text="Preencha os dados para calcular o IMC", font=('Arial', 12, 'bold'))
        self.imc_label.pack(pady=5)

        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        pdf_button = ttk.Button(bottom_frame, text="Gerar PDF dos exercícios", command=self._acao_gerar_pdf)
        pdf_button.pack(side=tk.RIGHT, padx=5, ipady=5)

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=10)
        
        self.daily_trees = {}
        for i in range(5):
            day_name = f"Dia {i+1}"; frame = ttk.Frame(self.notebook); self.notebook.add(frame, text=day_name)
            tree = self._criar_visualizador_de_treino(frame); tree.bind("<Double-1>", self.ao_clicar_no_exercicio)
            self.daily_trees[day_name] = tree

    def _criar_campo_de_entrada(self, parent, label_text):
        frame = ttk.Frame(parent); frame.pack(pady=4, fill=tk.X)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT, padx=5)
        entry = ttk.Entry(frame); entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        return entry

    def _criar_campo_combobox(self, parent, label_text, values):
        frame = ttk.Frame(parent); frame.pack(pady=4, fill=tk.X)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT, padx=5)
        var = tk.StringVar(); combobox = ttk.Combobox(frame, textvariable=var, values=values, state="readonly")
        combobox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        if values: combobox.set(values[0])
        return var, combobox

    def _criar_visualizador_de_treino(self, parent):
        cols = ["Exercício", "Grupo Muscular", "Séries", "Repetições", "Tipo"]
        tree = ttk.Treeview(parent, columns=cols, show="headings")
        for col in cols: tree.heading(col, text=col)
        tree.column("Exercício", width=300, anchor=tk.W); tree.column("Séries", width=80, anchor=tk.CENTER); tree.column("Repetições", width=100, anchor=tk.CENTER)
        tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        return tree

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
        for day_name, tree in self.daily_trees.items():
            tree.delete(*tree.get_children())
            for ex in self.ficha_semanal.get(day_name, []):
                valores = (ex.get("Nome", "N/A"), ex.get("Grupo", "N/A"), ex.get("Séries", "3"), ex.get("Repetições", "8-12"), ex.get("Tipo", "N/A"))
                tree.insert("", "end", values=valores)

    def ao_clicar_no_exercicio(self, event):
        tree = event.widget;
        if not tree.selection(): return
        item_id = tree.selection()[0]; nome_exercicio = tree.item(item_id, 'values')[0]
        detalhes_exercicio = self.df_exercicios[self.df_exercicios["Nome"] == nome_exercicio]
        if not detalhes_exercicio.empty: self._mostrar_detalhes_exercicio(detalhes_exercicio.iloc[0])

    def _mostrar_detalhes_exercicio(self, detalhes: pd.Series):
        popup = tk.Toplevel(self.master); popup.title(detalhes["Nome"]); popup.geometry("700x600"); popup.transient(self.master); popup.grab_set()
        content_frame = ttk.Frame(popup, padding="15"); content_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(content_frame, text=detalhes["Nome"], font=('Helvetica', 18, 'bold')).pack(pady=10)
        
        details_frame = ttk.Frame(content_frame); details_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        desc_frame = ttk.Frame(details_frame, width=350); desc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        desc_text = tk.Text(desc_frame, wrap=tk.WORD, relief=tk.FLAT, bg=config.CORES['FUNDO']); desc_text.insert(tk.END, detalhes.get("DescricaoDetalhada", "Descrição não disponível."))
        desc_text.config(state=tk.DISABLED); desc_text.pack(fill=tk.BOTH, expand=True)
        
        gif_frame = ttk.Frame(details_frame); gif_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        gif_label = ttk.Label(gif_frame); gif_label.pack(pady=10)
        
        gerenciador_gif = utils.Configuracoes_de_gifs(popup, gif_label)
        popup.gerenciador_gif = gerenciador_gif # <-- A CORREÇÃO ESTÁ AQUI
        
        caminho_gif_relativo = detalhes["GifURL"]
        caminho_gif_completo = os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho_gif_relativo)
        
        gerenciador_gif.carregar_e_iniciar(caminho_gif_completo)
        
        popup.bind("<Destroy>", lambda e: gerenciador_gif.parar())

    def _acao_gerar_pdf(self):
        if not self.ficha_semanal:
            messagebox.showwarning("Atenção", "Você precisa gerar uma ficha de treino antes de exportar para PDF.")
            return
        caminho_arquivo = filedialog.asksaveasfilename(title="Salvar PDF do Treino", defaultextension=".pdf", filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho_arquivo:
            sucesso = utils.gerar_pdf_treino_semanal(self.ficha_semanal, caminho_arquivo)
            if sucesso: messagebox.showinfo("Sucesso", f"PDF do treino salvo com sucesso em:\n{caminho_arquivo}")