import sys
import numpy as np
from argparse import ArgumentParser

from OpenGL import GL as gl
import glfw
import glm

from gl.gl_window import Window
from gl.gl_shader_program import Shader_Program
from gl.gl_model import Model


def main():

	parser = ArgumentParser()
	parser.add_argument('-f', '--file', help = 'Path to the input file')

	args = parser.parse_args()
	filename = args.file

	window_size = [1280, 1024]
	window = Window('Surface Visualizer', window_size)

	shader_paths = { gl.GL_VERTEX_SHADER   : 'src/shaders/vertex_shader.glsl',
				 	 gl.GL_FRAGMENT_SHADER : 'src/shaders/fragment_shader.glsl' }
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
	main()