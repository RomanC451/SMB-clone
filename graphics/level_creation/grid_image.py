import cv2

### python script used to grid the maps images of the game


name = r"20597.png"
img = cv2.imread(name)
GRID_SIZE = 16

height, width, channels = img.shape
for x in range(0, width - 1, GRID_SIZE):
    cv2.line(img, (x, 0), (x, height), (255, 0, 0), 1, 1)

for y in range(0, height - 1, GRID_SIZE):
    cv2.line(img, (0, y), (width, y), (255, 0, 0), 1, 1)


cv2.imwrite("1_2_grid.png", img)
