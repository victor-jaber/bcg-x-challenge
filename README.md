
# BCG-X Challenge

Este guia fornece as instruções para configurar e executar o projeto localmente utilizando Docker.

## Pré-requisitos

- Docker instalado em sua máquina
- Chave de API da OpenAI

## Configuração do Projeto

### 1. Clonar o Repositório

Clone o repositório do GitHub usando o comando abaixo:

```bash
git clone https://github.com/victor-jaber/bcg-x-challenge.git
```

### 2. Navegar até o Repositório

Entre na pasta do repositório clonado:

```bash
cd bcg-x-challenge
```

### 3. Configurar o Backend

- Dentro do repositório, há duas pastas principais: `back-bcg` e `front-bcg`.
- Navegue até a pasta `back-bcg`:

  ```bash
  cd back-bcg
  ```

- Em seguida, vá para a pasta `config`:

  ```bash
  cd config
  ```

- Renomeie o arquivo `config.ini.example` para `config.ini`:

  ```bash
  mv config.ini.example config.ini
  ```

- Abra o arquivo `config.ini` em um editor de texto e localize a linha 86. Substitua o valor da chave OpenAI pela sua chave de API:

  ```ini
  api_key=YOUR_OPENAI_API_KEY
  ```

  > **Nota:** Substitua `YOUR_OPENAI_API_KEY` pela sua chave de API da OpenAI.

- Salve e feche o arquivo.

### 4. Voltar à Pasta Raiz

Após configurar o arquivo `config.ini`, retorne à pasta raiz do projeto onde estão as pastas `front-bcg` e `back-bcg`:

```bash
cd ../..
```

### 5. Iniciar o Docker

Execute o seguinte comando para iniciar o projeto com Docker:

- Para visualizar logs diretamente no terminal:

  ```bash
  docker-compose up
  ```

- Para rodar em modo "detached" (em segundo plano):

  ```bash
  docker-compose up -d
  ```

### 6. Acessar a Aplicação

Após o Docker iniciar, acesse a aplicação no navegador em [localhost:3000](http://localhost:3000).

---

Pronto! Agora a aplicação está configurada e rodando localmente.
