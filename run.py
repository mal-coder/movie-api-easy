from app import main, config

application = main.get_app()

if __name__ == '__main__':
    application.run(host=config.host, port=config.port)
