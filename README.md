<<<<<<< HEAD
# BMVC People Manager

Projeto acadêmico desenvolvido com o framework BMVC (Bottle), com dois recursos: **portal** e **banco**.

## Funcionalidades

- Login e logout com sessão armazenada em cookie.
- Acesso restrito à área Banco.
- Modelo `UserAccount` para autenticação.
- Modelo `Pessoa` com `id`, `nome` e `idade`.
- Persistência local em arquivos JSON.
- API com operações GET, POST, PUT e DELETE.
- Interface web para cadastrar, listar e excluir pessoas.

## Requisitos

- Python 3.10 ou superior
- Linux (para executar os exemplos cURL)
- Biblioteca Bottle

## Instalação e execução

Na pasta raiz do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python route.py
```

Acesse `http://127.0.0.1:8080/portal`.

### Usuário inicial

Na primeira execução, o sistema cria automaticamente:

- Usuário: `admin`
- Senha: `admin123`

Altere essas credenciais antes de qualquer uso fora do ambiente acadêmico. A autenticação deste projeto é demonstrativa; as sessões ficam em memória e são encerradas quando o servidor reinicia.

## Testes da API com cURL

Os comandos abaixo devem ser executados em outro terminal, com o servidor ligado.

### 1. Login e armazenamento do cookie

```bash
curl -i -c cookies.txt -X POST http://127.0.0.1:8080/portal \
  -d "username=admin" \
  -d "password=admin123"
```

### 2. READ — listar pessoas

```bash
curl -i -b cookies.txt http://127.0.0.1:8080/api/pessoas
```

### 3. CREATE — cadastrar pessoa

```bash
curl -i -b cookies.txt -X POST http://127.0.0.1:8080/api/pessoas \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria Silva","idade":22}'
```

### 4. UPDATE — atualizar pessoa de ID 1

```bash
curl -i -b cookies.txt -X PUT http://127.0.0.1:8080/api/pessoas/1 \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria Souza","idade":23}'
```

### 5. DELETE — excluir pessoa de ID 1

```bash
curl -i -b cookies.txt -X DELETE http://127.0.0.1:8080/api/pessoas/1
```

### 6. Logout

```bash
curl -i -b cookies.txt -X POST http://127.0.0.1:8080/logout
```

> O ID usado no PUT/DELETE deve corresponder ao ID retornado pelo POST. O exemplo usa `1` considerando que o banco está vazio no primeiro teste.

## Organização da arquitetura

```text
bmvc_people_manager/
├── route.py
├── requirements.txt
├── README.md
└── app/
    ├── controllers/
    │   ├── application.py
    │   ├── datarecord.py
    │   └── db/
    │       ├── user_accounts.json
    │       └── pessoas.json
    ├── models/
    │   ├── user_account.py
    │   └── pessoa.py
    ├── views/
    │   └── html/
    │       ├── portal.tpl
    │       ├── banco.tpl
    │       └── helper.tpl
    └── static/
        └── css/
            └── style.css
```

## Arquitetura

- **Model:** `UserAccount` e `Pessoa` representam os dados do sistema.
- **DataRecord:** administra a leitura e gravação dos arquivos JSON, autenticação e operações sobre pessoas.
- **Application:** concentra a lógica da aplicação e prepara os dados enviados às views.
- **Views:** arquivos Bottle TPL responsáveis pela interface.
- **Routes:** `route.py` recebe as requisições HTTP e encaminha cada operação ao controlador.

## Respostas esperadas

- `200`: operação realizada com sucesso.
- `201`: registro criado.
- `400`: dados inválidos.
- `401`: usuário não autenticado.
- `404`: registro não encontrado.

## Observação sobre segurança

O projeto é voltado ao exercício acadêmico. As senhas são armazenadas com hash PBKDF2, mas as sessões são mantidas apenas em memória e o cookie está configurado para desenvolvimento local em HTTP. Para produção, seriam necessários HTTPS, gerenciamento persistente de sessões, proteção CSRF e outras medidas.
=======
# BMVC_People_Manager
>>>>>>> 88ead8578958df35c06558a9485ab9c539ac4338
