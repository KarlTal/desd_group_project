To containerize this project for Docker, open Command Prompt in the directory this README.md file is, and run these commands:

1. `docker build --tag uweflix-django uweflix/`
2. `docker run --publish 8000:8000 uweflix-django`

You can then connect to the website via `http://127.0.0.1:8000/`
