import tkinter as tk
from tkinter import ttk, messagebox
import config
import utils
from logica_de_treinos import GeradorDosTreinos

<<<<<<< HEAD
class AppAssistenteDeTreinos:
    def __init__(self, master):
=======
class GymAssistantApp:
    def inicio(self, master):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        self.master = master
        master.title("Assistente de Treinos - Ficha de Treino")
        master.geometry("1200x800")
        master.bind("<Escape>", lambda e: master.attributes('-fullscreen', False))

<<<<<<< HEAD
        #estilização
        self.style = ttk.Style()
        config.configurar_estilos(self.style)

        #carrega os dados
        self.df_exercicios = utils.carregar_dados_exercicios()
=======
        # Estilização
        self.style = ttk.Style()
        config.setup_styles(self.style)

        # Carregar dados
        self.df_exercicios = utils.load_exercise_data()
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        if self.df_exercicios is None:
            master.destroy()
            return

<<<<<<< HEAD
        self.mostrar_tela_inicial()

    def limpar_interface(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_interface()
=======
        self.show_welcome_screen()

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def tela_inicio(self):
        self.clear_frame()
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        welcome_frame = ttk.Frame(self.master, style='TFrame')
        welcome_frame.pack(expand=True, fill=tk.BOTH)
        
        canvas = tk.Canvas(welcome_frame, highlightthickness=0, bg=config.LIGHT_BLUE)
        canvas.pack(expand=True, fill=tk.BOTH)

        # Simplicidade na tela de boas-vindas
        ttk.Label(canvas, text="GYM Assistant", font=('Helvetica', 64, 'bold'), foreground=config.DEEP_BLUE, background=config.LIGHT_BLUE).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
<<<<<<< HEAD
        ttk.Button(canvas, text="Iniciar", command=self.mostrar_interface_principal, style='TButton').place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def mostrar_interface_principal(self):
        self.limpar_interface()
=======
        ttk.Button(canvas, text="Iniciar", command=self.show_main_app, style='TButton').place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def show_main_app(self):
        self.clear_frame()
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        main_frame = ttk.Frame(self.master, padding="20", style='TFrame')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        self._create_main_widgets(main_frame)

<<<<<<< HEAD
    def _create_main_widgets(self, parent):
=======
    def criar_widgets(self, parent):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        input_frame = ttk.Frame(parent, style='TFrame')
        input_frame.pack(pady=10, fill=tk.X, anchor='n')

        # Campos de entrada
        self.entrada_idade = self._create_input_field(input_frame, "Idade:")
        self.entrada_altura = self._create_input_field(input_frame, "Altura (cm):")
        self.entrada_peso = self._create_input_field(input_frame, "Peso (kg):")
<<<<<<< HEAD
        self.nivel_var, self.nivel_combo = self._create_combobox_field(input_frame, "Nível de treino:", config.NIVEIS_DE_TREINO)
=======
        self.nivel_var, self.nivel_combo = self._create_combobox_field(input_frame, "Nível de treino:", config.Niveis_de_treino)
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411

        ttk.Button(parent, text="Gerar Fichas de Treino", command=self.gerar_fichas).pack(pady=15, fill=tk.X)
        self.imc_label = ttk.Label(parent, text="", font=('Arial', 12, 'bold'), style='TLabel')
        self.imc_label.pack(pady=5)

<<<<<<< HEAD
        #Tela das fichas de exercícios
=======
        # Notebook para as fichas
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill=tk.BOTH, pady=10)
        self.daily_trees = {}
        for i in range(5):
            day_name = f"Dia {i+1}"
            frame = ttk.Frame(self.notebook, style='TFrame')
            self.notebook.add(frame, text=day_name)
            tree = self._create_treeview(frame)
<<<<<<< HEAD
            tree.bind("<Double-1>", self.ao_clicar_no_exercicio)
            self.daily_trees[day_name] = tree

    def _create_input_field(self, parent, label_text):
=======
            tree.bind("<Double-1>", self.on_exercise_click)
            self.daily_trees[day_name] = tree

    def criar_campo_entrada(self, parent, label_text):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        frame = ttk.Frame(parent, style='TFrame')
        frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT, padx=5)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        return entry

<<<<<<< HEAD
    def _create_combobox_field(self, parent, label_text, values):
=======
    def criar_caixa_texto(self, parent, label_text, values):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        frame = ttk.Frame(parent, style='TFrame')
        frame.pack(pady=2, fill=tk.X)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT, padx=5)
        var = tk.StringVar()
        combobox = ttk.Combobox(frame, textvariable=var, values=values, state="readonly")
        combobox.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        if values:
            combobox.set(values[0])
        return var, combobox

<<<<<<< HEAD
    def _create_treeview(self, parent):
=======
    def visualizacao(self, parent):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
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
<<<<<<< HEAD
            imc_class = utils.classificar_imc(imc)
            aerobic_time = utils.obter_tempo_aerobico(imc_class)
=======
            imc_class = utils.get_imc_classification(imc)
            aerobic_time = utils.get_aerobic_time(imc_class)
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
            
            self.imc_label.config(text=f"IMC: {imc:.2f} ({imc_class})")

            generator = GeradorDosTreinos(self.df_exercicios)
<<<<<<< HEAD
            ficha_semanal = generator.gerar_plano_semanal(nivel, imc_class, aerobic_time)
            
            self.mostrar_treino_semanal(ficha_semanal)
=======
            ficha_semanal = generator.generate_weekly_plan(nivel, imc_class, aerobic_time)
            
            self.display_weekly_plan(ficha_semanal)
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411

        except (ValueError, TypeError):
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

<<<<<<< HEAD
    def mostrar_treino_semanal(self, ficha_semanal):
        for day_name, tree in self.daily_trees.items():
            tree.delete(*tree.get_children())
=======
    def plano_semanal(self, ficha_semanal):
        for day_name, tree in self.daily_trees.items():
            tree.delete(*tree.get_children()) # Limpa a tabela
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
            exercises = ficha_semanal.get(day_name, [])
            for ex in exercises:
                values = (
                    ex.get("Nome", "N/A"), ex.get("Grupo", "N/A"),
                    ex.get("Séries", "3"), ex.get("Repetições", "8-12"),
                    ex.get("Tipo", "N/A")
                )
                tree.insert("", "end", values=values)

<<<<<<< HEAD
    def ao_clicar_no_exercicio(self, event):
=======
    def clickar_exercicio(self, event):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
        tree = event.widget
        if not tree.selection(): return
        
        item_id = tree.selection()[0]
        exercise_name = tree.item(item_id, 'values')[0]
        
        details = self.df_exercicios[self.df_exercicios["Nome"] == exercise_name]
        if not details.empty:
<<<<<<< HEAD
            self.mostrar_tela_detalhes_exercicios(details.iloc[0])

    def mostrar_tela_detalhes_exercicios(self, details):
=======
            self.show_exercise_details_popup(details.iloc[0])

    def mostrar_exercicio(self, details):
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
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

<<<<<<< HEAD
        gif_manager = utils.Configuracoes_de_gifs(popup, gif_label)
        gif_manager.carregar_e_iniciar(details["GifURL"])

        ttk.Button(content_frame, text="Fechar", command=popup.destroy).pack(pady=10)

        #faz o gif parar quando o popup fecha
        popup.bind("<Destroy>", lambda e: gif_manager.parar())
=======
        gif_manager = utils.GifManager(popup, gif_label)
        gif_manager.load_and_play(details["gifURl"])

        ttk.Button(content_frame, text="Fechar", command=popup.destroy).pack(pady=10)

        # Garante que a animação pare quando o popup fechar
        popup.bind("<Destroy>", lambda e: gif_manager.stop()) 
>>>>>>> 3c62c46341ee4527f69bf8c9348f7e00331c9411
