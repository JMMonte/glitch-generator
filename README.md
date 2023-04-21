# Glitch Art Generator

![Glitch Art Generator](/assets/Screenshot%202023-04-21%20at%2001.32.32.png)

|  |  |
|:-------------------------:|:-------------------------:|
![Glitch Art Generator](/assets/download%20(1).gif)  |  ![Glitch Art Generator](/assets/download%20(4).gif) |
![Glitch Art Generator](/assets/download%20(2).gif)  |  ![Glitch Art Generator](/assets/download%20(3).gif) |

Glitch Art Generator is an interactive image manipulation tool that allows you to apply various glitch effects to your images using a user-friendly interface. The tool is built using Streamlit and the Python Image Library (PIL) to process images.

## Features

- Upload images in PNG, JPG, or JPEG format
- Apply multiple glitch effects in a user-specified order
- Modify effect parameters through sliders and selection boxes
- Preview the glitched image before downloading
- Download the glitched image in PNG format
- Keep glitching option for continuous glitch effects

## Effects

- Pixelate
- Horizontal glitch
- Vertical glitch
- Color scale (Grayscale, Sepia, etc.)
- Overlay (Vignette, Light Leak)
- Reduce colors
- Kaleidoscope
- Noise (Grain, Speckle, Gaussian, S&P, Poisson)
- Edge detection
- Posterize
- Erosion
- Barrel distortion
- Vintage effect
- Halftone

## Usage

1. Install the required packages using pip:

    ```bash
    pip install streamlit Pillow
    ````

2. Clone the repository or copy the code into a Python file (e.g., `app.py`).
3. Run the Streamlit app using the following command:

    ```bash
    streamlit run app.py
    ```

4. Access the app via the link provided in the terminal.

## Note

The code provided in the question is the main application code for the Glitch Art Generator. Ensure that you have the required `image_effects.py` file in your working directory, which contains the `ImageEffects` class and the corresponding image manipulation functions.
