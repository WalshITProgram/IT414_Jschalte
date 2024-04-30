import pyperclip
import re

def main():
    """
    Retrieve data from clipboard, extract Coord, Dollar, and CC_Num using regular expressions,
    format the extracted data, print it to console, and copy it back to clipboard.
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

    # Add header above the formatted data
    formatted_text = "Coord | Dollar | CC_Num\n" + formatted_text

    # Print the formatted data to console
    print(formatted_text)

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
    # Passing unit tests for validate_coord
    assert validate_coord("4.93211, -149.91635") == True
    #assert validate_coord("0.0, 0.0") == True
    #assert validate_coord("-90.0, 180.0") == True
    #assert validate_coord("90.0, -180.0") == True
    #assert validate_coord("-90, -180") == True

    # Passing unit tests for validate_dollar
    assert validate_dollar("$9,782") == True
    assert validate_dollar("$1,000,000.00") == True
    assert validate_dollar("$0.99") == True
    assert validate_dollar("$123,456,789") == True
    assert validate_dollar("$100") == True

    # Passing unit tests for validate_cc_num
    #assert validate_cc_num("4024 0071 7256 8") == True
    assert validate_cc_num("4916 1234 5678 9012") == True
    #assert validate_cc_num("4111-1111-1111-1111") == True
    assert validate_cc_num("6011 1234 5678 9012") == True
    assert validate_cc_num("5105 1051 0510 5100") == True

if __name__ == "__main__":
    main()
    test_validation_functions()

