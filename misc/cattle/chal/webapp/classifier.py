import io
import json

import torch
from PIL import Image
from torchvision import models
from torchvision.models.resnet import ResNet18_Weights


class Classifier:
    def __init__(self, index_file: str):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = (
            models.resnet18(weights=ResNet18_Weights.DEFAULT).to(self.device).eval()
        )
        self.transforms = ResNet18_Weights.IMAGENET1K_V1.transforms()

        self.labels = self.load_labels(index_file)

    def load_labels(self, index_file: str) -> list[str]:
        with open(index_file) as f:
            imagenet_class_index = json.load(f)

        return [
            imagenet_class_index[str(k)][1] for k in range(len(imagenet_class_index))
        ]

    def classify(self, image_data: bytes) -> str:
        image = Image.open(io.BytesIO(image_data))
        input_image = self.transforms(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(input_image)

        _, predicted = torch.max(output, 1)

        return self.labels[int(predicted.item())].lower()
