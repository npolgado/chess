
def translate_move_s2t(notation: str) -> (int, int):
    ''' Converts string into a tuple of row and col
        example: A1 -> (0, 0)
                H8 -> (7, 7)
        NOTE: Assumes "A1H8" (capital)
    '''
    start_col = ord(notation[0]) - 65
    start_row = int(notation[1]) - 1

    end_col = ord(notation[2]) - 65
    end_row = int(notation[3]) - 1

    return (start_row, start_col), (end_row, end_col)



def translate_move_t2s(start_row: int, start_col: int, end_row: int, end_col: int) -> str:
    ''' Converts row and col to chess position 
        example: row 0, col 0 -> A1
                row 7, col 7 -> H8
    '''
    ans = ""
    ans += chr(start_col + 65)
    ans += str(start_row + 1)
    ans += chr(end_col + 65)
    ans += str(end_row + 1)
    return ans


print(translate_move_s2t("G2G4"))