# Arquitetura do projeto — guia arquivo por arquivo

Documento de estudo do `projeto-agenda-django-23`. Descreve o que o
`django-admin startproject project .` gerou, o que cada arquivo faz e, principalmente,
**quais nomes o Django exige e quais são escolha sua** — que é a confusão mais comum
no primeiro projeto.

Versão instalada aqui: **Django 6.1** rodando em **Python 3.13.13** dentro de `venv/`.

---

## 1. A árvore

```
projeto-agenda-django-23/          ← raiz do repositório (nome arbitrário)
├── manage.py                      ← Django
├── db.sqlite3                     ← Django (gerado pelo migrate, fora do Git)
├── project/                       ← Django: o "pacote de configuração"
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── venv/                          ← Python, não Django (fora do Git)
├── .gitignore                     ← Git
├── .vscode/settings.json          ← VS Code, não Django
└── comandos/README.md             ← seu caderno de anotações do curso
```

Só as duas primeiras seções (`manage.py` + `project/`) são Django. O resto é
ferramental ao redor.

---

## 2. Conceito antes dos arquivos: *project* vs *app*

Essa distinção organiza tudo o que vem depois.

| | **Project** (o que você tem hoje) | **App** (o que vem no próximo passo) |
|---|---|---|
| O que é | O pacote de **configuração** do site inteiro | Um módulo de **funcionalidade** |
| Quantos | Um por repositório | Vários por project |
| Criado por | `django-admin startproject project .` | `python manage.py startapp agenda` |
| Contém | `settings.py`, `urls.py`, `wsgi.py`, `asgi.py` | `models.py`, `views.py`, `admin.py`, `migrations/` |
| Analogia | A tomada e o quadro de luz da casa | Cada eletrodoméstico que você pluga |

Um app só passa a existir para o Django quando o nome dele entra em
`INSTALLED_APPS` no `settings.py`. Criar a pasta com `startapp` **não** basta —
é um passo manual, e esquecê-lo é o erro nº 1 de quem começa.

O Django chama seu padrão de **MTV** — Model, Template, View. É o MVC com outros
nomes: o *Template* do Django é a "view" do MVC (o HTML), e a *View* do Django é
o "controller" (a função Python que responde à requisição). Quando o professor
disser "view", ele quer dizer **código Python**, não tela.

---

## 3. `manage.py` — a porta de entrada da linha de comando

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
...
execute_from_command_line(sys.argv)
```

É o script que você chama em **todo** comando do dia a dia (`runserver`, `migrate`,
`startapp`, `createsuperuser`). O corpo dele faz só três coisas:

1. **Aponta o Django para o seu `settings.py`.** A variável de ambiente
   `DJANGO_SETTINGS_MODULE` recebe a string `'project.settings'` — que é um
   **caminho de import Python**, não um caminho de arquivo: significa "o módulo
   `settings` dentro do pacote `project`". Se você renomear a pasta `project/`,
   é essa string que quebra (em 4 arquivos: `manage.py`, `settings.py`,
   `wsgi.py`, `asgi.py`).
2. **`setdefault`, não `=`.** Ele só define se a variável ainda não existir. É o
   que permite, em produção, exportar `DJANGO_SETTINGS_MODULE=project.settings_prod`
   no ambiente e reaproveitar o mesmo `manage.py` sem editar nada.
3. **Delega tudo para o Django.** `execute_from_command_line(sys.argv)` lê os
   argumentos e procura o comando correspondente. Os comandos não moram aqui —
   vêm do Django e dos apps em `INSTALLED_APPS`.

O `try/except ImportError` existe por um motivo bem específico, e é exatamente a
situação que combinamos de deixar barulhenta: se você rodar `manage.py` **sem
ativar o venv**, o Django não é encontrado e a mensagem sugere justamente
*"Did you forget to activate a virtual environment?"*.

> **O nome `manage.py` é convenção, não regra.** Nada dentro do Django procura um
> arquivo com esse nome — você o executa explicitamente. Renomear funciona, mas
> não faça: todo tutorial e toda resposta de Stack Overflow assume `manage.py`.

---

## 4. `project/__init__.py` — o arquivo vazio que não é inútil

Tem **zero bytes** e é obrigatório na prática. É ele que marca a pasta `project/`
como um **pacote Python**, tornando `project.settings` e `project.urls` importáveis.

Isso é mecanismo nativo do Python, não do Django. (Rigor: desde o Python 3.3
existem *namespace packages*, que dispensam o `__init__.py` em certos casos — mas
o Django gera o arquivo e ele deve ficar. Apagar dá dor de cabeça por motivo
não-óbvio.)

Mais adiante no curso ele volta a aparecer: é aqui que se registra o Celery,
quando o projeto ganha tarefas assíncronas.

---

## 5. `project/settings.py` — o painel de controle

É um **módulo Python comum**, não um `.ini` nem um `.yaml`. Isso significa que
você pode usar `if`, `os.environ`, imports — é código de verdade, executado uma
vez na inicialização.

**Regra mecânica que quase ninguém explica:** o Django lê esse módulo e importa
**apenas os nomes em MAIÚSCULAS**. Uma variável `debug = True` em minúsculo é
silenciosamente ignorada pelo sistema de settings. Por isso toda configuração é
`SCREAMING_CASE` — não é estilo, é o filtro que o Django aplica.

### Linha a linha

**`BASE_DIR = Path(__file__).resolve().parent.parent`** (linha 16)

Resolve para a pasta que contém o `manage.py`. Desmontando:
`__file__` é `project/settings.py` → `.resolve()` transforma em caminho absoluto →
`.parent` sobe para `project/` → `.parent` de novo sobe para a raiz. É um `Path`
do `pathlib`, então você compõe caminhos com `/`: `BASE_DIR / 'templates'`.

**`SECRET_KEY`** (linha 23)

Chave usada em assinatura criptográfica: cookies de sessão, tokens CSRF, links de
recuperação de senha. O prefixo `django-insecure-` é um marcador deliberado,
posto pelo `startproject`, sinalizando "isto foi gerado para desenvolvimento".
Em produção sai do código e vai para variável de ambiente. **Nunca commite a de
produção.**

**`DEBUG = True`** (linha 26)

Liga duas coisas: a página de erro amarela com traceback completo, e o
serviço de arquivos estáticos pelo servidor de desenvolvimento. Em produção
**precisa** ser `False` — a página de erro expõe trechos do seu settings, incluindo
nomes de variáveis e caminhos.

**`ALLOWED_HOSTS = []`** (linha 28)

Lista de hosts que o Django aceita responder, defesa contra HTTP Host header
poisoning. Parece que a lista vazia bloquearia tudo, mas há uma exceção embutida:
**com `DEBUG = True`, uma lista vazia é tratada como
`['.localhost', '127.0.0.1', '[::1]']`** (o ponto inicial faz casar também os
subdomínios). É por isso que funciona hoje e quebra no
primeiro deploy com `DEBUG = False` — o famoso erro *"Invalid HTTP_HOST header"*.

**`INSTALLED_APPS`** (linhas 33–40)

Lista de caminhos de import dos apps ativos. Estar nessa lista é o que faz o
Django procurar, dentro daquele app: models (e portanto migrations), templates,
arquivos estáticos, comandos de `manage.py` e registros no admin.

Os seis que vieram são apps nativos:

| App | Responsabilidade | Criou tabela no `migrate`? |
|---|---|---|
| `django.contrib.admin` | O painel `/admin/` | sim |
| `django.contrib.auth` | Usuários, grupos, permissões, login | sim |
| `django.contrib.contenttypes` | Registro genérico de "que modelo é este" — base das permissões | sim |
| `django.contrib.sessions` | Sessão do usuário entre requisições | sim |
| `django.contrib.messages` | Mensagens de "salvo com sucesso" entre páginas | não (usa sessão) |
| `django.contrib.staticfiles` | Coleta e serve CSS/JS/imagens | não |

Aquelas ~18 linhas de `Applying ...` que rolaram no `migrate` vieram daqui.

**`MIDDLEWARE`** (linhas 42–50)

Camadas que envolvem **toda** requisição. A ordem importa e não é decorativa: a
requisição desce a lista de cima para baixo, e a resposta sobe de baixo para cima.

Dependência concreta: `SessionMiddleware` está **antes** de
`AuthenticationMiddleware` porque o segundo monta o `request.user` a partir do
ID guardado na sessão. Inverter os dois quebra a autenticação.

**`ROOT_URLCONF = 'project.urls'`** (linha 52)

Diz qual módulo é o ponto de entrada do roteamento. É o elo entre o `settings.py`
e o `urls.py`.

**`TEMPLATES`** (linhas 54–67)

Dois campos importam agora:
- `'DIRS': []` — nenhuma pasta de templates **no nível do project**. Quando você
  criar `templates/` na raiz, é aqui que registra: `'DIRS': [BASE_DIR / 'templates']`.
- `'APP_DIRS': True` — o Django procura automaticamente em `<cada_app>/templates/`.

Os `context_processors` injetam variáveis em todo template sem você passar nada:
é graças a eles que `{{ request }}` e `{{ user }}` existem em qualquer página.

**`WSGI_APPLICATION = 'project.wsgi.application'`** (linha 69)

Aponta para o objeto `application` dentro de `project/wsgi.py`. Detalhe que quase
todo tutorial erra: **o `runserver` usa isto**. O servidor de desenvolvimento
carrega o callable indicado aqui — o `wsgi.py` não é "só coisa de produção".

**`DATABASES`** (linhas 75–80)

SQLite, um único arquivo em `BASE_DIR / 'db.sqlite3'`. Zero configuração, perfeito
para aprender. Trocar para PostgreSQL depois é mudar `ENGINE`, `NAME`, `USER`,
`PASSWORD`, `HOST` — o resto do seu código não muda, que é o ponto do ORM.

**`AUTH_PASSWORD_VALIDATORS`** (linhas 86–99)

Rodam na **definição** de senha (no `createsuperuser`, em formulários de cadastro),
não no login. Por isso o `createsuperuser` reclama de senha curta.

**`LANGUAGE_CODE` / `TIME_ZONE` / `USE_I18N` / `USE_TZ`** (linhas 105–111)

Provavelmente as duas primeiras coisas que o curso vai mandar trocar:

```python
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
```

`LANGUAGE_CODE` traduz as strings do próprio Django (admin, mensagens de erro de
formulário) — não traduz o **seu** texto. Com `USE_TZ = True`, o banco guarda
tudo em UTC e a conversão para `TIME_ZONE` acontece na exibição; é o
comportamento correto, deixe ligado.

**`STATIC_URL = 'static/'`** (linha 117)

**Prefixo de URL**, não pasta no disco. Define que os estáticos são servidos sob
`/static/...`. A pasta física é assunto de `STATICFILES_DIRS` e `STATIC_ROOT`,
que aparecem mais para a frente.

**`MAILERS`** (linhas 123–127)

Configuração de e-mail. O backend `console` imprime a mensagem no terminal em vez
de enviar — ótimo para testar "recuperar senha" sem servidor SMTP.

> ⚠️ **Diferença de versão.** `MAILERS` é a forma do **Django 6.x**. O curso, se
> for gravado em 5.x, vai mostrar `EMAIL_BACKEND = '...'` como variável solta.
> Ver a seção 10.

---

## 6. `project/urls.py` — o mapa de rotas

```python
urlpatterns = [
    path('admin/', admin.site.urls),
]
```

**O nome `urlpatterns` é obrigatório.** O Django importa o módulo apontado por
`ROOT_URLCONF` e procura literalmente por uma variável com esse nome. Renomear
para `rotas` quebra o site inteiro.

Como o casamento acontece:

1. Chega `GET /admin/login/`.
2. O Django remove a barra inicial → sobra `admin/login/`.
3. Percorre `urlpatterns` **na ordem**, de cima para baixo.
4. **A primeira que casar vence** — as seguintes nem são testadas. Por isso rota
   genérica sempre vai por último.
5. Nenhuma casou → HTTP 404.

`admin.site.urls` não é uma view: é um conjunto inteiro de rotas que o app admin
oferece, plugado sob o prefixo `admin/`.

Quando você criar o app da agenda, este arquivo vira um **distribuidor** e delega:

```python
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('agenda.urls')),   # cada app cuida das suas rotas
]
```

---

## 7. `project/wsgi.py` e `project/asgi.py` — as portas do servidor

Os dois são quase idênticos: definem `DJANGO_SETTINGS_MODULE` e expõem um objeto
de módulo chamado `application`.

| | `wsgi.py` | `asgi.py` |
|---|---|---|
| Protocolo | WSGI — síncrono, uma requisição por vez | ASGI — assíncrono |
| Serve | HTTP tradicional | HTTP + WebSocket, long polling |
| Servidores | Gunicorn, uWSGI | Uvicorn, Daphne |
| Usado hoje? | **Sim, o `runserver` o utiliza** | Não, só se você trocar de servidor |

Você provavelmente **nunca vai editar esses dois arquivos**. Eles existem para o
servidor de produção ter um ponto de entrada padronizado: você aponta o Gunicorn
para `project.wsgi:application` e acabou.

---

## 8. Os arquivos que não são Django

| Arquivo | De quem é | Papel |
|---|---|---|
| `db.sqlite3` | gerado pelo `migrate` | O banco inteiro em um arquivo. Fora do Git — cada dev tem o seu, e ele é recriável com `migrate` |
| `venv/` | Python | Interpretador + Django isolados neste projeto. Fora do Git — quem clona recria com `python3 -m venv venv` |
| `.gitignore` | Git | Mantém banco, `venv/` e `__pycache__/` fora do repositório |
| `.vscode/settings.json` | VS Code | Aponta o interpretador para `venv/bin/python`. Vai pro Git de propósito, pra equipe herdar a config |
| `comandos/README.md` | você | Caderno de comandos do curso |
| `project/__pycache__/` | Python | Bytecode em cache, regenerado sozinho. Ignorado |

---

## 9. O caminho completo de uma requisição

Como as peças se conectam, do comando ao HTML — sem nenhum passo escondido:

```
$ python manage.py runserver
        │
        │ 1. manage.py define DJANGO_SETTINGS_MODULE = 'project.settings'
        ▼
   settings.py  ── é lido inteiro; só nomes MAIÚSCULOS entram
        │
        │ 2. lê WSGI_APPLICATION = 'project.wsgi.application'
        ▼
   wsgi.py  ── expõe o callable `application`; servidor sobe na :8000
        │
        ▼
╔═══ chega  GET /agenda/contato/5/  ═══════════════════════════════╗
        │
        │ 3. atravessa o MIDDLEWARE de cima para baixo
        │    (segurança → sessão → CSRF → autenticação → ...)
        ▼
        │ 4. settings.ROOT_URLCONF aponta para project/urls.py
        ▼
   urls.py  ── varre urlpatterns em ordem; a 1ª que casar vence
        │      (aqui: include() delega para agenda/urls.py)
        ▼
   views.py  ── SUA função Python: recebe request, devolve response
        │
        ├──▶ models.py    consulta o banco pelo ORM  ──▶ db.sqlite3
        │
        └──▶ template .html   renderiza o HTML com os dados
        │
        │ 5. a resposta sobe o MIDDLEWARE de baixo para cima
        ▼
╚═══ HTTP 200 + HTML para o navegador ═════════════════════════════╝
```

As três últimas caixas — `views.py`, `models.py`, template — **ainda não existem**
no seu projeto. Elas nascem com o primeiro app.

---

## 10. Nomes que você escolhe vs. nomes que o Django exige

A tabela mais útil deste documento. Trocar algo da coluna da direita quebra o
projeto de um jeito difícil de diagnosticar.

| Nome | Fixo ou livre? | Detalhe |
|---|---|---|
| `projeto-agenda-django-23/` | **Livre** | Só o nome da pasta do repositório |
| `project/` | **Livre** — você escolheu no `startproject` | Se mudar, ajuste a string `'project.…'` em 4 arquivos |
| `manage.py` | **Convenção** | Nada procura por esse nome, mas todo tutorial assume |
| `settings.py` | **Livre**, mas amarrado | Precisa bater com `DJANGO_SETTINGS_MODULE` |
| `urls.py` | **Livre**, mas amarrado | Precisa bater com `ROOT_URLCONF` |
| `wsgi.py` / `asgi.py` | **Livre**, mas amarrado | Precisa bater com `WSGI_APPLICATION` |
| `__init__.py` | **FIXO** | Regra do Python; sem ele não é pacote |
| `urlpatterns` | **FIXO** | O Django procura essa variável por nome |
| `application` (wsgi/asgi) | **Convenção forte** | O servidor aponta para `modulo:nome` |
| Settings em MAIÚSCULO | **FIXO** | Minúsculas são ignoradas pelo Django |
| `models.py`, `views.py`, `admin.py` | **Convenção** | Django encontra por import explícito; `admin.py` e `apps.py` são autocarregados por nome |
| `migrations/` | **FIXO** | O Django procura essa pasta dentro de cada app |

---

## 11. Diferenças da sua versão para a do curso

Você está no **Django 6.1**; o curso provavelmente é 5.x. O que vai divergir na
tela:

| Ponto | Curso (5.x) | Você (6.1) |
|---|---|---|
| E-mail no settings | `EMAIL_BACKEND = '...'` solto | dicionário `MAILERS` |
| `DEFAULT_AUTO_FIELD` | presente no settings | **ausente** — o padrão `BigAutoField` já é implícito |
| `context_processors` | inclui `...context_processors.debug` | não inclui |

Nenhuma dessas quebra o que ele ensina. Se ele mostrar uma linha que você não
tem, provavelmente é uma destas três.

---

## 12. Onde você está e o que vem a seguir

Hoje o projeto é um esqueleto funcional: sobe, tem banco migrado e tem admin.
O que **ainda não existe** é qualquer coisa sua.

```bash
source venv/bin/activate            # sempre o primeiro comando
python manage.py runserver          # http://127.0.0.1:8000/

python manage.py createsuperuser    # cria seu login
                                    # http://127.0.0.1:8000/admin/
```

A sequência natural daqui:

1. **`python manage.py startapp agenda`** — cria a pasta do app com
   `models.py`, `views.py`, `admin.py`, `apps.py`, `migrations/`, `tests.py`.
2. **Registrar `'agenda'` em `INSTALLED_APPS`** — o passo manual que todo mundo
   esquece.
3. **Escrever um model** (`class Contato(models.Model): ...`) — é a definição das
   colunas da tabela em Python.
4. **`makemigrations` → `migrate`** — o primeiro traduz o model em um arquivo de
   migration versionado; o segundo aplica no banco. São dois passos separados de
   propósito: a migration vai para o Git, o banco não.
5. **View + rota + template** — a função Python, a entrada em `urlpatterns` e o
   HTML.
6. **Registrar o model no `admin.py`** — e ganhar um CRUD completo de graça.
