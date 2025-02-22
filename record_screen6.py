import cv2
import numpy as np
import mss
import os

# Create a folder to save frames
os.makedirs("planetA", exist_ok=True)

# Define video settings
fps = 10  # Adjust frame rate if needed
frame_count = 0
saved_frame_count = 0 

# Define the recording area (214x214 pixels from the top-left corner)
#monitor = {"top": 159, "left": 47, "width": 214, "height": 214}
monitor = {"top": 158, "left": 46, "width": 61, "height": 61}

# Define circle mask parameters
center_x, center_y = monitor['width'] // 2, monitor['height'] // 2
diameter = 59
radius = diameter // 2

# Create the mask with EXACT same dimensions as the frame (214x214)
mask = np.zeros((monitor['height'], monitor['width']), dtype=np.uint8)
cv2.circle(mask, (center_x, center_y), radius, 255, -1)

print("Recording screen (51x51)... Press 'q' to stop.")

with mss.mss() as sct:
    while True:
        # Capture screen
        screenshot = sct.grab(monitor)
        
        # Convert screenshot to numpy array and remove alpha channel
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        # Double-check frame and mask sizes
        if frame.shape[:2] != mask.shape[:2]:
            mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
        
        # Apply the mask correctly
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Create alpha channel from the mask
        b, g, r = cv2.split(masked_frame)
        alpha = mask  # Use mask directly as alpha channel
        
        # Merge channels to create final transparent image
        final_frame = cv2.merge([b, g, r, alpha])
        
        # Save every 10th frame as PNG with transparency
        if frame_count % 1 == 0:
            filename = f"planetA/planetA_{saved_frame_count}.png"
            cv2.imwrite(filename, final_frame)
            saved_frame_count += 1
        
        frame_count += 1
        
        # Display recording preview (optional)
        # cv2.imshow("Recording", final_frame)
        
        # Stop recording if 'q' is pressed
        if cv2.waitKey(1000 // fps) & 0xFF == ord('q'):
            break

# Close OpenCV windows
cv2.destroyAllWindows()
print(f"Recording complete. Frames saved in 'frames' folder.")