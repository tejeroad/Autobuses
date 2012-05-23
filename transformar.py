import pyproj
p1 = pyproj.Proj(init='epsg:26915')
p2 = pyproj.Proj(init='epsg:26715')
x1, y1 = p1(-92.199881,38.56694)
x2, y2 = pyproj.transform(p1,p2,x1,y1)
print x2, y2

