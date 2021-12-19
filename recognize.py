import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def line(image):
	lines = np.sum(image, axis=0) // image.shape[0]
	return 1 in lines

def fill(image):
	return np.sum(image) / image.size

def account(image):
	b = ~image
	lb = label(b)
	areas = regionprops(lb)

	count_1 = 0
	count_2 = 0

	for area in areas:
		on_bound = False
		for y, x in area.coords:
			if y == 0 or x == 0 or \
				y == image.shape[0]-1 or \
				x == image.shape[1]-1:
				on_bound = True
				break
		if not on_bound:
			count_1 += 1
		else:
			count_2 += 1
	return count_1, count_2


def identify(region):
	if np.all(region.image):
		return '-'
	area_l, area_d = account(region.image)
	if area_l == 2:
		if line(region.image):
			return "B"
		else:
			return "8"
	elif area_l == 1:
		if area_d == 2:
				if region.image[region.image.shape[0]//2, region.image.shape[1]//2] > 0:
					return "P"
				else:
					return "D"
		elif area_d == 3:
			return "A"
		else:
			return "0"
	elif area_l == 0:
		if area_d == 2:
			return "/"
		elif area_d == 3 and line(region.image):
			return "1"

		del_ar_l ,del_ar_d = account(region.image[2:-2, 2:-2])
		if del_ar_d == 4:
			return "X"
		elif del_ar_d == 5:
			cy = region.image.shape[0] // 2
			cx = region.image.shape[1] // 2
			if region.image[cy, cx] > 0:
				return "*"
			return "W`"
	return None


image = plt.imread("symbols.png")
binary = np.sum(image, 2)
binary[binary > 0] = 1

labeled = label(binary)

regions = regionprops(labeled)

clr_ar = {None: 0}
for region in regions:
    symbol = identify(region)
    if symbol not in clr_ar:
        clr_ar[symbol] = 0
    clr_ar[symbol] += 1

identify = str(round((1. - clr_ar[None] / sum(clr_ar.values())) * 100, 2))

print("Словарь: " + str(clr_ar))
print("Распознано: " + identify + "%")
