library (spatstat)
library("rlist")


options(echo=TRUE)
args <- commandArgs(trailingOnly = TRUE)
boundaryDataPath = args[1]
pointsDataPath = args[2]
destinationRdataPath = args[3]


boundarysData = read.csv(boundaryDataPath)
pointsData = read.csv(pointsDataPath, sep="\t")


pointXList = pointsData[ , "Centroid.X.px"]
pointYList = pointsData[ , "Centroid.Y.px"]


pointPatterns = list()
regions = c("Infiltrating Tumor", "Perinecrotic zone", "Leading Edge", "Pseudopalisading cells but no visible necrosis", "Cellular Tumor", "Necrosis", "Microvascular proliferation", "Hyperplastic blood vessels", "Pseudopalisading cells around necrosis")
for (region in regions) {
  shapeID = 0
  boundaryXVector <<- c()
  boundaryYVector <<- c()
  boundaryList <<- list()
  for(i in 1:nrow(boundarysData)) {
    
    if (boundarysData[i, 4] != region)
    {
      next
    }
    
    if (boundarysData[i, 3] > shapeID)
    {
      if (length(boundaryXVector) > 2) {
        # Reverse to avoid negative area
        boundaryList <<- list.append(boundaryList, list(x=rev(boundaryXVector), y=rev(boundaryYVector)))
        
      }

      boundaryXVector <<- c()
      boundaryYVector <<- c()
      shapeID = shapeID + 1
    }
    
    boundaryXVector <<- append(boundaryXVector, boundarysData[i, 1])
    boundaryYVector <<- append(boundaryYVector, boundarysData[i, 2])
  }
  
  if (length(boundaryXVector) < 3 && length(boundaryList) == 0){
    next
  }

  if (length(boundaryXVector) > 2) {
    # Reverse to avoid negative area
    boundaryList <<- list.append(boundaryList, list(x=rev(boundaryXVector), y=rev(boundaryYVector)))
  }
  
  tryCatch(
    #try to do this
    {
      pp <- ppp(x=pointXList, y=pointYList, poly=boundaryList)
      marks(pp) <- rep(region, npoints(pp))
      pp <- as.ppp(pp)
      pointPatterns = append(pointPatterns, list(pp))
    },
    error=function(e) 
    {
      print(e)
    }
  )
}


save(pointPatterns, file=destinationRdataPath, compress=F)
