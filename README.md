# Filmow to Letterboxd

Exporta os filmes que você marcou como assistidos no Filmow para um arquivo
CSV aceito pelo Letterboxd.

## Antes de começar

1. Nesta página do GitHub, clique no botão verde **Code**.
2. Clique em **Download ZIP**.
3. Extraia o ZIP para uma pasta fácil de encontrar.
4. Siga abaixo as instruções do seu sistema.

Você precisa ter o Python 3.10 ou mais recente instalado.

## Windows

### Instalação

1. Baixe o Python em https://www.python.org/downloads/windows/.
2. Abra o instalador.
3. Marque a opção **Add Python to PATH** e conclua a instalação.
4. Abra a pasta extraída do projeto.
5. Clique na barra de endereço do Explorador de Arquivos, digite `cmd` e
   pressione **Enter**.
6. Na janela aberta, execute estes comandos, um por vez:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install .
```

A instalação só precisa ser feita uma vez.

### Como usar

Abra o terminal na pasta do projeto como explicado acima e execute:

```bat
.venv\Scripts\activate.bat
filmow-to-letterboxd SEU_USUARIO
```

## macOS

### Instalação

1. Baixe e instale o Python em https://www.python.org/downloads/macos/.
2. Abra o aplicativo **Terminal**.
3. Digite `cd `, incluindo o espaço no final.
4. Arraste a pasta extraída do projeto para dentro do Terminal e pressione
   **Enter**.
5. Execute estes comandos, um por vez:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

A instalação só precisa ser feita uma vez.

### Como usar

Abra o Terminal na pasta do projeto como explicado acima e execute:

```sh
source .venv/bin/activate
filmow-to-letterboxd SEU_USUARIO
```

## Linux

### Instalação

1. Abra a pasta extraída do projeto.
2. Clique com o botão direito dentro da pasta e escolha **Abrir no Terminal**.
3. Instale o Python caso ainda não esteja instalado.

No Ubuntu, Debian ou Linux Mint:

```sh
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

No Fedora:

```sh
sudo dnf install python3 python3-pip
```

4. Execute estes comandos, um por vez:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

A instalação só precisa ser feita uma vez.

### Como usar

Abra o terminal na pasta do projeto como explicado acima e execute:

```sh
source .venv/bin/activate
filmow-to-letterboxd SEU_USUARIO
```

## Qual é o meu usuário?

Seu usuário aparece no endereço do seu perfil do Filmow. Por exemplo:

```text
https://filmow.com/usuario/maria/
```

Nesse caso, o comando seria:

```sh
filmow-to-letterboxd maria
```

## Importando no Letterboxd

1. Aguarde até aparecer a mensagem **Concluído**.
2. O arquivo CSV estará na pasta do projeto.
3. Acesse https://letterboxd.com/import/.
4. Clique em **Select a file** e escolha o arquivo CSV criado.

Perfis com muitos filmes podem gerar mais de um CSV. Importe todos eles.

<!-- ## Pix

Gostou? Se economizou seu tempo e quiser agradecer, pode me pagar um café via
Pix.

**Chave Pix aleatória:** `COLOQUE_SUA_CHAVE_PIX_AQUI` -->
