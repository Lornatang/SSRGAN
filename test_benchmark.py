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
import argparse
import logging

import ssrgan.models as models
from ssrgan.utils.common import create_folder
from tester import Test

model_names = sorted(name for name in models.__dict__
                     if name.islower() and not name.startswith("__")
                     and callable(models.__dict__[name]))

logger = logging.getLogger(__name__)
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", metavar="DIR",
                        help="path to dataset")
    parser.add_argument("-a", "--arch", metavar="ARCH", default="dsgan",
                        choices=model_names,
                        help="model architecture: " +
                             " | ".join(model_names) +
                             " (default: dsgan)")
    parser.add_argument("-j", "--workers", default=8, type=int, metavar="N",
                        help="Number of data loading workers. (default:8)")
    parser.add_argument("-b", "--batch-size", default=16, type=int, metavar="N",
                        help="mini-batch size (default: 16), this is the total "
                             "batch size of all GPUs on the current node when "
                             "using Data Parallel or Distributed Data Parallel.")
    parser.add_argument("--image-size", type=int, default=128,
                        help="Image size of real sample. (default:128).")
    parser.add_argument("--upscale-factor", type=int, default=4, choices=[4],
                        help="Low to high resolution scaling factor. (default:4).")
    parser.add_argument("--model-path", default="weights/DSGAN.pth", type=str, metavar="PATH",
                        help="Path to latest checkpoint for model. (default: ``weights/DSGAN.pth``).")
    parser.add_argument("--pretrained", dest="pretrained", action="store_true",
                        help="Use pre-trained model.")
    parser.add_argument("--detail", dest="detail", action="store_true",
                        help="Evaluate all indicators. It is very slow.")
    parser.add_argument("--device", default="0",
                        help="device id i.e. `0` or `0,1` or `cpu`. (default: ``0``).")

    args = parser.parse_args()

    print("##################################################\n")
    print("Run Testing Engine.\n")
    print(args)

    create_folder("benchmark")

    logger.info("TestEngine:")
    print("\tAPI version .......... 0.1.1")
    print("\tBuild ................ 2020.11.30-1116-0c5adc7e")

    logger.info("Creating Testing Engine")
    test = Test(args)

    logger.info("Staring testing model")
    test.run()
    print("##################################################\n")

    logger.info("Test dataset performance evaluation completed successfully.\n")
