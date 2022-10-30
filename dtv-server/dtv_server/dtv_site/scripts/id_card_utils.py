import win32api
import win32print

from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import os # for file path stuff
import yaml # for config stuff

import base64 # for encoding license images

config_dict = {}

PRINTER_ENUM_LEVEL = 2 # list printers on another server

# ID card dimensions: 86x54mm
# Zebra P330i resolution: 300dpi, recommended resolution 600dpi+
ID_CARD_DPI = 600
ID_CARD_GLOBAL_X_OFFSET_MM = 1
MM_PER_IN = 25.4
PT_PER_IN = 72
ID_CARD_WIDTH_MM = 86
ID_CARD_HEIGHT_MM = 54
ID_CARD_PHOTO_WIDTH_MM = 25
ID_CARD_PHOTO_HEIGHT_MM = 34
ID_CARD_TEXT_HEIGHT_PT = 6
ID_CARD_FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "arialbd.ttf")
ID_CARD_WATERMARK_OPACITY = 0.4
ID_CARD_WATERMARK_HEIGHT_MM = 12.5
ID_CARD_WATERMARK_WIDTH_MM = ID_CARD_WATERMARK_HEIGHT_MM / ID_CARD_PHOTO_HEIGHT_MM * ID_CARD_PHOTO_WIDTH_MM
ID_CARD_TEMPLATE_IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "dtv_card_front_600dpi.png")

"""Public Functions"""

def assemble_id_card_image(
    output_path,
    save_pdf=True,
    license_number="A1234567",
    first_name="Im",
    costume_name="Batman",
    id_photo_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "toaster.jpg"),
    issued_date="01/02/1234",
    expiration_date="01/01/1970",
    treat_class="ID",
    treat_weight="00.0 oz",
    treat_length="12.3 in",
    favorite_number="1234567890",
    treat_wrapper_color="WHT",
    treat_exterior_flavor="PLAS",
    treat_interior_flavor="PLAS",
    issuer_code="123FK",
    id_card_template_path=ID_CARD_TEMPLATE_IMAGE_PATH
    ):
    """
    @brief Builds and ID card PNG and optional PDF file from text fields and image files.
    """

    print("Assembling ID card at {}.".format(output_path))

    # Field pre-processing
    expiration_date_no_slashes = "".join(c for c in expiration_date if c.isdigit())

    # Set up for putting text onto ID card
    id_card = Image.open(id_card_template_path)

     # Crop ID photo to 34x25mm
    id_photo = Image.open(id_photo_path)
    id_photo_width, id_photo_height = id_photo.size
    if (id_photo_height < mm2pix(ID_CARD_PHOTO_HEIGHT_MM)):
        # ID photo is not tall enough, needs to be upscaled
        scale_factor = mm2pix(ID_CARD_PHOTO_HEIGHT_MM) / id_photo_height
        id_photo = id_photo.resize((int(scale_factor*id_photo_width), int(scale_factor*id_photo_height)), resample=Image.BOX)
        id_photo_width, id_photo_height = id_photo.size
    # ignoring the "width too small" case since that's rare

    left = id_photo_width / 2 - mm2pix(ID_CARD_PHOTO_WIDTH_MM / 2)
    right = id_photo_width / 2 + mm2pix(ID_CARD_PHOTO_WIDTH_MM / 2)
    bottom = id_photo_height / 2 + mm2pix(ID_CARD_PHOTO_HEIGHT_MM / 2)
    top = id_photo_height / 2 - mm2pix(ID_CARD_PHOTO_HEIGHT_MM / 2)
    id_photo_cropped = id_photo.crop((left, top, right, bottom))

    # Insert ID photo
    id_card.paste(id_photo_cropped, (mm2pix(3.9+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(9.6)))

    # Add ID photo as watermark
    id_photo_watermark = ImageOps.grayscale(id_photo_cropped).convert("RGBA")
    watermark_size_ratio = ID_CARD_WATERMARK_HEIGHT_MM / ID_CARD_PHOTO_HEIGHT_MM
    id_photo_watermark_size = (mm2pix(ID_CARD_WATERMARK_WIDTH_MM), mm2pix(ID_CARD_WATERMARK_HEIGHT_MM))
    id_photo_watermark.thumbnail(id_photo_watermark_size)
    id_photo_watermark.putalpha(int(ID_CARD_WATERMARK_OPACITY * 255))
    id_card.paste(id_photo_watermark, (mm2pix(57+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(30)), id_photo_watermark)

    id_card_canvas = ImageDraw.Draw(id_card)
    id_card_fontsize_pix = math.ceil(ID_CARD_TEXT_HEIGHT_PT / PT_PER_IN * ID_CARD_DPI)
    id_card_font_smaller = ImageFont.truetype(ID_CARD_FONT_PATH, int(0.8*id_card_fontsize_pix))
    id_card_font_small = ImageFont.truetype(ID_CARD_FONT_PATH, id_card_fontsize_pix) # Bold 6pt Arial font
    id_card_font_medium = ImageFont.truetype(ID_CARD_FONT_PATH, int(1.3*id_card_fontsize_pix))
    id_card_font_large = ImageFont.truetype(ID_CARD_FONT_PATH, int(1.7*id_card_fontsize_pix))

    id_card_canvas.text((mm2pix(32.1+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(15.3)), license_number.upper(), font=id_card_font_large, fill=(200, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(33.7+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(19.2)), expiration_date.upper(), font=id_card_font_medium, fill=(200, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(32.4+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(23.1)), costume_name.upper(), font=id_card_font_medium, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(32.4+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(26)), first_name.upper(), font=id_card_font_medium, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(34.2+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(34.2)), favorite_number.upper(), font=id_card_font_medium, fill=(200, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(65.7+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(13.8)), treat_class.upper(), font=id_card_font_small, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(43.1+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(44.9)), treat_wrapper_color.upper(), font=id_card_font_small, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(57.3+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(44.9)), treat_exterior_flavor.upper(), font=id_card_font_small, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(72.1+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(44.9)), treat_interior_flavor.upper(), font=id_card_font_small, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(43.1+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(47.4)), treat_length, font=id_card_font_small, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(57.3+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(47.4)), treat_weight, font=id_card_font_small, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(70+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(34.2+3)), expiration_date_no_slashes.upper(), font=id_card_font_small, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(71.8+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(48.3+2)), issued_date.upper(), font=id_card_font_small, fill=(0, 0, 0), anchor='ls')

    dd_text = issued_date + issuer_code.upper() + "/" + config_dict["dd_info"]["dtv_code"].upper() + "/" + expiration_date[-4:-2]
    id_card_canvas.text((mm2pix(41.2+1+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(50.3)), dd_text, font=id_card_font_smaller, fill=(0, 0, 0), anchor='ls')

    id_card_canvas.text((mm2pix(29.7+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(28.8)), config_dict["dd_info"]["treat_license_address_line_1"].upper(), font=id_card_font_small, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(29.7+ID_CARD_GLOBAL_X_OFFSET_MM), mm2pix(31.2)), config_dict["dd_info"]["treat_license_address_line_2"].upper(), font=id_card_font_small, fill=(0, 0, 0), anchor='ls')

    # id_card.show()
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    id_card.save(output_path)
    if save_pdf:
        id_card.save(os.path.splitext(output_path)[0] + ".pdf")

def encode_id_card_image(image_path):
    """
    @brief Returns a base64 encloded string of an image at a given path, or the blank ID card image if the image is not found.
    """
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
    except:
        with open(ID_CARD_TEMPLATE_IMAGE_PATH, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
    return image_data
    

def print_id_card(id_card_pdf_path):
    """
    @brief Prints an ID card given a path to a PDF file.
    """
    print("Printing ID Card: {}".format(id_card_pdf_path))
    win32api.ShellExecute(0, "print", id_card_pdf_path, None,  ".",  0)

def initialize_id_printer():
    read_config()
    set_default_printer()

"""Private Utility Functions"""

def pix2mm(pix):
    return int(pix/ID_CARD_DPI*MM_PER_IN)

def mm2pix(mm):
    return int(mm/MM_PER_IN*ID_CARD_DPI)

def set_default_printer():
    # First, try setting default printer to match the name provided in the config file.
    all_printers = [printer[2] for printer in win32print.EnumPrinters(PRINTER_ENUM_LEVEL)]
    for printer_num, printer in enumerate(all_printers):
        if printer == config_dict["printer"]:
            print("Found printer name from config file, setting default printer to {}.".format(printer))
            win32print.SetDefaultPrinter(all_printers[printer_num])
            return
            
    # Ask the user to select a printer
    printer_num = int(input("Choose a printer:\n"+"\n".join([f"{n} {p}" for n, p in enumerate(all_printers)])+"\n"))
    # set the default printer
    win32print.SetDefaultPrinter(all_printers[printer_num])
    print("Manually set default printer to {}.".format(all_printers[printer_num]))

def read_config():
    global config_dict
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config", "id_card_config.yaml")) as f:
        config_dict = yaml.safe_load(f)
        # print(config_dict)

# NOTE: This script requires a PDF reader with shell extensions (like Foxit) to be installed and set as the default PDF reader!
def main():
    read_config()
    set_default_printer()
    id_card_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "outputs")
    assemble_id_card_image("{}/test.png".format(id_card_dir))
    print(encode_image(id_card_dir + "/test.png"))
    

    # print_id_card(os.path.join(id_card_dir, "test.pdf"))



if __name__ == "__main__":
    main()