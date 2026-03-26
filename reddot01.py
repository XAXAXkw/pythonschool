from PIL import Image, ImageDraw

def create_rebel_icon():
    # 1. Dimensions and Rebel Palette
    width, height = 500, 500
    background_color = (0, 128, 0)  # Nakatomi Green
    circle_color = (255, 0, 0)      # Emergency Red
    border_color = (255, 255, 0)    # Warning Yellow
    
    # 2. Create the canvas
    img = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # 3. Draw the Yellow Window Border
    # We draw a rectangle at the very edge of the image
    border_thickness = 15
    draw.rectangle(
        [0, 0, width - 1, height - 1], 
        outline=border_color, 
        width=border_thickness
    )
    
    # 4. Define the circle shape
    # Increased padding so it doesn't hit the new yellow border
    padding = 80
    shape = [padding, padding, width - padding, height - padding]
    
    # 5. Draw the red circle (No white outline)
    # Removing 'outline' and 'width' to keep it a solid red disk
    draw.ellipse(shape, fill=circle_color)
    
    # 6. Finalize
    img.save("rebel_icon_v2.png")
    img.show()
    print("Ventenus Icon: Generated with yellow warning border.")

if __name__ == "__main__":
    create_rebel_icon()