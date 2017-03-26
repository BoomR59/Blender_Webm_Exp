
bl_info = {
    "name": "WEBM Exporter",
    "description": "Converts exported image sequences to webms.",
    "author": "BoomR59",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Properties Menu",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/BoomR59/Blender_Webm_Exporter",
    "tracker_url": "https://github.com/BoomR59/Blender_Webm_Exporter/issues",
    "support": "COMMUNITY",
    "category": "Render"
    }



#----------------------------------------------------------
# File webmExport
#----------------------------------------------------------
import bpy
from bpy import context
import os
import operator;
from bpy.props import *
from bpy.utils import *
from bpy.types import PropertyGroup, Operator, Panel




#
#
#
#var = context.scene['ffmpegPath'] = "C:\\ffmpeg\\bin\\ffmpeg.exe"
#var2 = context.scene['BitInt'] = 9000 
#var3 = context.scene['exportPath'] = "C:\\Export"
#var4 = context.scene['fileNameURL'] = "Name"
#var5 = context.scene['imagePath'] = "/tmp"


#class WEBMVariables(bpy.types.PropertyGroup):
    


class UIPanel(bpy.types.Panel):
    bl_label = "Webm Exporter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "scene"
    def draw(self, context):
        layout = self.layout
        scn = context.scene


        # If Scene.my_prop wasn't created in register() or removed, draw a note
        if not hasattr(context.scene, "ffmpegPath"):
            layout.label("'ffmpegPath' not available")
        # It has the default property value, draw a label with no icon
        else:
            layout.prop(scn, 'fileNameURL')
            layout.prop(scn, 'imagePath')
            layout.prop(scn, 'ffmpegPath')
            layout.prop(scn, 'exportPath')            
            layout.prop(scn, 'BitInt')

        layout.operator(InitMyPropOperator.bl_idname, text=InitMyPropOperator.bl_label)    

        
        button = self.layout.operator("webm.rend", text='Render Webm')
        
        #button.fileNameURL=scn['fileNameURL'];
        #button.imagePath=scn['imagePath'];
        #button.ffmpegPath=ffmpegPath
        #button.bitrate=scn['BitInt'];
        #button.exportPath=scn['exportPath'];
class InitMyPropOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.init_my_prop"
    bl_label = "Initialize Variables"
 
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
 
    def execute(self, context):
        if context.scene.ffmpegPath != "C:\\ffmpeg\\bin\\ffmpeg.exe":

            self.__class__.bl_label = "Change Variables"
        else:
            var = context.scene['ffmpegPath'] = "C:\\ffmpeg\\bin\\ffmpeg.exe"
            var2 = context.scene['BitInt'] = 10200 
            var3 = context.scene['exportPath'] = "C:/Export"
            var4 = context.scene['fileNameURL'] = "Name"
            var5 = context.scene['imagePath'] = "/tmp"

            self.__class__.bl_label = self.bl_label
        return {'FINISHED'}


class OBJECT_OT_ExportWebmButton(bpy.types.Operator):
    bl_idname = "webm.rend"
    bl_label = "Export Webm"
    bl_context = "scene"

    #BitInt = bpy.props.StringProperty()
    #exportPath = bpy.props.StringProperty()
    #fileNameURL = bpy.props.StringProperty()
    #imagePath = bpy.props.StringProperty()
    #ffmpegPath = bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.render.render(animation=True)

        ffmpegPath = context.scene['ffmpegPath']
        imgPath = context.scene['imagePath']
        #newPath = r'C:\tmp'
        newPath = context.scene['exportPath']
        bitrate = context.scene['BitInt']
        fileNameURL =  context.scene['fileNameURL']
        startFrame = str(bpy.context.scene.frame_start)
        endFrame = str(bpy.context.scene.frame_end)
        print("**********")
        print("The bitrate is")
        print(bitrate)
        print("The Export Path is")
        print(newPath)
        print("The File Name is")
        print(fileNameURL)
        print("The image export path is")
        print(imgPath)
        print("The ffmpeg file url is")
        print(ffmpegPath)
        print("**********")
        imgNamePattern = "%04d.png"
        vidOut = fileNameURL + ".webm"

    


        vCodec = " libvpx "

        ffmCMD = ffmpegPath + " "
        ffmCMD += "-start_number "+ startFrame + " -i " 
        ffmCMD += imgPath + '\\' + imgNamePattern + " "
        ffmCMD += "-vframes " + endFrame + " "
        ffmCMD += "-auto-alt-ref 0 "
        ffmCMD += "-c:v" + vCodec + " -an -crf 32 "
        ffmCMD += "-maxrate: " +str(bitrate)+"K"+" -minrate "+str(bitrate)+"K"+" -b:v "+str(bitrate)+"K"+" "
        ffmCMD += "-threads 8 -quality best -lag-in-frames 16 -y "
        ffmCMD += newPath + '/' + vidOut


        print(ffmCMD)
        print("*************")
        print("launching ffmpeg")
        os.system(ffmCMD)
        return{'FINISHED'}    


def register():
    bpy.utils.register_module(__name__)


#############
    bpy.types.Scene.ffmpegPath = StringProperty(
        name = "ffmpeg path",
        default="C:\\ffmpeg\\bin\\ffmpeg.exe"
    )
    
    bpy.types.Scene.BitInt = IntProperty(
        name = "Bitrate",
        default=9000 
        )

    bpy.types.Scene.exportPath = StringProperty(
        name = "Export Path",
        default="C:/Export"
        )
    bpy.types.Scene.fileNameURL = StringProperty(
        name = "Name",
        default= "Name"
        )

    bpy.types.Scene.imagePath = StringProperty(
        name = "Image Path",
        default= "/tmp\\"
        )
    
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.ffmpegPath
    del bpy.types.Scene.BitInt
    del bpy.types.Scene.exportPath
    del bpy.types.ScenefileNameURL
    del bpy.types.Scene.imagePath


if __name__ == "__main__":

    register()

