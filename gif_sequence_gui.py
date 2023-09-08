import os
from tkinter import Label, Canvas, Button
from PIL import Image, ImageSequence, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

def process_gif(gif_path):
    with Image.open(gif_path) as img:
        frames = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(img)]
        
        for frame in frames:
            datas = frame.getdata()
            new_data = []

            target_color = (4, 254, 68)  # The RGB equivalent of #04fe44 just a green
            for item in datas:
                if item[0:3] == target_color:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)

            frame.putdata(new_data)

        widths, heights = zip(*(frame.size for frame in frames))
        total_width = sum(widths)
        max_height = max(heights)

        new_img = Image.new('RGBA', (total_width, max_height))

        x_offset = 0
        for frame in frames:
            new_img.paste(frame, (x_offset, 0), mask=frame)
            x_offset += frame.width

        output_path = os.path.splitext(gif_path)[0] + "_processed.png"
        new_img.save(output_path)
        return new_img

def drop(event):
    filepath = event.data
    processed_img = process_gif(filepath)
    
    # Resize the image if it's too large for display
    MAX_SIZE = (400, 400)
    processed_img.thumbnail(MAX_SIZE)
    
    # Convert to PhotoImage and display in the GUI
    photo = ImageTk.PhotoImage(processed_img)
    image_canvas.create_image(0, 0, anchor='nw', image=photo)
    image_canvas.image = photo  # Keep a reference to avoid garbage collection

root = TkinterDnD.Tk()
root.title("GIF Processor")
root.geometry("450x450")

label = Label(root, text="Drag and drop your GIF here!", pady=10)
label.pack(pady=10)

image_canvas = Canvas(root, bg="white")
image_canvas.pack(fill="both", expand=True, padx=10, pady=10)

button = Button(root, text="Quit", command=root.quit)
button.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.mainloop()
