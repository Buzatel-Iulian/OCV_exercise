

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

		return data

if __name__ == "__main__" :
	print(read_off("Appendix_C/sp.off"))
