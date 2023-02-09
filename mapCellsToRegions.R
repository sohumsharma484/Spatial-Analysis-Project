library (spatstat)
library("rlist")

boundarysData = read.csv("sampleOutput.csv")
pointsData = read.csv("detections.csv", sep="\t")


boundaryXVector = c()
boundaryYVector = c()
boundaryXList = list()
boundaryYList = list()
boundaryList = list()
shapeID = 0
polyID = 0
# Must be "Black", "Light Blue", "Blue", "Green", "Pink"
SHAPECOLOR = "Light Blue"

for(i in 1:nrow(boundarysData)) {

  if (boundarysData[i, 5] != SHAPECOLOR)
  {
    next
  }

  if (boundarysData[i, 4] > polyID)
  {
    polyID = polyID + 1
    shapeID = 0
  }


  if (boundarysData[i, 3] > shapeID)
  {
    boundaryXList = append(boundaryXList, boundaryXVector)
    boundaryYList = append(boundaryYList, boundaryYVector)
    # Reverse to avoid negative area
    boundaryList = list.append(boundaryList, list(x=rev(boundaryXVector), y=rev(boundaryYVector)))

    boundaryXVector = c()
    boundaryYVector = c()
    shapeID = shapeID + 1
  }

  
  boundaryXVector = append(boundaryXVector, boundarysData[i, 1])
  boundaryYVector = append(boundaryYVector, boundarysData[i, 2])
}


pointXList = c()
pointYList = c()
for(i in 1:nrow(pointsData)) {       # for-loop over rows
  pointXList = append(pointXList, pointsData[i, 1])
  pointYList = append(pointYList, pointsData[i, 2])
}


boundaryList

pp <- ppp(x=pointXList, y=pointYList, poly=boundaryList)
W <- Window(pp)
pp <- as.ppp(pp)
# reverse y axis to correct polygonal orientation
# Plot boundaries
plot(W, ylim=rev(W$yrange), main=NULL)
# Add cell points
plot(pp, add=T)

