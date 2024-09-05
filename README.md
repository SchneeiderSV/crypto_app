# Calculadora de Criptomoedas

Esta é uma aplicação web simples para calcular a quantidade de criptomoedas que podem ser compradas com um valor em BRL (Reais). A aplicação também exibe as últimas 10 transações realizadas.

## Funcionalidades

- **Calculadora de Criptomoedas**: Permite ao usuário selecionar uma criptomoeda e inserir um valor em BRL para calcular a quantidade de criptomoedas que podem ser compradas.
- **Histórico de Transações**: Exibe as últimas 10 transações realizadas, mostrando a criptomoeda, a quantidade comprada e o valor em BRL.

## Tecnologias Utilizadas

- **Frontend**: HTMX, CSS, Javascript
- **Backend**: FastAPI (Python)
- **Banco de Dados**: SQLite
- **Templates**: Jinja2
- **API de Preços**: CoinGecko
- **Gráficos**: ChartJS

## Estrutura do Projeto

- `main.py`: Contém a lógica do servidor FastAPI.
- `templates/`: Contém os arquivos HTML para renderização das páginas.
- `static/`: Contém os arquivos estáticos como CSS.
- `transactions.db`: Banco de dados SQLite para armazenar as transações.

## Como Executar

1. Clone o repositório:
    ```bash
    git clone https://github.com/SchneeiderSV/crypto_app
    cd crypto_app
    ```

2. Crie um ambiente virtual e instale as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Inicie o servidor:
    ```bash
    uvicorn main:app --reload
    ```

4. Acesse a aplicação no navegador:
    ```
    http://127.0.0.1:8000
    ```

## Exemplo de Uso

1. Selecione uma criptomoeda no formulário.
2. Insira um valor em BRL.
3. Clique em "Calcular".
4. O resultado será exibido abaixo do formulário e o histórico de transações será atualizado.
