import cv2
import numpy as np
import pandas as pd


def detectBoundaries(imagePath):
    image = cv2.imread(imagePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    coordinatesList = []


    colorOptions = [
        ["Infiltrating Tumor", np.array([148, 100, 20], dtype="uint8"), np.array([152, 255, 255], dtype="uint8")],
        ["Perinecrotic zone", np.array([96, 100, 210], dtype="uint8"), np.array([98, 255, 255], dtype="uint8")],
        ["Leading Edge", np.array([94, 100, 20], dtype="uint8"), np.array([95, 255, 200], dtype="uint8")],
        ["Pseudopalisading cells but no visible necrosis", np.array([103, 100, 20], dtype="uint8"), np.array([135, 255, 255], dtype="uint8")],
        ["Cellular Tumor", np.array([60, 100, 20], dtype="uint8"), np.array([62, 255, 255], dtype="uint8")],
        ['Necrosis', np.array([0, 0, 0], dtype="uint8"), np.array([10, 10, 10], dtype="uint8")],
        ['Microvascular proliferation', np.array([4, 50, 20], dtype="uint8"), np.array([6, 255, 255], dtype="uint8")],
        ['Hyperplastic blood vessels', np.array([11, 50, 20], dtype="uint8"), np.array([12, 255, 255], dtype="uint8")],
        ['Pseudopalisading cells around necrosis', np.array([83, 50, 20], dtype="uint8"), np.array([85, 255, 255], dtype="uint8")]
    ]

    for colorOption in colorOptions:
        mask = cv2.inRange(image, colorOption[1], colorOption[2])
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        polyNum = 0

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.00009 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)

            if area < 1000:
                continue

            # Used to flatten the array containing the co-ordinates of the vertices.
            n = approx.ravel()

            i = 0
            for j in n:
                if (i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]
                    coordinatesList.append([x, y, polyNum, colorOption[0]])
                i += 1

            polyNum += 1
        cv2.imwrite("mask.jpg", mask)

    df = pd.DataFrame(coordinatesList, columns=["x", "y", "shapeID", "region"])
    df.to_csv(f"{imagePath[:-4]}_boundaries.csv", index=False)
