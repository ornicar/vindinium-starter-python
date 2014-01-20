Should work with python2 and python3.

Install deps:

    pip install -r requirements.txt

Run with:

    python server.py <key> <[training|arena]> <number-of-games-to-play> [server-url]

Examples:

    python server.py mySecretKey arena 10
    python server.py mySecretKey training 10 http://localhost:9000
