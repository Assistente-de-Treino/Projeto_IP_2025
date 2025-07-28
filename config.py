from tkinter import ttk

#variáveis globais com valores fixos, ou seja, são as constantes
#do projeto
CAMINHO_ARQUIVO_CSV = "data/exercicios.csv"
COLUNAS_OBRIGATORIAS = ["Nome", "Grupo", "Nivel", "DemandaEnergetica", "Tipo", "DescricaoDetalhada", "GifURL"]
NIVEIS_DE_TREINO = ["Básico", "Intermediário", "Avançado"]

#aqui foi criado um dicionário para ajudar na hora de mudar as cores temas
#durante o código, associando um nome (exemplo: a cor do cabeçalho é chamada
#por 'cabeçalho' ao invés de usar o código RGB)
CORES = {
    'FUNDO': '#F0F0F0',
    'BOTAO_PRIMARIO': '#0056B3',
    'BOTAO_ATIVO': '#003366',
    'TEXTO_BOTAO': '#FFFFFF',
    'TEXTO_PADRAO': '#333333',
    'CABECALHO_TABELA': '#2C3E50',
    'ABA_SELECIONADA': '#0056B3',
    'ABA_INATIVA': '#A0A0A0',
}

#a função aqui é usada para facilitar na hora de atribuir caracteristicas
#do tema aos widgets, aplicando as cores e fontes de uma só vez ao widget 
def configurar_estilos_globais(style: ttk.Style):
    
    style.theme_use('clam') #tema base do projeto

    #configuração dos widgets
    style.configure('TFrame', background=CORES['FUNDO']) #cor de fundo dos containers
    style.configure('TLabel', background=CORES['FUNDO'], font=('Arial', 11), foreground=CORES['TEXTO_PADRAO']) # textos normais
    style.configure('TEntry', font=('Arial', 11)) #caixa de texto para digitação

    style.configure('TButton', font=('Arial', 11, 'bold'), background=CORES['BOTAO_PRIMARIO'], foreground=CORES['TEXTO_BOTAO'], borderwidth=0) #configuração dos botões
    style.map('TButton', background=[('active', CORES['BOTAO_ATIVO'])]) #aqui é definido o que acontece quando o mouse passa por cima do botão, nesse caso o 
    #mouse passa por cima do botão e ele fica com a cor de fundo 'botao_ativo'

    style.configure('TCombobox', font=('Arial', 11)) #caixa de seleção do nível de treino 

    style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5]) #configurações das abas (dia 1, dia 2... etc)
    style.map('TNotebook.Tab', background=[('selected', CORES['ABA_SELECIONADA'])], foreground=[('selected', CORES['TEXTO_BOTAO'])]) #o que acontece quando uma dessas abas está selecionada 


    #configuração da tabela que mostra os treinos
    style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), background=CORES['CABECALHO_TABELA'], foreground=CORES['TEXTO_BOTAO']) #--> cabeçalho
    style.configure('Treeview', font=('Arial', 10), rowheight=25, fieldbackground=CORES['FUNDO']) #--> corpo da tabela

    #cor da linha quando clica nela
    style.map('Treeview', background=[('selected', CORES['BOTAO_PRIMARIO'])])