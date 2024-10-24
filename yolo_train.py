from ultralytics import YOLO
import clearml
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', help='path of pretrained model', type=str, required=True)
    parser.add_argument('--data_config_path', help='path of dataset config', type=str,required=True)
    parser.add_argument('--img_size', help='image pixel size', type=int, required=True)
    parser.add_argument('-n','--name', help='name of this training', type=str, default="yolo_train")
    parser.add_argument('-b','--batch_size', help='batch size', type=int, default=8)
    parser.add_argument('-e', '--epoch', help='epoch number', type=int, default=10)
    args = parser.parse_args()
    # for ml monitor, must init clearml first in the cmd tool, see below link
    # login in to https://docs.ultralytics.com/yolov5/tutorials/clearml_logging_integration/
    clearml.browser_login()

    # load the model
    model = YOLO(args.model_path)
    # training
    model.train(
        data=args.data_config_path,
        imgsz = args.img_size,
        epochs = args.epoch,
        batch=args.batch_size,
        name = args.name,
    )


if __name__ == "__main__":
    main()
