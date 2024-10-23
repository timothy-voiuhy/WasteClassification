## Waste Classification 
This is a simple project we worked on i, and Mutawe Enock a friend of mine just as a fast submission for one of the competitions at Makerere University. And as the word says fast, it is not really up to standard.

## Working Mechanism of the design elements
So in the project we are using a small attached to a raspberry pi dev board and we are able to classify the different kinds of waste (so far : plastic, metal, organic) and then by the result of the classification model we are able to control the motor to rorate the holding container and then, after stoping at the right the degres and electromagnet is activated which then pushes a rod which makes the holding container to pour its contents into the right bin.

## How it works
At first we were trying to implement the semantic segmentation model from from scratch in this [file](https://github.com/timothy-voiuhy/WasteClassification/blob/main/CModel.py) using the resnet50 as the back bone of the encoder architecture with convTranspose layers in the decoder.
But because we did not have the masks for the data we decided to use the yolo classification model which actually has to be fitted on more waste data and also more linear layers added to it such as to support the 3 classes that we are supporting in the [raspberry pi driver file](https://github.com/timothy-voiuhy/WasteClassification/blob/main/rasp_driver.py)

## Classifier Code on Colab (copy and paste in browser)
[https://drive.google.com/file/d/1D5L-mim4VlHH8-WiG5mv0BwCN9kdT4S6/view?usp=sharing](https://drive.google.com/file/d1D5L-mim4VlHH8-WiG5mv0BwCN9kdT4S6/view?usp=sharing)

## Hardware 
At fisrt we implemented the code for an [arduino board](https://github.com/timothy-voiuhy/WasteClassification/blob/main/arduino-logic.cpp) but it turned out the board we had targeted had no the computing resources to actually handle the yolo model and so we rewrote the hardware control file in python which can actually run on a raspberry pi 4 with 4GB of ram.

## Conclusion
This was of course a very helpful competition as although we found out about late we were able to come up with something including all the 3d designs using solidworks software