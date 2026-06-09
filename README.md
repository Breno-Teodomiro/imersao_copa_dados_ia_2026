# ⚽ Bolão Copa do Mundo 2026

Aplicação web de bolão da Copa do Mundo FIFA 2026, construída em **Python + Streamlit** com persistência em **Supabase (PostgreSQL)**. O participante faz seus palpites desde a fase de grupos até a grande final, com visual premium e bandeiras reais de todas as 48 seleções.

> Projeto de portfólio — Imersão Jornada de Dados.

---

## ✨ Funcionalidades

- **Registro do participante** (nome, telefone, e-mail) com validação e bloqueio de e-mail duplicado
- **Fase de grupos** — 12 grupos (A–L) com a bandeira de cada seleção; o usuário escolhe o 1º e 2º colocado de cada grupo
- **Mata-mata completo** — palpites fase a fase, com o chaveamento sendo montado a partir das próprias escolhas:
  `16-avos → Oitavas → Quartas → Semifinal → Final`
- **8 melhores terceiros** sorteados automaticamente (simplificação do regulamento)
- **Ranking do bolão** — pódio das 3 seleções mais escolhidas como campeãs + planilha interativa com votos e % de todos os participantes
- **Visual premium** — tema dark, gradientes, bandeiras reais (flagcdn.com), animações e foco em **UX/UI e acessibilidade** (aria-labels, foco visível, contraste WCAG)

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Frontend / UI | [Streamlit](https://streamlit.io) |
| Banco de dados | [Supabase](https://supabase.com) (PostgreSQL) |
| Linguagem | Python 3.10+ |
| Bandeiras | [flagcdn.com](https://flagcdn.com) |

---

## 📁 Estrutura

```
.
├── app.py                  # Aplicação Streamlit (UI + fluxo das fases)
├── db.py                   # Integração com o Supabase
├── requirements.txt        # Dependências
├── .streamlit/
│   ├── config.toml         # Tema da aplicação
│   └── secrets.toml        # Credenciais (NÃO versionado)
└── picture/
    └── tela_de_captura.png # Referência de design
```

---

## 🗄️ Modelo de dados (Supabase)

- **`participants`** — `id`, `name`, `phone`, `email` (único), `created_at`
- **`picks`** — palpites da fase de grupos (1º e 2º por grupo)
- **`knockout_picks`** — palpites do mata-mata (`r32`, `r16`, `qf`, `sf`, `final`)

---

## 🚀 Como rodar localmente

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Configure as credenciais do Supabase
# Crie o arquivo .streamlit/secrets.toml com:
#   SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
#   SUPABASE_KEY = "sua-publishable-key"

# 3. Rode o app
streamlit run app.py
```

A aplicação abre em `http://localhost:8501`.

---

## ☁️ Deploy (Streamlit Community Cloud)

1. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com o GitHub
2. **Create app** → selecione este repositório, branch `main`, arquivo `app.py`
3. Em **Advanced settings → Secrets**, cole o conteúdo do `secrets.toml`
4. **Deploy** 🎉

---

## 📝 Licença

Projeto de portfólio para fins educacionais.
