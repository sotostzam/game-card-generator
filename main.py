from PIL import Image, ImageDraw, ImageFont, ImageColor

class Card:
	"""
	Class representing a customizable game card.
	"""
	def __init__(self, name, type, info, effect, image, attributes=None, layout="layout.png", border_size=5, font_size=30, font_path=None):
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
		self.layout = layout
		self.image_path = image
		self.border_size = border_size
		self.font_size = font_size
		self.font_path = font_path
		self.attributes = attributes
		
		self.safe_area_width = 8/100
		self.safe_area_height = 5.71/100

		self.green = "#9ac360"

	def create_card(self):
		"""
		Creates and saves the card image.
		"""
		# Load image
		layout = Image.open(f"assets/{self.layout}")

		# Get card dimensions with border
		card_width, card_height = layout.size
		card_width += 2 * self.border_size
		card_height += 2 * self.border_size

		details_pad_left = card_width * .3
		details_pad_top = card_height - (card_height * 32 / 100)

		# Create new image with border
		card_image = Image.new("RGB", (card_width, card_height), "black")
		card_image.paste(layout, (self.border_size, self.border_size))

		# Put the card's image
		card_avatar = Image.open(f"images/{self.image_path}")
		card_image.paste(card_avatar, ((card_width - card_avatar.size[0]) // 2, int(card_height * 0.6 - card_avatar.size[1]) // 2))

		draw = ImageDraw.Draw(card_image)
		normal_font = ImageFont.truetype(f"fonts/{self.font_path}" or "arial.ttf", self.font_size)

		# Draw the layout circle
		circle_radius = 65
		layout_circle_x = (details_pad_left - circle_radius * 2) // 2
		layout_circle_y = card_height - (card_height * .44)

		draw.ellipse((layout_circle_x, layout_circle_y,
					  layout_circle_x + circle_radius * 2, layout_circle_y + circle_radius * 2),
					  fill=ImageColor.getrgb(self.green))
	
		inner_offset = 5
		circle_radius = 55
		layout_circle_x = (details_pad_left - circle_radius * 2) // 2
		layout_circle_y = card_height - (card_height * .44) + 10

		draw.ellipse((layout_circle_x, layout_circle_y,
					  layout_circle_x + circle_radius * 2, layout_circle_y + circle_radius * 2),
					  fill=0)
		
		shape = [(0 + self.border_size, card_height - (card_height * .377)), (200, card_height - (card_height * .377))]
		draw.line(shape, fill ="red", width = 20)

		# Start drawing the attributes
		if self.attributes:
			rad = 35
			attributes_pad_left = (details_pad_left - rad * 2) // 2
			attributes_pad_top = card_height - (card_height * .28)

			for attribute, value in self.attributes.items():
				draw.ellipse((attributes_pad_left, attributes_pad_top,
							attributes_pad_left + rad * 2, attributes_pad_top + rad * 2),
							fill=ImageColor.getrgb("#966a00"))
				draw.ellipse((attributes_pad_left + 5, attributes_pad_top + 5,
							attributes_pad_left + 5 + (rad - 5) * 2, attributes_pad_top + 5 + (rad - 5) * 2),
							fill=0)
				
				attributes_pad_top += 100

		# Start drawing the details
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
		draw.text((details_pad_left, current_padding), self.info, fill="black", font=normal_font)
		current_padding += normal_font.getbbox(self.info)[3] + 10

		# Effect
		import textwrap
		para = textwrap.wrap(f"Effect: {self.effect}", width=40)
		
		for line in para:
			draw.text((details_pad_left, current_padding), line, fill="black", font=normal_font)
			current_padding += self.font_size + 5
		
		# Save the card image
		card_name = self.name.lower().replace(" ", "_")
		card_image.save(f"cards/{card_name}.png")
		print(f"Card created and saved as '{card_name}.png'.")

# Example usage
card = Card(name="Cum Snail",
			type="Mythical Encounter",
			info="It sticks everywhere.",
			effect="Rub each others genitals for 2 minutes.",
			image="penis.png",
			attributes={
				'genders': 'both',
				'cum': 'cum'
			},
			font_path="EduSABeginner.ttf")
card.create_card()
