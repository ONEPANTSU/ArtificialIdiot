import csv
import itertools
import math
import random

import numpy as np


class DatasetHandler:
    def __init__(self, file_path):
        self.dataset = None
        self.file_path = None
        self.read_file(file_path=file_path)

    def read_file(self, file_path):
        self.file_path = file_path
        self.dataset = []
        with open(self.file_path, newline="") as csvfile:
            data = csv.reader(csvfile, delimiter=" ", quotechar="|")
            answers = np.array([5, 6, 7, 8, 9, 5, 6, 7, 8, 9])
            iteration = 0
            for row in data:
                input_values = list(map(int, row[0].split(";")[:-1]))
                self.dataset.append([input_values, answers[iteration] - 5])
                iteration += 1

    def get_dataset(self):
        return self.dataset

    def add_noise(self, defective_percent):
        for data in self.dataset:
            defective_pixels_count = random.randint(
                0, math.ceil(len(data[0]) * defective_percent / 100)
            )
            for defective_pixel in range(defective_pixels_count):
                pixel_index = random.randint(0, len(data[0]) - 1)
                data[0][pixel_index] = int(not data[0][pixel_index])
        return self.dataset

    def get_full_dataset(self, defective_percent):
        full_dataset = []
        for data in self.dataset:
            defective_pixels_count = math.ceil(len(data[0]) * defective_percent / 100)
            defective_pixels = itertools.permutations(
                range(len(data[0])), defective_pixels_count
            )

            full_dataset.append(data)
            for pixels in defective_pixels:
                new_data = data
                for pixel in pixels:
                    new_data[0][pixel] = int(not new_data[0][pixel])
                full_dataset.append(new_data)
        random.shuffle(full_dataset)
        return full_dataset
