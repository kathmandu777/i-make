import cv2

png_image = cv2.imread("i-make/static/facepaints/custom/glitter/glitterL.png")
png_image_second = cv2.imread("i-make/static/facepaints/custom/eye-shadow/eye-shadow0-0.png", -1)
black_make = cv2.imread("i-make/static/facepaints/black_png.png")
white_make = cv2.imread("i-make/static/facepaints/white_png.png")
kirakira_make = cv2.imread("i-make/static/facepaints/kirakira_png.png")

blend = cv2.addWeighted(src1=black_make, alpha=1.0, src2=kirakira_make, beta=1.0, gamma=0)
cv2.imshow("demo", blend)
cv2.waitKey(0)
cv2.destroyAllWindows()
