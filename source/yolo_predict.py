import os
import cv2
import torch
from ultralytics import YOLO
from source.category import create_category
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', help='input image folder path', type=str, required=True)
    parser.add_argument('-m','--model_path', help='path of best model', type=str, required=True)
    parser.add_argument('-o','--out_dir', help='directory of outputs', type=str,required=True)
    parser.add_argument('-s', '--symbol_path', help='path of symbol list', type=str, required=True)
    parser.add_argument('-n','--out_name', help='name of output file', type=str, default="result.csv")
    parser.add_argument('--save_plot', help='whether to save plotting for predictions', action='store_true')
    args = parser.parse_args()

    model_path = args.model_path
    output_dir = args.out_dir
    symbol_path = args.symbol_path
    source = args.input_dir
    img_save_dir = os.path.join(output_dir, "images")
    if args.save_plot:
        os.makedirs(img_save_dir, exist_ok=True)

    # read symbol sets
    symbols_file = open(symbol_path, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()
    cat2class, class2cat = create_category(captcha_symbols)
    print(class2cat)

    image_names, cracked = yolo_classify(source, class2cat, model_path, img_save_dir,save_plot=args.save_plot)
    sorted_lists = sorted(zip(image_names, cracked))
    image_names, cracked = zip(*sorted_lists)

    for image_name, crack in zip(image_names, cracked):
        with open(f"{output_dir}/{args.out_name}","a") as f:
            f.write(f"{image_name},{crack}\n")


def yolo_classify(test_img_folder, class2cat, model_path, output_dir,save_plot=False):
    image_names = []
    cracked = []
    # load the model
    model = YOLO(model_path)
    results = model.predict(test_img_folder,
                            imgsz=(96,192),
                            max_det=6,
                            #conf=0.25,
                            iou=0.6)

    for result in results:
        # print(result.probs)
        # plot and save images for checking
        img_path = result.path
        image_name = os.path.basename(img_path)
        if save_plot:
            im_bgr = result.plot()
            cv2.imwrite(f"{output_dir}/{image_name}",im_bgr)
        #img = result.orig_img
        boxes = result.boxes
        box_class = boxes.cls
        box_xywh = boxes.xywh
        result = ""
        # concat xywh and class to sort according to x-center value
        concat = torch.concat([box_xywh, box_class[:, None]], dim=-1)
        # Get the indices that would sort the first column (first element in each row)
        sorted_indices = torch.argsort(concat[:, 0])
        sorted = concat[sorted_indices]
        # split again to give box_class back
        box_class = sorted[:, -1]
        for idx in box_class.tolist():
            cat = class2cat[idx]
            result += cat
        cracked.append(result)
        image_names.append(image_name)
    return image_names,cracked


if __name__ == '__main__':
    main()



