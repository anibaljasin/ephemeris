from server.server import create_app

if __name__ == '__main__':
    app, _ = create_app()
    app.run(debug=True, port=4000)
