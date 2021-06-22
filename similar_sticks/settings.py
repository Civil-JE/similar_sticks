import os


def set_settings(app):
    if app.config['ENV'] == 'development':
        app.config.from_object('similar_sticks.config.local.LocalConfig')
    elif app.config['ENV'] == 'production':
        app.config.from_object('similar_sticks.config.prod.ProductionConfig')
    else:
        print('WARNING: NO ENV WAS FOUND USING LOCAL CONFIG')
        app.config.from_object('similar_sticks.config.local.LocalConfig')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
