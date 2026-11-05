<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal | BMVC People Manager</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body class="login-page">
    <main class="login-card">
        <span class="eyebrow">BMVC PEOPLE MANAGER</span>
        <h1>Acesse o portal</h1>
        <p class="muted">Entre com suas credenciais para gerenciar os registros.</p>
        % if error:
            <div class="alert">{{error}}</div>
        % end
        <form action="/portal" method="post" class="form-stack">
            <label for="username">Usuário</label>
            <input id="username" name="username" type="text" placeholder="Seu usuário" required>
            <label for="password">Senha</label>
            <input id="password" name="password" type="password" placeholder="Sua senha" required>
            <button type="submit">Entrar</button>
        </form>
        <p class="hint">Acesso inicial: <strong>admin</strong> / <strong>admin123</strong></p>
    </main>
</body>
</html>
