from PIL import Image
import colors
import time


image_name = 'image.jpg'
make10x10 = True
make20x20 = True
make30x30 = True


def get_image_name(i):
    return f"img/img_{i}.png"


class config:
    def __init__(self, target_name='image.png'):
        self.POPULATION_SIZE = 128

        # Image filling constants
        self.NUM_IMAGES = 842
        self.IMG_SIZE = 10
        self.IMAGES = f"img/img_.png"  # To choose certain photo: IMAGES[:8] + str(i) + IMAGES[8:]

        # Target image constants
        self.TARGET = target_name
        self.tImage = Image.open(self.TARGET)
        self.WIDTH = self.tImage.size[0]
        self.HEIGHT = self.tImage.size[1]

        self.IMG = Image.new('RGB', (self.WIDTH, self.HEIGHT), color='black')


def make_siutable_size(c: config) -> config:
    c_local = c
    if c.WIDTH % c.IMG_SIZE == 0 and c.HEIGHT % c.IMG_SIZE == 0:
        return c
    new_width = c.WIDTH - c.WIDTH % c.IMG_SIZE
    new_height = c.HEIGHT - c.HEIGHT % c.IMG_SIZE

    c_local.WIDTH = new_width
    c_local.HEIGHT = new_height
    c_local.tImage = c_local.tImage.resize((c.WIDTH, c.HEIGHT))
    c_local.IMG = c_local.IMG.resize((c.WIDTH, c.HEIGHT))


def paste_image(target, source, pos, color):
    spix = source.load()
    tpix = target.load()
    for i in range(pos[0], pos[0] + source.size[0]):
        for j in range(pos[1], pos[1] + source.size[1]):
            i1 = i - pos[0]
            j1 = j - pos[1]
            if spix[i1, j1][0] == 0 or spix[i1, j1][1] == 0 or spix[i1, j1][2] == 0:
                # Pixelart: tpix[i, j][0] == 0 or tpix[i, j][1] == 0 or tpix[i, j][2] == 0:
                tpix[i, j] = tuple(color)
            else:
                tpix[i, j] = spix[i - pos[0], j - pos[1]]
    return target


def get_image_from_images(images, c, color_map, folder):
    image = Image.new('RGB', (c.WIDTH, c.HEIGHT), color='black')
    for i in range(c.WIDTH // c.IMG_SIZE):
        for j in range(c.HEIGHT // c.IMG_SIZE):
            image2paste = Image.open(folder + images[i][j] + ".png")
            image2paste = image2paste.resize((c.IMG_SIZE, c.IMG_SIZE))
            image = paste_image(image, image2paste, (i * c.IMG_SIZE, j * c.IMG_SIZE), color_map[images[i][j]])
    return image


def calc_mean_color(pix, n, i=0, j=0):
    colors = [0, 0, 0]  # R G B
    for i1 in range(n):
        for j1 in range(n):
            colors[0] += pix[i + i1, j + j1][0]
            colors[1] += pix[i + i1, j + j1][1]
            colors[2] += pix[i + i1, j + j1][2]
    for i1 in range(3):
        colors[i1] = colors[i1] // (n * n)
    return colors


def find_most_siutable(pix, i, j, n, colors=colors.colors10x10):
    color = calc_mean_color(pix, n, i=i, j=j)
    closest = 256 ** 3
    img = 'img_1'
    for i in colors:
        r, g, b = colors[i]
        loc = abs(color[0] - r) + abs(color[1] - g) + abs(color[2] - b)
        if closest > loc:
            closest = loc
            img = i
    return img


def makeXbyX(c, color_map, result_name, folder):
    print("Start")
    start_time = time.time()
    ans = []
    target = Image.open(c.TARGET)
    pix = target.load()

    for i in range(c.WIDTH // c.IMG_SIZE):
        sub_lst = []
        for j in range(c.HEIGHT // c.IMG_SIZE):
            sub_lst.append(find_most_siutable(pix, i * c.IMG_SIZE, j * c.IMG_SIZE, c.IMG_SIZE, color_map))
        ans.append(sub_lst)
    get_image_from_images(ans, c, color_map, folder).save(result_name)
    print(f"Done. Time {time.time() - start_time} s")


def main():
    c = config(image_name)
    if make10x10:
        c.IMG_SIZE = 10
        makeXbyX(c, colors.colors10x10, 'result10x10.png', 'img10x10/')
    if make20x20:
        c.IMG_SIZE = 10
        makeXbyX(c, colors.colors20x20, 'result20x20.png', 'img20x20/')
    if make30x30:
        c.IMG_SIZE = 30
        makeXbyX(c, colors.colors30x30, 'result30x30.png', 'img30x30/')


def createXbyX_calc_colors():
    f = open('yes.txt', 'wt')
    for i in range(1, 843):
        img = Image.open(f'img/img_{i}.png')
        img10x10 = img.resize((30, 30))
        img10x10.save(f'img30x30/img_{i}.png')

        f.write(f'"img_{i}": {calc_mean_color(img10x10.load(), 30)}, ')


if __name__ == '__main__':
    main()
