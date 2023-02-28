import requests
import shutil
from bs4 import BeautifulSoup
import os
import threading
from PIL import Image
# pip install lxml

def downloadImage(gene, ID, tissueSubBlock):
    # Download ISH Image
    img = requests.get(f"http://api.brain-map.org/api/v2/image_download/{ID}", stream=True)
    Image.MAX_IMAGE_PIXELS = 971441920
    try:
        if img.status_code == 200:
            with open(f"{tissueSubBlock}/{tissueSubBlock}_{ID}_{gene}_ISH.jpg", 'wb') as f:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw, f)
            try:
                i = Image.open(f"{tissueSubBlock}/{tissueSubBlock}_{ID}_{gene}_ISH.jpg")
            except:
                print(f"{tissueSubBlock}/{tissueSubBlock}_{ID}_{gene}_ISH.jpg")
                downloadImage(gene, ID, tissueSubBlock)

        else:
            print(img.status_code)
    except Exception as e:
        print(e)

    # Download corresponding annotated image
    img = requests.get(f"http://api.brain-map.org/api/v2/image_download/{ID}?view=tumor_feature_annotation", stream=True)
    try:
        if img.status_code == 200:
            with open(f"{tissueSubBlock}/{tissueSubBlock}_{ID}_{gene}_annotated.jpg", 'wb') as f:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw, f)
            try:
                i = Image.open(f"{tissueSubBlock}/{tissueSubBlock}_{ID}_{gene}_annotated.jpg")
            except:
                print(f"{tissueSubBlock}/{tissueSubBlock}_{ID}_{gene}_annotated.jpg")
                downloadImage(gene, ID, tissueSubBlock)
        else:
            print(img.status_code)
    except Exception as e:
        print(e)

    print(gene)



def requestImage(tissueSubBlock):
    try:
        os.mkdir(f"{tissueSubBlock}")
    except:
        print("sub block directory already exists")
        return

    # Get ID For Sub Block
    getID = requests.get(f"http://api.brain-map.org/api/v2/data/query.xml?criteria=model::SectionDataSet,rma::criteria,specimen[external_specimen_name$eq'{tissueSubBlock}'],treatments[name$eq'ISH'],rma::include,genes,sub_images", stream=True)

    if getID.status_code == 200:
        Bs_data = BeautifulSoup(getID.text, "xml")
        images = Bs_data.findAll("section-data-set")
        threads = []

        for image in images:
            try:
                gene = image.findNext("acronym").text
                print(gene)
                ID = image.find("sub-image").find("id").text
                t = threading.Thread(target=downloadImage, args=(gene, ID, tissueSubBlock))
                threads.append(t)
            except:
                pass

        # Start all threads
        for x in threads:
            x.start()

        # Wait for all of them to finish
        for x in threads:
            x.join()
