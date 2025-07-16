# Gráfico RT - Monitoramento de Eventos em Tempo Real
### Este repositório contém o código para uma aplicação web que monitora e exibe dados de um evento em tempo real, utilizando uma planilha Google Sheets como fonte de dados. 
> A aplicação é dividida em um backend Python (Flask) e um frontend web (HTML, CSS, JavaScript).

---
## Visão Geral
A aplicação permite visualizar métricas importantes de um evento, como o número de pessoas impactadas (hoje e total), o horário de pico de impacto e a zona com maior concentração de pessoas. 
Os dados são atualizados em tempo real, fornecendo uma visão dinâmica do status do evento.

## Funcionalidades
- **Coleta de Dados em Tempo Real**: O backend em Python se conecta a uma planilha Google Sheets para buscar os dados mais recentes do evento, através do Google Service Account da API do Google Sheets.

- **Cálculo de Métricas**: Calcula automaticamente:

  - Pessoas impactadas hoje.
  - Total de pessoas impactadas.
  - Horário de pico de detecção de pessoas.
  - Zona com maior número de pessoas detectadas.

- **Visualização Dinâmica no Frontend**: O frontend exibe essas métricas de forma clara e legível, atualizando os valores em intervalos regulares.

- **API RESTful**: O backend expõe uma API para que o frontend possa consumir os dados de forma eficiente.

- **CORS Configurado**: O backend possui configuração CORS para permitir requisições do frontend hospedado em domínios específicos.

## Tecnologias Utilizadas

- Backend
  - **Python**: Linguagem de programação principal.
  - **Flask**: Microframework web para Python, utilizado para construir a API.
  - **Flask-CORS**: Extensão para Flask que permite a configuração de Cross-Origin Resource Sharing.
  - **gspread**: Biblioteca Python para interagir com a API do Google Sheets.
  - **google-auth**: Biblioteca para autenticação com serviços Google.
  - **pandas**: Biblioteca para manipulação e análise de dados.

- Frontend
  - **HTML**: Estrutura da página web.
  - **CSS**: Estilização da interface de usuário.
  - **JavaScript**: Lógica para buscar e exibir os dados do backend, e para atualizar a interface.

- Hospedagem
  - **PythonAnywhere**: Plataforma de hospedagem para a aplicação Flask do backend.
  - **Vercel**: Plataforma de hospedagem para o frontend estático.
  - **Google Sheets**: Usado como banco de dados para armazenar os dados do evento.

## Estrutura do Repositório

```
grafico_rt/
├── backend/
│   ├── app.py
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

- **backend/app.py**: Contém o código da aplicação Flask que lê os dados do Google Sheet e expõe a API.
- **frontend/index.html**: A estrutura HTML da página do dashboard.
- **frontend/script.js**: O código JavaScript que interage com o backend e atualiza a interface.
- #**frontend/style.css**: Os estilos CSS para a interface do usuário.
