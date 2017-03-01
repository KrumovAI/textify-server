from PIL import Image

from textify.utils.image_processing import *
from textify.utils.contours_processing import *


def stretch_ver(img, baseheight):
    w, h = img.size
    return img.resize((w, baseheight), PIL.Image.ANTIALIAS)


def stretch_hor(img, basewidth):
    w, h = img.size
    return img.resize((basewidth, h), PIL.Image.ANTIALIAS)


def stretch_diagonally_left(img, basewidth):
    img = rotate_left(img, 45)
    img = stretch_hor(img, basewidth)
    img = rotate_right(img, 45)
    return img


def stretch_diagonally_right(img, basewidth):
    img = rotate_right(img, 45)
    img = stretch_hor(img, basewidth)
    img = rotate_left(img, 45)
    return img


def rotate_right(img, angle):
    return img.rotate(angle, expand=True)


def rotate_left(img, angle):
    return img.rotate(-angle, expand=True)


def save_img(img, save_path):
    if os.path.isfile(save_path):
        os.remove(save_path)

    img.save(save_path)


def create_variants(img):
    variants = list()
    variants.append(paste(img, True))
    variants.append(paste(img, True, x_offset=3, y_offset=0))
    variants.append(paste(img, True, x_offset=-3, y_offset=0))
    variants.append(paste(img, True, x_offset=3, y_offset=3))
    variants.append(paste(img, True, x_offset=-3, y_offset=3))
    variants.append(paste(img, True, x_offset=-3, y_offset=-3))
    variants.append(paste(img, True, x_offset=3, y_offset=-3))
    variants.append(paste(img, True, x_offset=0, y_offset=3))
    variants.append(paste(img, True, x_offset=0, y_offset=-3))
    return variants


def generate_data(user_folder):
    for i in range(26):
        path = os.path.join(os.getcwd(), "user_files")
        path = os.path.join(path, os.path.join(user_folder, "handwritten"))
        path = os.path.join(path, str(i))

        for j in range(1, 5):
            filename = path + "\\img-" + str(j) + ".png"
            im = cv2.imread(filename)
            thresh = threshold(im, False)
            contours = get_contours(thresh)
            height, width = im.shape[:2]
            min_x = width - 1
            max_x = 0
            min_y = height - 1
            max_y = 0

            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)

                if min_x > x:
                    min_x = x

                if max_x < (x + w):
                    max_x = x + w

                if min_y > y:
                    min_y = y

                if max_y < (y + h):
                    max_y = y + h

                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

            img_to_crop = Image.open(filename)
            crop = img_to_crop.crop((min_x, min_y, max_x, max_y))
            images = list()
            images.append([resize(crop, 74), 76, 59])
            images.append([resize(crop, 73), 75, 58])
            images.append([resize(crop, 70), 72, 55])
            images.append([resize(crop, 68), 70, 53])
            images.append([resize(crop, 67), 69, 52])
            counter = 1
            full_path = os.path.join(path, "data")

            for image in images:
                basename = os.path.join(full_path, "img-" + str(j) + "-" + str(counter) + "-")
                variant_counter = 0

                for variant in create_variants(image[0]):
                    save_img(expand(variant), basename + str(variant_counter) + ".png")
                    variant_counter += 1

                save_img(expand(paste(stretch_hor(image[0], image[1]), True)),
                         basename + str(variant_counter) + ".png")
                save_img(expand(paste(stretch_ver(image[0], image[2]), True)),
                         basename + str(variant_counter + 1) + ".png")
                save_img(expand(paste(stretch_hor(image[0], image[1] + 3), True)),
                         basename + str(variant_counter + 2) + ".png")
                save_img(expand(paste(stretch_ver(image[0], image[2] + 3), True)),
                         basename + str(variant_counter + 3) + ".png")
                save_img(expand(paste(rotate_right(image[0], 17), True)),
                         basename + str(variant_counter + 4) + ".png")
                save_img(expand(paste(rotate_left(image[0], 17), True)),
                         basename + str(variant_counter + 5) + ".png")
                save_img(expand(paste(rotate_right(image[0], 15), True)),
                         basename + str(variant_counter + 6) + ".png")
                save_img(expand(paste(rotate_left(image[0], 15), True)),
                         basename + str(variant_counter + 7) + ".png")
                save_img(expand(paste(rotate_right(image[0], 10), True)),
                         basename + str(variant_counter + 8) + ".png")
                save_img(expand(paste(rotate_left(image[0], 10), True)),
                         basename + str(variant_counter + 9) + ".png")
                save_img(expand(paste(stretch_diagonally_left(image[0], image[1]), True)),
                         basename + str(variant_counter + 10) + ".png")
                save_img(expand(paste(stretch_diagonally_right(image[0], image[1]), True)),
                         basename + str(variant_counter + 11) + ".png")
                counter += 1
