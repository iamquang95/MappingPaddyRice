import shapefile

sf = shapefile.Reader(".\PaddyRice.shp")

shapes = sf.shapes()

for shape in shapes:
	points = shape.points		
	