import pandas as pd
import cv2
from img_utils import *

def contour_properties(contours):
    '''basically run Matlab's regionprops
    '''
    
    df = pd.DataFrame(columns=[
        'Area',
        'Perimeter',
        'Aspect Ratio',
        'Extent',
        'Solidity',
        'Ellipse Center',
        'Ellipse Major Axis',
        'Ellipse Minor Axis',
        'Orientation',
        'Eccentricity',
        'contour'
    ])
    
    for ii,cnt in enumerate(contours):
        df.at[ii,'Area'] = cv2.contourArea(cnt)
        df.at[ii,'Perimeter'] = len(cnt)
        df.at[ii,'Aspect Ratio'] = calc_aspect_ratio(cnt)
        df.at[ii,'Extent'] = calc_extent(cnt)
        df.at[ii,'Solidity'] = calc_solidity(cnt)
        
        if len(cnt)>=5:
            (x,y),(ma,MA),angle = cv2.fitEllipse(cnt)
            df.at[ii,'Ellipse Center'] = (x,y)
            df.at[ii,'Ellipse Major Axis'] = MA
            df.at[ii,'Ellipse Minor Axis'] = ma
            df.at[ii,'Orientation'] = angle
            df.at[ii,'Eccentricity'] = (MA-ma)/(MA+ma)
            
        df.at[ii,'contour'] = cnt
        
    return df


def calc_extent(cnt):
    area = cv2.contourArea(cnt)
    x,y,w,h = cv2.boundingRect(cnt)
    rect_area = w*h
    extent = float(area)/rect_area
    return extent


def calc_aspect_ratio(cnt):
    x,y,w,h = cv2.boundingRect(cnt)
    aspect_ratio = float(w)/h
    return aspect_ratio


def calc_solidity(cnt):
    area = cv2.contourArea(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    solidity = float(area)/hull_area
    return solidity


def show_contour(img,
                 cnt,
                 figsize=(4,4)):
    '''Given an image and a contour, crop the image
    to the bounding box of the contour and show the
    cropped image
    '''
    
    # Draw the contour's outline
    img_rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    img_contour = cv2.drawContours(img_rgb, [cnt], -1, (0,255,0), 1)
    
    # Crop down to bounding box and plot
    x,y,w,h = cv2.boundingRect(cnt)
    img_crop = img_contour[y-2:y+h+2,x-2:x+w+2,:]
    ax = imshow(img_crop,
                figsize=figsize)
    return ax


