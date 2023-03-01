import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

FREQUENCY = 'Frequency'
S11_REAL = 'S11-S-Real'
S11_IMAG = 'S11-S-Imaginary'
S21_REAL = 'S21-S-Real'
S21_IMAG = 'S21-S-Imaginary'


def plot_s11_real(all_the_data: list[pd.DataFrame], labels=list[str]):
    title = "s11 real part"
    plt.xlabel("Frequency")
    plt.ylabel("No idea here")
    plt.title(title)
    x_axis = all_the_data[0][FREQUENCY].values.tolist()

    for data, label in zip(all_the_data, labels):
        y_values = data[S11_REAL].values.tolist()
        plt.plot(x_axis, y_values, label=label)

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.show()


def plot_s21_real(all_the_data: list[pd.DataFrame], labels=list[str]):
    title = "s21 real part"
    plt.xlabel("Frequency")
    plt.ylabel("No idea here")
    plt.title(title)
    x_axis = all_the_data[0][FREQUENCY].values.tolist()

    for data, label in zip(all_the_data, labels):
        y_values = data[S21_REAL].values.tolist()
        plt.plot(x_axis, y_values, label=label)

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.show()


def replace_comma_with_dot(string: str):
    if isinstance(string, str):
        return string.replace(',', '.')
    else:
        return string


if __name__ == '__main__':
    directory_path = "./example_data"
    # list all the '.csv' files under directory_path
    onlyfiles = [f for f in listdir(directory_path) if
                 isfile(join(directory_path, f)) and join(directory_path, f)[-4:] == '.csv']

    # load data in '.csv' files to memory
    all_the_data = [pd.read_csv(join(directory_path, file), sep=';') for file in onlyfiles]

    # some files for no apparent reason, have numbers decoded with comma instead of dot
    # so for example: '3,14' instead of '3.14'
    all_the_data = [dataframe.applymap(replace_comma_with_dot) for dataframe in all_the_data]
    # some files for no apparent reason, have numbers decoded as string not floats
    all_the_data = [dataframe.astype(float) for dataframe in all_the_data]

    for dataframe in all_the_data:
        print(dataframe.head())

    print(f"Number of loaded files: {len(all_the_data)}")

    plot_s11_real(all_the_data, onlyfiles)
    plot_s21_real(all_the_data, onlyfiles)
