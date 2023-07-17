import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops
import matplotlib.pyplot as plt
import numpy as np
import random
from skimage import feature
from skimage import morphology
from skimage import util
from skimage.morphology import square, cube

class ImageEffects:
    '''
    Class that contains image effects methods to apply to any image.
    Parameters:
    - image: The image to apply the effects to.
    '''
    def __init__(self, image):
        self.image = image

    @staticmethod
    def generate_random_colors(num_colors):
        '''
        Generates random colors.
        Parameters:
        - num_colors: The number of colors to generate.
        '''
        return [
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for _ in range(num_colors)
        ]

    def pixelate(self, image, block_size):
        '''
        Pixelates the image.
        Parameters:
        - block_size: The size of the pixelated blocks.
        '''
        width, height = image.size
        image = image.resize((width // block_size, height // block_size), Image.NEAREST)
        image = image.resize((width, height), Image.NEAREST)
        return image

    def color_scale_effect(self, image, color_scale):
        '''
        Applies a color scale to the image.
        Parameters:
        - color_scale: The scale of the color effect.
        '''
        if color_scale == "grayscale":
            image = ImageOps.grayscale(image)
        elif color_scale == "sepia":
            sepia_filter = ImageOps.colorize(
                ImageOps.grayscale(image), "#704238", "#C0B283"
            )
            image = Image.blend(image, sepia_filter, 0.5)
        elif color_scale in [
            "magma",
            "inferno",
            "plasma",
            "viridis",
            "cividis",
            "rocket",
            "mako",
            "turbo",
            "icefire",
            "solar",
            "hsv",
            "twilight",
            "twilight_shifted",
            "gnuplot",
            "gnuplot2",
            "CMRmap",
        ]:
            colormap = plt.get_cmap(color_scale)
            gray_image = ImageOps.grayscale(image)
            np_image = np.array(gray_image)
            colored_image = (colormap(np_image / 255) * 255).astype(np.uint8)
            image = Image.fromarray(colored_image[:, :, :3], "RGB")
        return image

    def overlay_effect(self, image, overlay):
        '''
        Overlay effect that adds a vignette or light leak to the image.
        '''
        width, height = image.size
        if overlay == "vignette":
            mask = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, width, height), fill=255)
            image = ImageOps.colorize(mask, "black", "white")
        elif overlay == "light_leak":
            light_leak = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(light_leak)
            for _ in range(10):
                x = random.randint(0, width)
                y = random.randint(0, height)
                r = random.randint(10, 200)
                color = (255, 255, 255, random.randint(64, 128))
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
            image = Image.alpha_composite(image.convert("RGBA"), light_leak).convert("RGB")
        return image

    def horizontal_glitch(self, image, block_size, glitch_chance):
        '''
        Glitches the image horizontally.
        Parameters:
        - block_size: The size of the glitched blocks.
        - glitch_chance: The chance of a glitch happening.
        '''
        width, height = image.size
        for y in range(0, height, block_size):
            if random.random() < glitch_chance:
                shift = random.randint(-block_size, block_size)
                glitched_block = image.crop((0, y, width, y + block_size))
                image.paste(glitched_block, (shift, y))
        return image

    def vertical_glitch(self, image, block_size, glitch_chance):
        '''
        Glitches the image vertically.
        Parameters:
        - block_size: The size of the glitched blocks.
        - glitch_chance: The chance of a glitch happening.
        '''
        width, height = image.size
        for x in range(0, width, block_size):
            if random.random() < glitch_chance:
                shift = random.randint(-block_size, block_size)
                glitched_block = image.crop((x, 0, x + block_size, height))
                image.paste(glitched_block, (x, shift))
        return image

    def reduce_colors(self, image, num_colors):
        '''
        Reduces the number of colors in the image.
        '''
        return image.quantize(colors=num_colors).convert("RGB")

    def kaleidoscope_effect(self, image, num_slices, rotation_angle, slice_angle=360):
        '''
        Kaleidoscope effect
        :param image: Image to apply effect
        :param num_slices: Number of slices
        :param rotation_angle: Rotation angle
        :param slice_angle: Slice angle
        :return: Image with kaleidoscope effect
        '''
        width, height = image.size
        slice_angle = slice_angle // num_slices
        mask = Image.new("1", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice((0, 0, width, height), 90, 90 + slice_angle, fill=1)

        base_slice = Image.composite(image, Image.new("RGB", (width, height)), mask)
        base_slice = base_slice.rotate(rotation_angle, resample=Image.BICUBIC, expand=True)

        kaleidoscope_image = Image.new("RGB", base_slice.size)
        for i in range(num_slices):
            rotated_slice = base_slice.rotate(i * slice_angle, resample=Image.BICUBIC)
            kaleidoscope_image.paste(rotated_slice, mask=rotated_slice.convert("L"))

        return kaleidoscope_image.resize((width, height), resample=Image.BICUBIC)

    def noise(self, image,grain_size,noise_type):
        '''
        Adds noise to the image.
        Paramenters:
        - grain_size: The size of the noise.
        - noise_type: The type of noise to add.
        '''
        width, height = image.size
        image_mode = image.mode
        if noise_type == "grain":
            grain = Image.new(image_mode, (width, height), (0, 0, 0))
            draw = ImageDraw.Draw(grain)
            for _ in range(width * height * grain_size // 100):
                x = random.randint(0, width)
                y = random.randint(0, height)
                draw.point((x, y), fill=(255, 255, 255))
            image = ImageChops.add(image, grain)
        elif noise_type == "speckle":
            speckle = Image.new(image_mode, (width, height), (0, 0, 0))
            draw = ImageDraw.Draw(speckle)
            for _ in range(width * height * grain_size // 100):
                x = random.randint(0, width)
                y = random.randint(0, height)
                draw.point((x, y), fill=(255, 255, 255))
            image = ImageChops.multiply(image, speckle)
        elif noise_type == "gaussian":
            image = image.filter(ImageFilter.GaussianBlur(grain_size))
        elif noise_type == "poisson":
            adapted_size = (width // grain_size, height // grain_size)
            image = image.resize(adapted_size, Image.NEAREST)
        elif noise_type == "s&p":
            image = image.filter(ImageFilter.ModeFilter(grain_size))
        elif noise_type == "speckle":
            image = image.filter(ImageFilter.MedianFilter(grain_size))
        return image

    def edge_detection(self, image, sigma=1):
        '''
        Edge detection using Canny algorithm
        Parameters:
        - image: Image to apply effect
        - sigma: Sigma value for Canny algorithm
        Returns:
        - Image with edge detection effect
        '''
        gray_image = ImageOps.grayscale(image)
        edges = feature.canny(np.array(gray_image), sigma=sigma)
        return Image.fromarray((edges * 255).astype(np.uint8))

    def erosion(self, image, selem_shape, selem_size):
        '''
        Erosion effect
        Parameters:
        - image: Image to apply effect
        - selem_shape: Shape of the structuring element ('disk', 'square', 'cube')
        - selem_size: Size of the structuring element
        Returns:
        - Image with erosion effect
        '''
        gray_image = ImageOps.grayscale(image)

        if selem_shape == 'disk':
            selem = morphology.disk(selem_size)
        elif selem_shape == 'square':
            selem = square(selem_size)
        elif selem_shape == 'cube':
            selem = np.ones((selem_size, selem_size), dtype=np.uint8)
        else:
            raise ValueError("Invalid selem_shape")

        eroded = morphology.erosion(np.array(gray_image), selem)
        return Image.fromarray(eroded)


    def barrel_distortion(self, image, k=-0.3):
        '''
        Barrel distortion effect
        Parameters:
        - image: Image to apply effect
        - k: Distortion coefficient
        Returns:
        - Image with barrel distortion effect
        '''
        width, height = image.size
        fx, fy = width / 2, height / 2
        camera_matrix = np.array([[fx, 0, width / 2], [0, fy, height / 2], [0, 0, 1]], dtype="double")
        dist_coeffs = np.zeros((4, 1))
        dist_coeffs[0, 0] = k
        map1, map2 = cv2.initUndistortRectifyMap(camera_matrix, dist_coeffs, None, camera_matrix, (width, height), 5)
        undistorted_img = cv2.remap(np.array(image), map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return Image.fromarray(undistorted_img)

    def vintage_effect(self, image, vignette_intensity=0.85, color_intensity=0.5):
        '''
        Vintage effect
        Parameters:
        - image: Image to apply effect
        - vignette_intensity: Intensity of the vignette effect
        - color_intensity: Intensity of the color effect
        Returns:
        - Image with vintage effect
        '''
        width, height = image.size
        sepia_filter = ImageOps.colorize(ImageOps.grayscale(image), "#704238", "#C0B283")
        image = Image.blend(image, sepia_filter, color_intensity)

        vignette = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(vignette)
        draw.ellipse((0, 0, width, height), fill=255)
        vignette = vignette.filter(ImageFilter.GaussianBlur(width // 2)).convert("1").point(lambda p: p * vignette_intensity)
        return Image.composite(image, Image.new("RGB", (width, height)), vignette)

    def halftone(self, image, scale=3):
        '''
        Halftone effect
        Parameters:
        - image: Image to apply effect
        - scale: Scale of the halftone effect
        Returns:
        - Image with halftone effect
        '''
        gray_image = ImageOps.grayscale(image)
        np_image = np.array(gray_image)
        halftoned_image = util.img_as_ubyte(util.img_as_float(np_image) > (util.img_as_float(np_image).mean() * scale))
        return Image.fromarray(halftoned_image)
