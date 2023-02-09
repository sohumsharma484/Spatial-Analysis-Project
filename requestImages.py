import requests
import shutil
from bs4 import BeautifulSoup
# pip install lxml

tissueSubBlock = "W6-1-1-F.2.02"
# Get ID For Image
getID = requests.get(f"http://api.brain-map.org/api/v2/data/query.xml?criteria=model::SectionDataSet,rma::criteria,specimen[external_specimen_name$eq'{tissueSubBlock}'],treatments[name$eq'ISH'],rma::include,genes,sub_images", stream=True)
if getID.status_code == 200:
    Bs_data = BeautifulSoup(getID.text, "xml")
    ID = Bs_data.find("sub-image").find("id").text

    # Download Image
    img = requests.get(f"http://api.brain-map.org/api/v2/image_download/{ID}?view=tumor_feature_annotation",
                       stream=True)
    if img.status_code == 200:
        with open("image.jpg", 'wb') as f:
            img.raw.decode_content = True
            shutil.copyfileobj(img.raw, f)
    else:
        print(img.status_code)
else:
    print(getID.status_code)

