import cv2
import numpy as np
import pandas as pd
import sqlite3 as sl

IMAGEPATH = ""
image = cv2.imread(IMAGEPATH)
original = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

con = sl.connect('system.db')
# Create coordinate database
studentList = pd.DataFrame({
    'x': [],
    'y': [],
    'shapeID': [],
    'colorNum': [],
    'color': [],
})
studentList.to_sql("coordinates", con, index= False)

# Retrieve database values
c = con.cursor()
c.execute('''
          SELECT
          *
          FROM coordinates
          ''')
coordinatesDb = pd.DataFrame(c.fetchall(), columns=['x', 'y', 'shapeID', 'colorNum', 'classification'])


colorOptions = [
    ["Black", np.array([0, 0, 0], dtype="uint8"), np.array([10, 10, 10], dtype="uint8")],
    ["Light Blue", np.array([96, 100, 210], dtype="uint8"), np.array([127, 255, 255], dtype="uint8")],
    ["Blue", np.array([90, 100, 20], dtype="uint8"), np.array([95, 255, 200], dtype="uint8")],
    ["Green", np.array([40, 100, 20], dtype="uint8"), np.array([80, 255, 255], dtype="uint8")],
    ["Pink", np.array([140, 100, 20], dtype="uint8"), np.array([160, 255, 255], dtype="uint8")],
    ['Red', np.array([0, 50, 20], dtype="uint8"), np.array([12, 255, 255], dtype="uint8")]
]

colorNum = 0
codes = []
for colorOption in colorOptions:
    mask = cv2.inRange(image, colorOption[1], colorOption[2])
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    polyNum = 0

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.00009 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if area < 1000 or area > 200000000:
            continue

        # Used to flatten the array containing the co-ordinates of the vertices.
        n = approx.ravel()

        i = 0
        for j in n:
            if (i % 2 == 0):
                x = n[i]
                y = n[i + 1]
                row = {"x": x, "y": y, "shapeID": int(polyNum), "colorNum": int(colorNum), "color": colorOption[0]}
                coordinatesDb = coordinatesDb.append(row, ignore_index=True)
            i += 1

        polyNum += 1

    colorNum += 1

coordinatesDb.to_csv("output.csv", index=False)
coordinatesDb.to_sql('coordinates', con, index=False, if_exists='replace')
