import sys
import numpy as np

from OpenGL import GL as gl
import glfw
import glm

from gl_window import Window
from gl_shader_program import Shader_Program
from gl_model import Model


def main(filename):

	window_size = [1280, 1024]
	window = Window('Surface Visualizer', window_size)

	shader_paths = { gl.GL_VERTEX_SHADER   : 'shaders/vertex_shader.glsl',
				 	 gl.GL_FRAGMENT_SHADER : 'shaders/fragment_shader.glsl' }
	shader_program = Shader_Program(shader_paths)

	position_location = gl.glGetAttribLocation(shader_program.program_id, 'vertex_pos')
	color_location = gl.glGetAttribLocation(shader_program.program_id, 'vertex_color')
	model = Model(filename, position_location, color_location)

	window.add_model(model)

	mvp_location = gl.glGetUniformLocation(shader_program.program_id, 'mvp')

	shader_program.activate()

	gl.glEnable(gl.GL_DEPTH_TEST)
	while not window.should_close():
		gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

		mvp_matrix = window.get_proj_matrix() * window.get_view_matrix() * model.get_matrix()

		gl.glUniformMatrix4fv(mvp_location, 1, gl.GL_FALSE, glm.value_ptr(mvp_matrix))
		model.draw()

		window.update()

	del model
	del shader_program
	del window
	glfw.terminate()

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('Missing filename')
	else:
		filename = sys.argv[1]
		main(filename)