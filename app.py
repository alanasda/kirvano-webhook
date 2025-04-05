from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import random
import os
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

# Configurações do e-mail
# Configurações do e-mail
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465  # Alterado de 587 para 465
EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE")
SENHA_APP = os.environ.get("SENHA_APP")

def criar_mensagem(email_destino: str, senha: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "✅ Seu Acesso à Área de Membros"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = email_destino

    corpo = f"""
    <h2 style="color: #2e6c80;">Olá, seja bem-vindo!</h2>
    <p>Seu acesso à área exclusiva foi liberado:</p>
    
    <div style="background: #f6f6f6; padding: 20px; border-radius: 10px;">
      <p>🔗 <strong>Plataforma:</strong> <a href="https://area.membros.com">https://area.membros.com</a></p>
      <p>📧 <strong>Login:</strong> {email_destino}</p>
      <p>🔒 <strong>Senha:</strong> {senha}</p>
    </div>

    <p style="margin-top: 30px;">Dúvidas? Responda este e-mail!</p>
    """
    
    msg.set_content(corpo, subtype="html")
    return msg
def enviar_email(email_destino: str, senha: str) -> bool:
    try:
        msg = criar_mensagem(email_destino, senha)
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:  # Usando SMTP_SSL
            server.login(EMAIL_REMETENTE, SENHA_APP)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"ERRO: {str(e)}")
        return False

@app.route("/checkout", methods=["POST"])
def webhook_kirvano():
    if not request.is_json:
        return jsonify({"erro": "Payload deve ser JSON"}), 400

    dados = request.get_json()
    email = dados.get("email")

    if not email:
        return jsonify({"erro": "Campo 'email' obrigatório"}), 400

    senha = str(random.randint(100000, 999999))  # Senha de 6 dígitos
    if enviar_email(email, senha):
        return jsonify({"mensagem": "Credenciais enviadas com sucesso!"}), 200
    else:
        return jsonify({"erro": "Falha no envio do e-mail"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
