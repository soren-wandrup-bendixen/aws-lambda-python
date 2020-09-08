import time
import os

print('Task starting..')
time.sleep(5)
print(os.environ['Command'])
print('Task ended, took 5 seconds') 


if __name__ == '__main__':
	print('in main')
else:	
	print('not in main')

