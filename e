warning: in the working copy of 'api/index.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'vercel.json', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/api/index.py b/api/index.py[m
[1mindex 74558727..c259cb6e 100644[m
[1m--- a/api/index.py[m
[1m+++ b/api/index.py[m
[36m@@ -7,4 +7,26 @@[m [mBACKEND = os.path.join(ROOT, "backend")[m
 if BACKEND not in sys.path:[m
     sys.path.insert(0, BACKEND)[m
 [m
[31m-from app.main import app[m
\ No newline at end of file[m
[32m+[m[32mfrom app.main import app as fastapi_app[m
[32m+[m
[32m+[m
[32m+[m[32mclass StripApiPrefix:[m
[32m+[m[32m    def __init__(self, app):[m
[32m+[m[32m        self.app = app[m
[32m+[m
[32m+[m[32m    async def __call__(self, scope, receive, send):[m
[32m+[m[32m        if scope["type"] == "http":[m
[32m+[m[32m            path = scope.get("path", "")[m
[32m+[m
[32m+[m[32m            if path.startswith("/api"):[m
[32m+[m[32m                scope = dict(scope)[m
[32m+[m[32m                scope["path"] = path[4:] or "/"[m
[32m+[m
[32m+[m[32m                raw_path = scope.get("raw_path")[m
[32m+[m[32m                if raw_path:[m
[32m+[m[32m                    scope["raw_path"] = raw_path[4:] or b"/"[m
[32m+[m
[32m+[m[32m        await self.app(scope, receive, send)[m
[32m+[m
[32m+[m
[32m+[m[32mapp = StripApiPrefix(fastapi_app)[m
\ No newline at end of file[m
[1mdiff --git a/vercel.json b/vercel.json[m
[1mindex a1166b19..f6d90044 100644[m
[1m--- a/vercel.json[m
[1m+++ b/vercel.json[m
[36m@@ -1,14 +1,4 @@[m
 {[m
   "buildCommand": "cd frontend && npm ci && npm run build",[m
[31m-  "outputDirectory": "frontend/build",[m
[31m-  "rewrites": [[m
[31m-    {[m
[31m-      "source": "/api/:path*",[m
[31m-      "destination": "/api"[m
[31m-    },[m
[31m-    {[m
[31m-      "source": "/((?!api/).*)",[m
[31m-      "destination": "/index.html"[m
[31m-    }[m
[31m-  ][m
[32m+[m[32m  "outputDirectory": "frontend/build"[m
 }[m
\ No newline at end of file[m
