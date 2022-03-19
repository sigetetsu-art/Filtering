from PIL import Image
from scipy import signal
import numpy as np

FILTER_LENGTH = 3
PADDING_SIZE = int((FILTER_LENGTH - 1) / 2)
Filter1 = np.array([[-1,0,1], [-1,0,1], [-1,0,1]]) #ソーベルフィルター
Filter2 = np.array([[1/16,1/8,1/16], [1/8,1/4,1/8], [1/16,1/8,1/16]]) #ガウシアン(ぼかし)フィルター
Filter3 = np.array([[-1,-1,-1], [-1,9,-1],[-1,-1,-1]]) #先鋭化フィルタ


def mirror_padding(img, padding_size):
    img_pixels = np.array(img)
    pad_img = np.pad(img_pixels, ((padding_size, padding_size), (padding_size, padding_size)), "edge")
    return pad_img

def filtering(padding_image, filter):
    filtered_img = signal.fftconvolve(filter[::-1,::-1], padding_image, mode='valid')
    filtered_img[filtered_img < 0] = 0
    filtered_img[filtered_img > 255] = 255
    filtered_img = (filtered_img * 2 + 1) // 2
    return filtered_img
    
def main():
    original_image = Image.open("landscape.jpg")
    original_image = original_image.convert("L")
    padding_image = mirror_padding(original_image, PADDING_SIZE)
    filtered_image = filtering(padding_image, Filter3)
    filtered_image = Image.fromarray(filtered_image.astype("uint8"))
    
    filtered_image.show()
    filtered_image.save("filtered_image.jpg")

if __name__ == "__main__":
    main()

