Contour Find
============

An OpenCV script for object detection on a plain background. The script optionally uses SURF, dilation, erosion, smoothing, and adaptive thresholding to convert detected contours into blobs so we can extract them. Found features are also shown on separate images as well as all together in one image.

Dependency
----------

Tested on Ubuntu 12.04 with OpenCV 2.4.6.

Example
-------

To run the script, simply

    python find_objects.py

This will pop up several windows showing found features and processed images.

![countourfind](http://users.wpi.edu/~benersuay/resimler/projects/contourfind.png "Contour Find")