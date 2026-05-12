# FinanceAPI

API de finanças pessoais feita com FastAPI, SQLAlchemy e PostgreSQL.

## Sobre

Esse projeto gerencia usuários, contas, categorias, transações, transferências, metas e relatórios de finanças.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT (`python-jose`)
- bcrypt

## Instalação

1. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Configure o arquivo `.env` com os valores:
   ```env
   SECRET_KEY=sua_chave_secreta_aqui
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/financeapi
   ```

## Executando a aplicação

```bash
uvicorn main:app --reload
```

## Testes

```bash
python -m pytest -q
```

## Observações

- O projeto inicializa a criação das tabelas automaticamente no `lifespan` do FastAPI.
- Não inclua o arquivo `.env` no repositório para proteger segredos.
# FinanceAPI
