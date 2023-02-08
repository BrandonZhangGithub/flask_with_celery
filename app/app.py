from initialization import create_app

app = create_app()
from initialization import blueprint_process


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')