import os
import argparse


def main(target_dir):
    print(os.listdir(target_dir))
    filepath = os.path.join(target_dir, 'movie_name.txt')
    
    # remind movie file name as txt file
    with open(filepath, 'w') as w:
        for f in os.listdir(target_dir):
            if f.find('movie_name.txt') >= 0:
                pass
            w.write(f)
            w.write('\n')
        w.close()

    # rename filename to "idnumber.webm"
    for idx, f in enumerate(os.listdir(target_dir)):
        filepath = os.path.join(target_dir, f)
        if f.find('.txt') >= 0:
            pass
        else:
            padding_number = '{0:06d}'.format(idx)
            modify_name = os.path.join(
                target_dir, str(padding_number)+'.webm'
            )
            os.rename(filepath, modify_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_dir',
                        dest='target_dir',
                        type=str,
                        default=None,
                        help='please enter the filepath which exist movie')
    argv = parser.parse_args()
    
    main(argv.target_dir)
