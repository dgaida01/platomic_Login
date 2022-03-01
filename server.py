from flask_app import app
from flask_app.controllers import users, authenticators

# TODO controllers import may need to be updated


if __name__ == '__main__':
    app.run(debug=True)
