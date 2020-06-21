# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import tensorflow as tf
from utils import label_map_util
from utils import visualization_utils as vis_util

MODEL_NAME = 'inference_graph'      # Название модели.

# Получение текущей директории.
CWD_PATH = os.getcwd()

# Путь до "замороженного" графа нейронной сети.
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')

# Путь к наименованиям.
PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'labelmap.pbtxt')

# Количество классов идентификации сетью.
NUM_CLASSES = 1

# Загрузка наименований и их идентификация.
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

num_for_file = 0


# Функция для поиска очагов на снимке.
def find_regions(image_name):
    global num_for_file

    # Путь к изображению.
    path_to_image = os.path.join(CWD_PATH, image_name)

    # Загрузка tf модели в память.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    # Получение входных тензоров.
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Выходные тензоры, выделенные участки на снимке.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Каждый score это уровень уверенности в выборе
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Количество найденных очагов.
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    image_file = open(path_to_image, "rb")
    image_bytes = image_file.read()
    bytes_arr = np.frombuffer(image_bytes, dtype=np.uint8)

    # Загрузка изображения в opencv матрицу.
    image = cv2.imdecode(bytes_arr, cv2.IMREAD_COLOR)

    image_expanded = np.expand_dims(image, axis=0)

    # Получение данных со снимка
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    # Тонкость линии выделения.
    thickness = 1

    list_of_classes, list_of_coords = vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=thickness,
        min_score_thresh=0.60,
        skip_labels=True,                   # Для удаления наименования области.
        skip_scores=True,
        draw_boxes=False)                   # Для удаления процентов распознавания.

    height = image.shape[0]
    width = image.shape[1]

    cutted_images = []

    num_of_regions = 0

    # Переводит относительные координаты в абсолютные (в пиксели).
    for i in range(len(list_of_coords)):
        global cutted
        ymin = (int(list_of_coords[i][0] * height))
        xmin = (int(list_of_coords[i][1] * width))
        ymax = (int(list_of_coords[i][2] * height))
        xmax = (int(list_of_coords[i][3] * width))

        # Координаты области очага.
        cutted = image[ymin + thickness:ymax - thickness, xmin + thickness:xmax - thickness]
        num_for_file += 1

        cutted_images.append([ymin, ymax, xmin, xmax])

        num_of_regions += 1

        simple_cutted = []

        for k in range(0, cutted.shape[0]):
            for j in range(0, cutted.shape[1]):
                simple_cutted.append(cutted[k, j][0])

        # Высчитывание средней интенсивности цвета на выделенном участке.
        mid_color = sum(simple_cutted) / len(simple_cutted)
        print(mid_color)

        # Закрашивает области очага в зеленый.
        for k in range(0, cutted.shape[0]):
            for j in range(0, cutted.shape[1]):
                if cutted[k, j][0] > mid_color:
                    cutted[k, j] = [0, 255, 0]

        rows, cols, channels = cutted.shape

        cutted = cv2.addWeighted(image[250: 250 + rows, 0:0 + cols], 0.5, cutted, 0.5, 0)

    print("Количество очагов " + str(num_of_regions))

    return image, num_of_regions
