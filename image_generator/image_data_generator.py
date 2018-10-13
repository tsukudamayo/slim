import os

import numpy as np
from PIL import Image

from tensorflow.contrib.keras.api.keras.preprocessing import image


# define filepath
_NUM_GENERATE = 10
_CATEGORY = 'bara'
_ORG_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/cooking_kurashiru_20181005'
_DST_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/cooking_kurashiru_20181005_x_10'


# ImageDatagenerator
datagen = image.ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.05,
    height_shift_range=0.05,
    shear_range=0,                    # default: 0.2
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',                # default: nearest
    samplewise_center=False,            # default: False
    samplewise_std_normalization=False, # default: False
    zca_whitening=False,                # default: False
)

# # when using featurewise_center, zca_whitening it needs that ndarray fit
# x_train = np.empty((256,256,3))
# x_train = np.expand_dims(x_train, axis=0)
# for f in filenames:
#     tmp = Image.open(os.path.join(_ORG_DIR, f))
#     tmp = np.expand_dims(tmp, axis=0)
#     print('tmp.shape', tmp.shape)
#     print('x_train.shape', x_train.shape)
#     x_train = np.concatenate((x_train, tmp), axis=0)


# x_train /= 255.0
# datagen.fit(x_train)

# define filepath
if os.path.exists(_DST_DIR) is False:
    os.mkdir(_DST_DIR)

category_directories = os.listdir(_ORG_DIR)
for category_dir in category_directories:
    print('category_dir', category_dir)
    org_dir = os.path.join(_ORG_DIR, category_dir)
    dst_dir = os.path.join(_DST_DIR, category_dir)
    print('org_dir', dst_dir)
    if os.path.exists(dst_dir) is False:
        os.mkdir(dst_dir)

    filenames = os.listdir(org_dir)

    # generate random image
    for f in filenames:
        print(f)
        img_path = os.path.join(org_dir, f)
        img = image.load_img(img_path, target_size=(256, 256))
        
        x = image.img_to_array(img)
        x = x.reshape((1,) + x.shape)
    
        # generate image data
        i = 0
        for batch in datagen.flow(x, batch_size=1):
            i += 1
    
            # gen_image is PIL.Image class object
            gen_image = image.array_to_img(batch[0])
    
            # specify filename and filepath
            fname, ext = os.path.splitext(f)
            padding_number = '{0:02d}'.format(i)
            generate_filename = '{0}_{1}{2}'.format(fname, padding_number, ext)
            
            gen_image.save(os.path.join(dst_dir, generate_filename))
    
            # generate number of file that specified by _NUM_GENERATE
            if i % _NUM_GENERATE == 0:
                break
