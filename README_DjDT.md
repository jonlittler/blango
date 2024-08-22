# Django Debug Toolbar

https://django-debug-toolbar.readthedocs.io/en/latest/

Django Debug Toolbar is a third party library that adds a toolbar to the side of your pages rendered by Django.

- History
- Versions
- Time
- Headers
- Request
- SQL
- Static
- Templates
- Signals
- Logging
- Intercept Redirects
- Profile

```bash
pip3 install django-debug-toolbar
```

Update settings.py

```python
INSTALLED_APPS = [
    # other existing settings truncated for brevity
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # other existing settings truncated for brevity
]

INTERNAL_IPS = ['127.0.0.1', '192.168.11.179']
```
