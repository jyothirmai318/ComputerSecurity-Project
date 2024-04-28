import time
import os

# Create a test file
with open('test.txt', 'wb') as f:
    f.write(b'Hello, World!')

# Open the test file in read-binary mode
with open('test.txt', 'rb+') as f:
    # Modify the file contents
    f.write(b'Goodbye, World!')
    time.sleep(10)  # Keep the file open for 10 seconds

# Clean up the test file
os.remove('test.txt')