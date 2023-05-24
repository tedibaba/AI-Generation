from __future__ import annotations
import unittest
from generative import flatten_image, unflatten_image, check_adjacent_for_one, pixel_flip, write_image, generate_new_images
from ai import read_image


class TestGenerative(unittest.TestCase):
    """Unit tests for the module generative.py"""

    def test_flatten_image(self) -> None:
        """
        Verify output of flatten_image for at least three different sizes of images.
        """
        assert flatten_image([[0,1],[1,0]]) == [0,1,1,0], "Image was not flattened correctly"
        assert flatten_image([[0,0,0],[1,1,1],[0,1,0]]) == [0,0,0,1,1,1,0,1,0], "Image was not flattened correctly"
        assert flatten_image([[0,0,0,0],[1,1,1,1],[0,1,0,1],[1,0,1,0]]) == [0,0,0,0,1,1,1,1,0,1,0,1,1,0,1,0], "Image was not flattened correctly"
        

    def test_unflatten_image(self) -> None:
        """
        Verify output of unflatten_image for at least three different sizes of flattened images.
        """
        assert unflatten_image([0,0,0,0,1,1,1,1,0,1,0,1,1,0,1,0]) == [[0,0,0,0],[1,1,1,1],[0,1,0,1],[1,0,1,0]], "Image was not unflattened correctly"
        assert unflatten_image([0,0,0,1,1,1,0,1,0]) == [[0,0,0],[1,1,1],[0,1,0]], "Image was not unflattened correctly"
        assert unflatten_image([0,1,1,0]) == [[0,1],[1,0]], "Image was not unflattened correctly"

    def test_check_adjacent_for_one(self) -> None:
        """
        Verify output of check_adjacent_for_one for three different pixel indexes of an image representing different scenarios.
        """
        assert check_adjacent_for_one([0,0,0,0,1,1,1,1,0,1,0,0,1,0,0,0], 0) == True, "check_adjacent_for_one incorrectly did not find an adjacent pixel containing 1 when checking at index 0"
        assert check_adjacent_for_one([0,0,0,0,1,1,1,1,0,1,0,0,1,0,0,0], 4) == True, "check_adjacent_for_one incorrectly did not find an adjacent pixel containing 1 awhen checking at index 4"
        assert check_adjacent_for_one([0,0,0,0,1,1,1,1,0,1,0,0,1,0,0,0], 15) == False, "check_adjacent_for_one incorrectly found an adjacent pixel containing 1 when checking at index 15"

    # def test_pixel_flip(self) -> None:
    #     """
    #     Verify output of pixel_flip for a 5x5 image with a budget of 2.
    #     """
    #     result = []
    #     image = flatten_image([
    #         [0,1,0,0,0],
    #         [1,1,0,0,0],
    #         [1,0,1,0,0],
    #         [1,1,1,0,1],
    #         [1,1,1,1,0]])

    #     pixel_flip(image, image, 2, result)
    #     assert len(result) == 28, ""

    def test_pixel_flip(self) -> None:
        """
        Verify output of pixel_flip for a 5x5 image with a budget of 2.
        """
        result = []
        image = flatten_image([
            [0,1,0,0,0],
            [1,1,0,0,0],
            [1,0,1,0,0],
            [1,1,1,0,1],
            [1,1,1,1,0]])

        expected_result = [[1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                        [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                        [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]

        pixel_flip(image, image, 2, result)
        for res in result:
            assert res in expected_result, "One of the results from pixel_flip is not in the expected result"
            expected_result.remove(res)
        assert len(expected_result) == 0, "pixel_flip did not produce every possible result in expected result"

    def test_generate_new_images(self) -> None:
        """
        Verify generate_new_images with image.txt and for each image of the generated images verify that:
        - image is of size 28x28,
        - all values in the generated image are either 1s or 0s,
        - the number of pixels flipped from original image are within budget,
        - all pixels flipped from the original image had an adjacent value of 1.
        """
        orig_image = read_image("image.txt")
        possible_images = generate_new_images(read_image("image.txt"), 2)
        for image in possible_images:
            differences = 0
            flattened_image = flatten_image(image)
            assert len(image) == 28, "There are not 28 rows" # Checking if there are 28 rows
            for row in range(len(image)):
                assert len(image[row]) == 28, "One row does not have 28 pixels" # Checking if each row has 28 pixels
                for index in range(len(image[row])):
                    assert image[row][index] == 0 or image[row][index] == 1 #Checking if each pixel is a 0 or 1
                    #If the pixel has been changed, then we check if there is a 1 adjacent to the pixel. 
                    if image[row][index] != orig_image[row][index]:
                        assert check_adjacent_for_one(flattened_image, row * 28 + index) == True, "A flipped pixel did not have a pixel with a value of 1 adjacent to it"
                        differences += 1

            assert 0 < differences <= 2, "Either no changes were made or the budget has been exceeded"


if __name__ == "__main__":
    unittest.main()

