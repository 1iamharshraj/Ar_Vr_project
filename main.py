import cv2
import numpy as np

# Load your custom marker image
marker_image = cv2.imread(r"C:\Users\eyeha\Desktop\marker.jpg", cv2.IMREAD_GRAYSCALE)

# Create an ORB detector
orb = cv2.ORB_create()

# Compute keypoints and descriptors for the marker image
keypoints_marker, descriptors_marker = orb.detectAndCompute(marker_image, None)

# Initialize the OpenCV camera capture
cap = cv2.VideoCapture(0)

# Create a brute-force matcher for ORB descriptors
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Compute keypoints and descriptors for the current frame
    keypoints_frame, descriptors_frame = orb.detectAndCompute(gray, None)

    # Match descriptors using the BFMatcher
    matches = bf.match(descriptors_marker, descriptors_frame)

    # Sort the matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Set a threshold for marker detection
    threshold = 17  # You may need to adjust this threshold

    if len(matches) > threshold:
        # Calculate the center of the marker
        h, w = marker_image.shape
        cX = w // 2
        cY = h // 2

        # Draw dots at the marker's corners
        for match in matches[:4]:
            x, y = keypoints_frame[match.trainIdx].pt
            x, y = int(x), int(y)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Red dots

        # Draw a rectangle around the detected marker
        top_left = (0, 0)
        bottom_right = (w, h)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # Display the frame with the detected marker and dots
    cv2.imshow('Marker Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()