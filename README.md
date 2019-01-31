# RaBe Cat Landing Page

[![Build Status](https://travis-ci.com/radiorabe/cat-page.svg?branch=master)](https://travis-ci.com/radiorabe/cat-page) [![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://renovatebot.com/)

Overengineered intranet landing page for [Radio Bern RaBe](https://www.rabe.ch).

![Screenshot of page.](docs/screenshot.png)

## Usage

1. Navigate to page
2. Find services
3. See cat
4. ???
5. PROFIT!!!

### Configuration

See `python app/server.py --help` for usage message and configuration info.

### Docker

```bash
docker run --rm -ti -p 5000:5000 radiorabe/catpage
```

Connect to [localhost:5000](http://localhost:5000).

### Docker-compose

```bash
cp env.example .env
$EDITOR .env
docker-compose up -d
```

## Contributing

### pre-commit hook

```bash
pip install pre-commit
pip install -r requirements-dev.txt -U
pre-commit install
```

### Running tests

```bash
pytest --cov=app
```
