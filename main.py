from website import criar_app


if __name__ == "__main__":
    app = criar_app()
    app.run(host='0.0.0.0', debug=True)

