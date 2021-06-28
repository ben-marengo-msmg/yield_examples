# Safely open the file
file = open("hello.txt", "w")

try:
    file.write("Hello, World!")
except Exception as e:
    print(f"An error occurred while writing to the file: {e}")
finally:
    # Make sure to close the file after using it
    file.close()


# use with 'context manager'
with open("hello.txt", "w") as file:
    file.write("Hello, World!")


"""
Simple syntax
Allows reusing the code for setup and teardown
Average dev doesnt have to care about setup and teardown
Helps avoid resource leaks
"""





