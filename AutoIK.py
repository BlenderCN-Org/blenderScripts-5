import bpy

"""#armature = bpy.data.objects["KeiraRig"].data
# better:
armature = bpy.data.armatures["Armature_Keira"]
armature.bones["IK_Leg_Pole.L"]
# For clearing parent:
armature.bones["IK_Leg_Pole.L"].parent
# For removing deform on control and pole bones
armature.bones["IK_Leg_Pole.L"].use_deform

# Creating an IK constraint and filling it in:
bpy.ops.pose.constraint_add(type="IK")
# Target/pole
pose.bones["shin.L"].constraints["IK"].target
pose.bones["shin.L"].constraints["IK"].subtarget
pose.bones["shin.L"].constraints["IK"].pole_target
pose.bones["shin.L"].constraints["IK"].pole_subtarget
# Arguments
pose.bones["shin.L"].constraints["IK"].chain_count
pose.bones["shin.L"].constraints["IK"].pole_angle

# Extruding the control bone (there's probably a better way to do this like just extrude()
# or maybe just add a bone out of thin air and move it so you don't have to deal with parenting and such)
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False},
                              TRANSFORM_OT_translate={"value":(0, 0.402255, 0),
                                                      "constraint_axis":(False, True, False),
                                                      "constraint_orientation":'GLOBAL',
                                                      "mirror":False,
                                                      "proportional":'DISABLED',
                                                      "proportional_edit_falloff":'SMOOTH',
                                                      "proportional_size":1,
                                                      "snap":False,
                                                      "snap_target":'CLOSEST',
                                                      "snap_point":(0, 0, 0),
                                                      "snap_align":False,
                                                      "snap_normal":(0, 0, 0),
                                                      "gpencil_strokes":False,
                                                      "texture_space":False,
                                                      "remove_on_cancel":False,
                                                      "release_confirm":False})

# Toggling modes
bpy.ops.object.posemode_toggle()
bpy.ops.object.editmode_toggle()

# Selected objects
bpy.context.scene.objects.active = bpy.data.objects['Sphere.017']
note: can also just do object.select = True

# Selected bones
bpy.context.selected_pose_bones
pbase.bone.select=True
pbase.bone.select_tail=True
pbase.bone.select_head=True

# Deselect all
bpy.ops.pose.select_all(action='DESELECT')
"""
# bpy.ops.object.mode_set(mode='POSE')
# newIK = bpy.ops.pose.constraint_add(type="IK")
# print(newIK.target)

class AutoIkOrder:
    def __init__(self, boneName, ikName, createPole, chainLength):
        self.boneName = boneName
        self.ikName = ikName
        self.createPole = createPole
        self.chainLength = chainLength

# Before running: select any number of rigs
for selectedRig in bpy.context.selected_objects:
    # Assume the user has an object with an armature selected
    armature = selectedRig.data

    # First, make sure we are in pose mode
    bpy.ops.object.mode_set(mode='POSE')

    # Next, make sure no bones are selected
    bpy.ops.pose.select_all(action='DESELECT')
    
    autoIkOrders = [AutoIkOrder('shin', 'IK_Leg', False, 2)]
    for order in autoIkOrders:
        # Mirror operations to both sides
        for side in ['.L', '.R']:
            boneName = '{}{}'.format(order.boneName, side)
            bone = armature.bones[boneName]

            # Change to edit mode to create IK bones
            bpy.ops.object.mode_set(mode='EDIT')
            # Next, make sure no bones are selected
            bpy.ops.armature.select_all(action='DESELECT')
            
            # Create target bone
            targetBoneName = '{}_Target{}'.format(order.ikName, side)
            targetBone = armature.edit_bones.new(name=targetBoneName)
            # New bone has zero length and will be removed until resized
            targetBone.head = bone.head
            targetBone.tail = bone.head
            targetBone.tail[1] -= 0.3
            # Target bones do not deform mesh
            targetBone.use_deform = False
            
            # Create pole bone
            poleBoneName = '{}_Pole{}'.format(order.ikName, side)
            poleBone = None
            if order.createPole:
                pass

            # Change to pose mode for IK (this also saves bones in edit_bones)
            bpy.ops.object.mode_set(mode='POSE')

            # Next, make sure no bones are selected
            bpy.ops.pose.select_all(action='DESELECT')

            poseBone = selectedRig.pose.bones[boneName]
            
            # Select the bone (this might not be necessary)
            bone.select = True

            # Make the pose bone active
            armature.bones.active = armature.bones[boneName]

            # Create IK constraint
            bpy.ops.pose.ik_add()
            # Target/pole
            print(poseBone.name)
            print(bpy.context.active_pose_bone)
            poseBone.constraints[0].target = selectedRig
            poseBone.constraints[0].subtarget = targetBoneName
            if order.createPole:
                poseBone.constraints[0].pole_target = selectedRig
                poseBone.constraints[0].pole_subtarget = poleBoneName
            # Arguments
            poseBone.constraints[0].chain_count = order.chainLength
            # TODO: Is this how degrees are actually specified?
            poseBone.constraints[0].pole_angle = 90.0

            # Deselect pose bone now that we're finished
            bone.select = False
