import os
from PIL import Image


_IMAGE_DIR = 'data/'
_TARGET_DIR = 'food256'


def main():
    image_dir = _IMAGE_DIR
    target_dir = os.path.join(_IMAGE_DIR, _TARGET_DIR)
    
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
                targetpath = os.path.join(sub_dir, f)
    
                # convert image
                img = Image.open(filepath)
                img_resize = img.resize((224, 224))
                img_resize.save(targetpath)
    
                # display progress
                count += 1
                print(progress.format(count, number_of_files, targetpath),end='')
            except OSError:
                print('%s can not convert by OSERROR' % f)
                pass


if __name__ == '__main__':
    main()

