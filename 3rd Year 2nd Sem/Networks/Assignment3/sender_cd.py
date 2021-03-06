import common as co
import time
import socket
import random
import time
import threading
import sys

if(len(sys.argv)<2):
	print('Error... usage python3 sender_cd.py input_file')
	sys.exit();
filename=sys.argv[1]


isBusyChannel=0
sockSend=co.createConn(co.portSenderReceive)	# Socket to send data to channel

time.sleep(1)
sockSignal=co.createConn(co.portSenderSignal)	# Socket to send data to channel

print('Connected to channel')

probab=10
p=6
timeSlot=2
kmax=15
# Function to send frames
def send_frame(list_of_frames):

	i=0
	k=0
	while(True):
		# Sense the channel and check if flag is 1 then dont send
		if(isBusyChannel==0): # Channel is free
			# Send the frame with a probability p
			pr=random.randint(0,probab)
			if(pr<=p):
				# Send the frame
				print('Sending frame '+str(i))
				co.send_frame(list_of_frames[i], sockSend)
				
				# Wait for signal whether transmission successfull or collision
				isCollision=sockSend.recv(1024).decode()
				if(isCollision=='0'): # No collision successfull transmission
					print('Sent successfully')
					if(list_of_frames[i]!='#'):
						i=i+1
						k=0

				else:
					# If collision detected
					print('Frame collision detected..resending')
					k=k+1
					# If max number of attempts exceeded
					if(k>kmax):
						print('Max attempts for resending exceeded discarding frame')
						i=i+1
						k=0
						continue
					r=random.randint(0,2**k-1)
					waitTime=r*timeSlot	
					time.sleep(waitTime)

				time.sleep(3)

			else:
				print('Waiting '+str(timeSlot))
				time.sleep(timeSlot)
				continue

		else: # Channel is busy
			print('Channel busy')
			time.sleep(2)
			continue



# Function to sense the medium
def sense_medium():
	global isBusyChannel

	while(True):
		if(sockSignal.recv(1024).decode()=='1'):
			# Means channel is busy
			isBusyChannel=1
		else:
			# Means channel is not busy
			isBusyChannel=0

list_of_frames=co.readfile(filename, co.frame_size)
list_of_frames.append('#')

sendThread=threading.Thread(target=send_frame, args=(list_of_frames,)) # create the sending thread
senseThread=threading.Thread(target=sense_medium) # create the sending thread

sendThread.start()
senseThread.start()

sendThread.join()
sendThread.join()