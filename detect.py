from ultralytics import YOLO

model = YOLO("yolov8m-seg.pt")

def segmentar_imagem(imagem):
    results = model(imagem)
    imagem_segmentada = results[0].plot()
    return imagem_segmentada