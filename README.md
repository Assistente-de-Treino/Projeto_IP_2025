Assistente de Academia



Este é um aplicativo desktop simples desenvolvido em Python com tkinter e pandas que atua como um assistente de academia. Ele calcula o Índice de Massa Corporal (IMC) do usuário e, com base nessa avaliação e no nível de treino, sugere um plano de exercícios personalizado.

✨ Funcionalidades
Cálculo de IMC: O usuário insere idade, altura (em cm) e peso (em kg) para obter seu IMC e classificação.

Recomendação de Exercícios Personalizada:

Gera fichas de treino para 5 dias da semana, seguindo estruturas específicas (ABC para Básico, PPL/Upper/Lower para Intermediário, Upper/Lower para Avançado).

Inclui exercícios compostos e isolados, e considera a demanda energética para usuários com sobrepeso/obesidade.

Adiciona tempo de aeróbico recomendado com base na classificação do IMC.

Visualização Detalhada do Exercício: Ao dar um clique duplo em um exercício na ficha, um pop-up exibe uma descrição detalhada de como executá-lo e um GIF animado do movimento.

Interface Gráfica Estilizada: Design moderno com uma paleta de cores em tons de azul e preto, remetendo a um ambiente de academia.

Modo Tela Cheia: O aplicativo pode ser executado em tela cheia para uma experiência imersiva (saída via Esc).

🚀 Tecnologias Utilizadas
Python: Linguagem de programação principal.

Tkinter: Biblioteca padrão do Python para criação de interfaces gráficas (GUI).

Pandas: Biblioteca para manipulação e análise de dados, utilizada para gerenciar os exercícios a partir de um arquivo CSV.

📁 Estrutura do Projeto
O projeto é organizado nas seguintes pastas para melhor modularidade:

seu_projeto_raiz/
├── main.py             # Ponto de entrada principal do programa
├── config.py           # Configurações globais e estilos de cor
├── logica_de_treinos.py # Lógica para gerar os planos de treino semanais
├── interface.py        # Lógica da interface gráfica principal do aplicativo
├── utils.py            # Funções utilitárias, incluindo o gerenciador de GIFs
├── data/               # Contém os arquivos de dados
│   └── exercicios.csv  # Arquivo CSV com a base de dados de exercícios
└── assets/             # Contém os arquivos de mídia (GIFs dos exercícios)
    ├── exercicio1.gif
    └── exercicio2.gif
    └── ...

⚙️ Como Executar
Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina. Você pode baixá-lo em python.org.

Instale as bibliotecas necessárias via pip:

pip install pandas

Configuração do exercicios.csv
O programa utiliza um arquivo exercicios.csv para carregar os dados dos exercícios. Este arquivo deve estar localizado na pasta data/ dentro do diretório raiz do seu projeto. Ele deve conter as seguintes colunas:

Nome: Nome do exercício.

Grupo: Grupo muscular principal (ex: Peito, Costas, Pernas, Abdômen, Aeróbico).

Nivel: Nível de dificuldade (Básico, Intermediário, Avançado).

DemandaEnergetica: Se o exercício tem "Alta" ou "Baixa" demanda energética.

Tipo: Tipo de exercício (Composto, Isolado, Cardio, Recuperação).

DescricaoDetalhada: Uma breve descrição de como executar o exercício.

GifURL: O caminho relativo para o arquivo GIF correspondente na pasta assets/ (ex: assets/agachamento_livre.gif).

Exemplo de conteúdo para data/exercicios.csv:

Nome,Grupo,Nivel,DemandaEnergetica,Tipo,DescricaoDetalhada,GifURL
Corrida (30 min),Aeróbico,Avançado,Alta,Cardio,"Corra em ritmo moderado, mantendo a frequência cardíaca elevada.","assets/corrida.gif"
Supino Reto com Halteres,Peito,Básico,Baixa,Composto,"Deite-se no banco, halteres acima do peito, desça controladamente e empurre.","assets/supino_halteres.gif"
Agachamento Livre,Pernas,Básico,Baixa,Composto,"Com os pés na largura dos ombros, agache como se fosse sentar, mantendo a coluna reta.","assets/agachamento_livre.gif"
Prancha,Abdômen,Básico,Baixa,Composto,"Mantenha o corpo reto, apoiado nos antebraços e ponta dos pés.","assets/prancha.gif"
# ... (adicione mais exercícios conforme a base de dados fornecida)

Configuração dos GIFs
Coloque todos os arquivos GIF dos exercícios na pasta assets/ dentro do diretório raiz do seu projeto. Certifique-se de que os nomes dos arquivos GIF correspondem exatamente aos caminhos especificados na coluna GifURL do exercicios.csv.

Executando o Aplicativo
Navegue até o diretório raiz do seu projeto (seu_projeto_raiz/) no terminal (ex: cd C:\Users\SeuUsuario\Documentos\GYM_Assistant).

Execute o script principal:

python main.py

🖥️ Uso do Programa
Ao iniciar, você verá uma Tela de Boas-Vindas estilizada. Clique no botão "Iniciar".

Na tela principal, insira sua Idade, Altura (cm) e Peso (kg) nos campos correspondentes.

Selecione seu Nível de treino (Básico, Intermediário, Avançado) na caixa de seleção.

Clique no botão "Gerar Fichas de Treino".

O aplicativo exibirá seu IMC e, em abas separadas, as fichas de treino para os 5 dias da semana.

Clique duas vezes (duplo clique) em qualquer exercício na ficha para abrir um pop-up com sua descrição detalhada e um GIF demonstrando o movimento.

🎨 Estilização e Responsividade
O aplicativo foi estilizado com uma paleta de cores em tons de azul e preto, utilizando os recursos do ttk.Style do Tkinter para criar uma aparência moderna e temática de academia.

A janela principal é configurada com um tamanho fixo de 1200x800 pixels e inicia em modo de tela cheia (fullscreen). Você pode sair do modo tela cheia a qualquer momento pressionando a tecla Esc. A centralização dos elementos na tela de boas-vindas é dinâmica para se adaptar a diferentes resoluções.

🤝 Contribuição
Contribuições são bem-vindas! Se você tiver sugestões de melhorias, detecção de bugs ou novas funcionalidades, sinta-se à vontade para abrir uma issue ou enviar um pull request no repositório do projeto.

📄 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
