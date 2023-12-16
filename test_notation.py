from new_game import *

print(pos_to_row_col("A1"))
print(row_col_to_pos(0, 0))

print(pos_to_row_col("H8"))
print(row_col_to_pos(7, 7))

print(
    pos_to_row_col(
        row_col_to_pos(0,0)
    )
)

print(
    pos_to_row_col(
        row_col_to_pos(7,7)
    )
)