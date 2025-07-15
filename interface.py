import tkinter as tk
from tkinter import ttk, messagebox
import config
import utils
from logica_de_treinos import GeradorDosTreinos

class AppAssistenteDeTreinos:
    def __init__(self, master):
        self.master = master
        master.title("Assistente de Treinos - Ficha de Treino")
        master.geometry("1200x800")
        master.bind("<Escape>", lambda e: master.attributes('-fullscreen', False))

        #estilização
        self.style = ttk.Style()
        config.configurar_estilos(self.style)

        #carrega os dados
        self.df_exercicios = utils.carregar_dados_exercicios()
        if self.df_exercicios is None:
            master.destroy()
            return

        self.mostrar_tela_inicial()

    def limpar_interface(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_interface()
        welcome_frame = ttk.Frame(self.master, style='TFrame')
        welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        canvas = tk.Canvas(welcome_frame, highlightthickness=0, bg=config.LIGHT_BLUE)
        canvas.pack(expand=True, fill=tk.BOTH)

        # Simplicidade na tela de boas-vindas
        ttk.Label(canvas, text="GYM Assistant", font=('Helvetica', 64, 'bold'), foreground=config.DEEP_BLUE, background=config.LIGHT_BLUE).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        ttk.Button(canvas, text="Iniciar", command=self.mostrar_interface_principal, style='TButton').place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def mostrar_interface_principal(self):
        self.limpar_interface()
        main_frame = ttk.Frame(self.master, padding="20", style='TFrame')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        self._create_main_widgets(main_frame)

    def _create_main_widgets(self, parent):
        input_frame = ttk.Frame(parent, style='TFrame')
        input_frame.pack(pady=10, fill=tk.X, anchor='n')

        # Campos de entrada
        self.entrada_idade = self._create_input_field(input_frame, "Idade:")
        self.entrada_altura = self._create_input_field(input_frame, "Altura (cm):")
        self.entrada_peso = self._create_input_field(input_frame, "Peso (kg):")
        self.nivel_var, self.nivel_combo = self._create_combobox_field(input_frame, "Nível de treino:", config.NIVEIS_DE_TREINO)

        ttk.Button(parent, text="Gerar Fichas de Treino", command=self.gerar_fichas).pack(pady=15, fill=tk.X)
        self.imc_label = ttk.Label(parent, text="", font=('Arial', 12, 'bold'), style='TLabel')
        self.imc_label.pack(pady=5)

        #Tela das fichas de exercícios
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill=tk.BOTH, pady=10)
        self.daily_trees = {}
        for i in range(5):
            day_name = f"Dia {i+1}"
            frame = ttk.Frame(self.notebook, style='TFrame')
            self.notebook.add(frame, text=day_name)
            tree = self._create_treeview(frame)
            tree.bind("<Double-1>", self.ao_clicar_no_exercicio)
            self.daily_trees[day_name] = tree

    def _create_input_field(self, parent, label_text):
        frame = ttk.Frame(parent, style='TFrame')
        frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT, padx=5)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        return entry

    def _create_combobox_field(self, parent, label_text, values):
        frame = ttk.Frame(parent, style='TFrame')
        frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT, padx=5)
        var = tk.StringVar()
        combobox = ttk.Combobox(frame, textvariable=var, values=values, state="readonly")
        combobox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        if values:
            combobox.set(values[0])
        return var, combobox

    def _create_treeview(self, parent):
        cols = ["Exercício", "Grupo Muscular", "Séries", "Repetições", "Tipo"]
        tree = ttk.Treeview(parent, columns=cols, show="headings", style='Treeview')
        for col in cols:
            tree.heading(col, text=col)
        tree.column("Exercício", width=250, anchor=tk.W)
        tree.column("Séries", width=80, anchor=tk.CENTER)
        tree.column("Repetições", width=100, anchor=tk.CENTER)
        tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        return tree

    def gerar_fichas(self):
        try:
            idade = int(self.entrada_idade.get())
            altura = float(self.entrada_altura.get())
            peso = float(self.entrada_peso.get())
            nivel = self.nivel_var.get()

            if altura <= 0 or peso <= 0 or idade <= 0:
                messagebox.showerror("Erro", "Valores de idade, altura e peso devem ser positivos.")
                return

            imc = utils.calcular_imc(peso, altura)
            imc_class = utils.classificar_imc(imc)
            aerobic_time = utils.obter_tempo_aerobico(imc_class)
            
            self.imc_label.config(text=f"IMC: {imc:.2f} ({imc_class})")

            generator = GeradorDosTreinos(self.df_exercicios)
            ficha_semanal = generator.gerar_plano_semanal(nivel, imc_class, aerobic_time)
            
            self.mostrar_treino_semanal(ficha_semanal)

        except (ValueError, TypeError):
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

    def mostrar_treino_semanal(self, ficha_semanal):
        for day_name, tree in self.daily_trees.items():
            tree.delete(*tree.get_children())
            exercises = ficha_semanal.get(day_name, [])
            for ex in exercises:
                values = (
                    ex.get("Nome", "N/A"), ex.get("Grupo", "N/A"),
                    ex.get("Séries", "3"), ex.get("Repetições", "8-12"),
                    ex.get("Tipo", "N/A")
                )
                tree.insert("", "end", values=values)

    def ao_clicar_no_exercicio(self, event):
        tree = event.widget
        if not tree.selection(): return
        
        item_id = tree.selection()[0]
        exercise_name = tree.item(item_id, 'values')[0]
        
        details = self.df_exercicios[self.df_exercicios["Nome"] == exercise_name]
        if not details.empty:
            self.mostrar_tela_detalhes_exercicios(details.iloc[0])

    def mostrar_tela_detalhes_exercicios(self, details):
        popup = tk.Toplevel(self.master)
        popup.title(details["Nome"])
        popup.geometry("700x600")
        popup.transient(self.master)
        popup.grab_set()
        
        content_frame = ttk.Frame(popup, padding="15", style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content_frame, text=details["Nome"], font=('Helvetica', 20, 'bold'), style='TLabel').pack(pady=10)

        details_viz_frame = ttk.Frame(content_frame, style='TFrame')
        details_viz_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Label(details_viz_frame, text=details["DescricaoDetalhada"], wraplength=300, justify=tk.LEFT).pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        gif_label = ttk.Label(details_viz_frame, background=config.LIGHT_BLUE)
        gif_label.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        gif_manager = utils.Configuracoes_de_gifs(popup, gif_label)
        gif_manager.carregar_e_iniciar(details["GifURL"])

        ttk.Button(content_frame, text="Fechar", command=popup.destroy).pack(pady=10)

        #faz o gif parar quando o popup fecha
        popup.bind("<Destroy>", lambda e: gif_manager.parar())