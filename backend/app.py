from flask import Flask, jsonify
from flask_cors import CORS
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://contagem-sj.vercel.app"}})

def ler_dados_google_sheet():
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds_path = '/home/GabrielBelo/credentials.json' 
            # Arquivo presente no diretório do PythonAnywhere com as credenciais do Google Service Account

            if not os.path.exists(creds_path):
                print(f"ATENÇÃO: Arquivo de credenciais NÃO encontrado em: {creds_path}")
                return None

            creds = Credentials.from_service_account_file(creds_path, scopes=scope)
            client = gspread.authorize(creds)

            sheet_name = "radar_gravata_interno"
            sheet = client.open(sheet_name).sheet1

            data = sheet.get_all_records()
            if not data:
                print("A planilha parece estar vazia.")
                return pd.DataFrame()

            df = pd.DataFrame(data)

            required_cols = ["timestamp", "total_detected", "zone"]
            if not all(col in df.columns for col in required_cols):
                print(f"ERRO: Colunas necessárias ({required_cols}) não encontradas.")
                print(f"Colunas encontradas: {df.columns.tolist()}")
                return pd.DataFrame()

            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            df['total_detected'] = pd.to_numeric(df['total_detected'], errors='coerce').fillna(0)
            df.dropna(subset=['timestamp'], inplace=True)

            return df

        except Exception as e:
            print(f"Erro inesperado ao ler dados do Google Sheet: {e}")
            return None

@app.route('/api/impact-data')
def get_impact_data():
        df = ler_dados_google_sheet()
        if df is None or df.empty:
            return jsonify({
                "impactedToday": 0,
                "impactedTotal": 0,
                "peakHour": "N/D",
                "topZoneByPeople": "N/D",
                "error": "Dados não disponíveis ou planilha em formato incorreto"
            }), 500

        hoje = datetime.now().date()
        df_hoje = df[df['timestamp'].dt.date == hoje]

        if not df_hoje.empty:
            impactadas_hoje = int(df_hoje['total_detected'].iloc[-1])
        else:
            impactadas_hoje = "Evento Pausado"
            
        impactadas_total = int(df['total_detected'].iloc[-1])  
    
        pico_por_hora = df.groupby(df['timestamp'].dt.hour)['total_detected'].sum()
        if not pico_por_hora.empty:
            hora_de_pico_num = pico_por_hora.idxmax()
            horario_pico_str = f"{int(hora_de_pico_num):02d}:00"
        else:
            horario_pico_str = "N/D"

        df_zonas = df.dropna(subset=['zone']) # Remove nulos
        df_zonas = df_zonas[df_zonas['zone'].astype(str).str.strip() != '']
        if not df_zonas.empty:
            pessoas_por_zona = df_zonas.groupby('zone')['total_detected'].sum()
            if not pessoas_por_zona.empty:
                zona_com_mais_pessoas = pessoas_por_zona.idxmax()
            else:
                zona_com_mais_pessoas = "Nenhuma"
        else:
            zona_com_mais_pessoas = "Nenhuma"


        return jsonify({
            "impactedToday": impactadas_hoje,
            "impactedTotal": impactadas_total,
            "peakHour": horario_pico_str,
            "topZoneByPeople": zona_com_mais_pessoas
        })

if __name__ == '__main__':
    app.run(debug=True)