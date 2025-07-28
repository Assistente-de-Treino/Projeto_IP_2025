import tkinter as tk
from tkinter import ttk, messagebox
import config
import utils
import os
import pandas as pd

def calcular_imc(peso, altura_cm):
    if altura_cm <= 0: return 0
    return peso / (altura_cm / 100) ** 2

def classificacao_imc(imc):
    if imc < 18.5: return "Abaixo do peso"
    if 18.5 <= imc < 25: return "Peso normal"
    if 25 <= imc < 30: return "Sobrepeso"
    if 30 <= imc < 35: return "Obesidade Grau I"
    if 35 <= imc < 40: return "Obesidade Grau II"
    return "Obesidade Grau III (Mórbida)"

def tempo_cardio(imc_classification):
    if "Obesidade" in imc_classification or "Sobrepeso" in imc_classification: return "30-45 min"
    if "Peso normal" in imc_classification: return "20-30 min"
    return "15-20 min"

from logica_de_treinos import GeradorDosTreinos 

class AppAssistenteDeTreinos:
    def __init__(self, master):
        self.master = master
        master.title("Assistente de Treinos - Ficha de Treino")
        master.geometry("1200x800")
        master.bind("<Escape>", lambda e: master.attributes('-fullscreen', False))

        self.style = ttk.Style()
        
        self.cores = {
            'PRIMARY_BLUE': '#0056B3',   # Azul médio para botões e destaques
            'DARK_BLUE': '#003366',      # Azul escuro para texto principal e elementos fortes
            'LIGHT_BLUE': '#F0F0F0',     # Cinza muito claro para fundo geral (quase branco)
            'MEDIUM_BLUE': '#A0A0A0',    # Cinza médio para abas e elementos secundários
            'DARKER_BLUE': '#2C3E50',    # Azul marinho/chumbo para cabeçalhos e bordas
            'DEEP_BLUE': '#1A1A1A',      # Preto quase puro para títulos e texto de alto contraste
            'TEXT_COLOR_LIGHT': '#FFFFFF', # Branco para texto em fundos escuros
            'TEXT_COLOR_DARK': '#333333' # Cinza escuro para texto em fundos claros
        }

        self._configurar_estilos_personalizados()

        self.df_exercicios = self._carregar_dados_exercicios()
        if self.df_exercicios is None: master.destroy(); return

        self.ficha_semanal = {}
        self.imc = None
        self.imc_classificacao = None

        self.welcome_canvas = None
        self.welcome_title_label = None # Este Label será substituído por create_text
        self.start_button_widget = None

        self.mostrar_tela_inicial()

    def _configurar_estilos_personalizados(self):
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.cores['LIGHT_BLUE'])
        self.style.configure('TLabel', background=self.cores['LIGHT_BLUE'], font=('Arial', 11), foreground=self.cores['TEXT_COLOR_DARK'])
        self.style.configure('TEntry', font=('Arial', 11), fieldbackground=self.cores['TEXT_COLOR_LIGHT'], foreground=self.cores['TEXT_COLOR_DARK'])
        self.style.configure('TButton', font=('Arial', 11, 'bold'), background=self.cores['PRIMARY_BLUE'], foreground=self.cores['TEXT_COLOR_LIGHT'], borderwidth=0, relief='raised')
        self.style.map('TButton', background=[('active', self.cores['DARKER_BLUE'])])
        self.style.configure('TCombobox', font=('Arial', 11), fieldbackground=self.cores['TEXT_COLOR_LIGHT'], foreground=self.cores['TEXT_COLOR_DARK'])
        self.style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), background=self.cores['MEDIUM_BLUE'], foreground=self.cores['TEXT_COLOR_DARK'])
        self.style.map('TNotebook.Tab', background=[('selected', self.cores['PRIMARY_BLUE'])], foreground=[('selected', self.cores['TEXT_COLOR_LIGHT'])])
        self.style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), background=self.cores['DARKER_BLUE'], foreground=self.cores['TEXT_COLOR_LIGHT'])
        self.style.configure('Treeview', font=('Arial', 10), rowheight=25, background=self.cores['LIGHT_BLUE'], foreground=self.cores['TEXT_COLOR_DARK'], fieldbackground=self.cores['LIGHT_BLUE'])
        self.style.map('Treeview', background=[('selected', self.cores['PRIMARY_BLUE'])], foreground=[('selected', self.cores['TEXT_COLOR_LIGHT'])])


    def _carregar_dados_exercicios(self):
        try:
            csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.CAMINHO_ARQUIVO_CSV)
            if not os.path.exists(csv_path): raise FileNotFoundError
            df = pd.read_csv(csv_path)
            if df.empty: raise pd.errors.EmptyDataError
            
            missing_cols = [col for col in config.COLUNAS_OBRIGATORIAS if col not in df.columns]
            if missing_cols:
                messagebox.showerror("Erro de Dados", f"O arquivo '{config.CAMINHO_ARQUIVO_CSV}' está faltando as colunas: {', '.join(missing_cols)}.")
                return None
            return df
        except FileNotFoundError:
            messagebox.showerror("Erro", f"Arquivo '{config.CAMINHO_ARQUIVO_CSV}' não encontrado."); return None
        except pd.errors.EmptyDataError:
            messagebox.showerror("Erro de Dados", f"O arquivo '{config.CAMINHO_ARQUIVO_CSV}' está vazio."); return None
        except Exception as e:
            messagebox.showerror("Erro ao Carregar CSV", f"Erro ao ler '{config.CAMINHO_ARQUIVO_CSV}': {e}"); return None

    def limpar_interface(self):
        for widget in self.master.winfo_children(): widget.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_interface()
        welcome_frame = ttk.Frame(self.master, style='TFrame'); welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        self.welcome_canvas = tk.Canvas(welcome_frame, highlightthickness=0, bg=self.cores['LIGHT_BLUE'])
        self.welcome_canvas.pack(expand=True, fill=tk.BOTH)

        # O botão Iniciar ainda precisa ser um widget Tkinter para ser criado_window
        self.start_button_widget = ttk.Button(self.welcome_canvas, text="Iniciar", command=self.mostrar_interface_principal, style='TButton')

        self.welcome_canvas.bind("<Configure>", self._update_welcome_screen_layout)
        self.master.after(10, self._update_welcome_screen_layout)

    def _update_welcome_screen_layout(self, event=None):
        """
        Atualiza o layout da tela de boas-vindas, centralizando os elementos
        com base nas dimensões atuais do canvas e redesenhando o gradiente.
        """
        if not self.welcome_canvas.winfo_width():
            self.master.after(10, self._update_welcome_screen_layout)
            return

        canvas_width = self.welcome_canvas.winfo_width()
        canvas_height = self.welcome_canvas.winfo_height()

        self.welcome_canvas.delete("all") # Limpa elementos antigos

        self._draw_gradient(self.welcome_canvas)

        # --- Título "GYM ASSISTANT" em alto relevo simulado ---
        title_text = "GYM ASSISTANT"
        font_size = 64
        font_family = 'Helvetica'
        font_weight = 'bold'
        
        # Simula alto relevo com múltiplas camadas de texto (sombra)
        # Camada de sombra mais escura
        for offset in range(3, 0, -1): # Pequenos offsets para a sombra
            self.welcome_canvas.create_text(
                canvas_width/2 + offset, canvas_height/2 - 100 + offset,
                text=title_text,
                font=(font_family, font_size, font_weight),
                fill=self.cores['DARKER_BLUE'], # Cor da sombra
                anchor=tk.CENTER
            )
        # Camada principal do texto
        self.welcome_canvas.create_text(
            canvas_width/2, canvas_height/2 - 100,
            text=title_text,
            font=(font_family, font_size, font_weight),
            fill=self.cores['DEEP_BLUE'], # Cor principal do texto
            anchor=tk.CENTER
        )
        # --- FIM Título ---

        # Adiciona elementos visuais de academia (emojis como placeholder)
        self.welcome_canvas.create_text(canvas_width/2 - 300, canvas_height/2 - 200, text="🏋️‍♂️", font=("Arial", 120), fill=self.cores['DARK_BLUE'], anchor=tk.CENTER)
        self.welcome_canvas.create_text(canvas_width/2 + 300, canvas_height/2 + 100, text="💪", font=("Arial", 80), fill=self.cores['DARK_BLUE'], anchor=tk.CENTER)
        self.welcome_canvas.create_text(canvas_width/2, canvas_height/2 + 250, text="🏃‍♀️", font=("Arial", 90), fill=self.cores['DARK_BLUE'], anchor=tk.CENTER)
        self.welcome_canvas.create_text(canvas_width/2 + 400, canvas_height/2 - 150, text="🤸", font=("Arial", 70), fill=self.cores['DARK_BLUE'], anchor=tk.CENTER)

        # Centraliza o botão Iniciar
        self.welcome_canvas.create_window(canvas_width/2, canvas_height/2 + 50, window=self.start_button_widget, anchor=tk.CENTER)

    def _draw_gradient(self, canvas):
        """Desenha um gradiente vertical no canvas."""
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        color1_rgb = tuple(int(self.cores['LIGHT_BLUE'][i:i+2], 16) for i in (1, 3, 5))
        color2_rgb = tuple(int(self.cores['DARKER_BLUE'][i:i+2], 16) for i in (1, 3, 5))

        for i in range(height):
            r = int(color1_rgb[0] + (color2_rgb[0] - color1_rgb[0]) * (i / height))
            g = int(color1_rgb[1] + (color2_rgb[1] - color1_rgb[1]) * (i / height))
            b = int(color1_rgb[2] + (color2_rgb[2] - color1_rgb[2]) * (i / height))
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color, width=1, tags="gradient")

    def mostrar_interface_principal(self):
        self.limpar_interface()
        main_frame = ttk.Frame(self.master, padding="20", style='TFrame'); main_frame.pack(expand=True, fill=tk.BOTH)
        self._create_main_widgets(main_frame)

    def _create_main_widgets(self, parent):
        input_frame = ttk.Frame(parent, style='TFrame'); input_frame.pack(pady=10, fill=tk.X, anchor='n')

        self.entrada_idade = self._create_input_field(input_frame, "Idade:")
        self.entrada_altura = self._create_input_field(input_frame, "Altura (cm):")
        self.entrada_peso = self._create_input_field(input_frame, "Peso (kg):")
        self.nivel_var, self.nivel_combo = self._create_combobox_field(input_frame, "Nível de treino:", config.NIVEIS_DE_TREINO)

        ttk.Button(parent, text="Gerar Fichas de Treino", command=self.gerar_fichas).pack(pady=15, fill=tk.X)
        self.imc_label = ttk.Label(parent, text="", font=('Arial', 12, 'bold'), style='TLabel'); self.imc_label.pack(pady=5)

        self.notebook = ttk.Notebook(parent); self.notebook.pack(expand=True, fill=tk.BOTH, pady=10)
        self.daily_trees = {}
        for i in range(5):
            day_name = f"Dia {i+1}"
            frame = ttk.Frame(self.notebook, style='TFrame'); self.notebook.add(frame, text=day_name)
            tree = self._create_treeview(frame); tree.bind("<Double-1>", self.ao_clicar_no_exercicio)
            self.daily_trees[day_name] = tree

    def _create_input_field(self, parent, label_text):
        frame = ttk.Frame(parent, style='TFrame'); frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT, padx=5)
        entry = ttk.Entry(frame); entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        return entry

    def _create_combobox_field(self, parent, label_text, values):
        frame = ttk.Frame(parent, style='TFrame'); frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT, padx=5)
        var = tk.StringVar(); combobox = ttk.Combobox(frame, textvariable=var, values=values, state="readonly"); combobox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        if values: combobox.set(values[0])
        return var, combobox

    def _create_treeview(self, parent):
        cols = ["Exercício", "Grupo Muscular", "Séries", "Repetições", "Tipo"]
        tree = ttk.Treeview(parent, columns=cols, show="headings", style='Treeview')
        for col in cols: tree.heading(col, text=col)
        tree.column("Exercício", width=250, anchor=tk.W)
        tree.column("Séries", width=80, anchor=tk.CENTER)
        tree.column("Repetições", width=100, anchor=tk.CENTER)
        tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        return tree

    def gerar_fichas(self):
        try:
            idade, altura, peso, nivel = self.entrada_idade.get(), self.entrada_altura.get(), self.entrada_peso.get(), self.nivel_var.get()

            if not idade.isdigit() or not (altura.replace('.', '', 1).isdigit() and altura.count('.') <= 1) or not (peso.replace('.', '', 1).isdigit() and peso.count('.') <= 1):
                messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos para Idade, Altura e Peso."); return

            idade, altura, peso = int(idade), float(altura), float(peso)
            if altura <= 0 or peso <= 0 or idade <= 0:
                messagebox.showerror("Erro", "Valores de idade, altura e peso devem ser positivos."); return

            self.imc = calcular_imc(peso, altura)
            self.imc_classificacao = classificacao_imc(self.imc)
            aerobic_time = tempo_cardio(self.imc_classificacao)
            
            self.imc_label.config(text=f"IMC: {self.imc:.2f} ({self.imc_classificacao})")

            generator = GeradorDosTreinos(self.df_exercicios)
            self.ficha_semanal = generator.gerar_plano_semanal(nivel, self.imc_classificacao, aerobic_time)
            
            self.mostrar_treino_semanal(self.ficha_semanal)
            
        except (ValueError, TypeError):
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def mostrar_treino_semanal(self, ficha_semanal):
        for day_name, tree in self.daily_trees.items():
            tree.delete(*tree.get_children())
            for ex in ficha_semanal.get(day_name, []):
                values = (ex.get("Nome", "N/A"), ex.get("Grupo", "N/A"), ex.get("Séries", "3"), ex.get("Repetições", "8-12"), ex.get("Tipo", "N/A"))
                if values[4] in ["Aeróbico", "Recuperação"]: values = (values[0], values[1], "-", "-", values[4])
                tree.insert("", "end", values=values)

    def ao_clicar_no_exercicio(self, event):
        tree = event.widget
        if not tree.selection(): return
        item_id = tree.selection()[0]
        exercise_name = tree.item(item_id, 'values')[0]
        
        details = self.df_exercicios[self.df_exercicios["Nome"] == exercise_name]
        if not details.empty: self.mostrar_tela_detalhes_exercicios(details.iloc[0])

    def mostrar_tela_detalhes_exercicios(self, details):
        popup = tk.Toplevel(self.master)
        popup.title(details["Nome"])
        popup.geometry("700x600")
        popup.transient(self.master)
        popup.grab_set()
        popup.focus_set()
        
        content_frame = ttk.Frame(popup, padding="15", style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content_frame, text=details["Nome"], font=('Helvetica', 20, 'bold'), style='TLabel').pack(pady=10)

        details_viz_frame = ttk.Frame(content_frame, style='TFrame')
        details_viz_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(details_viz_frame, text=details["DescricaoDetalhada"], wraplength=300, justify=tk.LEFT).pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        gif_label = ttk.Label(details_viz_frame, background=self.cores['LIGHT_BLUE'])
        gif_label.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        gif_manager = utils.Configuracoes_de_gifs(popup, gif_label)
        
        # Obter nome ou caminho do GIF do CSV
        gif_rel_path = details["GifURL"]

        dir_base_projeto = os.path.dirname(os.path.abspath(__file__))
        
        # Se for apenas o nome do arquivo, buscar na pasta 'assets'
        if not os.path.dirname(gif_rel_path):  
            gif_full_path = os.path.join(dir_base_projeto, "assets", gif_rel_path)
        else:
            gif_full_path = os.path.join(dir_base_projeto, gif_rel_path)

        gif_full_path = os.path.normpath(gif_full_path)

        # Verifica se o arquivo existe
        if not os.path.exists(gif_full_path):
            messagebox.showerror("Erro", f"GIF não encontrado:\n{gif_full_path}")
        else:
            gif_manager.carregar_e_iniciar(gif_full_path)

        ttk.Button(content_frame, text="Fechar", command=popup.destroy).pack(pady=10)
        popup.bind("<Destroy>", lambda e: gif_manager.parar())
