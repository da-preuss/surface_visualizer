from OpenGL import GL as gl
import sys


class Shader_Program:

	def __init__(self, shader_paths):
		self.program_id = gl.glCreateProgram()
		for shader_type, shader_path in shader_paths.items():
			shader_src = self.__read_shader_source(shader_path)
			shader_id  = self.__build_shader(shader_type, shader_src)

			gl.glAttachShader(self.program_id, shader_id)
			gl.glDeleteShader(shader_id)

		gl.glLinkProgram(self.program_id)

		logmsg = gl.glGetProgramInfoLog(self.program_id)
		if logmsg:
			print(str(logmsg).replace("\\n", "\n"))
			sys.exit(1)

		
	def __del__(self):
		self.deactivate()
		gl.glDeleteProgram(self.program_id)


	def activate(self):
		gl.glUseProgram(self.program_id)

	def deactivate(self):
		gl.glUseProgram(0)

	def __read_shader_source(self, shader_path):
		shader_source = ""
		try:
			with open(shader_path) as file:
				shader_source = file.read()
		except IOError:
			print('Error loading', shader_path)
		return shader_source

	def __build_shader(self, shader_type, shader_source):
		shader_id = gl.glCreateShader(shader_type)
		gl.glShaderSource(shader_id, shader_source)
		gl.glCompileShader(shader_id)

		logmsg = gl.glGetShaderInfoLog(shader_id)
		if logmsg:
			print(str(logmsg).replace("\\n", "\n"))
			sys.exit(1)

		return shader_id
