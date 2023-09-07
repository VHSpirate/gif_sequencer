from PIL import Image, ImageSequence

def gif_to_side_by_side_png(gif_path, output_path):
    with Image.open(gif_path) as img:
        frames = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(img)]
        
        for frame in frames:
            datas = frame.getdata()
            new_data = []

            target_color = (4, 254, 4)  # The RGB equivalent of #04fe44
            for item in datas:
                # Change all occurrences of the target color to transparent
                if item[0:3] == target_color:
                    new_data.append((255, 255, 255, 0))  # Fully transparent
                else:
                    new_data.append(item)
            
            frame.putdata(new_data)

        widths, heights = zip(*(frame.size for frame in frames))
        total_width = sum(widths)
        max_height = max(heights)

        new_img = Image.new('RGBA', (total_width, max_height))

        x_offset = 0
        for frame in frames:
            new_img.paste(frame, (x_offset, 0), mask=frame)  # Using mask to respect transparency
            x_offset += frame.width

        new_img.save(output_path)

# Example usage
gif_path = "sprDogEat.gif"
output_path = "output_image.png"
gif_to_side_by_side_png(gif_path, output_path)
