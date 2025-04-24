import os

# Determine which settings to import based on the environment
env = os.getenv("DJANGO_ENV", "development").lower()

if env == "production":
    from .production import *
elif env == "test":
    from .test import *
else:
    from .development import *

# Optional: Verify critical settings are configured
if not DEBUG and not ALLOWED_HOSTS:
    raise RuntimeError(
        "You must set settings.ALLOWED_HOSTS when DEBUG=False. "
        "Check your environment-specific settings file."
    )