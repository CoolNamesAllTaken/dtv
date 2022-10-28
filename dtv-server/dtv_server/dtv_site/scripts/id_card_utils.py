import win32api
import win32print

from PIL import Image, ImageDraw, ImageFont
import math
import os # for file path stuff

PRINTER_ENUM_LEVEL = 2 # list printers on another server

def print_id_card(id_card_file):
    win32api.ShellExecute(0, "print", id_card_file, None,  ".",  0)

# ID card dimensions: 86x54mm
# Zebra P330i resolution: 300dpi, recommended resolution 600dpi+
# @ 1000dpi, image resolution: 3386x2126pixels

ID_CARD_DPI = 600
MM_PER_IN = 25.4
PT_PER_IN = 72
ID_CARD_WIDTH_MM = 86
ID_CARD_HEIGHT_MM = 54
ID_CARD_PHOTO_WIDTH_MM = 25
ID_CARD_PHOTO_HEIGHT_MM = 34
ID_CARD_TEXT_HEIGHT_PT = 6
ID_CARD_FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "arialbd.ttf")
# ID_CARD_LENGTH_PIX = math.ceil(ID_CARD_LENGTH_MM / MM_PER_IN * ID_CARD_DPI)
# ID_CARD_WIDTH_PIX = math.ceil(ID_CARD_WIDTH_MM / MM_PER_IN * ID_CARD_DPI)

def pix2mm(pix):
    return int(pix/ID_CARD_DPI*MM_PER_IN)

def mm2pix(mm):
    return int(mm/MM_PER_IN*ID_CARD_DPI)

def assemble_id_card_image(
    output_path,
    license_number="AXXXXXXX",
    first_name="Im",
    costume_name="Batman",
    id_photo_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "toaster.jpg"),
    issued_date="MM/DD/YYYY",
    expiration_date="MM/DD/YYYY",
    treat_class="ID",
    treat_weight_oz="00.0 oz",
    treat_length_in="12.3",
    favorite_number="1234567890",
    id_card_template_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "dtv_card_front_600dpi.png")
    ):

    # Crop ID photo to 34x25mm
    id_photo = Image.open(id_photo_path)
    id_photo_width, id_photo_height = id_photo.size
    left = id_photo_width / 2 - mm2pix(ID_CARD_PHOTO_WIDTH_MM / 2)
    right = id_photo_width / 2 + mm2pix(ID_CARD_PHOTO_WIDTH_MM / 2)
    bottom = id_photo_height / 2 + mm2pix(ID_CARD_PHOTO_HEIGHT_MM / 2)
    top = id_photo_height / 2 - mm2pix(ID_CARD_PHOTO_HEIGHT_MM / 2)
    id_photo_cropped = id_photo.crop((left, top, right, bottom))
    # id_photo_cropped.show()

    id_card = Image.open(id_card_template_path)
    id_card_canvas = ImageDraw.Draw(id_card)
    id_card_fontsize_pix = math.ceil(ID_CARD_TEXT_HEIGHT_PT / PT_PER_IN * ID_CARD_DPI)
    id_card_font_small = ImageFont.truetype(ID_CARD_FONT_PATH, id_card_fontsize_pix) # Bold 6pt Arial font
    id_card_font_medium = ImageFont.truetype(ID_CARD_FONT_PATH, int(1.3*id_card_fontsize_pix))
    id_card_font_large = ImageFont.truetype(ID_CARD_FONT_PATH, int(1.7*id_card_fontsize_pix))
    # print("{} {} fontsize: {}".format(mm2pix(29.6+2.5), mm2pix(13.7), 1.5*id_card_fontsize_pix))

    id_card_canvas.text((mm2pix(32.1+1), mm2pix(15.3)), license_number.upper(), font=id_card_font_large, fill=(200, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(33.7+1), mm2pix(19.2)), expiration_date.upper(), font=id_card_font_medium, fill=(200, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(32.4+1), mm2pix(23.1)), costume_name.upper(), font=id_card_font_medium, fill=(0, 0, 0), anchor='ls')
    id_card_canvas.text((mm2pix(32.4+1), mm2pix(26)), first_name.upper(), font=id_card_font_medium, fill=(0, 0, 0), anchor='ls')
    # TODO: finish adding text fields, add DOB with slashes removed, add grayscale id photo
    id_card.show()


# NOTE: This script requires a PDF reader with shell extensions (like Foxit) to be installed and set as the default PDF reader!
def main():
    print ("{} x {}".format(mm2pix(ID_CARD_WIDTH_MM), mm2pix(ID_CARD_HEIGHT_MM)))
    assemble_id_card_image("fake")
    # # A List containing the system printers
    # all_printers = [printer[2] for printer in win32print.EnumPrinters(PRINTER_ENUM_LEVEL)]
    # # Ask the user to select a printer
    # printer_num = int(input("Choose a printer:\n"+"\n".join([f"{n} {p}" for n, p in enumerate(all_printers)])+"\n"))
    # # set the default printer
    # win32print.SetDefaultPrinter(all_printers[printer_num])
    # print_id_card("dtv_letter_card.pdf")



if __name__ == "__main__":
    main()