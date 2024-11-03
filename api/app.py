from flask import Flask, render_template, request, redirect, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta')  # Use variável de ambiente para a chave secreta

# Caminho do arquivo CSV com os dados
csv_path = os.path.join('C:\\Users\\Brazn\\Desktop\\Localizações\\api', 'endereços.csv')

# Tenta carregar o CSV com dados de instalação, medidor e coordenadas
try:
    df = pd.read_csv(csv_path)
    df['instalação'] = df['instalação'].astype(str).str.strip().str.lower()  # Limpeza ao carregar
    df['medidor'] = df['medidor'].astype(str).str.strip().str.lower()
except FileNotFoundError:
    print("Erro: O arquivo endereços.csv não foi encontrado.")
    df = pd.DataFrame()  # Cria um DataFrame vazio caso o arquivo não seja encontrado

@app.route("/")
def index():
    return render_template("index.html", mapa_url=None)

@app.route("/buscar", methods=["POST"])
def buscar():
    entrada = request.form.get("entrada", "").strip().lower()
    if not entrada:
        flash("Por favor, insira uma instalação ou medidor.", "error")
        return redirect("/")

    if df.empty or 'instalação' not in df.columns or 'medidor' not in df.columns:
        flash("Erro ao acessar os dados.", "error")
        return redirect("/")

    # Busca no DataFrame
    resultado = df[
        df['instalação'].str.contains(entrada) |
        df['medidor'].str.contains(entrada)
    ]

    if not resultado.empty:
        latitude, longitude = resultado.iloc[0][['latitude', 'longitude']]
        mapa_url = f"https://www.google.com/maps?q={latitude},{longitude}"
        flash("Localização encontrada!", "success")
        return render_template("index.html", mapa_url=mapa_url)
    
    flash("Instalação ou Medidor não encontrados.", "error")
    return redirect("/")

# O Vercel gerencia o ambiente, então remova o debug=True
if __name__ == "__main__":
    app.run()
