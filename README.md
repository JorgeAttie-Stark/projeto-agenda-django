# 📇 Agenda — Django

> Projeto de estudo para aprender **Django do zero**, construindo uma agenda de
> contatos passo a passo.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat-square&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-dev-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20andamento-yellow?style=flat-square)

---

## 📖 Sobre este repositório

Este é o meu **primeiro projeto em Django**, feito acompanhando um curso. O
objetivo aqui não é entregar um produto — é **entender o framework**.

Venho de front-end (TypeScript, React, Angular), então a curva não é "como
programar", e sim: como o Django organiza um back-end, o que ele resolve sozinho
e onde ficam as costuras entre as peças. Por isso o repositório é mais anotado do
que um projeto de trabalho normalmente seria — cada decisão vem com o *porquê*.

**O que estou construindo:** um CRUD de contatos com busca, painel administrativo
e autenticação — os blocos que aparecem em praticamente todo sistema Django.

---

## 🧰 Stack

| Camada | Escolha | Por quê |
|---|---|---|
| Linguagem | Python 3.13.13 | Versão do Homebrew, isolada no `venv/` |
| Framework | Django 6.1 | O objeto do estudo |
| Banco | SQLite | Zero configuração; um arquivo. Trocável por PostgreSQL depois sem mexer no código de aplicação |
| Templates | Django Templates | O motor nativo, sem front-end separado — o foco é back-end |
| Ambiente | `venv` no projeto | Dependências isoladas; nada instalado global |

---

## 🗂️ Estrutura

```
projeto-agenda-django-23/
├── manage.py               # ponto de entrada de todo comando do Django
├── db.sqlite3              # banco local (fora do Git — recriável com migrate)
├── project/                # pacote de configuração do site
│   ├── settings.py         #   painel de controle: apps, banco, middleware
│   ├── urls.py             #   mapa de rotas (ROOT_URLCONF)
│   ├── wsgi.py             #   entrada do servidor síncrono (usada pelo runserver)
│   └── asgi.py             #   entrada do servidor assíncrono
├── docs/
│   └── ARQUITETURA.md      # 📌 guia arquivo por arquivo — comece por aqui
├── comandos/
│   └── README.md           # caderno de comandos do curso
├── .vscode/settings.json   # aponta o interpretador para venv/bin/python
└── venv/                   # ambiente virtual (fora do Git)
```

---

## 🚀 Rodando localmente

Quem clonar o repositório não recebe o `venv/` nem o `db.sqlite3` — os dois são
recriáveis, e é justamente por isso que ficam fora do Git.

```bash
git clone <url> && cd projeto-agenda-django-23

python3 -m venv venv
source venv/bin/activate         # sem isto, o Django não é encontrado
pip install django

python manage.py migrate         # cria o db.sqlite3 e as tabelas
python manage.py createsuperuser # seu login do admin
python manage.py runserver
```

| Endereço | O que é |
|---|---|
| http://127.0.0.1:8000/ | A aplicação |
| http://127.0.0.1:8000/admin/ | Painel administrativo |

`Ctrl+C` encerra. `deactivate` sai do ambiente virtual.

> 💡 **`source venv/bin/activate` é sempre o primeiro comando da sessão.** Sem ele,
> `python manage.py` falha com `ModuleNotFoundError: No module named 'django'` —
> o erro é proposital: o Django foi instalado só dentro do `venv`, nunca global.

---

## 📚 Documentação do estudo

| Documento | Conteúdo |
|---|---|
| [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md) | **O material principal.** Cada arquivo e sua responsabilidade, o `settings.py` linha a linha, o caminho completo de uma requisição e a tabela de quais nomes o Django exige vs. quais são escolha minha |
| [`comandos/README.md`](comandos/README.md) | Comandos de venv, Django e Git usados no curso |

---

## 🗺️ Progresso

**Fundação**

- [x] Ambiente virtual e Django instalados
- [x] `startproject` — pacote `project/` e `manage.py`
- [x] `migrate` inicial (auth, sessions, admin, contenttypes)
- [x] Git com `.gitignore` de Django
- [x] Documentação da arquitetura

**Aplicação**

- [ ] `startapp` e registro em `INSTALLED_APPS`
- [ ] Model `Contato` + `makemigrations` / `migrate`
- [ ] Registro no admin (CRUD sem escrever formulário)
- [ ] Views, rotas e templates
- [ ] Busca e paginação
- [ ] Upload de foto do contato
- [ ] Formulários e validação
- [ ] Login, logout e cadastro de usuário

**Produção**

- [ ] `settings.py` separado por ambiente
- [ ] `SECRET_KEY` e `DEBUG` via variável de ambiente
- [ ] PostgreSQL no lugar do SQLite
- [ ] Deploy

---

## 📝 Notas de versão

Estou no **Django 6.1**, mais novo que o do curso (5.x). As divergências que já
mapeei — todas cosméticas, nenhuma muda o que é ensinado:

| Ponto | Curso (5.x) | Aqui (6.1) |
|---|---|---|
| E-mail | `EMAIL_BACKEND` como variável solta | dicionário `MAILERS` |
| `DEFAULT_AUTO_FIELD` | presente no `settings.py` | ausente — `BigAutoField` já é o padrão implícito |
| `context_processors` | inclui `...context_processors.debug` | não inclui |

Detalhes em [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md), seção 11.

---

<sub>Projeto de estudo. Não é código de produção — o `SECRET_KEY` versionado e o
`DEBUG = True` são intencionais enquanto o objetivo for aprender.</sub>
