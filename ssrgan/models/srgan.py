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
import torch
import torch.nn as nn
from torch.hub import load_state_dict_from_url

model_urls = {
    "srgan": "https://github.com/Lornatang/SRGAN-PyTorch/releases/download/0.1.0/SRGAN_4x4_16_DIV2K-57e43f2f.pth"
}


class Generator(nn.Module):
    r"""The main architecture of the generator."""

    def __init__(self):
        r""" This is an esrgan model defined by the author himself.

        We use two settings for our generator – one of them contains 16 residual blocks, with a capacity similar
        to that of SRGAN and the other is a deeper model with 23 RRDB blocks.
        """
        super(Generator, self).__init__()
        # First layer
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=9, stride=1, padding=4),
            nn.PReLU()
        )

        # 16 Residual blocks
        residual_blocks = []
        for _ in range(16):
            residual_blocks.append(ResidualBlock(64))
        self.Trunk = nn.Sequential(*residual_blocks)

        # Second conv layer post residual blocks
        self.conv2 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(64)
        )

        # Upsampling layers
        upsampling = []
        for _ in range(2):
            upsampling.append(UpsampleBlock(256))
        self.upsampling = nn.Sequential(*upsampling)

        # Final output layer
        self.conv3 = nn.Conv2d(64, 3, kernel_size=9, stride=1, padding=4)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        out1 = self.conv1(input)
        out = self.Trunk(out1)
        out2 = self.conv2(out)
        out = torch.add(out1, out2)
        out = self.upsampling(out)
        out = self.conv3(out)

        return out


class UpsampleBlock(nn.Module):
    r"""Main upsample block structure"""

    def __init__(self, channels):
        r"""Initializes internal Module state, shared by both nn.Module and ScriptModule.

        Args:
            channels (int): Number of channels in the input image.
        """
        super(UpsampleBlock, self).__init__()
        self.conv = nn.Conv2d(channels // 4, channels, kernel_size=3, stride=1, padding=1)
        self.pixel_shuffle = nn.PixelShuffle(upscale_factor=2)
        self.prelu = nn.PReLU()

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        out = self.conv(input)
        out = self.pixel_shuffle(out)
        out = self.prelu(out)

        return out


class ResidualBlock(nn.Module):
    r"""Main residual block structure"""

    def __init__(self, channels):
        r"""Initializes internal Module state, shared by both nn.Module and ScriptModule.

        Args:
            channels (int): Number of channels in the input image.
        """
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.prelu = nn.PReLU()
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        out = self.conv1(input)
        out = self.bn1(out)
        out = self.prelu(out)
        out = self.conv2(out)
        out = self.bn2(out)

        return out + input


def _gan(arch, pretrained, progress):
    model = Generator()
    if pretrained:
        state_dict = load_state_dict_from_url(model_urls[arch],
                                              progress=progress,
                                              map_location=torch.device("cpu"))
        model.load_state_dict(state_dict)
    return model


def srgan(pretrained: bool = False, progress: bool = True) -> Generator:
    r"""GAN model architecture from the
    `"One weird trick..." <https://arxiv.org/abs/1609.04802>`_ paper.

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    return _gan("srgan", pretrained, progress)
