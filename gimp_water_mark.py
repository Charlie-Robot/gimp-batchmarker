#!/usr/bin/env python
import os, sys
from gimpfu import *
#import PIL

def batch_marker(*args):
    source_directory, watermark_image, opacity,\
    justify_x, x,\
    justify_y, y = args
    count = 0
    #Get a list of files to apply water mark to
    file_list = [fn for fn in os.listdir(source_directory)\
                 if os.path.isfile('{}\{}'.format(source_directory, fn))]
    
    #New Directory for marked images
    new_dir = source_directory + r"\Marked"
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
        
    #Iterate over image files applying identicle water mark to each one
    for img in file_list:
        try:
            #Rename watermarked file and alter directory,
            #keeping originals unaltered and inplace
            fn = img.split('.')
            new_fn = fn[0] + '_MARKED_Opacity_{}'.format(int(opacity))
            fn[0] = new_fn
            new_fn = '{}\{}'.format(new_dir, '.'.join(fn))
            
            #Load image
            img = '{}\{}'.format(source_directory, img)
            
            image = pdb.gimp_file_load(img, img)
            #Image size
            height = image.height
            width = image.width
            
            #Create a water mark layer from specified image with given opacity
            mark = pdb.gimp_file_load_layer(image, watermark_image)
            mark.opacity = opacity

            #X,Y coords
            active_x = x
            active_y = y

            #Adjust active coords for padding
            if justify_x == 0:
                active_x = (width / 2) - (mark.width / 2)
            elif justify_x  == 2:
                active_x = width - mark.width - x
            if justify_y == 0:
                active_y = (height / 2) - (mark.height / 2)
            elif justify_y == 2:
                active_y = height - mark.height - y

            #Add the watermark to base image
            image.add_layer(mark)
            if mark.width > width or mark.height > height:
                RATIO = max(mark.width / width, mark.height / height)
                mark.scale(mark.width / RATIO,
                           mark.height / RATIO)
            
            mark.translate(active_x,active_y)
            #Merge Layers and Save Image
           
            drawable = pdb.gimp_image_merge_down(image, mark, 1)
            pdb.gimp_file_save(image, drawable, new_fn, new_fn)

            #Close image when done
            gimp.pdb.gimp_image_delete(image)              
           
        except RuntimeError:
            pass


register(
    "batch_mark",
    "Add a watermark to a Folder of images",
    "Help Me help Myself",
    "Kelly Wyss",
    "Kelly Wyss",
    "2016.11.21",
    "<Toolbox>/File/Watermark",
    "",
    [
     (PF_DIRNAME,   "source_directory",     "Source Directory",     "C:"),
     (PF_FILE,      "watermark_image",      "Water Mark Image",     None),
     (PF_SLIDER,    "watermark_opacity",    "Water Mark Opacity",   50,     (0,100, 1)),
     (PF_OPTION,    "justify_x",            "Justify X:",           0,      ["Center",
                                                                             "Left",
                                                                             "Right"]),
     (PF_INT,       "x",                    "Pad X",                0),
     (PF_OPTION,    "justify_y",            "Justify Y:",           0,      ["Center",
                                                                             "Top",
                                                                             "Bottom"]),
     (PF_INT,       "y",                    "Pad Y",                0),
    ],
    [],
    batch_marker)

main()
