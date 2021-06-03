from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# Create your views here.
from keras.models import load_model  # use to load model 
from keras.preprocessing import image # image processing tool
import tensorflow as tf
import json,os
from tensorflow import Graph, Session
import numpy as np


img_height, img_width=224,224
with open('./models/imagenet_classes.json','r') as f:
    labelInfo=f.read()

labelInfo=json.loads(labelInfo)


model_graph = Graph()
with model_graph.as_default():
    tf_session = Session()
    with tf_session.as_default():
        model=load_model('./models/MobileNetModelImagenet.h5')



def home(request):
    return render(request,'home.html')
def predictImage(request):
    print(request)
    print(request.POST.dict())
    print("*******************")
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName = fs.url(filePathName)
    
    testimage='.'+filePathName
    #loading the image
    img = image.load_img(testimage, target_size=(img_height, img_width))
    #converting it into array
    x = image.img_to_array(img)
    #Normalizing it
    x=x/255
    #reshape the array
    x=x.reshape(1,img_height, img_width,3)
    with model_graph.as_default():
        with tf_session.as_default():
            predi=model.predict(x)

    predictedLabel=labelInfo[str(np.argmax(predi[0]))]

    context={'filePathName':filePathName, 'predictedLabel':predictedLabel}
    return render(request,'home.html',context)

def viewDataBase(request):
    listOfImages = os.listdir('./media/')
    listOfImagesPath = ['./media/'+i for i in listOfImages]
    context = {'listOfImagesPath':listOfImagesPath}
    return render(request,'viewDB.html',context)