import qupath.lib.gui.scripting.QP.*;
import qupath.lib.gui.scripting.QPEx.*;
import qupath.lib.gui.scripting.QPEx;


setImageType('BRIGHTFIELD_H_E');
setColorDeconvolutionStains('{"Name" : "H&E default", "Stain 1" : "Hematoxylin", "Values 1" : "0.65111 0.70119 0.29049", "Stain 2" : "Eosin", "Values 2" : "0.2159 0.8012 0.5581", "Background" : " 255 255 255"}');
runPlugin('qupath.imagej.detect.tissue.SimpleTissueDetection2', '{"threshold": 240, "requestedPixelSizeMicrons": 5.0, "minAreaMicrons": 1000000.0, "maxHoleAreaMicrons": 10000000.0, "darkBackground": false, "smoothImage": true, "medianCleanup": true, "dilateBoundaries": false, "smoothCoordinates": true, "excludeOnBoundary": false, "singleAnnotation": true}');
selectAnnotations()



runPlugin('qupath.imagej.detect.cells.WatershedCellDetection', '{"detectionImageBrightfield":"Hematoxylin OD","backgroundByReconstruction":true,"backgroundRadius":15.0,"medianRadius":0.0,"sigma":1.5,"minArea":10.0,"maxArea":1000.0,"threshold":0.1,"maxBackground":2.0,"watershedPostProcess":true,"cellExpansion":0.0,"includeNuclei":true,"smoothBoundaries":false,"makeMeasurements":true}')

saveDetectionMeasurements("C:\\Users\\sohum\\OneDrive\\Documents\\MDAnderson\\detections.csv", "Centroid X px", "Centroid Y px")


//Command: "C:\Users\sohum\Downloads\QuPath-0.4.2-Windows\QuPath-0.4.2\QuPath-0.4.2 (console).exe" script --image=C:\Users\sohum\OneDrive\Documents\MDAnderson\264712751_02_266291108.jpg "C:\Users\sohum\OneDrive\Documents\MDAnderson\detectCells.groovy