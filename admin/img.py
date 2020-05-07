

# ## Importing Necessary Modules
# import requests # to get image from the web
# import shutil # to save it locally

# ## Set up the image URL and filename
# image_url = "https://cdn.pixabay.com/photo/2020/02/06/09/39/summer-4823612_960_720.jpg"
# filename = image_url.split("/")[-1]

# # Open the url image, set stream to True, this will return the stream content.
# r = requests.get(image_url, stream = True)

# # Check if the image was retrieved successfully
# if r.status_code == 200:
#     # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
#     r.raw.decode_content = True
    
#     # Open a local file with wb ( write binary ) permission.
#     with open(filename,'wb') as f:
#         shutil.copyfileobj(r.raw, f)
        
#     print('Image sucessfully Downloaded: ',filename)
# else:
#     print('Image Couldn\'t be retreived')

import os.path
from os import path
from PIL import ImageTk, Image

img_path = "/home/maria/Documents/Facultate/Anul4II/IDP/Proiect/client/poze/seriesPictures/highSchoolMusical.jpg"
splitPath = img_path.split(".")
copy_file = splitPath[0] + "_copy_" + str(200) + "." + splitPath[1]
size = 200, 200

if not path.exists(copy_file) :
	img = Image.open(img_path)
	img = img.resize(size, Image.ANTIALIAS)
	img.save(copy_file)