from tortoise.contrib.flask import register_tortoise

db = register_tortoise

def init_app(app):
    db(app, config={
        'connections': {
            'default': app.config['DATABASE_URL']
        },
        'apps': {
            'models': ['app.models'],
            'default_connection': 'default',
        }
    })
