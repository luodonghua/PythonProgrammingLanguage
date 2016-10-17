import urllib.request
from xml.etree.ElementTree import XML
import sys
if len(sys.argv)!=3:
    raise SystemExit('Usage: nextbus.py route stopid')

route=sys.argv[1]
stopid=sys.argv[2]
print('Route: {}'.format(route))
print('Stop ID: {}'.format(stopid))

u=urllib.request.urlopen('http://ctabustracker.com/bustime/map/getStopPredictions.jsp?stop={}&route={}'.format(stopid,route))
data=u.read()
# print(data)
doc=XML(data)

for pt in doc.findall('.//pt'):
    print(pt.text)