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
from ssrgan_pytorch.models.bionet import BioNet
from ssrgan_pytorch.models.inception import Inception
from ssrgan_pytorch.models.mobilenetv1 import MobileNetV1
from ssrgan_pytorch.models.mobilenetv2 import MobileNetV2
from ssrgan_pytorch.models.mobilenetv3 import MobileNetV3
from ssrgan_pytorch.models.squeezenet import SqueezeNet
from ssrgan_pytorch.models.srgan import SRGAN
from ssrgan_pytorch.models.u_net import SymmetricBlock
from ssrgan_pytorch.models.u_net import UNet
from ssrgan_pytorch.models.vgg import DiscriminatorForVGG

__all__ = [
    "BioNet",
    "Inception",
    "MobileNetV1",
    "MobileNetV2",
    "MobileNetV3",
    "SqueezeNet",
    "SRGAN",
    "SymmetricBlock",
    "UNet",
    "DiscriminatorForVGG"]
