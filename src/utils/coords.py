def convert_coords_to_index(coords):
    """Convert coordinate (e.g., 'B4') to grid index (row, col)."""
    if len(coords) != 2:
        raise ValueError("Invalid coordinate format. Use 'LetterNumber' (e.g., 'B4').")
    
    letter, number = coords[0].upper(), coords[1]
    
    if letter < 'A' or letter > 'J' or not number.isdigit() or int(number) < 1 or int(number) > 10:
        raise ValueError("Coordinates out of bounds. Use 'A1' to 'J10'.")
    
    row = int(number) - 1
    col = ord(letter) - ord('A')
    
    return row, col

def convert_index_to_coords(row, col):
    """Convert grid index (row, col) to coordinate (e.g., 'B4')."""
    if row < 0 or row > 9 or col < 0 or col > 9:
        raise ValueError("Index out of bounds. Valid range is 0-9 for both row and column.")
    
    letter = chr(col + ord('A'))
    number = str(row + 1)
    
    return f"{letter}{number}"

def is_valid_coordinate(coords):
    """Check if the given coordinate is valid."""
    try:
        convert_coords_to_index(coords)
        return True
    except ValueError:
        return False