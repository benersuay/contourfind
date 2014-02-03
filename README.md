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

In this image below 3 objects are detected. Yellow rectangles show the bounding boxes for detected objects. It is possible to adjust the amount of smoothing, or eroding applied to this image and it will remarkably change the object detection rate. Depending on the surface of the object(s) you are trying to detect, you may want to use SURF (e.g. if there are patterns) or not. You can somewhat control the behavior of the script by adjusting the find_surf, dilation, erosion, adaptive_threshold and smooth variables.

The script also outputs found region of interest properties in a txt file: ROI properties.txt.

![countourfind](http://users.wpi.edu/~benersuay/resimler/projects/contourfind.png "Contour Find")
