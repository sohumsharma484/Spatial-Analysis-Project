import qupath.lib.gui.scripting.QP.*;
import qupath.lib.gui.scripting.QPEx.*;


setImageType('BRIGHTFIELD_H_E');
setColorDeconvolutionStains('{"Name" : "H&E default", "Stain 1" : "Hematoxylin", "Values 1" : "0.65111 0.70119 0.29049", "Stain 2" : "Eosin", "Values 2" : "0.2159 0.8012 0.5581", "Background" : " 255 255 255"}');
createFullImageAnnotation(true)

//For downloaded H&E image
//runPlugin('qupath.imagej.detect.cells.WatershedCellDetection', '{"detectionImageBrightfield":"Hematoxylin OD","backgroundByReconstruction":true,"backgroundRadius":15.0,"medianRadius":0.0,"sigma":1.5,"minArea":10.0,"maxArea":1000.0,"threshold":0.1,"maxBackground":2.0,"watershedPostProcess":true,"cellExpansion":0.0,"includeNuclei":true,"smoothBoundaries":false,"makeMeasurements":true}')

//For downloaded ISH image
runPlugin('qupath.imagej.detect.cells.WatershedCellDetection', '{"detectionImageBrightfield":"Optical density sum","backgroundByReconstruction":true,"backgroundRadius":15.0,"medianRadius":0.0,"sigma":1.5,"minArea":10.0,"maxArea":1000.0,"threshold":0.1,"maxBackground":2.0,"watershedPostProcess":true,"cellExpansion":0.0,"includeNuclei":true,"smoothBoundaries":false,"makeMeasurements":true}')

String path = getCurrentImageData().getServer().getPath()
path = path.substring(29,path.length() - 17) + "_detections.csv"
saveDetectionMeasurements(path, "Centroid X px", "Centroid Y px")
