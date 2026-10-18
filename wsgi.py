import os
from app import app, init, UPLOADS
os.makedirs(UPLOADS, exist_ok=True)
init()
