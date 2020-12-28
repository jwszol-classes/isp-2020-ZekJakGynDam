import time
import datetime
from datetime import timezone
print(time.time())
print(datetime.datetime.now())
print(datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp())
exit()


import reverse_geocoder as rg
coordinates = ((-37.81, 144.96),)
print(rg.search(coordinates))


import reverse_geocode
coordinates = ((-37.81, 144.96),)
print(reverse_geocode.search(coordinates))