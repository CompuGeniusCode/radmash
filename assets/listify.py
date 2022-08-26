import os
from titlecase import titlecase


template = "<li><a href=\"%s\" target=\"blank\">%s</a></li>"
path = "/divrei_torah/maamarei_full/"
for x in os.listdir():
    parsha = str(x.split("- ")[1]).removesuffix(" 2022.pdf")
    print(template % ((path + x), (titlecase(parsha)) + " 5782"))
