import PIL.Image as Image
import torchvision.transforms.functional as F
from image import *
from model import CSRNet
import torch
import os
from torchvision import datasets, transforms


def make_prediction(model, image_to_predict):
    
    base_path = os.getcwd()
    checkpoint_path = base_path + '/src/trained_csrnet/7model_best.pth.tar'
    image_path = base_path + f'/data/{image_to_predict}'
    
    transform=transforms.Compose([transforms.ToTensor(),transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225]),])

    model = model.cuda()
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint['state_dict'])
    # TODO: Switch with image_to_predict
    img = transform(Image.open(image_path).convert('RGB')).cuda()

    output = model(img.unsqueeze(0))
    # print("Predicted Count : ",int(output.detach().cpu().sum().numpy()))
    return int(output.detach().cpu().sum().numpy())

