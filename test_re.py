import re
p = re.compile(r'(\b1?2?3?4?\b)')
print(p.match('12311'))