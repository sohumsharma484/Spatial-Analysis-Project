from requestImages import requestImage
from detectBoundaries import detectBoundaries
import os
from threading import Thread

# Variables
tissueSubBlock = "W31-1-1-E.01"
QuPathAbsPath = r"C:\Users\sohum\Downloads\QuPath-0.4.2-Windows\QuPath-0.4.2\QuPath-0.4.2 (console).exe"
RscriptAbsPath = r'C:\"Program Files"\R\R-4.2.2\bin\Rscript.exe'
currentDirectory = r"C:\Users\sohum\OneDrive\Documents\MDAnderson"


# Download images
requestImage(tissueSubBlock)

# Detect boundaries for images
threads = []
for file in os.listdir(tissueSubBlock):
    filename = os.fsdecode(file)
    if "annotated.jpg" in filename:
        imagePath = os.path.join(tissueSubBlock, filename)
        detectBoundaries(imagePath)
        t = Thread(target=detectBoundaries, args=(imagePath,))
        threads.append(t)

# Start all threads
for x in threads:
    x.start()

# Wait for all of them to finish
for x in threads:
    x.join()
    
print("boundary detection complete")

# Detect Cells
for file in os.listdir(tissueSubBlock):
    filename = os.fsdecode(file)
    if "ISH" in filename:
        imagePath = os.path.join(tissueSubBlock, filename)
        os.system(f'cmd /c ""{QuPathAbsPath}" script --image={os.path.abspath(imagePath)} "{os.path.abspath("detectCells.groovy")}"')

# Load into Spatstat
def runR(command):
    os.system(command)
    print(command)

for file in os.listdir(tissueSubBlock):
    filename = os.fsdecode(file)
    if "boundaries" in filename:
        parts = filename.split("_")

        command = rf'cmd /c {RscriptAbsPath} "{currentDirectory}\mapCellsToRegions.R" "{currentDirectory}\{tissueSubBlock}\{filename}" "{currentDirectory}\{tissueSubBlock}\{parts[0]}_{parts[1]}_{parts[2]}_ISH_detections.csv" "{currentDirectory}\{tissueSubBlock}\{parts[0]}_{parts[1]}_{parts[2]}.Rdata"'

        thread = Thread(target=runR, args=(command,))
        thread.start()
