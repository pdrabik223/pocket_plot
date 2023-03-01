import enum
import math

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


class Connection(enum.Enum):
    S11 = "S11"
    S21 = "S21"


def plot_real(connection: Connection, all_the_data: list[pd.DataFrame], labels=list[str]):
    title = f"{str(connection.value)} real part"
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("[dB]")
    plt.title(title)
    x_axis = all_the_data[0][FREQUENCY].values.tolist()

    if connection == Connection.S11:
        column_name = S11_REAL
    elif connection == Connection.S21:
        column_name = S21_REAL

    for data, label in zip(all_the_data, labels):
        y_values = data[column_name].values.tolist()
        plt.plot(x_axis, y_values, label=label)

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.show()


def plot_imag(connection: Connection, all_the_data: list[pd.DataFrame], labels=list[str]):
    title = f"{str(connection.value)} imaginary part"
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("[dB]")
    plt.title(title)
    x_axis = all_the_data[0][FREQUENCY].values.tolist()

    if connection == Connection.S11:
        column_name = S11_IMAG
    elif connection == Connection.S21:
        column_name = S21_IMAG

    for data, label in zip(all_the_data, labels):
        y_values = data[column_name].values.tolist()
        plt.plot(x_axis, y_values, label=label)

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.show()


# magnitude [dB] = 20 * Log(sqr(Re^2 + Im^2))
def magnitude(real, imag):
    return 20 * math.log(math.sqrt(real ** 2 + imag ** 2))


def plot_magnitude(connection: Connection, all_the_data: list[pd.DataFrame], labels=list[str]):
    title = f"{str(connection.value)} magnitude"
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("[dB]")
    plt.title(title)
    x_axis = all_the_data[0][FREQUENCY].values.tolist()

    if connection == Connection.S11:
        real_column_name = S11_REAL
        imag_column_name = S11_IMAG
    elif connection == Connection.S21:
        real_column_name = S21_REAL
        imag_column_name = S21_IMAG

    for data, label in zip(all_the_data, labels):
        y_values = [magnitude(r, i) for r, i in
                    zip(data[real_column_name].values.tolist(), data[imag_column_name].values.tolist())]
        plt.plot(x_axis, y_values, label=label)

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.show()


# phase = arctan(Im / Re)
def phase(real, imag):
    return math.atan(imag / real)


def plot_phase(connection: Connection, all_the_data: list[pd.DataFrame], labels=list[str]):
    title = f"{str(connection.value)} phase"
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("[dB]")
    plt.title(title)
    x_axis = all_the_data[0][FREQUENCY].values.tolist()

    if connection == Connection.S11:
        real_column_name = S11_REAL
        imag_column_name = S11_IMAG
    elif connection == Connection.S21:
        real_column_name = S21_REAL
        imag_column_name = S21_IMAG

    for data, label in zip(all_the_data, labels):
        y_values = [phase(r, i) for r, i in
                    zip(data[real_column_name].values.tolist(), data[imag_column_name].values.tolist())]
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

    plot_real(Connection.S11, all_the_data, onlyfiles)
    plot_imag(Connection.S11, all_the_data, onlyfiles)
    plot_magnitude(Connection.S11, all_the_data, onlyfiles)
    plot_phase(Connection.S11, all_the_data, onlyfiles)

    plot_real(Connection.S21, all_the_data, onlyfiles)
    plot_imag(Connection.S21, all_the_data, onlyfiles)
    plot_magnitude(Connection.S21, all_the_data, onlyfiles)
    plot_phase(Connection.S21, all_the_data, onlyfiles)
