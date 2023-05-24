"""
This file is part of Assignment 3 of FIT1045, S1 2023.

It contains methods for generating new images from existing images.

@file generative.py
@author Randil Hettiarachchi
@date 24/05/2023
"""
from __future__ import annotations
from ai import predict_number, read_image

def flatten_image(image: list[list[int]]) -> list[int]:
    """
    Flattens a 2D list into a 1D list.
    
    :param image: 2D list of integers representing an image.
    :return: 1D list of integers representing a flattened image.
    """
    return sum(image, [])


def unflatten_image(flat_image: list[int]) -> list[list[int]]:
    """
    Unflattens a 1D list into a 2D list.
        
    :param flat_image: 1D list of integers representing a flattened image.
    :return: 2D list of integers.
    """
    image = []
    jump_count = int(len(flat_image)**0.5) #The number of bits in a row
    for i in range(0, len(flat_image), jump_count):
        image.append(flat_image[i: i + jump_count]) #Appending a row
    return image

def check_adjacent_for_one(flat_image: list[int], flat_pixel: int) -> bool:
    """
    Checks if a pixel has an adjacent pixel with the value of 1.
    
    :param flat_image: 1D list of integers representing a flattened image.
    :param flat_pixel: Integer representing the index of the pixel in question.
    :return: Boolean.
    """
    #The number of indexes that need to be jumped to move vertically
    #This is also used to check if the element adjacent is on the same row in the unflattened array
    vertical_index_distance = int(len(flat_image) ** 0.5) 
    if flat_pixel > 0 and (flat_pixel + 1) % vertical_index_distance != 0 and flat_image[flat_pixel + 1] == 1:
        return True
    elif flat_pixel < len(flat_image) - 2 and flat_pixel % vertical_index_distance != 0 and flat_image[flat_pixel - 1] == 1:
        return True
    elif flat_pixel +vertical_index_distance < len(flat_image) and flat_image[flat_pixel + vertical_index_distance] == 1:
        return True
    elif flat_pixel - vertical_index_distance >= 0 and flat_image[flat_pixel - vertical_index_distance] == 1:
        return True
    return False

def pixel_flip(lst: list[int], orig_lst: list[int], budget: int, results: list, i: int = 0) -> None:
    """
    Uses recursion to generate all possibilities of flipped arrays where
    a pixel was a 0 and there was an adjacent pixel with the value of 1.

    :param lst: 1D list of integers representing a flattened image.
    :param orig_lst: 1D list of integers representing the original flattened image.
    :param budget: Integer representing the number of pixels that can be flipped.
    :param results: List of 1D lists of integers representing all possibilities of flipped arrays, initially empty.
    :param i: Integer representing the index of the pixel in question.
    :return: None.
    """
    #Base case: budget = 0 or no more changes to make
    if budget == 0 or i == len(orig_lst) -1:
        if lst != orig_lst:
            results.append(lst)
        return
    
    #Recursion: Moving towards base case by flipping numbers and reducing the budget. Also move to towards the base case by incrementing i
    if orig_lst[i] == 0 and check_adjacent_for_one(orig_lst, i):
        new_possible_lst = lst[:] #Copying the list so the change does not affect the other 
        new_possible_lst[i] = 1 #Making the possible bit flip
        pixel_flip(new_possible_lst, orig_lst, budget - 1, results, i + 1)
    pixel_flip(lst, orig_lst, budget, results, i + 1) #Search for other bits that can be flipped assuming the current bit cannot be flipped or is not flipped even though it can be 

    

def write_image(orig_image: list[list[int]], new_image: list[list[int]], file_name: str) -> None:
    """
    Writes a newly generated image into a file where the modified pixels are marked as 'X'.
    
    :param orig_image: 2D list of integers representing the original image.
    :param new_image: 2D list of integers representing a newly generated image.
    :param file_name: String representing the name of the file.
    :return: None.
    """
    array_to_write = []
    for i in range(len(orig_image)):
        row = [] #One row in the image
        for j in range(len(orig_image[i])):
            if orig_image[i][j] ^ new_image[i][j]: #Using XOR to see if the two bits at that position are different
                row.append("X")
            else: #if no change has occured
                row.append(str(orig_image[i][j]))
        array_to_write.append("".join(row))
    with open(file_name, "w") as output_file:
        for row in array_to_write:
            output_file.write(row+"\n")

def generate_new_images(image: list[list[int]], budget: int) -> list[list[list[int]]]:
    """
    Generates all possible new images that can be generated within the budget.
    
    :param image: 2D list of integers representing an image.
    :param budget: Integer representing the number of pixels that can be flipped.
    :return: List of 2D lists of integers representing all possible new images.
    """
    flattened_image = flatten_image(image)
    orig_bot_prediction = predict_number(image) #What number the bot predicts the original image to be
    results= [] #The array that stores all possible images that could created from the original image
    pixel_flip(flattened_image, flattened_image, budget, results) #Finding all possible images
    possible_new_images = [] #list of images where the bot has guessed the number in the adjusted image as the same as the number in the original image
    for result in results:
        unflattened_result = unflatten_image(result) 
        if predict_number(unflattened_result) == orig_bot_prediction: #if the bot still predicts the adjusted image as the same number
            possible_new_images.append(unflattened_result)
    return possible_new_images


if __name__ == "__main__":
    # image = read_image("image.txt")
    # new_images = generate_new_images(image, 2)
    # print(f"Number of new images generated: {len(new_images)}")
    # # Write first image to test generation
    # write_image(image, new_images[0], "new_image_1.txt") 
    image = flatten_image([
            [0,1,0,0,0],
            [1,1,0,0,0],
            [1,0,1,0,0],
            [1,1,1,0,1],
            [1,1,1,1,0]])
    res = []
    pixel_flip(image, image, 2, res)
    print(len(res))
    for result in res:
        print(result)


