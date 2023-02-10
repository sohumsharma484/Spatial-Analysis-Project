import requests
import shutil
from bs4 import BeautifulSoup
import os
# pip install lxml

def requestImage(tissueSubBlock):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    os.mkdir(f"{tissueSubBlock}")

    # Get ID For Sub Block
    getID = requests.get(
        f"http://api.brain-map.org/api/v2/data/query.xml?criteria=model::SectionDataSet,rma::criteria,specimen[external_specimen_name$eq'{tissueSubBlock}'],treatments[name$eq'ISH'],rma::include,genes,sub_images",
        stream=True)
    if getID.status_code == 200:
        Bs_data = BeautifulSoup(getID.text, "xml")
        images = Bs_data.findAll("section-data-set")
        for image in images:
            gene = image.findNext("acronym").text
            ID = image.find("sub-image").find("id").text
            print(ID)
            print(gene)

            # Download ISH Image
            img = requests.get(f"http://api.brain-map.org/api/v2/image_download/{ID}", stream=True)
            if img.status_code == 200:
                with open(f"{tissueSubBlock}/{tissueSubBlock}_{ID}_{gene}_ISH.jpg", 'wb') as f:
                    img.raw.decode_content = True
                    shutil.copyfileobj(img.raw, f)
            else:
                print(img.status_code)

            # Download corresponding annotated image
            img = requests.get(f"http://api.brain-map.org/api/v2/image_download/{ID}?view=tumor_feature_annotation",
                               stream=True)
            if img.status_code == 200:
                with open(f"{tissueSubBlock}/{tissueSubBlock}_{ID}_{gene}_annotated.jpg", 'wb') as f:
                    img.raw.decode_content = True
                    shutil.copyfileobj(img.raw, f)
            else:
                print(img.status_code)

    return
