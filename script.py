import os
import pandas as pd
import requests
import json
import re

BASE_URL = ""
API_URL = f"{BASE_URL}"

def format_whatsapp(number):
    if pd.isna(number):
        return None

    number = str(number)
    number = re.sub(r"[^\d]", "", number)

    if number.startswith("55"):
        number = number[2:]

    if len(number) == 11:
        return f"+55{number}"
    
    return None

def is_valid_name(name):
    return isinstance(name, str) and len(name.strip().split()) >= 2

def process_excel_file(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    if "-" not in filename:
        print(f"❌ Nome do arquivo inválido (esperado: eventCode-subscriptionTypeId): {filename}")
        return

    eventCode, subscriptionTypeId = filename.split("-", 1)
    df = pd.read_excel(filepath, usecols="A:C", header=None, skiprows=1)
    df.columns = ['name', 'whatsApp', 'email']

    invalid_rows = []

    for _, row in df.iterrows():
        name = str(row['name']).strip()
        whatsApp = format_whatsapp(row['whatsApp'])
        email = row['email']

        if not is_valid_name(name) or not whatsApp:
            print(f"⚠️ Dados inválidos ignorados - Nome: '{name}', WhatsApp: '{row['whatsApp']}, Email: '{email}'")
            invalid_rows.append(row)
            continue

        data = {
            "paymentTypeId": 0,
            "installments": 1,
            "payerName": name,
            "eventCode": eventCode,
            "registrations": [
                {
                    "name": name,
                    "email": email,
                    "whatsApp": whatsApp,
                    "subscriptionTypeId": subscriptionTypeId,
                    "fieldResponses": [],
                    "selectedVariants": [],
                    "customDonationValue": 0
                }
            ]
        }

        try:
            print(f"\n📤 Enviando JSON para {name}:\n{json.dumps(data, indent=2, ensure_ascii=False)}\n")
            response = requests.post(API_URL, json=data)

            try:
                response_data = response.json()
            except ValueError:
                response_data = response.text or "[Resposta vazia ou não JSON]"

            print(f"✅ Resposta da API ({name}): {response.status_code} - {response_data}")
        except Exception as e:
            print(f"❌ Erro ao enviar dados para {name}: {e}")

    if invalid_rows:
        invalid_df = pd.DataFrame(invalid_rows)
        output_file = f"{eventCode}-invalidos.xlsx"
        invalid_df.to_excel(output_file, index=False)
        print(f"\n📄 Planilha de inválidos gerada: {output_file}")

def main():
    for file in os.listdir("."):
        if file.endswith(".xlsx") and "-" in file:
            print(f"\n📄 Processando {file}...")
            process_excel_file(file)

if __name__ == "__main__":
    main()