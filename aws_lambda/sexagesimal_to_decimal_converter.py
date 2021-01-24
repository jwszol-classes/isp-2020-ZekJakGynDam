# -*- coding: utf-8 -*-

import json
import numpy


def sexagesimal2decimal(degrees_sexagesimal):
    digits = "0123456789"
    numbers = []
    number = ""
    for i in range(len(degrees_sexagesimal)):
        if degrees_sexagesimal[i] in digits:
            number += degrees_sexagesimal[i]
        else:
            if number!= "":
                numbers.append(number)
            number = ""
    degrees_decimal = str(int(numbers[0]) + int(numbers[1])/60 + int(numbers[2])/3600)
    return degrees_decimal


def convert_coords_from_sexagesimal_to_decimal(latitude_sexagesimal, longitude_sexagesimal):
    latitude_decimal  = sexagesimal2decimal(latitude_sexagesimal)
    longitude_decimal = sexagesimal2decimal(longitude_sexagesimal)
    return latitude_decimal, longitude_decimal


# if __name__ == "__main__":
#     dictionary = json.load(open(".\\aws_lambda\\polish_airports_old.json", "r"))
#     new_dictionary = {}
#     for airport in dictionary.keys():
#         latitude_sexagesimal, longitude_sexagesimal = dictionary[airport].split()
#         latitude_decimal, longitude_decimal = convert_coords_from_sexagesimal_to_decimal(latitude_sexagesimal, longitude_sexagesimal)
#         coordinates_sexagesimal = {
#             "latitude_sexagesimal": latitude_sexagesimal,
#             "longitude_sexagesimal": longitude_sexagesimal
#         }
#         coordinates_decimal = {
#             "latitude_decimal": latitude_decimal,
#             "longitude_decimal": longitude_decimal
#         }
#         coordinates = {
#             "coordinates_sexagesimal": coordinates_sexagesimal,
#             "coordinates_decimal": coordinates_decimal

#         }
#         new_dictionary[airport] = coordinates

#     json.dump(new_dictionary, open('polish_airports.json', 'w'))