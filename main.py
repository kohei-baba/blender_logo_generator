import bpy
def main(text,text_info,background_info,spotlight=True):
    #すでにあるデータの消去
    for col in bpy.data.collections:
        for item in col.objects:
            col.objects.unlink(item)
            bpy.data.objects.remove(item)
    for item in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(item)
    for item in bpy.data.objects:
        bpy.data.objects.remove(item)
    for item in bpy.data.cameras:
        bpy.data.cameras.remove(item)
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
    for item in bpy.data.materials:
        bpy.data.materials.remove(item)
    for item in bpy.data.lights:
        bpy.data.lights.remove(item)
    # フォントの変更(例、mac)
    #fnt = bpy.data.fonts.load('/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc')
    # テキストオブジェクトを追加
    bpy.ops.object.text_add()
    ob=bpy.context.object
    ob.data.name = "logo_text"      
    ob.data.body = text            
    #ob.data.font = fnt              # テキストオブジェクトのフォント設定
    #テキストのマテリアル設定
    mat_logo = bpy.data.materials.new('logo_material')
    mat_logo.use_nodes = True
    p_BSDF_1 = mat_logo.node_tree.nodes["Principled BSDF"]
    lr,lg,lb = text_info[:3]
    p_BSDF_1.inputs[0].default_value = (lr, lg, lb, 1)
    p_BSDF_1.inputs[4].default_value = 1
    p_BSDF_1.inputs[7].default_value = text_info[3]
    p_BSDF_1.inputs[15].default_value = text_info[4]
    bpy.ops.object.material_slot_add()
    bpy.context.object.active_material = mat_logo

    s=bpy.data.objects["Text"]
    s.name = "logo_text" 
    # テキストの大きさ指定
    s.scale[0] = 0.2        
    s.scale[1] = 0.2
    s.scale[2] = 0.2
    #テキストの形状指定
    #法線方向への拡大
    s.data.offset=0.002
    #厚み
    thickness = 0.2
    s.data.extrude= thickness
    #面取りの深さと細かさ
    s.data.bevel_depth=0.01
    s.data.bevel_resolution=1
    # メッシュに変換
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    
    #背景の追加
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, -thickness), scale=(100, 100, 100))
    #背景のマテリアル設定
    mat_background = bpy.data.materials.new('background_material')
    mat_background.use_nodes = True
    p_BSDF_2 = mat_background.node_tree.nodes["Principled BSDF"]
    br,bg,bb = background_info[:3]
    p_BSDF_2.inputs[0].default_value = (br, bg, bb, 1)
    p_BSDF_2.inputs[7].default_value = background_info[3]
    p_BSDF_2.inputs[15].default_value = background_info[4]
    bpy.ops.object.material_slot_add()
    bpy.context.object.active_material = mat_background
    
    #ライトの追加
    bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(0, 0, 1), scale=(0.3*len(text), 0.3*len(text), 0.3*len(text)))
    bpy.context.object.data.energy = 500
    if spotlight:
        bpy.ops.object.light_add(type='SPOT', align='WORLD', location=(0, 0, 1), scale=(0.3*len(text), 0.3*len(text), 0.3*len(text)))
        bpy.context.object.data.energy = 100
    
    #カメラの追加
    bpy.ops.object.camera_add(align='VIEW', location=(0, 0, 0.4 + 0.2*len(text)), rotation=(0,0,0), scale=(0.05*len(text), 0.05*len(text),0.05*len(text)))
    bpy.context.scene.camera = bpy.context.object
    #レンダリング設定
    bpy.context.scene.render.resolution_x = 960
    bpy.context.scene.render.resolution_y = 540
    bpy.context.scene.render.resolution_percentage = 100
    #レンダリング
    output_path = "logo.png"
    bpy.ops.render.render()
    bpy.data.images['Render Result'].save_render(output_path)

if __name__ == "__main__":
    #ロゴにする文字列
    text = "Qiita"

    #テキストの色(R,G,B,roughness,transmission)
    text_info = (1,0.95,1,0,1)

    #背景の色(R,G,B,roughness,transmission)
    background_info = (0.1,0.9,0,0.8,0.2)

    main(text,text_info,background_info)
