# -*- coding: utf-8 -*-
import cv2
import numpy as np
import socket


class CamstrumentClient:
    """Class for the Camstrument Client.

    Starts up the camera and contains state for image processing.
    Sends data to server over UDP containing information about
    which parts of the image where motion is seen.

    Attributes:
        camera_index: An integer starting at zero representing which camera
        that should be used.
        ip: The destination IP of the server that data should be sent to.
        port: The destination port of the server that data should be sent to.
        grid_count: The number of rows and columns should the grid contain.
        threshold: Monochrome (0-255) value that should be considered motion.
        debug: Boolean value. If True, show window to display detected motion.
    """
    def __init__(self, camera_index=0, ip='127.0.0.1', port=10001,
                 grid_count=8, threshold=20, debug=False):
        self.debug = debug
        if self.debug:
            self.win_name = "Debug"
            cv2.namedWindow(self.win_name, cv2.CV_WINDOW_AUTOSIZE)
        self.ip = ip
        self.port = port
        self.grid_count = grid_count
        self.threshold = threshold
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cam = cv2.VideoCapture(camera_index)
        self.prev_img = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        self.curr_img = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        self.next_img = cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
        self.img_height, self.img_width = self.next_img.shape
        self.tile_width = int(self.img_width/float(self.grid_count))
        self.tile_height = int(self.img_height/float(self.grid_count))
        self.tiles = map(lambda i: self.generate_tile(self.tile_width,
                         self.tile_height, i[0], i[1]), self.generate_coords())

    def msg(self, x, y):
        return str(x) + "," + str(y)

    def is_b_or_w(self, image, black_max_bgr=2):
        # I got this from http://stackoverflow.com/a/22714410
        # Takes the mean of each cell. If mean is greater than
        # black_max_bgr, then return True.

        # use this if you want to check channels are all basically equal
        # I split this up into small steps to find out where your error
        # is coming from
        mean_bgr_float = np.mean(image, axis=(0, 1))
        mean_bgr_rounded = np.round(mean_bgr_float)
        mean_bgr = mean_bgr_rounded.astype(np.uint8)
        # use this if you just want a simple threshold for simple grayscale
        # or if you want to use an HSV (V) measurement as in your example
        # mean_intensity = int(round(np.mean(image)))
        return False if np.all(mean_bgr < black_max_bgr) else True

    def generate_coords(self):
        lst = []
        for i in xrange(0, self.grid_count):
            for j in xrange(0, self.grid_count):
                lst.append((i, j))
        return lst

    def generate_tile(self, w, h, x, y):
        x_mn = x * w
        x_mx = x_mn + w
        y_mn = y * h
        y_mx = y_mn + h

        return {'xmin': x_mn, 'xmax': x_mx, 'ymin': y_mn, 'ymax': y_mx,
                'x': x, 'y': y}

    def diff_img(self, prev, curr, nxt):
        diff_one = cv2.absdiff(nxt, curr)
        diff_two = cv2.absdiff(curr, prev)
        result = cv2.bitwise_and(diff_one, diff_two)
        erode_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        thresh = cv2.threshold(result, self.threshold, 255,
                               cv2.THRESH_BINARY)[1]
        return cv2.erode(thresh, erode_kernel)

    def run(self):
        while True:
            diffed_img = self.diff_img(self.prev_img, self.curr_img,
                                       self.next_img)
            if self.debug:
                cv2.imshow(self.win_name, diffed_img)

            self.prev_img = self.curr_img
            self.curr_img = self.next_img
            self.next_img = cv2.cvtColor(self.cam.read()[1],
                                         cv2.COLOR_RGB2GRAY)
            for i in self.tiles:
                ymin = i['ymin']
                ymax = i['ymax']
                xmin = i['xmin']
                xmax = i['xmax']
                x = i['x']
                y = i['y']
                if self.is_b_or_w(diffed_img[ymin:ymax, xmin:xmax]):
                    self.sock.sendto(self.msg(x, y), (self.ip, self.port))
            if self.debug:
                key = cv2.waitKey(10)
                if key == 27:
                    cv2.destroyWindow(self.win_name)
                    break
