# Spatial-Analysis-Project

This program takes a sub block from the ISH database of the Ivy Glioblastoma Atlas Project and loads the different regions into the R library spatstat. It  downloads the images using the API, detects the different boundaries within the images, detects the cells within the images, and finally saves the result in a spatstat ppp object in a seperate .Rdata file for each gene. 

To run the program follow these steps (Note: the application has only been tested for Windows devices)
Installation:
  1. Download this GitHub repository
  2. Download QuPath
     https://github.com/qupath/qupath/releases/tag/v0.4.3
     Make sure to download the .zip version and extract the contents
  3. Run the following commands in the command prompt (or any terminal) in the same directory as this repository to install the necessary dependencies
     pip install -r requirements.txt
     pip install lxml
  4. Download R
     https://cran.r-project.org/bin/windows/base/
  5. Run the following R commands
     install.packages("spatstat")
     install.packages("rlist")

Running the application:
1. Update the tissueSubBlock, QuPathAbsPath, RscriptAbsPath, and currentDirectory variables in the top of the main.py file to the desired values.
2. Run the main.py file. Make sure to run main.py in the same working directory as the repository
