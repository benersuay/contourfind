# Pixel checking orders for blob finding:
#
# ORDER 1    ORDER 2        ORDER 3        ORDER 4
# 6 7 8        4 5 6        2 3 4        8 1 2
# 5 x 1        3 x 7        1 x 5        7 x 3
# 4 3 2        2 1 8        8 7 6        6 5 4

import cv
import operator

find_surf = 1
dilation = 10
erosion = 2
adaptive_threshold = 1
smooth = 0
rectangle_min_x=0
rectangle_max_x=0
rectangle_min_y=0
rectangle_max_y=0
find_centroids=1

ROI_count=0 # Number of rectangle of interests

white_color = cv.CV_RGB(255,255,255)

font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN,0.5,0.5) #font type, horiz. scale, vert. scale

LOCAL_FILE = 'ROI properties.txt'
f = open(LOCAL_FILE,'w')

def track_edges(entry_y,entry_x):
    global wb, rectangle_min_x, rectangle_max_x, rectangle_min_y, rectangle_max_y

    direction = 3
    x = entry_x
    y = entry_y

    rectangle_min_x = x
    rectangle_max_x = x
    rectangle_min_y = y
    rectangle_max_y = y

    # Entry point was found at x, y
    # Now find a white pixel neighbor
    while(1):

        cv.Set2D(im,y,x,cv.CV_RGB(255,0,0))
           
        # Did you move down or lower left with respect to previous center pixel?
        # Start checking in [ORDER 1] for the next iteration
        if direction == 0:
            if wb[y,x+1]==255:   
                x=x+1
                direction=3
            elif wb[y-1,x+1]==255:
                y=y-1
                x=x+1
                direction=3
            elif wb[y-1,x]==255:
                y=y-1
                direction=0
            elif wb[y-1,x-1]==255:
                y=y-1
                x=x-1
                direction=0
            elif wb[y,x-1]==255:
                x=x-1
                direction=1
            elif wb[y+1,x-1]==255:
                x=x-1
                y=y+1
                direction=1
            elif wb[y+1,x]==255:
                y=y+1
                direction=2
            elif wb[y+1,x+1]==255:
                y=y+1
                x=x+1
                direction=2
        # Did you move left or upper left with respect to previous center pixel?
        # Start checking in [ORDER 2] in the next iteration
        elif direction == 1:
            if wb[y-1,x]==255:
                y=y-1
                direction=0
            elif wb[y-1,x-1]==255:
                y=y-1
                x=x-1
                direction=0
            elif wb[y,x-1]==255:
                x=x-1
                direction=1
            elif wb[y+1,x-1]==255:
                x=x-1
                y=y+1
                direction=1
            elif wb[y+1,x]==255:
                y=y+1
                direction=2
            elif wb[y+1,x+1]==255:
                y=y+1
                x=x+1
                direction=2
            elif wb[y,x+1]==255:
                x=x+1
                direction=3
            elif wb[y-1,x+1]==255:
                y=y-1
                x=x+1
                direction=3

        # Did you move up or upper right with respect to previous center pixel?
        # Start checking in [ORDER 3] in the next iteration
        elif direction == 2:
            if wb[y,x-1]==255:
                x=x-1
                direction=1
            elif wb[y+1,x-1]==255:
                x=x-1
                y=y+1
                direction=1
            elif wb[y+1,x]==255:
                y=y+1
                direction=2
            elif wb[y+1,x+1]==255:
                y=y+1
                x=x+1
                direction=2
            elif wb[y,x+1]==255:
                x=x+1
                direction=3
            elif wb[y-1,x+1]==255:
                y=y-1
                x=x+1
                direction=3
            elif wb[y-1,x]==255:
                y=y-1
                direction=0
            elif wb[y-1,x-1]==255:
                y=y-1
                x=x-1
                direction=0
        # Did you move right or lower right with respect to previous center pixel?
        # Start checking in [ORDER 4] in the next iteration       
        elif direction == 3:
            if wb[y+1,x]==255:
                y=y+1
                direction=2
            elif wb[y+1,x+1]==255:
                y=y+1
                x=x+1
                direction=2
            elif wb[y,x+1]==255:
                x=x+1
                direction=3
            elif wb[y-1,x+1]==255:
                y=y-1
                x=x+1
                direction=3
            elif wb[y-1,x]==255:
                y=y-1
                direction=0
            elif wb[y-1,x-1]==255:
                y=y-1
                x=x-1
                direction=0
            elif wb[y,x-1]==255:
                x=x-1
                direction=1
            elif wb[y+1,x-1]==255:
                x=x-1
                y=y+1
                direction=1
        # Boundary conditions for safety
        if x<=0:
            x=1
        if x>=im.width:
            x=im.width-1
        if y<=0:
            y=1
        if y>=im.height:
            y=im.height-1
       
        # Update the boundary rectangle size
        if x<rectangle_min_x:
            rectangle_min_x=x
        if x>rectangle_max_x:
            rectangle_max_x=x
        if y<rectangle_min_y:
            rectangle_min_y=y
        if y>rectangle_max_y:
            rectangle_max_y=y
        if entry_x==x and entry_y==y:
            break


im = cv.LoadImage("im4.png")

# Single channel versions of the original RGB image
im_r = cv.CreateImage((im.width,im.height),8,1)
im_g = cv.CreateImage((im.width,im.height),8,1)
im_b = cv.CreateImage((im.width,im.height),8,1)

# Thresholded images to obtain a binary image of each channel
im_r_threshold = cv.CreateImage((im.width,im.height),8,1)
im_g_threshold = cv.CreateImage((im.width,im.height),8,1)
im_b_threshold = cv.CreateImage((im.width,im.height),8,1)
im_gray_threshold = cv.CreateImage((im.width,im.height),8,1)


#covMat = cv.CreateMat(max(im.width,im.height),max(im.width,im.height),cv.CV_32FC1)
#avgMat = cv.CreateMat(max(im.width,im.height),max(im.width,im.height),cv.CV_32FC1)

#cv.Set(covMat,0)
#cv.Set(avgMat,0)

# Images that show contours in each channel
im_r_contours = cv.CreateImage((im.width,im.height),8,3)
im_g_contours = cv.CreateImage((im.width,im.height),8,3)
im_b_contours = cv.CreateImage((im.width,im.height),8,3)
im_gray_contours = cv.CreateImage((im.width,im.height),8,3)

im_no_line = cv.CreateImage((im.width,im.height),8,3)
cv.Copy(im,im_no_line)

all_in_one = cv.CreateImage((im.width,im.height),8,3)

# Gray image, which is obtained by converting the original to cv.RGB2GRAY
gray = cv.CreateImage((im.width,im.height),8,1)
cv.CvtColor(im,gray,cv.CV_RGB2GRAY)


# Image where white blobs will be shown
wb = cv.CreateImage((im.width,im.height),8,1)

cv.Set(all_in_one,0)
cv.Set(im_r_contours,0)

cv.Set(im_gray_threshold,0)
cv.Set(wb,0)

# Image that shows common robust features that are found in all of the channels
# This is decided by comparing their locations and not their descriptors' values
common_feature_locations = cv.CreateImage((im.width,im.height),8,3)
cv.Set(common_feature_locations,0)

# Original image window
cv.NamedWindow("Original",1)

# Windows where single channels are shown
cv.NamedWindow("R",1)
cv.NamedWindow("G",1)
cv.NamedWindow("B",1)

# Windows where features of the single channel images are shown
cv.NamedWindow("All in one",1)

# Window where the gray image is shown
cv.NamedWindow("GRAY",1)

# Window where the white blobs are shown
cv.NamedWindow("White Blobs",1)

# Separate the original image to its channels
for x in range(im.width):
    for y in range(im.height):
        im_r[y,x]=im[y,x][0]
        im_g[y,x]=im[y,x][1]
        im_b[y,x]=im[y,x][2]

for i in range(smooth):
    cv.Smooth(gray,gray,cv.CV_GAUSSIAN,3,3)
    cv.Smooth(im_r,im_r,cv.CV_GAUSSIAN,3,3)
    cv.Smooth(im_b,im_b,cv.CV_GAUSSIAN,3,3)
    cv.Smooth(im_g,im_g,cv.CV_GAUSSIAN,3,3)

# Threshold the image using an adaptive filter or a constant threshold value
if adaptive_threshold == 1:
    cv.AdaptiveThreshold(im_r,im_r_threshold,255,cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV)
    cv.AdaptiveThreshold(im_g,im_g_threshold,255,cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV)
    cv.AdaptiveThreshold(im_b,im_b_threshold,255,cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV)
    cv.AdaptiveThreshold(gray,im_gray_threshold,255,cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV)
else:
    cv.Threshold(im_r,im_r_threshold,50,255,cv.CV_THRESH_BINARY_INV)
    cv.Threshold(im_g,im_g_threshold,50,255,cv.CV_THRESH_BINARY_INV)
    cv.Threshold(im_b,im_b_threshold,50,255,cv.CV_THRESH_BINARY_INV)

seq = cv.FindContours(im_r_threshold,cv.CreateMemStorage())
cv.DrawContours(im_r_contours,seq,cv.CV_RGB(255,0,0),cv.CV_RGB(255,255,255),1,1)

while seq != None:
    convex_hull = cv.ConvexHull2(seq,cv.CreateMemStorage(),cv.CV_CLOCKWISE, 1)
   
    #print str(len(convex_hull))
    #for i in range(len(convex_hull)):
        #print str(convex_hull[i])
    cv.PolyLine(all_in_one,[convex_hull],1,cv.CV_RGB(255,0,0))

    #for i in range(len(seq)):
    #    cv.Circle(im,seq[i],1,cv.CV_RGB(255,0,0))
    seq = seq.h_next()

seq = cv.FindContours(im_g_threshold,cv.CreateMemStorage())
cv.DrawContours(im_g_contours,seq,cv.CV_RGB(0,255,0),cv.CV_RGB(255,255,255),1,1)

while seq != None:
    convex_hull = cv.ConvexHull2(seq,cv.CreateMemStorage(),cv.CV_CLOCKWISE, 1)
   
    #print str(len(convex_hull))
    #for i in range(len(convex_hull)):
        #print str(convex_hull[i])
    cv.PolyLine(all_in_one,[convex_hull],1,cv.CV_RGB(0,255,0))

    #for i in range(len(seq)):
    #    cv.Circle(im,seq[i],1,cv.CV_RGB(255,0,0))
    seq = seq.h_next()

seq = cv.FindContours(im_b_threshold,cv.CreateMemStorage())
cv.DrawContours(im_b_contours,seq,cv.CV_RGB(0,0,255),cv.CV_RGB(255,255,255),1,1)

while seq != None:
    convex_hull = cv.ConvexHull2(seq,cv.CreateMemStorage(),cv.CV_CLOCKWISE, 1)
   
    #print str(len(convex_hull))
    #for i in range(len(convex_hull)):
        #print str(convex_hull[i])
    cv.PolyLine(all_in_one,[convex_hull],1,cv.CV_RGB(0,0,255))

    #for i in range(len(seq)):
    #    cv.Circle(im,seq[i],1,cv.CV_RGB(255,0,0))
    seq = seq.h_next()

seq = cv.FindContours(im_gray_threshold,cv.CreateMemStorage())
cv.DrawContours(im_gray_contours,seq,cv.CV_RGB(0,0,255),cv.CV_RGB(255,255,255),1,1)

while seq != None:
    convex_hull = cv.ConvexHull2(seq,cv.CreateMemStorage(),cv.CV_CLOCKWISE, 1)
   
    #print str(len(convex_hull))
    #for i in range(len(convex_hull)):
        #print str(convex_hull[i])
    cv.PolyLine(all_in_one,[convex_hull],1,cv.CV_RGB(255,255,255))

    #for i in range(len(seq)):
    #    cv.Circle(im,seq[i],1,cv.CV_RGB(255,0,0))
    seq = seq.h_next()


for i in range(dilation):
    cv.Dilate(im_r_contours,im_r_contours)
    cv.Dilate(im_g_contours,im_g_contours)
    cv.Dilate(im_b_contours,im_b_contours)

for i in range(erosion):
    cv.Erode(im_r_contours,im_r_contours)
    cv.Erode(im_g_contours,im_g_contours)
    cv.Erode(im_b_contours,im_b_contours)

# Find robust features and mark their locations on the images
if find_surf == 1:
    (keypoints, descriptors) = cv.ExtractSURF(im_r, None, cv.CreateMemStorage(), (0, 300, 3, 1))
    
    for ((x, y), laplacian, size, dir, hessian) in keypoints:
        x = int(x)
        y = int(y)
        cv.Circle(im_r_contours,(x,y),1,cv.CV_RGB(255,0,0))
        cv.Circle(all_in_one,(x,y),1,cv.CV_RGB(255,0,0))
        common_feature_locations[y,x]=(1,common_feature_locations[y,x][1],common_feature_locations[y,x][2])

    (keypoints, descriptors) = cv.ExtractSURF(im_g, None, cv.CreateMemStorage(), (0, 300, 3, 1))
    for ((x, y), laplacian, size, dir, hessian) in keypoints:
        x = int(x)
        y = int(y)
        cv.Circle(im_g_contours,(x,y),1,cv.CV_RGB(0,255,0))
        cv.Circle(all_in_one,(x,y),1,cv.CV_RGB(0,255,0))
        common_feature_locations[y,x]=(common_feature_locations[y,x][0],1,common_feature_locations[y,x][2])

    (keypoints, descriptors) = cv.ExtractSURF(im_b, None, cv.CreateMemStorage(), (0, 300, 3, 1))
    for ((x, y), laplacian, size, dir, hessian) in keypoints:
        x = int(x)
        y = int(y)
        cv.Circle(im_b_contours,(x,y),1,cv.CV_RGB(0,0,255))
        cv.Circle(all_in_one,(x,y),1,cv.CV_RGB(0,0,255))
        common_feature_locations[y,x]=(common_feature_locations[y,x][0],common_feature_locations[y,x][1],1)

    (keypoints, descriptors) = cv.ExtractSURF(gray, None, cv.CreateMemStorage(), (0, 300, 3, 1))
    for ((x, y), laplacian, size, dir, hessian) in keypoints:
        x = int(x)
        y = int(y)
        cv.Circle(all_in_one,(x,y),1,cv.CV_RGB(255,255,255))

    for x in range(im.width):
        for y in range(im.height):
            if( common_feature_locations[y,x][0] and common_feature_locations[y,x][1] and common_feature_locations[y,x][2]):
                cv.Circle(im,(x,y),1,(135,255,120))

    for x in range(im.width):
        for y in range(im.height):
            if( common_feature_locations[y,x][0] or common_feature_locations[y,x][1] or common_feature_locations[y,x][2]):
                cv.Circle(im,(x,y),1,cv.CV_RGB(0,255,255))

for i in range(dilation):
    cv.Dilate(all_in_one,all_in_one)

for i in range(erosion):
    cv.Erode(all_in_one,all_in_one)

# Now, after dilating the mixed features image, we want to find the locations and the bounding rectangles of the white blobs
# Copy these white blobs to a new image
for x in range(im.width):
    for y in range(im.height):
        if(all_in_one[y,x][0]==255 and all_in_one[y,x][1]==255 and all_in_one[y,x][2]==255):
                    cv.Set2D(wb,y,x,255)

avg_ROI_size=0
total_ROI_size=0
rectangles=[]

# In this new image find blobs' center points and bounding rectangles
if find_centroids == 1:
	for x in range(im.width):
    		for y in range(im.height):
        		if wb[y,x] == 255:
           
            			entry_point_x = x
           			entry_point_y = y
            			# Safety for the corners and image limits
            			if x>=1 and x<im.width and y>=1 and y<im.height:
                			track_edges(y,x)
                			dx=rectangle_max_x-rectangle_min_x
                			dy=rectangle_max_y-rectangle_min_y
                			#print "max x is "+str(rectangle_max_x)
			                #print "max y is "+str(rectangle_max_y)
	
			                #print "min x is "+str(rectangle_min_x)
			                #print "min y is "+str(rectangle_min_y)
	
			                #print "dx is "+str(dx)
			                #print "dy is "+str(dy)
			                for i in range(dx+1):
			                    for j in range(dy+1):
			                        #print j+rectangle_min_y
			                        #print i+rectangle_min_x
			                        cv.Set2D(wb,j+rectangle_min_y,i+rectangle_min_x,0)
		
			                ROI_size = dx*dy
			                rectangles.append([ROI_size,rectangle_max_x,rectangle_max_y,rectangle_min_x,rectangle_min_y])
			                ROI_count = ROI_count + 1
			                total_ROI_size = (total_ROI_size + ROI_size)


	avg_ROI_size = total_ROI_size / ROI_count

	for c in range(ROI_count):   
	    total_red = 0
	    total_green = 0
	    total_blue = 0
	    total_gray = 0
	    surfs=0
	    if rectangles[c][0] >= avg_ROI_size:
        	cv.Rectangle(im,(rectangles[c][1],rectangles[c][2]),(rectangles[c][3],rectangles[c][4]),cv.CV_RGB(255,255,0))
        	cv.NamedWindow("ROI: "+str(c),1)
        	dx=rectangles[c][1]-rectangles[c][3]
        	dy=rectangles[c][2]-rectangles[c][4]
        	obj_im=cv.CreateImage((dx+1,dy+1),8,3)
        	#obj_im_gray=cv.CreateImage((dx+1,dy+1),8,1)
       
        	for i in range(dx+1):
            		for j in range(dy+1):
                		cv.Set2D(obj_im,j,i,(im[j+rectangles[c][4],i+rectangles[c][3]][0],
                	                im[j+rectangles[c][4],i+rectangles[c][3]][1],
                	                im[j+rectangles[c][4],i+rectangles[c][3]][2]))

               	 		total_red = total_red + im_no_line[j+rectangles[c][4],i+rectangles[c][3]][2]
                		total_green = total_green + im_no_line[j+rectangles[c][4],i+rectangles[c][3]][1]
                		total_blue = total_blue + im_no_line[j+rectangles[c][4],i+rectangles[c][3]][0]
                		total_gray = total_gray + gray[j+rectangles[c][4],i+rectangles[c][3]]
               
                		if( common_feature_locations[j+rectangles[c][4],i+rectangles[c][3]][0] or common_feature_locations[j+rectangles[c][4],i+rectangles[c][3]][1] or common_feature_locations[j+rectangles[c][4],i+rectangles[c][3]][2]):
                     			surfs=surfs+1
                    
        #cv.CvtColor(obj_im,obj_im_gray,cv.CV_RGB2GRAY)


        	avg_red = total_red / (dx*dy)
        	avg_green = total_green / (dx*dy)
        	avg_blue = total_blue / (dx*dy)
        	avg_gray = total_gray / (dx*dy)
       

        	(mean,stdDev) = cv.AvgSdv(obj_im)
        	print "ROI MEAN " +str(c) + ":" + str(mean)
        	print "ROI STDDEV "+str(c)+":"+str(stdDev)
       
        	f.write("ROI #" +str(c) + " MEAN : " + str(mean)+"\n")
        	f.write("ROI #"+str(c)+" STDDEV : "+str(stdDev)+"\n")
        	f.write("ROI #"+str(c)+" SURFs : "+str(surfs)+"\n")
        	f.write("ROI #"+str(c)+" rectangle dimensions (width,height,ratio) : "+str(dx)+","+str(dy)+","+str(float(operator.truediv(dx,dy)))+"\n")
        	cx = int((rectangles[c][1]+rectangles[c][3])/2)
        	cy = int((rectangles[c][2]+rectangles[c][4])/2)
        	f.write("ROI #"+str(c)+" center coordinates (x,y) : "+str(cx)+","+str(cy)+"\n")
        	f.write("\n")
       
        	#cv.CalcCovarMatrix([obj_im_gray],covMat,avgMat,cv.CV_COVAR_NORMAL)
       
        	cv.PutText(obj_im,str(c),(20,20),font,white_color)
        	#cv.PutText(obj_im,"ar: "+str(avg_red),(20,20),font,white_color)
        	#cv.PutText(obj_im,"ag: "+str(avg_green),(20,40),font,white_color)
        	#cv.PutText(obj_im,"ab: "+str(avg_blue),(20,60),font,white_color)
        	#cv.PutText(obj_im,"a: "+str(avg_gray),(20,80),font,white_color)
   
       		#cv.PutText(obj_im,"mean: "+str(mean),(20,80),font,white_color)
       
        	cv.ShowImage("ROI: "+str(c),obj_im)

cv.ShowImage("R",im_r_contours)
cv.ShowImage("G",im_g_contours)
cv.ShowImage("B",im_b_contours)

cv.ShowImage("All in one",all_in_one)

cv.ShowImage("GRAY",gray)

cv.ShowImage("White Blobs",wb)

cv.ShowImage("R",im_r_threshold)
cv.ShowImage("G",im_g_threshold)
cv.ShowImage("B",im_b_threshold)

#cv.ShowImage("R",im_r)
#cv.ShowImage("G",im_g)
#cv.ShowImage("B",im_b)

cv.ShowImage("Original",im)

f.close()

cv.WaitKey(0)

