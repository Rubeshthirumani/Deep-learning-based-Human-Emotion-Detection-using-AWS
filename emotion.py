
import boto3
import io
import cv2
import numpy
import imageio
from PIL import Image, ImageDraw, ExifTags, ImageColor

if __name__ == "__main__":
     
    # Change bucket to the S# bucket that contains the image file.
    # Change photo to the image filename. 
    bucket="your_bucket_name"
    photo="the_image.jpg"
    client=boto3.client('rekognition')
    img = cv2.imread("the_image.jpg")
    

    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)
    
    #Call DetectFaces 
    response = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        Attributes=['ALL'])

    imgWidth, imgHeight = image.size  
    draw = ImageDraw.Draw(image)  
                    

    # calculate and display bounding boxes for each detected face       
    print('Detected faces for ' + photo) 
       
    for faceDetail in response['FaceDetails']:
        
            
        d=0
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old is given id =%d'%d)
        a  = max(faceDetail['Emotions'], key=lambda ev: ev['Confidence'])
        print (a['Type'])
        b = (faceDetail['Gender'])
        #print (b['Value'])
        
        box = faceDetail['BoundingBox']
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']
        
                

        L=('Left: ' + '{0:.0f}'.format(left))
        T=('Top: ' + '{0:.0f}'.format(top))
        #print (L)
        #print (T)
        w=('Face Width: ' + "{0:.0f}".format(width))
        h=('Face Height: ' + "{0:.0f}".format(height))
        #print(w)
        #print(h)
        """cv2.putText(im,(a['Type']),(0,20),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)"""

        points = (
            (left,top),
            (left + width, top),
            (left + width, top + height),
            (left , top + height),
            (left, top)

        )
        draw.line(points, fill='#00d500', width=4)

        # Alternatively can draw rectangle. However you can't set line width.
        #draw.rectangle([left,top, left + width, top + height], outline='#00d400')
        #cv2.rectangle(img, (100,100), (100,100),(0,0,255), 2) 
        cv2.putText(img,(a['Type']),(0,20),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        


    #cv2.imshow("img",img)
    image.show("img",img)
    cv2.waitKey(0)
