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


def convert_make_color(
    image: np.ndarray, h_ch: int, s_ch: int, v_ch: int, return_include_alphachannel: bool
) -> np.ndarray:
    """指定したHSVにメイクを変更する.

    Args:
        image(_type_): B255で塗りつぶした透過メイク素材、1024x1024
        h_ch(_type_):HSVのHの数値
        s_ch(_type_):HSVのSの数値
        v_ch(_type_):HSVのVの数値
        return_include_alphachannel(_type_):returnする画像にアルファチャンネルを含むか否か
    """
    delete_alpha_image, mask = convert_rgba_to_rgb(image, True)
    hsv = cv2.cvtColor(delete_alpha_image, cv2.COLOR_BGR2HSV)

    hsv[:, :, 0] = np.where(hsv[:, :, 0] == 120, h_ch / 2, hsv[:, :, 0])
    hsv[:, :, 1] = np.where(hsv[:, :, 1] == 255, s_ch, hsv[:, :, 1])
    hsv[:, :, 2] = np.where(hsv[:, :, 2] != 0, (v_ch * (hsv[:, :, 2] / 255)), hsv[:, :, 2])
    # ↑グラデーションの比率を保ったまま、明度を変更する

    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    if return_include_alphachannel:
        b_ch, g_ch, r_ch = cv2.split(bgr[:, :, :3])
        include_alpha_bgr_image = cv2.merge((b_ch, g_ch, r_ch, mask))
        return include_alpha_bgr_image
    else:
        return bgr


image = cv2.imread("i-make/static/facepaints/B255.png", cv2.IMREAD_UNCHANGED)

return_make = convert_make_color(image, 19, 255, 148, True)
cv2.imshow("test.png", return_make)
cv2.waitKey(0)
cv2.destroyAllWindows()
