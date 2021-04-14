from PIL import Image
import random

image_name = 'image.png'


class config:
    def __init__(self, target_name=image_name):
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


def get_image_name(i):
    return f"img10x10/img_{i}.png"


def make_siutable_size(c: config) -> config:  # If we have wrong size it will make in devideble in chunks
    c_local = c
    if c.WIDTH % c.IMG_SIZE == 0 and c.HEIGHT % c.IMG_SIZE == 0:
        return c
    new_width = c.WIDTH - c.WIDTH % c.IMG_SIZE
    new_height = c.HEIGHT - c.HEIGHT % c.IMG_SIZE

    c_local.WIDTH = new_width
    c_local.HEIGHT = new_height
    c_local.tImage = c_local.tImage.resize((c.WIDTH, c.HEIGHT))
    c_local.IMG = c_local.IMG.resize((c.WIDTH, c.HEIGHT))


def paste_image(target, source, pos):
    spix = source.load()
    tpix = target.load()
    for i in range(pos[0], pos[0] + source.size[0]):
        for j in range(pos[1], pos[1] + source.size[1]):
            i1 = i - pos[0]
            j1 = j - pos[1]
            tpix[i, j] = spix[i - pos[0], j - pos[1]]
    return target


def get_image_from_gen(gen: list, c):
    image = Image.new('RGB', (c.WIDTH, c.HEIGHT), color='black')
    for i in range(c.WIDTH // c.IMG_SIZE):
        for j in range(c.HEIGHT // c.IMG_SIZE):
            image2paste = Image.open(get_image_name(gen[i][j]))
            image2paste = image2paste.resize((c.IMG_SIZE, c.IMG_SIZE))
            image = paste_image(image, image2paste, (i * c.IMG_SIZE, j + c.IMG_SIZE))
    return image


def calc_mean_color(pix, n, i=0, j=0):  # Calculating ariphmetic mean from segment on photo
    colors = [0, 0, 0]  # R G B
    for i1 in range(n):
        for j1 in range(n):
            colors[0] += pix[i + i1, j + j1][0]
            colors[1] += pix[i + i1, j + j1][1]
            colors[2] += pix[i + i1, j + j1][2]
    for i1 in range(3):
        colors[i1] = colors[i1] // (n * n)
    return colors


class Gen:

    def __init__(self, genes=None):
        self.genes = genes
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self, c=config()):
        if self.genes is None:
            return 0
        fitness = 0
        for i in range(c.HEIGHT // c.IMG_SIZE):
            for j in range(c.WIDTH // c.IMG_SIZE):
                pix = c.tImage.load()
                color = calc_mean_color(pix, c.IMG_SIZE, i=i, j=j)
                closest = 256 ** 3
                img = 'img_1'
                for i1 in range(2, c.NUM_IMAGES):
                    color_em = calc_mean_color(Image.open(get_image_name(self.genes[i][j])).load(), c.IMG_SIZE)
                    r, g, b = color_em
                    loc = abs(color[0] - r) + abs(color[1] - g) + abs(color[2] - b)
                    if closest > loc:
                        closest = loc
                        img = i1
                fitness += closest
        return fitness

    def get_child(self, par, c):
        child = []
        for i in range(len(par.genes)):
            ch1 = []
            for gen1, gen2 in zip(self.genes[i], par.genes[i]):
                p = random.random()
                if p > 0.45:
                    ch1.append(gen1)
                elif p < 0.9:
                    ch1.append(gen2)
                else:
                    ch1.append(random.randint(1, c.NUM_IMAGES))
            child.append(ch1)
        return Gen(child)


def get_gnome(c: config):
    if c.WIDTH % c.IMG_SIZE != 0 or c.HEIGHT % c.IMG_SIZE != 0:
        c = make_siutable_size(c)
    gnome = []
    for i in range(c.WIDTH // c.IMG_SIZE):
        h = []
        for j in range(c.HEIGHT // c.IMG_SIZE):
            h.append(random.randint(1, c.NUM_IMAGES))
        gnome.append(h)
    return gnome


def main():
    c = config(image_name)
    pop = []
    print("Start")
    generation = 0

    pop = []
    for i in range(c.POPULATION_SIZE):
        pop.append(Gen(get_gnome(c)))
    for j in range(10 ** 4):
        pop = sorted(pop, key=lambda x: x.fitness)
        if pop[0].fitness < 20 * ((c.WIDTH * c.HEIGHT) / (c.IMG_SIZE ** 2)):
            get_image_from_gen(pop[0].genes, c).show()
            break

        new_pop = []
        s = int((10 * c.POPULATION_SIZE) / 100)
        new_pop.extend(pop[:s])
        s = int((90 * c.POPULATION_SIZE) / 100)
        for _ in range(s):
            parent1 = random.choice(pop[:c.POPULATION_SIZE // 2])
            parent2 = random.choice(pop[:c.POPULATION_SIZE // 2])
            child = parent1.get_child(parent2, c)
            new_pop.append(child)

        # if j % 100 == 0:
        get_image_from_gen(pop[0].genes, c).save(f'img{j}.png')
        print(f"Generation {generation}. Fitness {pop[0].fitness}")
        generation += 1
        pop = new_pop


if __name__ == '__main__':
    main()
