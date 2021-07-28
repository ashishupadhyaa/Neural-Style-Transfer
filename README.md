# Neural Style Transfer

The project is to convert an image style with the other image's style. The content image uses other style image to change the style of the content image. I used *Tensorflow* to read the image from the input which is taken from the flask app. The model was a pretrained model available on *tensorflow-hub*.

The Flask webapp was containarized using **docker** with **nginx**. The client connects with the **nginx** that connects with the development pupose server **gunicorn** which ultimatly connects to the flask app. This whole system is containerized using **docker**. To connect the **nginx** with **flask**, I used docker-compose with **nginx configuration**. You can run the docker-container by running following line in CLI (For Ubuntu):
```
sudo docker-compose up
```

The nginx client connect to the port 80 which connect to the gunicorn at port 8000. The flask app runs on the ***localhost*** server. The flask app's home page looks like the following:
![home page](/Images/image3.png)

You can choose the content and style images in the home page. The file which don't have extension of an image (.jpg, .jpeg, .png) is not accepted by the page and it will return to the homepage if you do so. After submmitting the images you will find the page as follows:
![style image page](/Images/image1.png)

And the other example is as follows:
![Style image lion/tiger](/Images/image2.png)

From ***Download*** button you can download the *styled image* easily in your local storage.

**- The End
