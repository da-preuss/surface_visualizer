from OpenGL import GL as gl
import ctypes
import numpy as np


class VAO:

	def __init__(self):
		self.vertex_array_id = gl.glGenVertexArrays(1)
		self.buffer_ids = []

	def __del__(self):
		self.unbind()

		gl.glDeleteBuffers(len(self.buffer_ids), self.buffer_ids)
		gl.glDeleteVertexArrays(1, [self.vertex_array_id])


	def attach_vertex_buffer(self, attrib_location, vertex_data, size_element):
		self.bind()

		vertex_buffer_id = gl.glGenBuffers(1)
		gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer_id)

		vertex_data = np.array(vertex_data, dtype = 'float32')
		gl.glBufferData(gl.GL_ARRAY_BUFFER, len(vertex_data) * ctypes.sizeof(ctypes.c_float), vertex_data.tobytes(), gl.GL_STATIC_DRAW)
		gl.glVertexAttribPointer(attrib_location, size_element, gl.GL_FLOAT, False, 0, None)
		gl.glEnableVertexAttribArray(attrib_location)

		self.buffer_ids.append(vertex_buffer_id)
		self.unbind()

		return vertex_buffer_id

	def bind(self):
		gl.glBindVertexArray(self.vertex_array_id)

	def unbind(self):
		gl.glBindVertexArray(0)