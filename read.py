import cv2
import easyocr
from matplotlib import pyplot as plt
import numpy as np

def read(img_path):

    # Load image
    #img_path = '/Users/4ndr45/PycharmProjects/pythonProject/sudoku2.jpg'

    # Read image
    img = cv2.imread(img_path)

    # Create a copy
    img_original2 = cv2.imread(img_path)

    # Convert image to gray before blurring
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur image
    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)

    # Perform adaptive thresholding
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    # Invert colors to help OCR
    inverted = cv2.subtract(255, thresh)

    # Create contours to find Sudoku
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find puzzle based on area
    max_area = 0
    c = 0
    area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000:
            if area > max_area:
                max_area = area
                x, y, w, h = cv2.boundingRect(i)
                best_cnt = i
                image = cv2.drawContours(img, contours, c, (0, 255, 0), 3)
        c += 1

    # Load easy ocr reader
    reader = easyocr.Reader(['en'], gpu=False)

    # Break sudoku down into blocks

    # Create a list for storing cell coordinates
    cells = []

    # Create a list for storing the sudoku
    sudoku = []

    # Create a list for storing the sudoku without 0s
    sudoku_display = []

    # Estimate height of a single cell
    height = h / 4

    # Estimate width of a single cell
    width = w / 4

    # Iterate over all columns
    for j in range(4):

        # Create a list for a single row's coordinates
        to_append = []

        # Create a list for a single row's numbers
        sudoku_row = []

        # Create a list for a single row's numbers without 0s
        sudoku_row_display = []

        # Iterate over all rows
        for k in range(4):

            # Calculate coordinates for a single cell
            top = int(y + j * height)
            left = int(x + k * width)
            bottom = int(top + height)
            right = int(left + width)

            # Add coordinates for a single cell
            to_append.append([left, top, right, bottom])

            # Create an image of a single cell with inverted colors
            rectangle = inverted[top:bottom, left:right]

            # Create an image of a single cell with thresholding applied
            original_thresh = thresh[top:bottom, left:right]

            # Calculate the centroid of a single cell
            M = cv2.moments(rectangle)
            block_x = int(M["m10"] / M["m00"])
            block_y = int(M["m01"] / M["m00"])

            # Find the contours in a single cell
            contours, _ = cv2.findContours(rectangle, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Loop through contours and find the one that should contain a number
            c = 0
            for i in contours:
                x2, y2, w2, h2 = cv2.boundingRect(i)
                if (height * width) / 2 > cv2.contourArea(i) > 100 and cv2.pointPolygonTest(i, (block_x, block_y),
                                                                                            True) >= -15:
                    cv2.rectangle(rectangle, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 1)
                    break
                c += 1

            # Try to slice the image using the contour
            try:
                cropped = original_thresh[y2:y2+h2,x2:x2+w2]

            # If slicing is not possible, the cell is empty
            except:
                cropped = original_thresh
            # Read the number
            result = reader.readtext(cropped, allowlist="1234")

            # Add number to row
            if len(result) == 0:
                sudoku_row.append(0)
                # No zeros path
                sudoku_row_display.append(' ')

            else:
                sudoku_row.append(int(result[0][1]))
                # No zeros path
                sudoku_row_display.append(result[0][1])

        # Add row to sudoku list
        sudoku.append(sudoku_row)

        sudoku_display.append(sudoku_row_display)

    # Create a list for returning values
    sudoku_list = [sudoku, sudoku_display]

    return sudoku_list
    # Print sudoku
    for i in range(4):
        print(sudoku_list[0][i])

            #cv2.imshow(text, img_original[top:bottom,left:right])
        #cells.append(to_append)
    #rint(cells)
    #print("Width: %s Height: %s X: %s Y: %s" % (w, h, x, y))


