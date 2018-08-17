import sys 
import time

for i in range(10):
    s = str(i)*(10-i)
    sys.stdout.write('\033[2K\033[G%s' % s)
    sys.stdout.flush()
    time.sleep(0.5)
print()
