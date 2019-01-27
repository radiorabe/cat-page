# RaBe Cat Landing Page

## Usage

1. Navigate to page
2. Find services
3. See cat
4. ???
5. PROFIT!!!

### Configuration

See `python app/server.js` for usage message and configuration info.

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
