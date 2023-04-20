import io
from PIL import Image
import streamlit as st
from image_effects import ImageEffects, ImageOps
import time


def apply_glitch_effects(
    image,
    block_size,
    glitch_chance,
    color_scale,
    overlay,
    effects_order,
    num_colors,
    kaleidoscope_slices,
    kaleidoscope_angle,
    kaleidoscope_slice_angle,
    grain_size,
    noise_type,
    sigma,
    levels,
    selem_shape,
    selem_size,
    k,
    vignette_intensity,
    color_intensity,
    scale
):
    '''
    Applies the glitch effects to the image.
    Parameters:
    - block_size: The size of the glitched blocks.
    - glitch_chance: The chance of a glitch happening.
    - color_scale: The scale of the color effect.
    - overlay: The overlay effect.
    - effects_order: The order of the effects.
    - num_colors: The number of colors to reduce the image to.
    - kaleidoscope_slices: The number of slices in the kaleidoscope effect.
    - kaleidoscope_angle: The angle of the kaleidoscope effect.
    - kaleidoscope_slice_angle: The angle of the slices in the kaleidoscope effect.
    - grain_size: The size of the noise.
    - noise_type: The type of noise to add.
    '''

    for effect in effects_order:
        if effect == "pixelate":
            image = image_effects.pixelate(image, block_size)
        elif effect == "color_scale":
            image = image_effects.color_scale_effect(image, color_scale)
        elif effect == "overlay":
            image = image_effects.overlay_effect(image, overlay)
        elif effect == "horizontal_glitch":
            image = image_effects.horizontal_glitch(image, block_size, glitch_chance)
        elif effect == "vertical_glitch":
            image = image_effects.vertical_glitch(image,block_size, glitch_chance)
        elif effect == "reduce_colors":
            image = image_effects.reduce_colors(image, num_colors)
        elif effect == "kaleidoscope":
            image = image_effects.kaleidoscope_effect(image, kaleidoscope_slices, kaleidoscope_angle, kaleidoscope_slice_angle)
        elif effect == "noise":
            image = image_effects.noise(image, grain_size, noise_type)
        elif effect == "edges":
            image = image_effects.edge_detection(image,sigma)
        elif effect == "posterize":
            image = ImageOps.posterize(image, levels)
        elif effect == "erosion":
            image = image_effects.erosion(image, selem_shape, selem_size)
        elif effect == "barrel_distortion":
            image = image_effects.barrel_distortion(image, k)
        elif effect == "vintage_effect":
            image = image_effects.vintage_effect(image, vignette_intensity, color_intensity)
        elif effect == "halftone":
            image = image_effects.halftone(image, scale)
    return image

st.title("Glitch Art Generator")

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file).convert("RGB")
    image_effects = ImageEffects(input_image)
    st.image(input_image, caption="Input Image", use_column_width=True)

    with st.sidebar.expander("Parameters"):
        block_size = st.slider("Pixelate Block size", 1, 100, 10, key="block_size")
        glitch_chance = st.slider("Glitch chance", 0.0, 1.0, 0.1, 0.01, key="glitch_chance")
    
    with st.sidebar.expander("Kaleidoscope"):
        kaleidoscope_slices = st.slider("Number of slices", 2, 20, 8, key="kaleidoscope_slices")
        kaleidoscope_angle = st.slider("Rotation angle", 0, 360, 0, key="kaleidoscope_angle")
        kaleidoscope_slice_angle = st.slider("Slice angle", 0, 360, 360, key="kaleidoscope_slice_angle")

    with st.sidebar.expander("Noise"):
        grain_size = st.slider("Grain size", 1, 100, 10, key="grain_size")
        noise_type = st.selectbox("Noise type", ["grain", "speckle","gaussian", "s&p", "poisson"])

    with st.sidebar.expander("Color"):
        color_scale = st.selectbox(
            "Color scale",
            [
                "none",
                "grayscale",
                "sepia",
                "magma",
                "inferno",
                "plasma",
                "viridis",
                "cividis",
                "rocket",
                "mako",
                "turbo",
            ],
        )
        overlay = st.selectbox("Overlay", ["none", "vignette", "light_leak"])
        num_colors = st.slider(" Number of colors", 1, 100, 6, key="num_colors")

    with st.sidebar.expander("Edges"):
        sigma = st.slider("Sigma", 0.0, 10.0, 1.0, 0.1, key="sigma")

    with st.sidebar.expander("Posterize"):
        levels = st.slider("Levels", 1, 10, 4, key="levels")

    with st.sidebar.expander("Erosion"):
        selem_shape = st.selectbox("Selem Shape", ["disk", "square", "cube"])
        selem_size = st.slider("Selem Size", min_value=1, max_value=20, value=5)  # Adjust the min, max, and default values as needed

    with st.sidebar.expander("Barrel Distortion"):
        k = st.slider("K", 0.0, 10.0, 1.0, 0.1, key="k")

    with st.sidebar.expander("Vintage Effect"):
        vignette_intensity = st.slider("Vignette Intensity", 0.0, 10.0, 1.0, 0.1, key="vignette_intensity")
        color_intensity = st.slider("Color Intensity", 0.0, 10.0, 1.0, 0.1, key="color_intensity")

    with st.sidebar.expander("Halftone"):
        scale = st.slider("Scale", 1, 100, 10, key="scale")


    effects_order = st.sidebar.multiselect(
        "Effects order",
        options=[
            "pixelate",
            "horizontal_glitch",
            "vertical_glitch",
            "color_scale",
            "overlay",
            "reduce_colors",
            "kaleidoscope",
            "noise",
            "edges",
            "posterize",
            "unsharp_mask",
            "erosion",
            "barrel_distortion",
            "vintage_effect",
            "halftone",
        ],
        default=["pixelate", "horizontal_glitch"],
    )

    apply_glitch = st.button("Apply Glitch Effects")
    keep_glitching = st.button("Keep Glitching")

    if apply_glitch:
        glitched_image = apply_glitch_effects(
            input_image.copy(),
            block_size,
            glitch_chance,
            color_scale,
            overlay,
            effects_order,
            num_colors,
            kaleidoscope_slices,
            kaleidoscope_angle,
            kaleidoscope_slice_angle,
            grain_size,
            noise_type,
            sigma,
            levels,
            selem_shape,
            selem_size,
            k,
            vignette_intensity,
            color_intensity,
            scale
        )
        st.image(glitched_image, caption="Glitched Image", use_column_width=True)

        buffer = io.BytesIO()
        glitched_image.save(buffer, format="PNG")
        st.download_button(
            "Download Glitched Image",
            buffer.getvalue(),
            "glitched_image.png",
            "image/png",
        )
    
    if keep_glitching:
        output_image = st.empty()
        breakoff = st.button("Stop Glitching")
        if breakoff:
            st.stop()
        while True:
            glitched_image = apply_glitch_effects(
                input_image.copy(),
                block_size,
                glitch_chance,
                color_scale,
                overlay,
                effects_order,
                num_colors,
                kaleidoscope_slices,
                kaleidoscope_angle,
                kaleidoscope_slice_angle,
                grain_size,
                noise_type,
                sigma,
                levels,
                selem_shape,
                selem_size,
                k,
                vignette_intensity,
                color_intensity,
                scale
            )
        
            output_image.image(glitched_image, caption="Glitched Image", use_column_width=True)
        
            time.sleep(0.005)
