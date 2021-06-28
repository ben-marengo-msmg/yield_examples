

list_of_rows = [row for row in open('file.txt')]
row_generator = (row for row in open('file.txt'))

print(list_of_rows)
print(row_generator)


no_rows_with_hashes = (row for row in row_generator if '#' not in row)
removed_whitespace = (row.replace(' ', '') for row in no_rows_with_hashes)


print(removed_whitespace)
print(list(removed_whitespace))

