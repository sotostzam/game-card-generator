from PIL import Image, ImageDraw, ImageFont, ImageColor
import math

class Card:
	"""
	Class representing a customizable game card.
	"""
	def __init__(self, name, type, info, effect, image, attributes=None, border_size=5, font_size=30, font_path=None):
		"""
		Initializes a Card object.

		Args:
		name: (str) Name of the card.
		info: (str) Additional information for the card.
		image_path: (str) Path to the image for the card.
		border_size: (int, optional) Size of the card border (default: 10).
		font_size: (int, optional) Size of the text font (default: 20).
		font_path: (str, optional) Path to a custom font file (default: None).
		"""
		self.name = name
		self.type = type
		self.info = info
		self.effect = effect
		self.image_path = image
		self.border_size = border_size
		self.attributes = attributes

		self.font_size = font_size
		self.font_path = font_path
		self.normal_font = ImageFont.truetype(f"fonts/{self.font_path}" or "arial.ttf", self.font_size)

		self.layout_size = (750, 1050)

		self.inner_bg = "black"
		self.green = ImageColor.getrgb("#9ac360")
		self.yellow = ImageColor.getrgb("#966a00")

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
		card_avatar = Image.open(f"images/{self.image_path}")
		card.paste(card_avatar, ((card_width - card_avatar.size[0]) // 2, int(card_height * 0.6 - card_avatar.size[1]) // 2))

		# Initialize drawing methods
		draw = ImageDraw.Draw(card)

		details_pad_left = card_width * .3
		details_pad_top = card_height - (card_height * 32 / 100)

		# Draw the layout's shapes
		shape = [(0 + self.border_size, card_height - (card_height * .377)), (card_width - self.border_size - 0.01, card_height - (card_height * .377))]
		draw.line(shape, fill=self.green, width=20)

		circle_radius = 65
		circle_x = (details_pad_left - circle_radius * 2) // 2
		circle_y = card_height - (card_height * .44)

		draw.ellipse((circle_x, circle_y, circle_x + circle_radius * 2, circle_y + circle_radius * 2),
					  fill=self.inner_bg,
					  outline=self.green,
					  width=10)

		vertices = self.makeRectangle(41, 41, 45*math.pi/180, offset=(card_width * .308, card_height - (card_height * .377)))
		draw.polygon(vertices, fill=self.inner_bg, width=10, outline=self.green)

		# Draw the circles for the attributes
		if self.attributes:
			circle_radius = 35
			attributes_pad_left = (details_pad_left - circle_radius * 2) // 2
			attributes_pad_top = card_height - (card_height * .28)

			for attribute, value in self.attributes.items():
				draw.ellipse((attributes_pad_left, attributes_pad_top,
							attributes_pad_left + circle_radius * 2, attributes_pad_top + circle_radius * 2),
							fill=self.inner_bg,
							outline=self.yellow,
					  		width=5)
				
				attributes_pad_top += 100

		# Draw the details section
		current_padding = details_pad_top

		# Set Title
		title_font = ImageFont.truetype("fonts/asap_symbol.otf" or "arial.ttf", self.font_size+10)
		draw.text((details_pad_left, current_padding), self.name.upper(), fill="black", font=title_font)
		current_padding += title_font.getbbox(self.name.upper())[3] + 5

		# Set Type
		type_font = ImageFont.truetype("fonts/EduSABeginner_bold.ttf" or "arial.ttf", self.font_size-10)
		draw.text((details_pad_left, current_padding), self.type, fill=ImageColor.getrgb("#966a00"), font=type_font)
		current_padding += type_font.getbbox(self.type)[3] + 10

		# Information
		draw.text((details_pad_left, current_padding), self.info, fill="black", font=self.normal_font)
		current_padding += self.normal_font.getbbox(self.info)[3] + 10

		# Effect
		import textwrap
		para = textwrap.wrap(f"Effect: {self.effect}", width=40)
		
		for line in para:
			draw.text((details_pad_left, current_padding), line, fill="black", font=self.normal_font)
			current_padding += self.font_size + 5
		
		# Save the card image
		card_name = self.name.lower().replace(" ", "_")
		card.save(f"cards/{card_name}.png")
		print(f"Card created and saved as '{card_name}.png'.")

# Example usage
card = Card(name="Cum Snail",
			type="Mythical Encounter",
			info="It sticks everywhere.",
			effect="Rub each others genitals for 2 minutes.",
			image="penis.png",
			border_size=0,
			attributes={
				'genders': 'both',
				'cum': 'cum'
			},
			font_path="EduSABeginner.ttf")
card.create_card()
