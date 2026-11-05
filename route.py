from bottle import Bottle, request, response, redirect, run
from app.controllers.application import Application

app = Bottle()
ctl = Application()


@app.get("/")
def index():
    redirect("/portal")


@app.get("/portal")
def portal():
    return ctl.portal()


@app.post("/portal")
def action_portal():
    username = (request.forms.get("username") or "").strip()
    password = request.forms.get("password") or ""
    session_id = ctl.authenticate_user(username, password)

    if not session_id:
        response.status = 401
        return ctl.portal("Usuário ou senha inválidos.")

    response.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600
    )
    redirect("/banco")


@app.post("/logout")
def logout():
    ctl.logout_user()
    response.delete_cookie("session_id")
    redirect("/portal")


@app.get("/banco")
def banco():
    user = ctl.current_user()
    if not user:
        redirect("/portal")
    return ctl.banco(user)


@app.post("/pessoas")
def create_pessoa_from_form():
    if not ctl.current_user():
        redirect("/portal")
    nome = (request.forms.get("nome") or "").strip()
    idade = request.forms.get("idade") or ""
    try:
        ctl.create_pessoa(nome, idade)
    except ValueError as error:
        response.status = 400
        return str(error)
    redirect("/banco")


@app.post("/pessoas/<pessoa_id:int>/delete")
def delete_pessoa_from_form(pessoa_id):
    if not ctl.current_user():
        redirect("/portal")
    ctl.delete_pessoa(pessoa_id)
    redirect("/banco")


# API: todas as rotas abaixo exigem uma sessão autenticada.
@app.get("/api/pessoas")
def api_list_pessoas():
    if not ctl.current_user():
        response.status = 401
        return {"erro": "Autenticação necessária."}
    return {"pessoas": ctl.list_pessoas()}


@app.post("/api/pessoas")
def api_create_pessoa():
    if not ctl.current_user():
        response.status = 401
        return {"erro": "Autenticação necessária."}

    data = request.json or {}
    try:
        pessoa = ctl.create_pessoa(data.get("nome"), data.get("idade"))
    except (ValueError, TypeError) as error:
        response.status = 400
        return {"erro": str(error)}
    response.status = 201
    return {"mensagem": "Pessoa cadastrada.", "pessoa": pessoa}


@app.put("/api/pessoas/<pessoa_id:int>")
def api_update_pessoa(pessoa_id):
    if not ctl.current_user():
        response.status = 401
        return {"erro": "Autenticação necessária."}

    data = request.json or {}
    try:
        pessoa = ctl.update_pessoa(
            pessoa_id,
            data.get("nome"),
            data.get("idade")
        )
    except (ValueError, TypeError) as error:
        response.status = 400
        return {"erro": str(error)}

    if not pessoa:
        response.status = 404
        return {"erro": "Pessoa não encontrada."}
    return {"mensagem": "Pessoa atualizada.", "pessoa": pessoa}


@app.delete("/api/pessoas/<pessoa_id:int>")
def api_delete_pessoa(pessoa_id):
    if not ctl.current_user():
        response.status = 401
        return {"erro": "Autenticação necessária."}

    if not ctl.delete_pessoa(pessoa_id):
        response.status = 404
        return {"erro": "Pessoa não encontrada."}
    return {"mensagem": "Pessoa removida."}


if __name__ == "__main__":
    run(app, host="127.0.0.1", port=8080, debug=True, reloader=True)
