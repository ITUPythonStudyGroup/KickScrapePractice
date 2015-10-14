import urllib.request
import lxml.html
import re, json, html
# Make a GET request and parse the HTML into a tree
# urlKs = 'https://www.kickstarter.com/projects/agfa/agfa-and-something-weird'
# htmlRaw = urllib.request.urlopen(urlKs).read()
# text_file = open("project.html", "w")
# text_file.write(htmlRaw.decode("utf-8"))
# text_file.close()

text_file = open("project.html")
tree = lxml.html.fromstring(text_file.read())
text_file.close()

# print(tree)

# Find the script that contains the JSON object
script = tree.xpath('//script[contains(text(), "window.current_project")]')[0]
# Get the JSON object from the script
jsonRaw = re.search('window.current_project = "([^"]*)', script.text).group(1)
# Fix some odd double escaping
jsonRaw = jsonRaw.replace('\\\\&quot;', '\\&quot;')
# Unescape
jsonRaw = html.unescape(jsonRaw)
# Parse and print
jsonParsed = json.loads(jsonRaw)
print(json.dumps(jsonParsed, indent=4))
