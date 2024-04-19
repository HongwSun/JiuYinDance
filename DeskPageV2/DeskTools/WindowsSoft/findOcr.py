from numpy import fromfile, uint8
from ppocronnx.predict_system import TextSystem
import cv2

text_sys = TextSystem()


def find_ocr(image, temp_text: str) -> list or None:
    """
    :param image: ��Ҫ�������ֵ�ͼƬ
    :param temp_text: ��Ҫ��ͼƬ�в�ѯ������
    :return ���ҵ��ĵ�һ��ƥ������ֵ�����
    """
    if isinstance(image, str):
        # img_read = cv2.cv2.imread(img)   # ��������޷���������ĵ�·��
        img_read = cv2.imdecode(fromfile(image, dtype=uint8), -1)
    else:
        img_read = image
    res = text_sys.detect_and_ocr(img_read)
    for boxed_result in res:
        if temp_text in boxed_result.ocr_text:
            rect = boxed_result.box
            x_center = (rect[0][0] + rect[2][0])/2
            y_center = (rect[0][1] + rect[2][1])/2
            return [int(x_center), int(y_center)]
    return None
