from PIL import Image
import os, sys, subprocess, logging
os.chdir(os.path.dirname(__file__))


def process_input_list(input_list_str):
    # Convert the input list string back to a list

    print("in:", input_list_str)

    input_list = list(map(str, input_list_str.split(',')))

    # Process the list and two integers as needed
  #  result = [x for x in input_list] 

    # Print or use the result
    print(type(input_list))

    print("Py:", input_list)

    return input_list



def custom_sort_key(dice_string):
    # Split the string into dice type and roll value
    dice_type, roll_value = map(int, dice_string.split('/'))
    return (dice_type, roll_value)


def combine_images_into_grid(image_paths, output_path):

    print("py:", image_paths)

    for x in range(len(image_paths)):
        if image_paths[x].startswith("/home/evans/Documents/Discord/DiceMaiden/DiceRolls/d"):
            image_paths[x] = image_paths[x][52:-4]

    print("py:", image_paths)
    logging.debug("py:", image_paths)
  #  image_paths.sort(key=custom_sort_key)
  #  print("py:", image_paths)

    new_list = []

    for each in image_paths:
        take_list = each.split("/")[1].split("~")
        for x in take_list:
            new_list.append( each.split("/")[0] + "/" + x )

    
    print("th:", new_list)



  #  output_file = os.path.join(output_path, "_".join(image_paths).replace("/", "=") + ".png")
    output_file = os.path.join(output_path, "_".join(new_list).replace("/", "=") + ".png")

    if os.path.exists(output_file):
        print("This Exists in the cache and will be used instead.")
        return output_file

    # Determine the number of rows and columns based on the number of images
    num_images = len(new_list)
  
    num_rows = int(num_images**0.5)
    num_columns = (num_images + num_rows - 1) // num_rows

    # Create a blank canvas for the grid
    grid_width = num_columns * 200  # Assuming each image is 200x200 pixels
    grid_height = num_rows * 200
    grid = Image.new('RGBA', (grid_width, grid_height), (255, 255, 255, 0))

    # Paste each image onto the grid
    for i, new_list in enumerate(new_list): # image_paths\
        try:
            img = Image.open("/home/evans/Documents/Discord/DiceMaiden/DiceRolls/d" + new_list + ".png")
        except FileNotFoundError:
            img = Image.open('/home/evans/Documents/Discord/DiceMaiden/DiceRolls/DiceFindError.png')

        grid.paste(img, ((i % num_columns) * 200, (i // num_columns) * 200))

    # Save the combined image to the specified output path
    if not os.path.exists(output_path):
        os.makedirs(output_path)

  #  output_file = os.path.join(output_path, "_".join(image_paths).replace("/", "=") + ".png")
    
    print(output_file)
    try:
        grid.save(output_file)
    except OSError:
        grid.save( os.path.join(output_path, "ThisFileWasTooLong.png") )
        output_file = os.path.join(output_path, "ThisFileWasTooLong.png")
    return output_file

for x in range(len(sys.argv)):
    print(f"arg{x}:", sys.argv[x])

# Example usage:
image_paths = [
    '/home/evans/Documents/Discord/DiceMaiden/DiceRolls/d6/5.png',
    '/home/evans/Documents/Discord/DiceMaiden/DiceRolls/d10/5.png',
    '/home/evans/Documents/Discord/DiceMaiden/DiceRolls/d10/10.png',
    '/home/evans/Documents/Discord/DiceMaiden/DiceRolls/d6/1.png',
    '/home/evans/Documents/Discord/DiceMaiden/DiceRolls/d10/1.png',
    'Test', # d12/10.png',
]

output_directory = './DiceRolls/Cache'

# Process the input list
print(len(sys.argv))
if len(sys.argv) == 4: 
  #  try:
    if True:
        out = combine_images_into_grid(process_input_list(sys.argv[1]), output_directory)
  #  except:
  #      out = "/home/evans/Documents/Discord/DiceMaiden/DiceRolls/Error.png"
    guild   = sys.argv[2]
    channel = sys.argv[3]

else: #except Exception as e: #  print(e)
    print("args not valid, using template")
    guild   = 987570723365216296
    channel = 987570882866184263
    out = combine_images_into_grid(image_paths, output_directory)


print(os.path.abspath(os.curdir))
os.chdir("..")
print(os.path.abspath(os.curdir))

print(str(out))

#subprocess.run(f"python3 /home/evans/Documents/Discord/Send.py LINK:./DiceMaiden{str(out)[1:]} {guild} {channel}", shell=True) 

import socket

def send_data(socket, data):
    chunk_size = 1024  # Adjust the chunk size as needed
    total_size = len(data)

    # Send the total size first
    socket.send(str(total_size).encode())

    # Send the data in chunks
    for i in range(0, total_size, chunk_size):
        chunk = data[i:i + chunk_size]
        socket.send(chunk.encode())


def send_packet(file_path, int1, int2):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 8888))

        message = f"{file_path},{int1},{int2}"
        s.sendall(message.encode())

        data = s.recv(100)
        response = data.decode()
        print(response)

send_packet(str(out), guild, channel)