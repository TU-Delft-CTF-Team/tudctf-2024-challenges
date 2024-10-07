import argparse

import uvicorn

from app import app

# Run the application. It should be run as a module, not as a script.
# Move to the directory that contains the `app` directory, and run `python -m app`.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)
