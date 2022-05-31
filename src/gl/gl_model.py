import numpy as np
import pandas as pd
import matplotlib as mpl
from scipy.spatial import Delaunay
import ctypes

from OpenGL import GL as gl
import glfw
import glm

from gl.gl_vao import VAO


class Model:

	def __init__(self, filename, position_loc, color_loc):

		self.color_loc = color_loc

		self.points, self.indices, vertex_positions, vertex_pressures = load_points(filename)
		self.vertex_colors = pressure_to_color(vertex_pressures)

		self.vao = VAO()
		self.vao.attach_vertex_buffer(position_loc, vertex_positions, 3)
		self.color_buffer_id = self.vao.attach_vertex_buffer(color_loc, self.vertex_colors[0], 4, gl.GL_DYNAMIC_DRAW)

		self.update_matrix([0.0, 0.0, 0.0])

	def __del__(self):
		del self.vao

	def bind(self):
		self.vao.bind()

	def unbind(self):
		self.vao.unbind()

	def update_color(self, index):
		self.bind()
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.color_buffer_id)
		data = np.array(self.vertex_colors[index], dtype = 'float32')
		gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, len(data) * ctypes.sizeof(ctypes.c_float), data.tobytes())
		self.unbind()

	def update_indices(self, triang):
		if triang == 0:
			self.indices = triangulate(self.points, [0, 1])
		if triang == 1:
			self.indices = triangulate(self.points, [0, 2])
		if triang == 2:
			self.indices = triangulate(self.points, [1, 2])

	def draw(self):
		self.bind()
		gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices), gl.GL_UNSIGNED_INT, self.indices)
		self.unbind()

	def update_matrix(self, rotation):
		matrix = glm.mat4()
		matrix = glm.rotate(matrix, rotation[0], glm.vec3(1.0, 0.0, 0.0))
		matrix = glm.rotate(matrix, rotation[1], glm.vec3(0.0, 1.0, 0.0))
		self.model_matrix = glm.rotate(matrix, rotation[2], glm.vec3(0.0, 0.0, 1.0))

	def get_matrix(self):
		return self.model_matrix


def load_points(input_file):
	dataframe = pd.read_excel(input_file)

	points = [dataframe.iloc[:, 1][1:].to_numpy().flatten(),
					dataframe.iloc[:, 2][1:].to_numpy().flatten(),
					dataframe.iloc[:, 3][1:].to_numpy().flatten()]

	min_values = [0.5 * min(points[0]), 0.5 * min(points[1]), 0.5 * min(points[2])]
	max_values = [0.5 * max(points[0]), 0.5 * max(points[1]), 0.5 * max(points[2])]

	indices = triangulate(points, [0, 1])

	position_data = dataframe.iloc[:, [1, 2, 3]]
	position_data = position_data[1:]

	vertex_positions = position_data.to_numpy()
	transformed_positions = transform_to_ndc(vertex_positions, min_values, max_values)

	pressure_data = dataframe.iloc[:, [4, 5, 6, 7]]
	pressure_data = pressure_data[1:]

	vertex_pressures = [dataframe.iloc[:, index][1:].to_numpy().flatten() for index in range(4, 8)]

	return points, indices, transformed_positions, vertex_pressures

def triangulate(points, plane):
	x1 = np.vstack((points[plane[0]], points[plane[1]])).T
	triang = Delaunay(x1)
	return triang.simplices.flatten()

def transform_to_ndc(vertex_positions, min_values, max_values):

	transformed_positions = vertex_positions.copy()	
	for position in transformed_positions:
		position[0] = position[0] - min_values[0] - max_values[0]
		position[1] = position[1] - min_values[1] - max_values[1]
		position[2] = position[2] - min_values[2] - max_values[2]

	transformed_positions = transformed_positions.flatten()
	max_value = abs(max(transformed_positions, key = abs))
	for i in range(len(transformed_positions)):
		transformed_positions[i] /= max_value
		
	return transformed_positions

def pressure_to_color(vertex_pressures):
	# scale pressures between 0 and 1
	for idx, perc_pressures in enumerate(vertex_pressures):
		min_pressure, max_pressure = min(perc_pressures), max(perc_pressures)
		vertex_pressures[idx] = [(pressure - min_pressure) / (max_pressure - min_pressure) for pressure in perc_pressures]

	# map pressure values to colormap
	cmap = mpl.colormaps['viridis']
	return [cmap(pressure).flatten() for pressure in vertex_pressures]