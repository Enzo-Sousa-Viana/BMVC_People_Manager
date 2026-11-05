<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banco | BMVC People Manager</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <header class="topbar">
        <div>
            <span class="eyebrow">BMVC PEOPLE MANAGER</span>
            <h1>Banco de pessoas</h1>
        </div>
        <div class="user-area">
            <span>Olá, {{user}}</span>
            <form action="/logout" method="post">
                <button class="button-secondary" type="submit">Sair</button>
            </form>
        </div>
    </header>

    <main class="container">
        <section class="panel">
            <h2>Cadastrar pessoa</h2>
            <form action="/pessoas" method="post" class="form-inline">
                <div class="field">
                    <label for="nome">Nome</label>
                    <input id="nome" name="nome" type="text" maxlength="100" required>
                </div>
                <div class="field small-field">
                    <label for="idade">Idade</label>
                    <input id="idade" name="idade" type="number" min="0" max="120" required>
                </div>
                <button type="submit">Adicionar</button>
            </form>
        </section>

        <section class="panel">
            <div class="section-heading">
                <div>
                    <h2>Registros cadastrados</h2>
                    <p class="muted">Os dados são armazenados em arquivo JSON.</p>
                </div>
                <span class="count">{{len(pessoas)}} registro(s)</span>
            </div>

            % if pessoas:
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr><th>ID</th><th>Nome</th><th>Idade</th><th>Ação</th></tr>
                        </thead>
                        <tbody>
                            % for pessoa in pessoas:
                                <tr>
                                    <td>{{pessoa["id"]}}</td>
                                    <td>{{pessoa["nome"]}}</td>
                                    <td>{{pessoa["idade"]}}</td>
                                    <td>
                                        <form action="/pessoas/{{pessoa['id']}}/delete" method="post">
                                            <button class="button-danger" type="submit">Excluir</button>
                                        </form>
                                    </td>
                                </tr>
                            % end
                        </tbody>
                    </table>
                </div>
            % else:
                <p class="empty">Nenhuma pessoa cadastrada ainda.</p>
            % end
        </section>
        <p class="api-note">API disponível em <code>/api/pessoas</code> — GET, POST, PUT e DELETE.</p>
    </main>
</body>
</html>
