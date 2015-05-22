camstrument-client
==================

Use a camera to turn motion into sound. See it in action here: https://www.youtube.com/watch?v=cpfBpndtUmU#t=30m0s

Setup
-----

Clone the repo.

Install python-opencv and OpenCV. On Ubuntu, the easiest way to do this
is: ``sudo apt-get install python-opencv``.

Installation
------------

You don't have to install the program on your system to run it, but you
can if you'd like

To run the program without installing, from the root of the project run
``python -m camstrument_client``

To install the program to your system, run ``python setup.py install``.
On success, you should be able to run the ``camstrument_client``
command.

Usage
-----

There are several options you can pass to the program via environment
variables.

Those variables are:

-  ``CAMERA``: An integer starting at zero representing which camera
   that should be used.
-  ``IP``: The destination IP of the server that data should be sent to.
-  ``PORT``: The destination port of the server that data should be sent
   to.
-  ``GRID_COUNT``: The number of rows and columns should the grid
   contain.
-  ``THRESHOLD``: Monochrome (0-255) value that should be considered
   motion.
-  ``DEBUG``: Boolean value. If True, show window to display detected
   motion.

Example:
``CAMERA=0 IP='127.0.0.1' PORT=10001 GRID_COUNT=8 THRESHOLD=20 DEBUG=True camstrument_client``
