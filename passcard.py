'''
Generates a random password card that can be printed for simple password management
Outputs a PNG because PIL's pdf library uses _TERRIBLE_ JPG compression
'''

import secrets
from PIL import Image, ImageDraw, ImageFont

def letter_options(*, upper=True, lower=True, numbers=True, special=True)->str:
  '''Returns a str containing character choices for the random password'''
  # Create a dictionary of the function's arguments
  args = locals().items()
  # Create a dictionary of possible character choices
  choices = {
    "upper": "QWERTYUIOPASDFGHJKLZXCVBNM",
    "lower": "qwertyuiopasdfghjklzxcvbnm",
    "numbers": "1234567890",
    "special": "!@#$%^&*()-=+~,.?"
  }
  output = ""
  # For loop thru the arguments, adding appropriate characters to the output
  for key, value in args:
    if value:
      output += choices[key]
  return output


def simple_cypher():
  '''Generate simple cypher map of a keyboard'''
  choices = letter_options()
  cypher_map = {}
  for letter in letter_options(lower=False, special=False, numbers=False):
    candidate = letter
    # Don't let the cypher letter be the same as the original letter
    while candidate.upper() == letter:
      candidate = secrets.choice(choices)
    # Remove the cypher letter from the list of choices
    choices = choices.replace(candidate, "")
    cypher_map[letter] = candidate
  return cypher_map


def is_special(character):
  '''Returns True if character is a special character'''
  if character in letter_options(upper=False, lower=False, numbers=False, special=True):
    return True
  else:
    return False


def generate_code(*, code_length=8, letters=letter_options()):
  '''Generate spacebar code'''
  output = ""
  # Check to make sure there's a number, an uppper-case and a special character in the code
  while not ((any(character.isdigit() for character in output)) and\
    (any(character.isupper() for character in output)) and\
    (any(is_special(character) for character in output))):
    # Always start with a lowercase letter, because some sites don't like
    # starting passwords with a special character or number
    output = secrets.choice(letter_options(upper=False, special=False, numbers=False))
    for _ in range(code_length - 1):
      output += secrets.choice(letters)
  return output


def draw_box(box_x, box_y, tile_size, char_a, char_b, destination):
  '''Draws a single box of the keyboard map'''
  square = ImageDraw.Draw(destination)
  # Draws a black bg
  line_width = tile_size//20
  square.rectangle([(box_x, box_y), (box_x + tile_size, box_y + tile_size)], fill=(0,0,0), outline=(255,255,255), width=line_width)

  # Draw the text inside the square
  center_x = (box_x + (tile_size // 2))
  center_y = (box_y + (tile_size // 2))
  font_size = int(tile_size / 2.5)
  font = ImageFont.truetype("Hack-Bold.ttf", size=font_size)
  letter_width = font.getsize(char_a)[0]
  letter_height = font.getsize(char_a)[1]
  square.text((center_x - letter_width, center_y - letter_height), char_a, font=font, fill=(255,255,255))
  square.text((center_x, center_y), char_b, font=font, fill=(255,255,255))


def draw_instructions(box_x, box_y, height, width, start_code, destination):
  '''Draw the instructions bar at the bottom'''
  bar = ImageDraw.Draw(destination)
  # Draws a black bg
  line_width = height//20
  bar.rectangle([(box_x, box_y), (box_x + width, box_y + height)], fill=(0,0,0), outline=(255,255,255), width=line_width)
  # Set up the font...
  font_size = int(height / 2.5)
  font = ImageFont.truetype("Hack-Bold.ttf", size=font_size)
  instructions = start_code + " + [Your Secret] + [Site Code]"
  text_x = box_x + (width // 2) - (font.getsize(instructions)[0] // 2)
  text_y = box_y + (height // 2) - (font_size // 2)
  bar.text((text_x, text_y), instructions, font=font, fill=(255,255,255))



def generate_image(output_file="card.png"):
  '''Generate image'''
  start_code = generate_code()
  keyboard_map = simple_cypher()
  qwerty = letter_options(upper=True, lower=False, numbers=False, special=False)
  row_split = [10, 9, 7] # How many letters on each row of the keyboard

  # Create a white credit-card-sized image to start with
  card_width = 1000
  card_height = 400
  card = Image.new("RGB", (card_width, card_height), color = "white")

  # Draw the keyboard map
  tile_size = 100
  current_index = -1
  for row in range(3):
    for column in range(row_split[row]):
      current_index += 1
      letter = qwerty[current_index]
      box_x = column * tile_size
      box_y = row * tile_size
      draw_box(box_x, box_y, tile_size, letter, keyboard_map[letter], card)

  # Place a box with the start code
  draw_instructions(0, card_height - tile_size, tile_size, card_width, start_code, card)
  card.save(open(output_file, "wb"), "PNG", creator="Passcard")


if __name__ == "__main__":
  generate_image()