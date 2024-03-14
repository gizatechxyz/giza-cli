import os

__version__ = "0.14.1"
# Until DNS is fixed
API_HOST = os.environ.get("GIZA_API_HOST", "https://api.gizatech.xyz")
