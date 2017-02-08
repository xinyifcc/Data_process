import os
import cv2
import numpy as np 

def resize(im, target_size, max_size):
    """
    only resize input image to target size and return scale
    :param im: BGR image input by opencv
    :param target_size: one dimensional size (the short side)
    :param max_size: one dimensional max size (the long side)
    :return:
    """
    im_shape = im.shape
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    im_scale = float(target_size) / float(im_size_min)
    # prevent bigger axis from being more than max_size:
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)
    im = cv2.resize(im, None, None, fx=im_scale, fy=im_scale, interpolation=cv2.INTER_LINEAR)
    return im, im_scale

def im_mean(img_dir, target_size, max_size):
    imgs = os.listdir(img_dir)
    im_means = []

    for img in imgs:
        img = '/'.join([img_dir,img])
        im = cv2.imread(img)
        im, im_scale = resize(im, target_size, max_size)
        im_mean = np.mean(im)
        im_means.append(im_mean)

    s = np.sum(im_means)
    n = len(im_means) 
    imgs_mean = s / n
    
    return  imgs_mean

if __name__ == "__main__":
    img_dir = './'
    target_size = 800
    max_size = 1000
    img_mean = im_mean(img_dir, target_size, max_size)
    print(img_mean)
