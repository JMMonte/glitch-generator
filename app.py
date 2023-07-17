import io
from PIL import Image
import streamlit as st
from image_effects import ImageEffects
from PIL import Image, ImageOps
import imageio
import base64
import random

def randomize_parameters():
    '''
    Returns a dictionary with randomized parameters for the glitch effects.
    '''
    parameters = {}
    parameters['block_size'] = random.randint(1, 100)
    parameters['glitch_chance'] = random.uniform(0.0, 1.0)
    parameters['color_scale'] = random.choice(
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
        ]
    )
    parameters['overlay'] = random.choice(["none", "vignette", "light_leak"])
    parameters['effects_order'] = random.sample(
        [
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
        k=random.randint(1, 15),
    )
    parameters['num_colors'] = random.randint(1, 100)
    parameters['kaleidoscope_slices'] = random.randint(2, 20)
    parameters['kaleidoscope_angle'] = random.randint(0, 360)
    parameters['kaleidoscope_slice_angle'] = random.randint(0, 360)
    parameters['grain_size'] = random.randint(1, 100)
    parameters['noise_type'] = random.choice(["grain", "speckle","gaussian", "s&p", "poisson"])
    parameters['sigma'] = random.uniform(0.0, 10.0)
    parameters['levels'] = random.randint(1, 10)
    parameters['selem_shape'] = random.choice(["disk", "square", "cube"])
    parameters['selem_size'] = random.randint(1, 20)
    parameters['k'] = random.uniform(0.0, 10.0)
    parameters['vignette_intensity'] = random.uniform(0.0, 10.0)
    parameters['color_intensity'] = random.uniform(0.0, 10.0)
    parameters['scale'] = random.randint(1, 100)

    return parameters


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

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file).convert("RGB")
    st.write(f"Image mode: {input_image.mode}") 
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
    randomize = st.button("Randomize Effects")
    apply_glitch = st.button("Apply Glitch Effects")
    gif_glitch = st.button("Create GIF glitch")

    if randomize:
        randomized_parameters = randomize_parameters()
        
        block_size = randomized_parameters['block_size']
        glitch_chance = randomized_parameters['glitch_chance']
        color_scale = randomized_parameters['color_scale']
        overlay = randomized_parameters['overlay']
        effects_order = randomized_parameters['effects_order']
        num_colors = randomized_parameters['num_colors']
        kaleidoscope_slices = randomized_parameters['kaleidoscope_slices']
        kaleidoscope_angle = randomized_parameters['kaleidoscope_angle']
        kaleidoscope_slice_angle = randomized_parameters['kaleidoscope_slice_angle']
        grain_size = randomized_parameters['grain_size']
        noise_type = randomized_parameters['noise_type']
        sigma = randomized_parameters['sigma']
        levels = randomized_parameters['levels']
        selem_shape = randomized_parameters['selem_shape']
        selem_size = randomized_parameters['selem_size']
        k = randomized_parameters['k']
        vignette_intensity = randomized_parameters['vignette_intensity']
        color_intensity = randomized_parameters['color_intensity']
        scale = randomized_parameters['scale']
        
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
        
        st.image(glitched_image, caption="Randomly Glitched Image", use_column_width=True)

        buffer = io.BytesIO()
        glitched_image.save(buffer, format="PNG")
        st.download_button(
            "Download Randomly Glitched Image",
            buffer.getvalue(),
            "randomly_glitched_image.png",
            "image/png",
        )
        

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
    
    if gif_glitch:
        images_list = []
        for _ in range(25):
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
            images_list.append(glitched_image)

        # Save the images as a GIF using imageio
        gif_buffer = io.BytesIO()
        images_as_bytes = []
        for image in images_list:
            img_buffer = io.BytesIO()
            imageio.imwrite(img_buffer, image, format="PNG")
            images_as_bytes.append(img_buffer.getvalue())
        
        imageio.mimsave(gif_buffer, [imageio.imread(img_bytes) for img_bytes in images_as_bytes], format="GIF", duration=0.1)

        # Reset buffer cursor to the beginning
        gif_buffer.seek(0)

        # Convert GIF bytes to base64 and display using HTML img tag
        gif_base64 = base64.b64encode(gif_buffer.getvalue()).decode("utf-8")
        st.markdown(f'<img src="data:image/gif;base64,{gif_base64}" alt="Glitched Image" style="max-width:100%;">', unsafe_allow_html=True)

        # Offer the option to download the GIF
        st.download_button(
            "Download Glitched Image",
            gif_buffer.getvalue(),
            "glitched_image.gif",
            "image/gif",
        )

