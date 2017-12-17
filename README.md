# Filmow to Letterboxd

Esse programa vai importar os filmes assistidos/avaliados no Filmow pra um arquivo .csv, pra depois ser importado pelo Letterboxd. c:

#### Requisitos:
1. Já ter uma conta no Letterboxd feita (mesmo que não tenha nada lá, só é necessário já ter a criado)
2. Ter uma conta no Filmow
3. Ter conexão com internet

![alt text](https://i.imgur.com/k0CHeVU.gif)

### Para usuários Windows:

Descompacte o arquivo .zip, vá para **filmow_to_letterboxd\Windows**, clique com o botão direito em **\_\_init.bat\_\_** e selecione *Executar como administrador*.

### Para usuários Mac OS:

Descompacte o arquivo .zip baixado com o descompactador de sua escolha.

Dentro da pasta descompactada clique com o botão direito em um canto vazio e escolhar Abrir o terminal aqui.

Dentro do terminal, digite os seguintes comandos:

$ cd filmow_to_letterboxd-master/Mac-e-Linux

$ bxcode-select --install

$ sudo easy_install pip

$ sudo pip install -U pip

$ sudo pip robobrowser

$ ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"

$ brew install python3

$ python3 filmowToLetterboxd.py

### Para usuários Linux:

#### Ubuntu : 
Descompacte o arquivo .zip baixado com o descompactador de sua escolha.

Dentro da pasta descompactada clique com o botão direito em um canto vazio e escolhar Abrir o terminal aqui.

Dentro do terminal, digite os seguintes comandos:

$ cd filmow_to_letterboxd-master/Mac-e-Linux

$ sudo apt-get update

$ sudo apt-get install python3.6

$ sudo pip install -U pip

$ sudo pip install robobrowser

$ python3.6 filmowToLetterboxd.py

## *Usando o programa*

Digite seu nome de usuário e senha (opcional) do Filmow e espere o programa terminar. 
Depois, vá para https://letterboxd.com/import/, SELECT A FILE, selecione o(s) arquivo(s) de extensão *.csv* criado(s) pelo programa
na nova pasta **ARQUIVOS**
Aí é só corrigir se algum filme não foi importado, avaliações erradas, erros, etc.

*Comente algo aqui se tiver alguma sugestão, encontrar algum erro ou manda um email em yanarimy@gmail.com (:*
