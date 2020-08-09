from server.server import create_app

if __name__ == '__main__':
    app, db = create_app()

    app.run(debug=True, host='0.0.0.0', port=4000)
