import cv2
import numpy as np
import datetime
import threading
import queue

def read_kbd_input(inputQueue):
  print('Press q to quit:')
  while (True):
      # Receive keyboard input from user.
      input_str = input()

      # Enqueue this input string.
      # Note: Lock not required here since we are only calling a single Queue method, not a sequence of them 
      # which would otherwise need to be treated as one atomic operation.
      inputQueue.put(input_str)
 
def main():
  # Create a VideoCapture object
  cap = cv2.VideoCapture(0)
  
  # Check if camera opened successfully
  if (cap.isOpened() == False):
    print("Unable to read camera feed")
  
  # Default resolutions of the frame are obtained.The default resolutions are system dependent.
  # We convert the resolutions from float to integer.
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))

  # Get current datetime and compose output video file name.
  dt = datetime.datetime.now()
  output_file = f"{dt.year}-{dt.month}-{dt.day}_{dt.hour}:{dt.minute}:{dt.second}.avi"
  
  # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
  out = cv2.VideoWriter(output_file,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

  # Keyboard input queue to pass data from the thread reading the keyboard inputs to the main thread.
  inputQueue = queue.Queue()

  # Create & start a thread to read keyboard inputs.
  # Set daemon to True to auto-kill this thread when all other non-daemonic threads are exited. This is desired since
  # this thread has no cleanup to do, which would otherwise require a more graceful approach to clean up then exit.
  inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
  inputThread.start()

  terminated = False # Sets initial condition on while loop

  while not terminated:
    ret, frame = cap.read()
  
    if ret == True: 
      
      # Write the frame into the file
      out.write(frame)
  
      # # Display the resulting frame
      # cv2.imshow('frame',frame)
  
      # # Press Q on keyboard to stop recording
      # if cv2.waitKey(1) & 0xFF == ord('q'):
      #   break

    # Break the loop
    else:
      terminated = True

    # if the keyboard input has been entered, check input
    if inputQueue.qsize() > 0:
      input_str = inputQueue.get()

      # If user entered a q, quit the program
      if input_str == "q":
        terminated = True
  
  # When everything done, release the video capture and video write objects
  cap.release()
  out.release()
  
  # # Closes all the frames
  # cv2.destroyAllWindows()

if __name__ == "__main__":
  main()