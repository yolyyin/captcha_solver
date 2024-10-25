from ultralytics import YOLO
#import onnx


if __name__ == "__main__":
    # load a model
    model = YOLO("runs/detect/1024_yolox/weights/best.pt")
    model.export(format="onnx",
                 imgsz=(96,192), #half, dynamic,
                 simplify=True,
                 batch=1)