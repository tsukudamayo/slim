import os
import argparse

import numpy as np
from PIL import Image


# _IMAGE_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/food_google_search'
# _TARGET_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/food_google_search_224'


def difference_to_target(org_size, target_size):
    """
    return image size which is appropriately resized with keeping aspect ratio.
    
    input: PIL image.size
    output: tuple(width, height)
    """
    large_value = np.argmax(org_size)
    small_value = np.argmin(org_size)

    changed_size = []
    rate_of_change = target_size[large_value] / org_size[large_value]
    if large_value == 0:
        changed_size.append(int(target_size[0]))
        changed_size.append(int(org_size[1] * rate_of_change))
    else:
        changed_size.append(int(org_size[0] * rate_of_change))
        changed_size.append(int(target_size[1]))
        
    return tuple(changed_size)


def square_margin(img, background_color):
    """
    make a square background and add margins.
    
    input
      img: PIL Image
      background_color: (R,G,B)
    output: PIL Image which add margin
    """
    width, height = img.size
    if width == height:
        return img
    elif width > height:
        result = Image.new(img.mode, (width, width), background_color)
        result.paste(img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(img.mode, (height, height), background_color)
        result.paste(img, ((height - width) // 2, 0))
        return result


def main(image_dir, target_dir):

    # image_dir = _IMAGE_DIR
    # target_dir = _TARGET_DIR
    target_size = tuple((224,224))
    
    #----------------------#
    # generate directories #
    #----------------------#
    print(os.listdir(image_dir))
    sub_directories = os.listdir(image_dir)
    
    if os.path.isdir(target_dir) is False:
        os.mkdir(target_dir)
        for sub_directory in sub_directories:
            directory = os.path.join(target_dir, sub_directory)
            os.mkdir(directory)
    
    #--------#
    # resize #
    #--------#
    
    # count the number of all image files
    number_of_files = 0
    for sub_directory in sub_directories:
        sub_directory = os.path.join(image_dir, sub_directory)
        number_of_files += len(os.listdir(sub_directory))
    
    # all image files convert into (256,256) and save target directories
    count = 0
    progress = "\r>>{0}/{1} targetfile:{2}"
    for root, dirs, files in os.walk(image_dir):
        for f in files:
            try:
                # define filepath
                filepath = os.path.join(root, f)
                dirname = os.path.basename(os.path.dirname(filepath))
                sub_dir = os.path.join(target_dir, dirname)
                # TODO directory check
                if os.path.exists(sub_dir) is False:
                    os.mkdir(sub_dir)
                targetpath = os.path.join(sub_dir, f)
    
                # convert image
                img = Image.open(filepath)
                changed_size = difference_to_target(img.size, target_size)
                img_resize = img.resize(changed_size)
                img_resize = square_margin(img_resize, (255,255,255))
                img_resize.save(targetpath)
    
                # display progress
                count += 1
                print(progress.format(count, number_of_files, targetpath),end='')
            except OSError:
                print('%s can not convert by OSERROR' % f)
                pass
            except TypeError:
                print('%s can not convert by TypeError' % f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir',
                        dest='image_dir',
                        type=str,
                        default=None,
                        help='enter the directory that include image file')
    parser.add_argument('--target_dir',
                        dest='target_dir',
                        type=str,
                        default=None,
                        help='enter the directory that you want to output')
    argv = parser.parse_args()
                        
    main(argv.image_dir, argv.target_dir)
