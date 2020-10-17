# Copyright 2020 Dakewe Biotech Corporation. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""It mainly implements all the losses used in the model."""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torchvision.models import vgg19

__all__ = [
    "TVLoss", "VGG22Loss", "VGG34Loss", "VGG54Loss"
]


class VGG22Loss(nn.Module):
    r""" Where VGG2.2 represents the feature map of 7th layer in pretrained VGG19 model.

    `"Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network" <https://arxiv.org/pdf/1609.04802.pdf>`_

    A loss defined on feature maps of higher level features from deeper network layers
    with more potential to focus on the content of the images. We refer to this network
    as SRGAN in the following.
    """

    def __init__(self, feature_layer: int = 7) -> None:
        """ Constructing characteristic loss function of VGG network. For VGG5.4 layer.

        Args:
            feature_layer (int): How many layers in VGG19. (Default:7).

        Notes:
            features(
              (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (1): ReLU(inplace=True)
              (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (3): ReLU(inplace=True)
              (4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (6): ReLU(inplace=True)
            )
        """
        super(VGG22Loss, self).__init__()
        model = vgg19(pretrained=True)
        self.features = nn.Sequential(*list(model.features.children())[:feature_layer]).eval()
        # Freeze parameters. Don't train.
        for name, param in self.features.named_parameters():
            param.requires_grad = False

    def forward(self, input: Tensor, target: Tensor) -> Tensor:
        vgg_loss = F.mse_loss(self.features(input), self.features(target))

        return vgg_loss


class VGG34Loss(nn.Module):
    r""" Where VGG_conv34 represents the feature map of 34th layer in pretrained VGG19 model.

    "Perceptual Extreme Super Resolution Network with Receptive Field Block" <https://arxiv.org/pdf/2005.12597.pdf>`_

    A loss defined on feature maps of higher level features from deeper network layers
    with more potential to focus on the content of the images. We refer to this network
    as SRGAN in the following.
    """

    def __init__(self, feature_layer: int = 34) -> None:
        """ Constructing characteristic loss function of VGG network. For VGG34 layer.

        Args:
            feature_layer (int): How many layers in VGG19. (Default:34).

        Notes:
            features(
              (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (1): ReLU(inplace=True)
              (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (3): ReLU(inplace=True)
              (4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (6): ReLU(inplace=True)
              (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (8): ReLU(inplace=True)
              (9): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (11): ReLU(inplace=True)
              (12): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (13): ReLU(inplace=True)
              (14): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (15): ReLU(inplace=True)
              (16): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (17): ReLU(inplace=True)
              (18): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (19): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (20): ReLU(inplace=True)
              (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (22): ReLU(inplace=True)
              (23): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (24): ReLU(inplace=True)
              (25): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (26): ReLU(inplace=True)
              (27): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (29): ReLU(inplace=True)
              (30): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (31): ReLU(inplace=True)
              (32): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (33): ReLU(inplace=True)
            )
        """
        super(VGG34Loss, self).__init__()
        model = vgg19(pretrained=True)
        self.feature_extractor = nn.Sequential(*list(model.features.children())[:feature_layer]).eval()

    def forward(self, input: Tensor, target: Tensor) -> Tensor:
        vgg_loss = F.mse_loss(self.feature_extractor(input), self.feature_extractor(target))

        return vgg_loss


class VGG54Loss(nn.Module):
    r""" Where VGG5.4 represents the feature map of 34th layer in pretrained VGG19 model.

    `"Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network" <https://arxiv.org/pdf/1609.04802.pdf>`_

    A loss defined on feature maps of higher level features from deeper network layers
    with more potential to focus on the content of the images. We refer to this network
    as SRGAN in the following.
    """

    def __init__(self, feature_layer: int = 34) -> None:
        """ Constructing characteristic loss function of VGG network. For VGG5.4 layer.

        Args:
            feature_layer (int): How many layers in VGG19. (Default:34).

        Notes:
            features(
              (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (1): ReLU(inplace=True)
              (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (3): ReLU(inplace=True)
              (4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (6): ReLU(inplace=True)
              (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (8): ReLU(inplace=True)
              (9): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (11): ReLU(inplace=True)
              (12): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (13): ReLU(inplace=True)
              (14): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (15): ReLU(inplace=True)
              (16): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (17): ReLU(inplace=True)
              (18): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (19): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (20): ReLU(inplace=True)
              (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (22): ReLU(inplace=True)
              (23): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (24): ReLU(inplace=True)
              (25): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (26): ReLU(inplace=True)
              (27): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
              (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (29): ReLU(inplace=True)
              (30): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (31): ReLU(inplace=True)
              (32): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
              (33): ReLU(inplace=True)
            )
        """
        super(VGG54Loss, self).__init__()
        model = vgg19(pretrained=True)
        self.features = nn.Sequential(*list(model.features.children())[:feature_layer]).eval()
        # Freeze parameters. Don't train.
        for name, param in self.features.named_parameters():
            param.requires_grad = False

    def forward(self, input: Tensor, target: Tensor) -> Tensor:
        vgg_loss = F.mse_loss(self.features(input), self.features(target))

        return vgg_loss


# Source from `https://github.com/jxgu1016/Total_Variation_Loss.pytorch/blob/master/TVLoss.py`
class TVLoss(nn.Module):
    r"""Regularization loss based on Li FeiFei."""

    def __init__(self, weight: Tensor) -> None:
        """The weight information of loss is based on the image information generated by the generator.

        Args:
            weight (tensor): Fake high resolution image weight.
        """
        super(TVLoss, self).__init__()
        self.weight = weight

    def forward(self, input: Tensor) -> Tensor:
        batch_size = input.size()[0]
        h_x = input.size()[2]
        w_x = input.size()[3]
        count_h = self.tensor_size(input[:, :, 1:, :])
        count_w = self.tensor_size(input[:, :, :, 1:])
        h_tv = torch.pow((input[:, :, 1:, :] - input[:, :, :h_x - 1, :]), 2).sum()
        w_tv = torch.pow((input[:, :, :, 1:] - input[:, :, :, :w_x - 1]), 2).sum()
        tv_loss = self.weight * 2 * (h_tv / count_h + w_tv / count_w) / batch_size

        return tv_loss

    @staticmethod
    def tensor_size(t):
        return t.size()[1] * t.size()[2] * t.size()[3]
