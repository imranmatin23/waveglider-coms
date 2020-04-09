import cv2
import os

IMG_DIR = "images"

# read image from computer
img = cv2.imread(os.path.join(IMG_DIR,"temp.png"))
print(img.shape)

# encode into bytes and write to disk
# specify path to External Hard Drive
result, encoded_img = cv2.imencode(".png", img)
encoded_img.tofile(os.path.join(IMG_DIR, "img1.png"))
print(encoded_img.shape)

# decode bytes and write to disk
decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_UNCHANGED)
cv2.imwrite(os.path.join(IMG_DIR, "img1.png"),decoded_img)
print(decoded_img.shape)