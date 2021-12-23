#from math import *
from vectors import *

def normal(face):
	#print(cross(subtract(face[1], face[0]), subtract(face[2], face[0])))
	return(cross(subtract(face[1], face[0]), subtract(face[2], face[0])))


def shade(face, light=(20,0,20)):
	#print(color_map(1 - dot(unit(normal(face)), unit(light))))
	print(1 - dot(unit(normal(face)), unit(light)))
	return 1 - dot(unit(normal(face)), unit(light))
	#return color_map(1 - dot(unit(normal(face)), unit(light)))


def read_off( file ):
	with open( file ) as f :
		line = f.readline()
		data = {}
		print("importing " + line + " file")
		line = f.readline()
		v_count, f_count, e_count = line.split(" ")
		print(v_count + " vertexes")
		print(f_count + " faces")
		print(e_count + " edges")
		data["vertex_count"] = int(v_count)
		data["face_count"] = int(f_count)
		data["edge_count"] = int(e_count)
		data["vertexes"] = {}
		data["faces"] = {}
		data["edges"] = {}
		for i in range(data["vertex_count"]):
			#print(i)
			line = f.readline()
			#print(line)
			x, y, z, aux= line.split(" ")
			data["vertexes"][i] = {}
			data["vertexes"][i]["x"] = float(x)
			data["vertexes"][i]["y"] = float(y)
			data["vertexes"][i]["z"] = float(z)
		for i in range(data["face_count"]):
			line = f.readline()
			n, v1, v2, v3, aux = line.split(" ")
			data["faces"][i] = {}
			data["faces"][i]["v1"] = int(v1)
			data["faces"][i]["v2"] = int(v2)
			data["faces"][i]["v3"] = int(v3)

		return data

if __name__ == "__main__" :
	print(read_off("Appendix_C/sp.off"))
