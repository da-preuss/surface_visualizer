#version 330 core

layout (location = 0) in vec3 vertex_pos;
layout (location = 1) in vec4 vertex_color;

smooth out vec4 frag_color;

uniform mat4 mvp;


void main() {
	gl_Position = mvp * vec4(vertex_pos, 1.0);
	frag_color = vertex_color;
}