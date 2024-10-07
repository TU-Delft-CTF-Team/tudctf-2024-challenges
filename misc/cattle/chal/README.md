# Cattle

## Docker

To run this challenge via docker, execute:

```bash
docker build -t cattle .
docker run --rm -p 8888:8888 cattle
```

## Locally

First, it is recommended you create a new virtual environment:

### Linux/Mac OS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python3 -m venv .venv
.venv\Scripts\Activate.ps1
```

---

Then, install all dependencies:

```bash
pip install -r requirements.txt
```

Finally, you can start the server by running:

```bash
uvicorn main:app --host 0.0.0.0 --port 8888
```
