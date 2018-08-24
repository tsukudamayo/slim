import os


_TARGET_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/mov/ingradient/tomato/20180824'

print(os.listdir(_TARGET_DIR))
filepath = os.path.join(_TARGET_DIR, 'movie_name.txt')

# remind movie file name
with open(filepath, 'w') as w:
    for f in os.listdir(_TARGET_DIR):
        if f.find('movie_name.txt') >= 0:
            pass
        w.write(f)
        w.write('\n')
    w.close()
        
for idx, f in enumerate(os.listdir(_TARGET_DIR)):
    filepath = os.path.join(_TARGET_DIR, f)
    if f.find('.txt') >= 0:
        pass
    else:
        padding_number = '{0:06d}'.format(idx)
        modify_name = os.path.join(_TARGET_DIR, str(padding_number)+'.webm')
        os.rename(filepath, modify_name)
