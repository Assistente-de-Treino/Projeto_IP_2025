ASSISTENTE DE ACADEMIA
Este é um aplicativo desktop simples desenvolvido em Python com tkinter e pandas que atua como um assistente de academia. Ele calcula o Índice de Massa Corporal (IMC) do usuário e, com base nessa avaliação e no nível de treino, sugere um plano de exercícios personalizado.

✨ FUNCIONALIDADES PRINCIPAIS
CÁLCULO DE IMC: O usuário insere idade, altura (em cm) e peso (em kg) para obter seu IMC e classificação correspondente.

RECOMENDAÇÃO DE EXERCÍCIOS PERSONALIZADA:

Gera fichas de treino para 5 dias da semana, seguindo estruturas específicas (ABC para nível Básico, PPL/Upper/Lower para Intermediário e Upper/Lower para Avançado).

Inclui exercícios compostos e isolados, considerando a demanda energética para usuários com sobrepeso ou obesidade.

Adiciona o tempo de aeróbico recomendado com base na classificação do IMC do usuário.

VISUALIZAÇÃO DETALHADA DO EXERCÍCIO: Ao dar um clique duplo em qualquer exercício na ficha de treino, um pop-up é exibido, mostrando uma descrição detalhada de como executá-lo e um GIF animado do movimento.

INTERFACE GRÁFICA ESTILIZADA: Apresenta um design moderno com uma paleta de cores em tons de azul e preto, remetendo a um ambiente de academia.

MODO TELA CHEIA: O aplicativo pode ser executado em tela cheia para uma experiência imersiva. A saída do modo tela cheia é feita pressionando a tecla Esc.

🚀 TECNOLOGIAS UTILIZADAS
PYTHON: Linguagem de programação principal do projeto.

TKINTER: Biblioteca padrão do Python para a criação de interfaces gráficas de usuário (GUI).

PANDAS: Biblioteca utilizada para manipulação e análise de dados, essencial para gerenciar a base de dados de exercícios a partir de um arquivo CSV.

📁 ESTRUTURA DO PROJETO
O projeto é organizado nas seguintes pastas para garantir uma melhor modularidade e organização do código:

seu_projeto_raiz/
├── main.py                 # Ponto de entrada principal do programa.
├── config.py               # Contém configurações globais e definições de estilos de cor.
├── logica_de_treinos.py    # Abriga a lógica para gerar os planos de treino semanais.
├── interface.py            # Responsável pela lógica da interface gráfica principal do aplicativo.
├── utils.py                # Inclui funções utilitárias diversas, como o gerenciador de GIFs.
├── data/                   # PASTA DE DADOS.
│   └── exercicios.csv      # Arquivo CSV com a base de dados de exercícios.
└── assets/                 # PASTA DE MÍDIA.
    ├── exercicio1.gif
    └── exercicio2.gif
    └── ...                 # Contém todos os arquivos GIF dos exercícios.

⚙️ COMO EXECUTAR O APLICATIVO
PRÉ-REQUISITOS
Certifique-se de ter o Python instalado em sua máquina. Você pode baixá-lo diretamente do site oficial: python.org.

Em seguida, instale as bibliotecas necessárias utilizando o pip, o gerenciador de pacotes do Python:

pip install pandas

CONFIGURAÇÃO DO ARQUIVO exercicios.csv
O programa depende de um arquivo exercicios.csv para carregar os dados dos exercícios. Este arquivo DEVE estar localizado na pasta data/ dentro do diretório raiz do seu projeto. Ele precisa conter as seguintes colunas, com os dados formatados corretamente:

Nome: Nome do exercício.

Grupo: Grupo muscular principal (ex: Peito, Costas, Pernas, Abdômen, Aeróbico).

Nivel: Nível de dificuldade (Básico, Intermediário, Avançado).

DemandaEnergetica: Indica se o exercício tem "Alta" ou "Baixa" demanda energética.

Tipo: Tipo de exercício (Composto, Isolado, Cardio, Recuperação).

DescricaoDetalhada: Uma breve descrição de como executar o exercício.

GifURL: O caminho RELATIVO para o arquivo GIF correspondente, localizado na pasta assets/ (ex: assets/agachamento_livre.gif).

EXEMPLO DE CONTEÚDO PARA data/exercicios.csv:

Nome,Grupo,Nivel,DemandaEnergetica,Tipo,DescricaoDetalhada,GifURL
Corrida (30 min),Aeróbico,Avançado,Alta,Cardio,"Corra em ritmo moderado, mantendo a frequência cardíaca elevada.","assets/corrida.gif"
Supino Reto com Halteres,Peito,Básico,Baixa,Composto,"Deite-se no banco, halteres acima do peito, desça controladamente e empurre.","assets/supino_halteres.gif"
Agachamento Livre,Pernas,Básico,Baixa,Composto,"Com os pés na largura dos ombros, agache como se fosse sentar, mantendo a coluna reta.","assets/agachamento_livre.gif"
Prancha,Abdômen,Básico,Baixa,Composto,"Mantenha o corpo reto, apoiado nos antebraços e ponta dos pés.","assets/prancha.gif"
# ... (adicione mais exercícios conforme a base de dados fornecida)

CONFIGURAÇÃO DOS ARQUIVOS GIF
Todos os arquivos GIF que demonstram os exercícios DEVEM ser colocados na pasta assets/ dentro do diretório raiz do seu projeto. É FUNDAMENTAL que os nomes dos arquivos GIF e seus caminhos na coluna GifURL do exercicios.csv correspondam EXATAMENTE aos nomes dos arquivos na pasta assets/.

EXECUTANDO O APLICATIVO
Abra o terminal (ou o terminal integrado do VS Code).

Navegue até o diretório raiz do seu projeto (seu_projeto_raiz/). Por exemplo:

cd C:\Users\SeuUsuario\Documentos\GYM_Assistant

Execute o script principal do programa:

python main.py

🖥️ COMO UTILIZAR O PROGRAMA
Ao iniciar o aplicativo, você será recebido por uma TELA DE BOAS-VINDAS com um design estilizado. Clique no botão "Iniciar" para prosseguir.

Na tela principal, insira sua IDADE, ALTURA (em cm) e PESO (em kg) nos campos de entrada correspondentes.

Selecione seu NÍVEL DE TREINO (Básico, Intermediário, Avançado) utilizando a caixa de seleção.

Clique no botão "Gerar Fichas de Treino".

O aplicativo irá exibir seu IMC e, em abas separadas, as fichas de treino personalizadas para os 5 DIAS DA SEMANA.

Para visualizar detalhes sobre um exercício específico, incluindo uma descrição e um GIF demonstrativo, CLIQUE DUAS VEZES (DUPLO CLIQUE) sobre o nome do exercício na ficha.

🎨 ESTILIZAÇÃO E RESPONSIVIDADE
O aplicativo foi cuidadosamente estilizado com uma paleta de cores em tons de azul e preto, utilizando os recursos do ttk.Style do Tkinter para criar uma aparência moderna e temática de academia.

A janela principal é configurada com um tamanho fixo de 1200x800 pixels e inicia em modo de tela cheia (fullscreen). Você pode sair do modo tela cheia a qualquer momento pressionando a tecla Esc. A centralização dos elementos na tela de boas-vindas é dinâmica, adaptando-se a diferentes resoluções de tela para garantir uma apresentação consistente.

🤝 CONTRIBUIÇÃO
Contribuições para este projeto são muito bem-vindas! Se você tiver sugestões de melhorias, encontrar algum bug ou desejar implementar novas funcionalidades, sinta-se à vontade para abrir uma issue ou enviar um pull request no repositório do projeto no GitHub.

📄 LICENÇA
Este projeto está licenciado sob a Licença MIT. Para mais detalhes, consulte o arquivo LICENSE no repositório.
