"""This is a custom model is supposed to replace or do what the yolo model can do
bring the number of classes to 3 and the the 80 that are used with the yolo model"""
import torch 
from torchvision.utils import draw_segmentation_masks
from torch.utils.data import DataLoader, Dataset
import torch.nn as nn
import torchvision.models as models
import torch.optim as optim

"""In this project, am using the resnet50 pretrained model as the detection backbone
in the encoder of the model and then am adding upsampling convTranspose layers in the decoder part of the 
model"""

class WasteClassificationModel(nn.Module):
    def __init__(self):
        super(WasteClassificationModel, self).__init__()
        self.resnet  = models.resnet50(pretrained=True)
        self.encoder = self.getEncoder()
        self.decoder = self.getDecorder()
    
    def getEncoder(self):
        # the encoder part is of a resnet50 model that has already learned the different features from the imageNet dataset 
        resnetbackbone  =  nn.Sequential(
            self.resnet.conv1, # this is the initial conv layer
            self.resnet.bn1, # this is a batch normalization layer to prevent overfiting of the model 
            self.resnet.relu, # to capture non linearities in the image .
            self.resnet.layer1, # this is the first block of layers 
            self.resnet.layer2, # this is the second block of layers 
            self.resnet.layer3, # this is the third block of layers for the resnet50 
            self.resnet.layer4,  # fourth block of layers meaning that this has the deepest feature maps 
        ) # i have left out the fully connected layers since for this task i have 
        # to pass the future maps to the decoder and i have to remove the layers that do the classfication 
        # this can also be achieved using the following easier method.
        # resnetbackbone = nn.Sequential(
        #     *list(self.resnet.children())[:-2] # take every thing apart from the last 2 layers
        # )

    def getDecorder(self):
        # the decoder part of the segmentation portion of the model
        return nn.Sequential(
            nn.ConvTranspose2d(2048, 1024, kernel_size=2, stride=2),
            # now lets apply some batch normalization to cater for overfitting
            nn.BatchNorm2d(1024),
            nn.ReLU(),
            nn.ConvTranspose2d(1024, 512, kernel_size=2, stride=2), 
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.ConvTranspose2d(256, 3, kernel_size=2,stride=2) # here i have used 3 since the class size is 3
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x) 
        return x
    
model = WasteClassificationModel()

# defining the optimizer and loss function
optimizer  = optim.adam.Adam()
lossfn  = nn.CrossEntropyLoss()

def train():
    pass 