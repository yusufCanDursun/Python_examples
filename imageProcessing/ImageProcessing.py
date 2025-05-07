import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Menu, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu, threshold_yen
from skimage.morphology import skeletonize

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")
        self.image = None
        self.original = None

        self.canvas1 = tk.Canvas(root, width=300, height=300, bg='gray')
        self.canvas1.grid(row=0, column=0)
        self.canvas2 = tk.Canvas(root, width=300, height=300, bg='gray')
        self.canvas2.grid(row=0, column=1)

        tk.Button(root, text="Open Image", command=self.open_image).grid(row=1, column=0, columnspan=2)

        self.create_menu()

    def create_menu(self):
        menu = Menu(self.root)
        tools = Menu(menu, tearoff=0)
        tools.add_command(label="Edge Filter", command=self.edge_filter)
        tools.add_command(label="Mean Filter", command=self.mean_filter)
        tools.add_command(label="Median Filter", command=self.median_filter)
        tools.add_command(label="Blur", command=self.blur_filter)
        tools.add_command(label="Sharpen", command=self.sharpen_filter)
        tools.add_command(label="Rotate (90)", command=self.rotate)
        tools.add_command(label="Flip", command=self.flip)
        tools.add_command(label="Histogram", command=self.show_histogram)
        tools.add_command(label="Histogram Equalization", command=self.hist_equalize)
        tools.add_command(label="Contrast Stretching", command=self.contrast_stretch)
        tools.add_command(label="Thresholding (Manual)", command=self.manual_threshold)
        tools.add_command(label="Thresholding (OTSU)", command=self.otsu_threshold)
        tools.add_command(label="Thresholding (Kapur)", command=self.kapur_threshold)
        tools.add_command(label="Erosion", command=self.erosion)
        tools.add_command(label="Dilation", command=self.dilation)
        tools.add_command(label="Centroid", command=self.centroid)
        tools.add_command(label="Skeletonize", command=self.skeletonize_image)
        menu.add_cascade(label="Tools", menu=tools)
        self.root.config(menu=menu)

    def open_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original = cv2.imread(path)
            self.image = self.original.copy()
            self.show_image(self.original, self.canvas1)

    def show_image(self, img, canvas):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300, 300))
        im_pil = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im_pil)
        canvas.image = imgtk
        canvas.create_image(0, 0, anchor='nw', image=imgtk)

    def update_output(self, img):
        self.image = img
        self.show_image(img, self.canvas2)

    # Filters
    def edge_filter(self):
        edges = cv2.Canny(self.image, 100, 200)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.update_output(edges)

    def mean_filter(self):
        blur = cv2.blur(self.image, (5, 5))
        self.update_output(blur)

    def median_filter(self):
        blur = cv2.medianBlur(self.image, 5)
        self.update_output(blur)

    def blur_filter(self):
        blur = cv2.GaussianBlur(self.image, (5, 5), 0)
        self.update_output(blur)

    def sharpen_filter(self):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharp = cv2.filter2D(self.image, -1, kernel)
        self.update_output(sharp)

    # Transformations
    def rotate(self):
        rot = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        self.update_output(rot)

    def flip(self):
        flip = cv2.flip(self.image, 1)
        self.update_output(flip)

    # Histogram operations
    def show_histogram(self):
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([self.image], [i], None, [256], [0, 256])
            plt.plot(histr, color=col)
        plt.title("Histogram")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        plt.show()

    def hist_equalize(self):
        img_yuv = cv2.cvtColor(self.image, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        equalized = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        self.update_output(equalized)

    def contrast_stretch(self):
        img = self.image.copy()
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        self.update_output(img)

    # Thresholding
    def manual_threshold(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        self.update_output(cv2.cvtColor(th, cv2.COLOR_GRAY2BGR))

    def otsu_threshold(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        th_val = threshold_otsu(gray)
        _, th = cv2.threshold(gray, th_val, 255, cv2.THRESH_BINARY)
        self.update_output(cv2.cvtColor(th, cv2.COLOR_GRAY2BGR))

    def kapur_threshold(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        th_val = threshold_yen(gray)  # Approximation of Kapur
        _, th = cv2.threshold(gray, th_val, 255, cv2.THRESH_BINARY)
        self.update_output(cv2.cvtColor(th, cv2.COLOR_GRAY2BGR))

    # Morphological operations
    def erosion(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(gray, kernel, iterations=1)
        self.update_output(cv2.cvtColor(erosion, cv2.COLOR_GRAY2BGR))

    def dilation(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3, 3), np.uint8)
        dil = cv2.dilate(gray, kernel, iterations=1)
        self.update_output(cv2.cvtColor(dil, cv2.COLOR_GRAY2BGR))

    def centroid(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        moments = cv2.moments(gray)
        if moments['m00'] != 0:
            cX = int(moments['m10'] / moments['m00'])
            cY = int(moments['m01'] / moments['m00'])
            img_copy = self.image.copy()
            cv2.circle(img_copy, (cX, cY), 5, (0, 0, 255), -1)
            self.update_output(img_copy)

    def skeletonize_image(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 1, cv2.THRESH_BINARY)
        skeleton = skeletonize(binary).astype(np.uint8) * 255
        skeleton = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)
        self.update_output(skeleton)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
