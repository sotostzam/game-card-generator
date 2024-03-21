from PIL import Image, ImageDraw, ImageFont, ImageColor
import math
import json
import textwrap

class Card:
	"""
	Base class representing a customizable game card.
	"""
	def __init__(self, name, type, description, effect=None, attributes=None, image=None):
		"""
		Initializes a Card object.

		Args:
		name: (str) Name of the card.
		type: (str) Type of the card.
		description: (str) Description for the card.
		effect: (str) Effect of the card.
		attributes: (dict) The attributes describing the card.
		image: (str) Path to the image for the card.
		"""

		self.name = name
		self.description = description
		self.effect = effect
		self.image = image
		self.border_size = 5
		self.attributes = attributes

		self.font_size = 30
		self.normal_font = ImageFont.truetype("fonts/EduSABeginner.ttf" or "arial.ttf", self.font_size)
		self.title_font = ImageFont.truetype("fonts/asap_symbol.otf" or "arial.ttf", self.font_size+10)
		self.type_font = ImageFont.truetype("fonts/EduSABeginner_bold.ttf" or "arial.ttf", self.font_size-10)

		self.layout_size = (750, 1050)

		self.inner_bg = "black"
		self.green = ImageColor.getrgb("#9ac360")

		# Set the card accent colors and class based on creature type
		if type == 'normal':
			self.accent_color = ImageColor.getrgb("#4446c2") # Blue
			self.type = 'creature'
		elif type == 'annoying':
			self.accent_color = ImageColor.getrgb("#bf3f3f") # Red
			self.type = 'creature'
		elif type == 'mythical':
			self.accent_color = ImageColor.getrgb("#966a00") # Gold
			self.type = 'creature'
		elif type == 'magic':
			self.accent_color = ImageColor.getrgb("#9560c3") # ???
			self.type = type
		elif type == 'buff':
			self.accent_color = ImageColor.getrgb("#41c4bc") # ???
			self.type = type
		elif type == 'debuff':
			self.accent_color = ImageColor.getrgb("#c74a7e") # ???
			self.type = type
		
	def create(self):
		"""
		Creates and saves the card image.
		"""

		def create_rectangle(l, w, theta, offset=(0,0)):
			c, s = math.cos(theta), math.sin(theta)
			rectCoords = [(l/2.0, w/2.0), (l/2.0, -w/2.0), (-l/2.0, -w/2.0), (-l/2.0, w/2.0)]
			return [(c*x-s*y+offset[0], s*x+c*y+offset[1]) for (x,y) in rectCoords]
		
		def create_circle(radius, x, y, fill, outline, width):
			draw.ellipse((x, y, x + radius * 2, y + radius * 2), fill=fill, outline=outline, width=width)

		def draw_outline():
			shape = [(0 + self.border_size, card_height - (card_height * .377)), (card_width - self.border_size - 0.01, card_height - (card_height * .377))]
			draw.line(shape, fill=self.accent_color, width=20)

			create_circle(
				radius = 65,
				x = (desc_padding - 65 * 2) // 2,
				y = card_height - (card_height * .44),
				fill = self.inner_bg,
				outline=self.accent_color,
				width=10
			)
			
			card_class_image = Image.open(f"assets/{self.type}.png")
			card_class_image = card_class_image.resize([int(0.15 * s) for s in card_class_image.size], Image.LANCZOS)

			card_class_image_x = int(desc_padding - card_class_image.size[0]) // 2
			card_class_image_y = int(card_height - (card_height * .417))
			self.card.paste(card_class_image, (card_class_image_x, card_class_image_y), mask=card_class_image)

			vertices = create_rectangle(41, 41, 45*math.pi/180, offset=(card_width * .308, card_height - (card_height * .377)))
			draw.polygon(vertices, fill=self.inner_bg, width=10, outline=self.accent_color)

		def draw_attributes():
			if self.attributes:
				current_padding_top = int(card_height - (card_height * .29))

				for attribute, value in self.attributes.items():
					create_circle(
						radius = 40,
						x = (desc_padding - 40 * 2) // 2,
						y = current_padding_top,
						fill = self.inner_bg,
						outline=self.accent_color,
						width=10
					)
					
					try:
						attribute_img = Image.open(f"assets/{value}.png")
						attribute_img = attribute_img.resize([int(0.09 * s) for s in attribute_img.size], Image.LANCZOS)
						attribute_img_x = int(desc_padding - attribute_img.size[0]) // 2
						attribute_img_y = current_padding_top + 17
						self.card.paste(attribute_img, (attribute_img_x, attribute_img_y), mask=attribute_img)
					except Exception:
						pass
					
					current_padding_top += 100

		def write_description():
			current_padding = card_height - (card_height * 32 / 100)

			# Set Title
			draw.text((desc_padding, current_padding), self.name.upper(), fill="black", font=self.title_font)
			current_padding += self.title_font.getbbox(self.name.upper())[3] + 5

			# Set Type
			draw.text((desc_padding, current_padding), f"{self.type.capitalize()} Encounter", fill=self.accent_color, font=self.type_font)
				
			current_padding += self.type_font.getbbox(self.type)[3] + 10

			# Information
			para = textwrap.wrap(self.description, width=42)
			for line in para:
				draw.text((desc_padding, current_padding), line, fill="black", font=self.normal_font)
				current_padding += self.font_size + 5
			current_padding += 12

			# Effect
			para = textwrap.wrap(f"Effect: {self.effect}", width=42)
			for line in para:
				draw.text((desc_padding, current_padding), line, fill="black", font=self.normal_font)
				current_padding += self.font_size + 5

		#----------------------------------------------------------------------------------------------------------------------------------------#
		# Start drawing the card's details                                                                                                       #
		#----------------------------------------------------------------------------------------------------------------------------------------#
		layout = Image.new("RGB", self.layout_size, "white")

		# Get card dimensions with border
		card_width, card_height = layout.size
		card_width += 2 * self.border_size
		card_height += 2 * self.border_size

		# Create new image with border
		self.card = Image.new("RGB", (card_width, card_height), "black")
		self.card.paste(layout, (self.border_size, self.border_size))

		# Put the card's image
		card_avatar = Image.open(f"card_images/{self.image}")
		self.card.paste(card_avatar, ((card_width - card_avatar.size[0]) // 2, int(card_height * 0.6 - card_avatar.size[1]) // 2))

		# Initialize drawing methods
		draw = ImageDraw.Draw(self.card)

		# The left padding where the description text starts
		desc_padding = card_width * .3

		# Draw the layout's shapes
		draw_outline()

		# Draw the attribute circles
		draw_attributes()

		# Draw the details section
		write_description()

	def export(self):
		self.create()
		
		card_name = self.name.lower().replace(" ", "_")
		self.card.save(f"cards/{card_name}.png")
		print(f"Card '{card_name}' created successfully.")

if __name__ == "__main__":
	json_file = open('cards.json')
	cards = json.load(json_file)

	for item in cards:
		card = Card(**item)
		card.export()
