import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam gagal dibuka")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Tidak bisa membaca frame")
        break

    cv2.imshow("Webcam Test", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()