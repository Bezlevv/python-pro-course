---
title: Exam: Computer Vision
summary: Final assessment for the "Computer Vision" module.
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: exam, opencv, yolo, video
---

<!--QUIZ-->
In what color order does OpenCV store images?
- BGR
- RGB
- HSV
* Correct answer: BGR
OpenCV reads and stores colors in BGR order, not RGB.

What will cv2.imread return if the file does not exist?
- None
- An empty array
- An exception
* Correct answer: None
imread returns None, so the result is always checked.

What does cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) do?
- Finds the threshold itself and binarizes the image
- Blurs the image
- Finds contours
* Correct answer: Finds the threshold itself and binarizes the image
Otsu's method picks the optimal threshold automatically.

What is morphological opening?
- Erosion, then dilation
- Dilation, then erosion
- Only blurring
* Correct answer: Erosion, then dilation
Opening removes white noise from the background.

What does cv2.findContours return in OpenCV 4?
- Contours and hierarchy
- Only contours
- Contours and image
* Correct answer: Contours and hierarchy
In version 4 the function returns two values.

What is a SIFT descriptor?
- A vector of 128 float32 numbers
- A vector of 32 uint8 bytes
- A point coordinate
* Correct answer: A vector of 128 float32 numbers
SIFT describes a point with a vector of 128 floating-point numbers.

Which function searches for a template in an image?
- cv2.matchTemplate
- cv2.matchFeatures
- cv2.findTemplate
* Correct answer: cv2.matchTemplate
matchTemplate slides the template and returns a similarity map.

What does detectMultiScale of a Haar cascade return?
- A list of rectangles (x, y, w, h)
- A list of descriptors
- Confidence of each pixel
* Correct answer: A list of rectangles (x, y, w, h)
The cascade finds boxes around faces.

How do you load a pretrained YOLO model?
- YOLO("yolov8n.pt")
- cv2.YOLO("yolov8n.pt")
- YOLO.load("yolov8n.pt")
* Correct answer: YOLO("yolov8n.pt")
Ultralytics loads the model through the class constructor.

What does result.boxes.xyxy store?
- Box coordinates (x1, y1, x2, y2)
- Class names
- Confidence percentages
* Correct answer: Box coordinates (x1, y1, x2, y2)
The xyxy format is two opposite corners of the box.
<!--/QUIZ-->
