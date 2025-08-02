# 📥 Sheet2Api Importador de Planilhas Excel para API

Este script automatiza o processo de leitura de arquivos `.xlsx`, extraindo informações de participantes (nome, WhatsApp, e-mail) e enviando os dados para uma API com base em um formato padronizado. Ideal para **eventos com inscrições em massa** via planilhas.

---

## ✅ O que este script faz

- Lê arquivos `.xlsx` com colunas: Nome, WhatsApp e E-mail.
- Formata os números de WhatsApp para o padrão internacional `+55xxxxxxxxxxx`.
- Valida nomes (apenas se tiverem nome + sobrenome).
- Constrói uma estrutura JSON para envio à API.
- Faz o POST para a API definida no `API_URL`.
- Gera uma nova planilha com os registros inválidos.

---

## 🗂️ Estrutura esperada dos arquivos

- O **nome do arquivo Excel deve seguir o padrão**:
```

eventCode-subscriptionTypeId.xlsx

```
Exemplo:
```

evento123-4.xlsx

````

- A **planilha deve ter as colunas** nas posições corretas:

| A (nome) | B (whatsApp) | C (email) |
|----------|--------------|-----------|
| João Silva | (11) 91234-5678 | joao@email.com |

---

## ⚙️ Requisitos

- Python 3.8+
- Pandas
- OpenPyXL
- Requests

### Instalação das dependências

```bash
pip install pandas openpyxl requests
````

---

## 🚀 Como usar

1. Coloque seus arquivos `.xlsx` na mesma pasta do script.
2. Edite o valor da variável `BASE_URL` no topo do script, apontando para a sua API.
3. Execute o script:

```bash
python importador_excel.py
```

4. O script irá:

   * Processar todos os arquivos `.xlsx` que seguem o padrão esperado.
   * Enviar os dados válidos para a API.
   * Informar registros inválidos no console.
   * Gerar um arquivo `eventCode-invalidos.xlsx` com os dados rejeitados.

---

## 🧠 Regras de validação aplicadas

* **Nome**: Deve conter pelo menos nome e sobrenome.
* **WhatsApp**: Deve ter 11 dígitos (DDD + número), no formato brasileiro, e será transformado em `+55...`.

---

## 🛠️ Exemplo de JSON enviado para a API

```json
{
  "paymentTypeId": 0,
  "installments": 1,
  "payerName": "João Silva",
  "eventCode": "evento123",
  "registrations": [
    {
      "name": "João Silva",
      "email": "joao@email.com",
      "whatsApp": "+5511912345678",
      "subscriptionTypeId": "4",
      "fieldResponses": [],
      "selectedVariants": [],
      "customDonationValue": 0
    }
  ]
}
```

---

## 📄 Saída de erros

Caso alguma linha tenha dados inválidos (nome incompleto ou WhatsApp inválido), ela será ignorada e registrada em uma nova planilha chamada:

```
<eventCode>-invalidos.xlsx
```

---

## 👤 Autor

Desenvolvido por [Eduardo Caversan](mailto:educaversan.dev@gmail.com)
GitHub: [@EduardoCaversan](https://github.com/EduardoCaversan)

---

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!
Sinta-se à vontade para abrir uma issue ou enviar um pull request.