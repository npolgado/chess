
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



print(translate_move_t2s(1,2, 2,1))

ROW = 1 # 2
COL = 2 # B