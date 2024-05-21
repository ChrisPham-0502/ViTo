# HairStyle

To inference this repo, you need to execute the following setup steps:
```sh
!wget https://github.com/ninja-build/ninja/releases/download/v1.8.2/ninja-linux.zip
!sudo unzip ninja-linux.zip -d /usr/local/bin/
!sudo update-alternatives --install /usr/bin/ninja ninja /usr/local/bin/ninja 1 --force

!git clone https://github.com/ChrisPham-0502/ViTo.git
```

Next, go to the ViTo folder, continue to setup some packages:
```sh
!pip install pillow==10.0.0 face_alignment dill==0.2.7.1 addict fpie \
git+https://github.com/openai/CLIP.git -q

!git clone https://huggingface.co/AIRI-Institute/HairFastGAN
!cd HairFastGAN && git lfs pull && cd ..
!mv HairFastGAN/pretrained_models pretrained_models
!mv HairFastGAN/input input
!rm -rf HairFastGAN
```

To implement model via code, you could refer to the following code:
```sh
import argparse
from pathlib import Path
from hair_swap import HairFast, get_parser

# Initialize model
model_args = get_parser()
hair_fast = HairFast(model_args.parse_args([]))
```

Create a function to display images:
```sh
import requests
from io import BytesIO
from PIL import Image
from functools import cache

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import torchvision.transforms as T
import torch
%matplotlib inline


def to_tuple(func):
    def wrapper(arg):
        if isinstance(arg, list):
            arg = tuple(arg)
        return func(arg)
    return wrapper


@to_tuple
@cache
def download_and_convert_to_pil(urls):
    pil_images = []
    for url in urls:
        response = requests.get(url, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        img = Image.open(BytesIO(response.content))
        pil_images.append(img)
        print(f"Downloaded an image of size {img.size}")
    return pil_images


def display_images(images=None, **kwargs):
    is_titles = images is None
    images = images or kwargs

    grid = gridspec.GridSpec(1, len(images))
    fig = plt.figure(figsize=(20, 10))

    for i, item in enumerate(images.items() if is_titles else images):
        title, img = item if is_titles else (None, item)

        img = T.functional.to_pil_image(img) if isinstance(img, torch.Tensor) else img
        img = Image.open(img) if isinstance(img, str | Path) else img

        ax = fig.add_subplot(1, len(images), i+1)
        ax.imshow(img)
        if title:
            ax.set_title(title, fontsize=20)
        ax.axis('off')

    plt.show()
```

Finally, send input images to model:
```sh
face_path = '1.jpg'
shape_path = '2.jpg'
color_path = '3.jpg'

final_image, face_align, shape_align, color_align = hair_fast.swap(face_path, shape_path, color_path, align=True)
display_images(result=final_image, face=face_align, shape=shape_align, color=color_align)
```

### Output:
![output](https://github.com/ChrisPham-0502/ViTo/assets/126843941/c9581a20-8a97-4c1e-9d39-ad0cba4bf2c2)
