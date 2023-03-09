from flask import Flask
# app = Flask(__name__)
# @app.route('/hello')
# def hello_world():
#     return 'Hello world!'
if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run(port=8000)