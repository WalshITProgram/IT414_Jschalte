import pyperclip
import re

def main():
    """
    Retrieve data from clipboard, extract Coord, Dollar, and CC_Num using regular expressions,
    format the extracted data, and copy it back to clipboard.
    """
    # Retrieve data from clipboard
    data = pyperclip.paste()

    # Regular expressions to extract Coord, Dollar, and CC_Num
    coord_regex = re.compile(r'(-?\d+\.\d+,\s?-?\d+\.\d+)')
    dollars_regex = re.compile(r'\$[\d,]+')
    cc_num_regex = re.compile(r'\b\d{4} ?\d{3,4} ?\d{3,4} ?\d{4}\b')

    # Extracting data
    coords = coord_regex.findall(data)
    dollars = dollars_regex.findall(data)
    cc_nums = cc_num_regex.findall(data)

    # Ensure all lists have the same length
    min_length = min(len(coords), len(dollars), len(cc_nums))
    coords = coords[:min_length]
    dollars = dollars[:min_length]
    cc_nums = cc_nums[:min_length]

    # Format the extracted data
    formatted_data = [f"{coord} | {dollar} | {cc_num}" for coord, dollar, cc_num in zip(coords, dollars, cc_nums)]

    # Joining the formatted data
    formatted_text = '\n'.join(formatted_data)

    # Copy the formatted data back to clipboard
    pyperclip.copy(formatted_text)

def validate_coord(coord: str) -> bool:
    """
    Validate the format of Coord.
    Args:
        coord (str): The Coord to validate.
    Returns:
        bool: True if Coord is valid, False otherwise.
    """
    coord_pattern = r'^-?\d{1,2}\.\d{4,},\s*-?\d{1,3}\.\d{4,}$'
    return re.match(coord_pattern, coord) is not None

def validate_dollar(dollar: str) -> bool:
    """
    Validate the format of Dollar.
    Args:
        dollar (str): The Dollar to validate.
    Returns:
        bool: True if Dollar is valid, False otherwise.
    """
    dollars_pattern = r'^\$\d{1,3}(,\d{3})*(\.\d{1,2})?$'
    return re.match(dollars_pattern, dollar) is not None

def validate_cc_num(cc_num: str) -> bool:
    """
    Validate the format of CC_Num.
    Args:
        cc_num (str): The CC_Num to validate.
    Returns:
        bool: True if CC_Num is valid, False otherwise.
    """
    cc_num_pattern = r'^\d{4}\s?\d{3,4}\s?\d{3,4}\s?\d{4}$'
    return re.match(cc_num_pattern, cc_num) is not None

def test_validation_functions():
    """
    Test cases for validation functions.
    """
    assert validate_coord("4.93211, -149.91635") == True
    assert validate_dollar("$9,782") == True
    assert validate_cc_num("4024 007 17 2568") == True

    assert validate_coord("invalid_coord") == False
    assert validate_dollar("invalid_dollar") == False
    assert validate_cc_num("invalid_cc_num") == False

if __name__ == "__main__":
    main()
    test_validation_functions()
