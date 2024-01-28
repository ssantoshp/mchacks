from fastsam import FastSAMPrompt, FastSAM
from fastapi import UploadFile
import torch
import numpy as np
import cv2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


async def read_img(raw_file: UploadFile):
    contents = await raw_file.read()
    nparray = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    return img

def get_masks(image_path: str, model: FastSAM):
    results = model(image_path, device=device, retina_masks=True, imgsz=1024, conf=0.1, iou=0.9)
    prompt_process = FastSAMPrompt(image_path, results, device=device)
    ann = prompt_process.everything_prompt().cpu().numpy()
    masks = np.where(ann > 0, 255, 0).astype(np.uint8)
    return masks

def apply_masks_on_img(image_path: str, masks: np.ndarray):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    segmented_imgs = []
    for mask in masks:
        segmented_imgs.append(cv2.bitwise_and(img, img, mask=mask))
    return segmented_imgs


