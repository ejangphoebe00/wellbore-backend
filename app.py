from backend import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from backend.controllers.user import create_default_user_and_security_level
        create_default_user_and_security_level()
    app.run(debug=True,port=8899)
