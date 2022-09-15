import cv2
import numpy as np


def convert_rgba_to_rgb(image: np.ndarray, return_mask: bool) -> np.ndarray:
    """Convert RGBA image to RGB image.

    Args:
        image (_type_): RGBA image
        return_mask (_type_):アルファチャンネルの配列をreutrnするかどうか

    Returns:
        _type_: RGB imageもしくは
    """
    mask = image[:, :, 3]
    if return_mask:
        return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8), mask
    else:
        return (image[:, :, :3] * np.dstack([mask / 255] * 3)).astype(np.uint8)


def convert_make_hsvcolor(
    image: np.ndarray, hue: int, saturation: int, value: int, include_alpha_ch: bool
) -> np.ndarray:
    """指定したHSVにメイクを変更する.

    Args:
        image(_type_): B255で塗りつぶした透過メイク素材、1024x1024
        hue(_type_):HSVのHueの数値
        saturation(_type_):HSVのSaturationの数値
        value(_type_):HSVのVvalueの数値
        include_alpha_ch(_type_):returnする画像にアルファチャンネルを含むか否か
    Return:
        np.array:任意の色、設定に変更したメイクのnumpy配列
    """
    image_wo_alpha, mask = convert_rgba_to_rgb(image, True)
    image_hsv = cv2.cvtColor(image_wo_alpha, cv2.COLOR_BGR2HSV)

    image_hsv[:, :, 0] = np.where(image_hsv[:, :, 0] == 120, hue / 2, image_hsv[:, :, 0])
    image_hsv[:, :, 1] = np.where(image_hsv[:, :, 1] == 255, saturation, image_hsv[:, :, 1])
    image_hsv[:, :, 2] = np.where(image_hsv[:, :, 2] != 0, (value * (image_hsv[:, :, 2] / 255)), image_hsv[:, :, 2])
    # ↑グラデーションの比率を保ったまま、明度を変更する

    image_bgr = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    if include_alpha_ch:
        b_ch, g_ch, r_ch = cv2.split(image_bgr[:, :, :3])
        image_bgr_w_alpha = cv2.merge((b_ch, g_ch, r_ch, mask))
        return image_bgr_w_alpha
    else:
        return image_bgr


image = cv2.imread("i-make/static/facepaints/B255.png", cv2.IMREAD_UNCHANGED)

return_make = convert_make_hsvcolor(image, 240, 119.85, 163.2, True)
cv2.imshow("test.png", return_make)
cv2.waitKey(0)
cv2.destroyAllWindows()
