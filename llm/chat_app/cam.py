import cv2

def main():
    # 1. Initialize the webcam (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit the video window.")

    while True:
        # 2. Capture frame-by-frame
        try:
            ret, frame = cap.read()

            # If frame is read correctly, ret is True
            if not ret:
                print("Error: Can't receive frame.")
                break

            # 3. Display the resulting frame
            cv2.imshow('Webcam Feed', frame)

            # 4. Wait for the 'q' key to be pressed to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(e)
    # 5. When everything done, release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()