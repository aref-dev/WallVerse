import json

# Example of product to be hosted on the site:

# quote_pack = {
#     "Name": "Fortune",
#     "Description": "A fun command-line tool that delivers random quotes, jokes, or messages to brighten your terminal.",
#     "img_url": "",
#     "Quotes": ['A radioactive cat has eighteen half-lives.',
#                'A real patriot is the fellow who gets a parking ticket and rejoices that the system works.']
# }

# I want the user to be able to sync the quote packs they own with a token through an API

# Creating sample product from fortune.txt
# with open("resources/quote_packs/franklin.txt") as file:
#     data = file.read().split("%")
#     quotes = [quote.strip('\n') for quote in data]
#     franklin_pack = {
#         "Name": "Poor Richard's Almanack",
#         "Description": "Benjamin Franklin's timeless collection of practical wisdom and advice.",
#         "img_url": "",
#         "Quotes": quotes}
#
# with open("resources/quote_packs/franklin.json", "w") as file:
#     json.dump(franklin_pack, file)