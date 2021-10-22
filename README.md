# CS50 Final Project - Sudoku solver 4x4

My final project is an application that solves 4x4 sudokus using OCR (optical character recognition) and backtracking.  I have always enjoyed solving sudoku puzzles and wanted to create an app that does just that. 

### Technologies used:
* Flask
* HTML
* CSS
* Python
* cv2
* easyOCR

### Usage
1. User uploads the image of a 4x4 sudoku that has outside borders by clicking **Upload**.
2. The uploaded image is displayed on the left of the page while the numbers detected are displayed in the center.
3. In case some numbers were incorrectly detected or not at all, the user has the option of manually correcting those manually.
4. Clicking **Solve** will run the backtracking algorithm that fills the puzzle.
5. Finally the solved puzzle and the **Again** button are displayed. Clicking the button will clear the session and take the user back to the initial page.

### Upload
The initial step is uploading an image on the **`index.html`** page. The form takes only files with the following extensions: png, jpg, jpeg or gif. I used the code from the Uploading Files section of [Flask’s documentation](https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/).  If the extension is valid 3 session variables are created:
- ```raw_sudoku``` that contains the puzzle as a list with empty cells indicated as 0s
- ```display_raw_sudoku``` that contains the puzzle as a list with empty cells as whitespace
- ```sudoku_location``` stores the path of the image

### Sudoku detection
Once we have the image we need to find the puzzle so we can extract the numbers. The assumption is that the object with the largest area on the image is the puzzle. To find the objects (contours) on the image I use OpenCV’s findContours function. But before doing that the image needs to be cleaned. I use the standard image processing steps (grayscale, blur, adaptive thresholding, invert colors) to prepare the image for contour detection.  From the list of contours the one with the largest area is selected and its coordinates, height and width are saved. 

### Number detection
Ideally a sudoku puzzle has the same height and weight. Unfortunately that’s not always the case. With the assumption that the puzzle is at least rectangular, the part of the image defined above (the puzzle) is cut into 16 identically sized, smaller images (cells). On these cells I perform contour detection again, but looking strictly around the center of the cell to find the numbers. The assumption here is that the digit will be at the center of the cell. If there aren’t any contours, that means the cell is empty. In case there is a contour, I use easyOCR to identify the numbers. The output is written into raw_sudoku and display_raw_sudoku.

### Editing numbers
While easyOCR is doing a great job most of the time, I encountered several images in which the number one (1) was not recognized. I circumvented this issue with allowing the users to edit the detected puzzle. The puzzle in **`check.html`** is a grid with cells containing text inputs. Only a single digit is allowed from 1 to 4. Any changes in the grid is reflected in the raw_sudoku and display_raw_sudoku variables.

### Solver algorithm
Rules of solving a sudoku are the following: a number should appear only once in any column, only once in any row and only once in any of the smaller squares. The solver algorithm looks for the first empty cell and fills it with the number one (1). Then it checks if the number is correct by validating the 3 conditions above. If any of the conditions aren’t met, the number is increased by 1. This process is repeated until a suitable number is found, and repeated on the next empty cell. In case all the options are exhausted (if the number 4 is reached and rejected), the algorithm goes back to the previous non-prefilled cell and restarts the iteration. This is called [backtracking](https://en.wikipedia.org/wiki/Backtracking). Once backtracking is called on the last cell - which means the puzzle is unsolvable - the function returns the original puzzle and prompts the user for restarting the process.


### Improvement ideas
I chose to limit the scope of my project to keep my sanity. If I had more time I would work on the following:
* Scale to a full 9x9 puzzle.
* Improve sudoku detection. Current implementation needs a clearly visible border.
* Improve number detection. In some cases the number 1 is not found.
* Support pictures taken in low light conditions or at an angle.
* Support real-time puzzle solving using cameras. 
