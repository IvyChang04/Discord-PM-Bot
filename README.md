# Discord Project Management Bot

A Discord bot that helps manage tasks and projects directly inside your server.

Built with discord.py (slash commands + views), SQLAlchemy, and Supabase (Postgres).

## Features

-   Slash commands for managing tasks
    -   `/task_add` -- create a new task (with task title, description and )
    -   `/task_list` -- list existing tasks
    -   `/task_update` -- update task details or status
    -   `/task_delete` -- delete existing tasks according to task id
    -   `/task_assign` -- assign a task to a user
-   Interactive buttons to change task status (`Todo`, `In Progress`, `Done`)
-   Database-backed with Supabase Postgres (via SQLAlchemy)

## Project Structure

```bash
discord-pm-bot/
│── app/
│   │── bot.py                  # startup & wiring
│   │── discord_handlers.py     # slash cmds, views, modals
│   │── embeds.py               # reusable embeds
│   └── views.py                # Buttons/Selects
│── domain/
│   └── models.py               # Task, Project, enums
│── infra/
│   └── config.py               # project configuration
│── persistence/
│   │── base.py                 # Session, engine
│   │── models.py               # SQLAlchemy ORM tables
│   └── repositories.py         # Repo impls
│── services/
│   └── task_service.py         # use cases
│── README.md
│── requirements.txt            # python environment requirements
│── .env
└── .gitignore
```

## Setup & Running Locally

1. Clone & install

```bash
git clone https://github.com/yourname/discord-pm-bot.git
cd discord-pm-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Environment variables
   create a `.env` file

```env
DISCORD_TOKEN=your-bot-token-here
DATABASE_URL=postgresql+psycopg2://postgres:<ENCODED_PASSWORD>@aws-1-us-west-1.pooler.supabase.com:6543/postgres?sslmode=require
```

3. Run

```bash
python -m app.bot
```

## Database Noets:

this project uses:

```python
Base.metadata.create_all(bind=engine)
```

to create tables automatically.

If you change your models, you’ll need to drop/recreate tables or add migrations (see Alembic if you want schema evolution without losing data).

## Adding Bot to Discord

1. Go to Discord Developer Portal → Your App → OAuth2 → URL Generator.
2. Select bot and applications.commands scopes.
3. Select needed bot permissions (at least Send Messages, Embed Links).
4. Open the generated link in your browser, choose your server, and click Authorize.

## License

MIT License
