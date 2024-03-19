from PIL import Image, ImageDraw, ImageFont, ImageColor
import math
import json
import textwrap

class Card:
	"""
	Class representing a customizable game card.
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
		self.type = type
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
		self.red = ImageColor.getrgb("#bf3f3f")
		self.green = ImageColor.getrgb("#9ac360")
		self.blue = ImageColor.getrgb("#4446c2")
		self.yellow = ImageColor.getrgb("#966a00")

		self.buff = ImageColor.getrgb("#41c4bc")
		self.debuff = ImageColor.getrgb("#c74a7e")
		self.magic = ImageColor.getrgb("#9560c3")

		# Set the card accent colors and class based on creature type
		if self.type == 'normal':
			self.accent_color = self.blue
			self.card_class = 'creature'
		elif self.type == 'annoying':
			self.accent_color = self.red
			self.card_class = 'creature'
		elif self.type == 'mythical':
			self.accent_color = self.yellow
			self.card_class = 'creature'
		elif self.type == 'magic':
			self.accent_color = self.magic
			self.card_class = 'magic'
		elif self.type == 'buff':
			self.accent_color = self.buff
			self.card_class = 'buff'
		elif self.type == 'debuff':
			self.accent_color = self.debuff
			self.card_class = 'debuff'

	def makeRectangle(self, l, w, theta, offset=(0,0)):
		c, s = math.cos(theta), math.sin(theta)
		rectCoords = [(l/2.0, w/2.0), (l/2.0, -w/2.0), (-l/2.0, -w/2.0), (-l/2.0, w/2.0)]
		return [(c*x-s*y+offset[0], s*x+c*y+offset[1]) for (x,y) in rectCoords]
		
	def create_card(self):
		"""
		Creates and saves the card image.
		"""
		layout = Image.new("RGB", self.layout_size, "white")

		# Get card dimensions with border
		card_width, card_height = layout.size
		card_width += 2 * self.border_size
		card_height += 2 * self.border_size

		# Create new image with border
		card = Image.new("RGB", (card_width, card_height), "black")
		card.paste(layout, (self.border_size, self.border_size))

		# Put the card's image
		card_avatar = Image.open(f"card_images/{self.image}")
		card.paste(card_avatar, ((card_width - card_avatar.size[0]) // 2, int(card_height * 0.6 - card_avatar.size[1]) // 2))

		# Initialize drawing methods
		draw = ImageDraw.Draw(card)

		details_pad_left = card_width * .3
		details_pad_top = card_height - (card_height * 32 / 100)

		# Draw the layout's shapes
		shape = [(0 + self.border_size, card_height - (card_height * .377)), (card_width - self.border_size - 0.01, card_height - (card_height * .377))]
		draw.line(shape, fill=self.accent_color, width=20)

		circle_radius = 65
		circle_x = (details_pad_left - circle_radius * 2) // 2
		circle_y = card_height - (card_height * .44)

		draw.ellipse((circle_x, circle_y, circle_x + circle_radius * 2, circle_y + circle_radius * 2),
					  fill=self.inner_bg,
					  outline=self.accent_color,
					  width=10)
		
		card_class_image = Image.open(f"assets/{self.card_class}.png")
		card_class_image = card_class_image.resize([int(0.15 * s) for s in card_class_image.size], Image.LANCZOS)

		card_class_image_x = int(details_pad_left - card_class_image.size[0]) // 2
		card_class_image_y = int(card_height - (card_height * .417))
		card.paste(card_class_image, (card_class_image_x, card_class_image_y), mask=card_class_image)

		vertices = self.makeRectangle(41, 41, 45*math.pi/180, offset=(card_width * .308, card_height - (card_height * .377)))
		draw.polygon(vertices, fill=self.inner_bg, width=10, outline=self.accent_color)

		# Draw the circles for the attributes
		if self.attributes:
			circle_radius = 40
			attributes_pad_left = (details_pad_left - circle_radius * 2) // 2
			attributes_pad_top = int(card_height - (card_height * .29))

			for attribute, value in self.attributes.items():
				draw.ellipse((attributes_pad_left, attributes_pad_top,
							attributes_pad_left + circle_radius * 2, attributes_pad_top + circle_radius * 2),
							fill=self.inner_bg,
							outline=self.accent_color,
					  		width=5)
				
				try:
					attribute_img = Image.open(f"assets/{value}.png")
					attribute_img = attribute_img.resize([int(0.09 * s) for s in attribute_img.size], Image.LANCZOS)
					attribute_img_x = int(details_pad_left - attribute_img.size[0]) // 2
					attribute_img_y = attributes_pad_top + 17
					card.paste(attribute_img, (attribute_img_x, attribute_img_y), mask=attribute_img)
				except Exception:
					pass
				
				attributes_pad_top += 100

		# Draw the details section
		current_padding = details_pad_top

		# Set Title
		draw.text((details_pad_left, current_padding), self.name.upper(), fill="black", font=self.title_font)
		current_padding += self.title_font.getbbox(self.name.upper())[3] + 5

		# Set Type
		draw.text((details_pad_left, current_padding), f"{self.type.capitalize()} Encounter", fill=self.accent_color, font=self.type_font)
			
		current_padding += self.type_font.getbbox(self.type)[3] + 10

		# Information
		para = textwrap.wrap(self.description, width=42)
		for line in para:
			draw.text((details_pad_left, current_padding), line, fill="black", font=self.normal_font)
			current_padding += self.font_size + 5
		current_padding += 12

		# Effect
		para = textwrap.wrap(f"Effect: {self.effect}", width=42)
		for line in para:
			draw.text((details_pad_left, current_padding), line, fill="black", font=self.normal_font)
			current_padding += self.font_size + 5
		
		# Save the card image
		card_name = self.name.lower().replace(" ", "_")
		card.save(f"cards/{card_name}.png")
		print(f"Card '{card_name}' created successfully.")

if __name__ == "__main__":
	json_file = open('cards.json')
	cards = json.load(json_file)

	for item in cards:
		card = Card(**item)
		card.create_card()
