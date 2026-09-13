import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

from app.main import app as fastapi_app


class StripApiPrefix:
    """Expose FastAPI under /api/* while keeping its existing /cases, /auth, etc. routes."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope.get("path", "").startswith("/api"):
            scope = dict(scope)
            path = scope.get("path", "")
            scope["path"] = path[4:] or "/"
            raw_path = scope.get("raw_path")
            if raw_path:
                scope["raw_path"] = raw_path[4:] or b"/"
        await self.app(scope, receive, send)


app = StripApiPrefix(fastapi_app)
