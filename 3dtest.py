import bpy

# 1. Clear the stage (Delete the default cube/objects)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. Define our Rebel message for the console
print("VENTENVS VIVIT - Constructing Monument...")

# 3. Create a stack of blocks (The Monument)
for i in range(5):
    # Calculate height for each block
    z_location = i * 2.2 
    
    # Add a cube at the calculated location
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, z_location))
    
    # Give it a slightly random rotation for a "weathered" look
    bpy.context.object.rotation_euler[2] = i * 0.1

print("Donec Perficiam: Construction Complete.")