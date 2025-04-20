from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_jwt(app):
    jwt.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'your-secret-key-here'
    
    return jwt
