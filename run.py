#! /usr/bin/env python3.8
"""
AUTHOR : MOHAN KUMAR PALURU
Description : Audio Server Starter App
                Run this file with python3.8 to start the service
"""


import uvicorn
from decouple import config

if __name__ == "__main__":
    AUDIO_SERVER_PORT = int(config("AUDIO_SERVER_PORT"))
    uvicorn.run("app:app", reload=False, port=AUDIO_SERVER_PORT)
