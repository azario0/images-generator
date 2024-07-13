import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import random
import colorsys

def generate_gradient_image(width, height, start_color, end_color):
    # Create a new image with the given dimensions
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # Calculate color step for each pixel
    r_step = (end_color[0] - start_color[0]) / width
    g_step = (end_color[1] - start_color[1]) / width
    b_step = (end_color[2] - start_color[2]) / width

    # Draw gradient
    for x in range(width):
        r = int(start_color[0] + r_step * x)
        g = int(start_color[1] + g_step * x)
        b = int(start_color[2] + b_step * x)
        draw.line([(x, 0), (x, height)], fill=(r, g, b))

    return image
def generate_random_image(width, height, num_shapes):
    # Create a new image with a random background color
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Define shape types
    shapes = ['rectangle', 'ellipse', 'line']

    # Draw random shapes
    for _ in range(num_shapes):
        shape = random.choice(shapes)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Random coordinates
        x1 = random.randint(0, width - 1)
        y1 = random.randint(0, height - 1)
        x2 = random.randint(x1, width)
        y2 = random.randint(y1, height)

        if shape == 'rectangle':
            draw.rectangle([x1, y1, x2, y2], fill=color)
        elif shape == 'ellipse':
            draw.ellipse([x1, y1, x2, y2], fill=color)
        elif shape == 'line':
            draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 5))

    return image

def generate_matching_color(base_color, variation=0.2):
    h, s, v = colorsys.rgb_to_hsv(*[x/255.0 for x in base_color])
    h = (h + random.uniform(-variation, variation)) % 1.0
    s = max(0, min(1, s + random.uniform(-variation, variation)))
    v = max(0, min(1, v + random.uniform(-variation, variation)))
    return tuple(int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v))

def generate_random_image_matching_colors(width, height, num_shapes):
    # Create a new image with a random base color
    base_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(image)

    # Define shape types
    shapes = ['rectangle', 'ellipse', 'line']

    # Draw random shapes
    for _ in range(num_shapes):
        shape = random.choice(shapes)
        color = generate_matching_color(base_color)

        # Random coordinates
        x1 = random.randint(0, width - 1)
        y1 = random.randint(0, height - 1)
        x2 = random.randint(x1, width)
        y2 = random.randint(y1, height)

        if shape == 'rectangle':
            draw.rectangle([x1, y1, x2, y2], fill=color)
        elif shape == 'ellipse':
            draw.ellipse([x1, y1, x2, y2], fill=color)
        elif shape == 'line':
            draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 5))

    return image
def generate_random_image_with_watermark(width, height, num_shapes, watermark_text):
    # Create a new image with a random base color
    base_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(image)

    # Define shape types
    shapes = ['rectangle', 'ellipse', 'line']

    # Draw random shapes
    for _ in range(num_shapes):
        shape = random.choice(shapes)
        color = generate_matching_color(base_color)

        # Random coordinates
        x1 = random.randint(0, width - 1)
        y1 = random.randint(0, height - 1)
        x2 = random.randint(x1, width)
        y2 = random.randint(y1, height)

        if shape == 'rectangle':
            draw.rectangle([x1, y1, x2, y2], fill=color)
        elif shape == 'ellipse':
            draw.ellipse([x1, y1, x2, y2], fill=color)
        elif shape == 'line':
            draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 5))

    # Add watermark
    font_size = int(height / 20)  # Adjust font size based on image height
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Get text bounding box
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((width - text_width) / 2, height - text_height - 10)

    # Draw text outline
    outline_color = (0, 0, 0)  # Black outline
    for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
        draw.text((text_position[0] + offset[0], text_position[1] + offset[1]),
                  watermark_text, font=font, fill=outline_color)

    # Draw main text
    text_color = (255, 255, 255)  # White text
    draw.text(text_position, watermark_text, font=font, fill=text_color)

    return image

def main():
    st.title("Image Generator")


    tab1, tab2, tab3, tab4 = st.tabs(["Gradient Image", "Random Shape Image", "Matching Colors Image", "Watermarked Image"])


    with tab1:
        st.header("Gradient Image Generator")

        # Input for image dimensions
        width = st.number_input("Width", min_value=1, max_value=1000, value=300, key="gradient_width")
        height = st.number_input("Height", min_value=1, max_value=1000, value=200, key="gradient_height")

        # Input for start and end colors
        start_color = st.color_picker("Start Color", "#FF0000")
        end_color = st.color_picker("End Color", "#0000FF")

        # Convert hex colors to RGB tuples
        start_rgb = tuple(int(start_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        end_rgb = tuple(int(end_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        # Generate and display the image
        if st.button("Generate Gradient"):
            image = generate_gradient_image(width, height, start_rgb, end_rgb)
            st.image(image, caption="Generated Gradient", use_column_width=True)

            # Save image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Download button
            st.download_button(
                label="Download Gradient Image",
                data=img_byte_arr,
                file_name="gradient.png",
                mime="image/png"
            )

    with tab2:
        st.header("Random Shape Image Generator")

        # Input for image dimensions and number of shapes
        width = st.number_input("Width", min_value=1, max_value=1000, value=400, key="random_width")
        height = st.number_input("Height", min_value=1, max_value=1000, value=300, key="random_height")
        num_shapes = st.number_input("Number of Shapes", min_value=1, max_value=100, value=10)

        # Generate and display the image
        if st.button("Generate Random Shape Image"):
            image = generate_random_image(width, height, num_shapes)
            st.image(image, caption="Generated Random Shape Image", use_column_width=True)

            # Save image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Download button
            st.download_button(
                label="Download Random Shape Image",
                data=img_byte_arr,
                file_name="random_shapes.png",
                mime="image/png"
            )
    with tab3:
        st.header("Matching Colors Image Generator")

        # Input for image dimensions and number of shapes
        width = st.number_input("Width", min_value=1, max_value=1000, value=400, key="matching_width")
        height = st.number_input("Height", min_value=1, max_value=1000, value=300, key="matching_height")
        num_shapes = st.number_input("Number of Shapes", min_value=1, max_value=100, value=15, key="matching_shapes")

        # Generate and display the image
        if st.button("Generate Matching Colors Image"):
            image = generate_random_image_matching_colors(width, height, num_shapes)
            st.image(image, caption="Generated Matching Colors Image", use_column_width=True)

            # Save image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Download button
            st.download_button(
                label="Download Matching Colors Image",
                data=img_byte_arr,
                file_name="matching_colors.png",
                mime="image/png"
            )
    
    with tab4:
        st.header("Watermarked Image Generator")

        # Input for image dimensions and number of shapes
        width = st.number_input("Width", min_value=1, max_value=1000, value=400, key="watermark_width")
        height = st.number_input("Height", min_value=1, max_value=1000, value=300, key="watermark_height")
        num_shapes = st.number_input("Number of Shapes", min_value=1, max_value=100, value=15, key="watermark_shapes")
        watermark_text = st.text_input("Watermark Text", "Made by Benmalek Zohir")

        # Generate and display the image
        if st.button("Generate Watermarked Image"):
            image = generate_random_image_with_watermark(width, height, num_shapes, watermark_text)
            st.image(image, caption="Generated Watermarked Image", use_column_width=True)

            # Save image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Download button
            st.download_button(
                label="Download Watermarked Image",
                data=img_byte_arr,
                file_name="watermarked_image.png",
                mime="image/png"
            )


if __name__ == "__main__":
    main()