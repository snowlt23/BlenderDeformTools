
import bpy
import bmesh

bl_info = {
	"name": "BlenderDeformTools",
	"author": "shsnow23",
	"version": (0, 1),
	"blender": (2, 7, 6),
	"location": "",
	"description": "",
	"warning": "",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Sculpt"
}

class DeformOperator(bpy.types.Operator):
	bl_idname = "wm.deform_operator"
	bl_label = "DeformOperator"

	def execute(self, context):
		bpy.ops.object.mode_set(mode='SCULPT')
		bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.reveal()
		bpy.ops.object.vertex_group_assign_new()

		bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
		selected_verts = [i.co for i in bm.verts if i.select]

		top = None
		bottom = None
		left = None
		right = None
		front = None
		back = None
		for v in selected_verts:
			if top == None:
				top = v[2]
			elif top < v[2]:
				top = v[2]

			if bottom == None:
				bottom = v[2]
			elif bottom > v[2]:
				bottom = v[2]

			if left == None:
				left = v[1]
			elif left > v[1]:
				left = v[1]

			if right == None:
				right = v[1]
			elif right < v[1]:
				right = v[1]

			if front == None:
				front = v[0]
			elif front < v[0]:
				front = v[0]

			if back == None:
				back = v[0]
			elif back > v[0]:
				back = v[0]

		bpy.ops.mesh.select_all(action='DESELECT')

		lattice = bpy.data.lattices.new("Lattice")
		lattice_ob = bpy.data.objects.new("Lattice", lattice)

		x_scale = (front - back) / (lattice.points[5].co[0] - lattice.points[4].co[0])
		y_scale = (right - left) / (lattice.points[7].co[1] - lattice.points[5].co[1])
		z_scale = (top - bottom) / (lattice.points[5].co[2] - lattice.points[1].co[2])

		lattice_ob.scale = (x_scale, y_scale, z_scale)
		lattice_ob.location = ((front+back) / 2, (right+left) / 2, (top+bottom) / 2)

		scene = bpy.context.scene

		lattice_mod = scene.objects.active.modifiers.new("Lattice", 'LATTICE')
		lattice_mod.object = lattice_ob
		lattice_mod.vertex_group = bpy.context.object.vertex_groups.active.name

		scene.objects.link(lattice_ob)
		scene.update()

		for o in bpy.context.scene.objects:
			o.select = False
		lattice_ob.select = True
		bpy.context.scene.objects.active = lattice_ob
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.editmode_toggle()

		return {'FINISHED'}

class DeformTools(bpy.types.Panel):
	bl_idname = "OBJECT_PT_deform_tools"
	bl_label = "DeformTools"
	bl_category = "Sculpt"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("wm.deform_operator", text="CreateDeformBox")

def register():
	bpy.utils.register_class(DeformOperator)
	bpy.utils.register_class(DeformTools)

def unregister():
	bpy.utils.unregister_class(DeformOperator)
	bpy.utils.unregister_class(DeformTools)

if __name__ == "__main__":
	register()