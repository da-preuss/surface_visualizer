import sys

from OpenGL import GL as gl
import glfw
import glm


class Window:

	def __init__(self, title, size,
				 profile = { glfw.CONTEXT_VERSION_MAJOR : 3, 
				 			 glfw.CONTEXT_VERSION_MINOR : 3,
				 			 glfw.OPENGL_FORWARD_COMPAT : True,
				 		 	 glfw.OPENGL_PROFILE : glfw.OPENGL_CORE_PROFILE }):

		self.mouse = [0.0, 0.0]
		self.mouse_wheel_factor = 0.1

		self.translate = False
		self.translation_factor = 0.01
		self.translation = [0.0, 0.0, -2.5]
		
		self.rotate = False
		self.rotation_factor = 0.01
		self.rotation = [0.0, 0.0, 0.0]

		self.pressure_perc = 1
		self.triang = 0
		self.wireframe = False

		self.__build_proj_matrix(size)
		self.__build_view_matrix()

		if not glfw.init():
			print('GLFW could not be initialized')
			sys.exit(1)

		for key, value in profile.items():
			glfw.window_hint(key, value)

		self.window = glfw.create_window(size[0], size[1], title, None, None)
		if not self.window:
			print('GLFW window could not be created')
			glfw.terminate()
			sys.exit(1)

		glfw.make_context_current(self.window)

		glfw.set_window_size_callback(self.window, self.__window_size_callback)
		glfw.set_cursor_pos_callback(self.window, self.__mouse_move_callback)
		glfw.set_mouse_button_callback(self.window, self.__mouse_button_callback)
		glfw.set_scroll_callback(self.window, self.__scroll_callback)
		glfw.set_key_callback(self.window, self.__key_callback)

		gl.glClearColor(0.0, 0.0, 0.0, 1.0)
		gl.glViewport(0, 0, size[0], size[1])

	def __del__(self):
		#glfw.terminate()
		#glfw.destroy_window(self.window)
		pass
		
	def add_model(self, model):
		self.model = model

	def __window_size_callback(self, window, width, height):
		gl.glViewport(0, 0, width, height)
		self.__build_proj_matrix([width, height])
		pass

	def __mouse_button_callback(self, window, button, action, mods):
		if button == glfw.MOUSE_BUTTON_LEFT:
			if action == glfw.PRESS:
				x_pos, y_pos = glfw.get_cursor_pos(window)
				self.mouse = [x_pos, y_pos]
				self.rotate = True
			elif action == glfw.RELEASE:
				self.rotate = False
		elif button == glfw.MOUSE_BUTTON_RIGHT:
			if action == glfw.PRESS:
				x_pos, y_pos = glfw.get_cursor_pos(window)
				self.mouse = [x_pos, y_pos]
				self.translate = True
			elif action == glfw.RELEASE:
				self.translate = False
		
	def __mouse_move_callback(self, window, x_pos, y_pos):
		if self.rotate:
			self.rotation[0] -= (self.mouse[1] - y_pos) * self.rotation_factor
			self.rotation[2] -= (self.mouse[0] - x_pos) * self.rotation_factor
			self.mouse = [x_pos, y_pos]
			self.model.update_matrix(self.rotation)
		elif self.translate:
			self.translation[0] += (self.mouse[0] - x_pos) * self.translation_factor
			self.translation[1] -= (self.mouse[1] - y_pos) * self.translation_factor
			self.mouse = [x_pos, y_pos]
			self.__build_view_matrix()

	def __scroll_callback(self, window, x_offset, y_offset):
		self.translation[2] += self.mouse_wheel_factor * y_offset
		if self.translation[2] >= 0:
			self.translation[2] = 0

		self.__build_view_matrix()

	def __key_callback(self, window, key, scancode, action, mods):
		if key == glfw.KEY_W and action == glfw.PRESS:
			self.wireframe = not self.wireframe
			if self.wireframe:
				gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
			else:
				gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

		elif key == glfw.KEY_R and action == glfw.PRESS:
			self.rotation = [0, 0, 0]
			self.translation = [0, 0, -2.5]
			self.model.update_matrix(self.rotation)
			self.__build_view_matrix()

		elif key == glfw.KEY_1 and action == glfw.PRESS:
			if self.pressure_perc != 1:
				self.pressure_perc = 1
				self.model.update_color(self.pressure_perc - 1)
		elif key == glfw.KEY_2 and action == glfw.PRESS:
			if self.pressure_perc != 2:
				self.pressure_perc = 2
				self.model.update_color(self.pressure_perc - 1)
		elif key == glfw.KEY_3 and action == glfw.PRESS:
			if self.pressure_perc != 3:
				self.pressure_perc = 3
				self.model.update_color(self.pressure_perc - 1)
		elif key == glfw.KEY_4 and action == glfw.PRESS:
			if self.pressure_perc != 4:
				self.pressure_perc = 4
				self.model.update_color(self.pressure_perc - 1)

		elif key == glfw.KEY_LEFT and action == glfw.PRESS:
			self.triang -= 1
			self.triang = 2 if self.triang == -1 else self.triang
			self.model.update_indices(self.triang)
		elif key == glfw.KEY_RIGHT and action == glfw.PRESS:	
			self.triang = (self.triang + 1) % 3
			self.model.update_indices(self.triang)

	def __build_proj_matrix(self, size, fov = 45.0, 
						  planes = { 'Near' : 0.1, 'Far' : 100.0 }):
		self.proj_matrix = glm.perspective(fov, size[0] / size[1], 
									planes['Near'], planes['Far'])

	def __build_view_matrix(self):
		self.view_matrix = glm.translate(glm.mat4(), glm.vec3(self.translation))

	def should_close(self):
		return glfw.window_should_close(self.window)

	def update(self):
		glfw.poll_events()
		glfw.swap_buffers(self.window)

	def get_view_matrix(self):
		return self.view_matrix

	def get_proj_matrix(self):
		return self.proj_matrix

