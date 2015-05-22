#!/usr/bin/env python
import os
from camstrument_client import CamstrumentClient

CAMERA = os.getenv('CAMERA', 0)
IP = os.getenv('IP', '127.0.0.1')
PORT = os.getenv('PORT', 10001)
GRID_COUNT = os.getenv('GRID_COUNT', 8)
THRESHOLD = os.getenv('THRESHOLD', 20)
DEBUG = os.getenv('DEBUG', 'False') == 'True'


def main():
    c = CamstrumentClient(CAMERA, IP, PORT, GRID_COUNT, THRESHOLD, DEBUG)
    c.run()

if __name__ == '__main__':
    main()
