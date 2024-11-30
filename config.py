# config.py
DATABASE_CONFIG = {
    "connections": {
        "default": "postgres://postgres:postgres@localhost:5432/mindsync",
    },
    "apps": {
        "models": {
            "models": [
                "app.models.users",
                "app.models.notes",
                "app.models.organizations",
                "app.models.memberships",
                "app.models.documents",
                "app.models.chats",
                "app.models.whatsapps",
                "aerich.models",
            ],  # Tambahkan aerich.models
            "default_connection": "default",
        },
    },
}
