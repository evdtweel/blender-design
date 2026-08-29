import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


def parse_args(argv):
    blender_args = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser(description="Build the Phase 2 Blender probe house.")
    parser.add_argument("--config", required=True, help="Path to phase2_probe.json.")
    parser.add_argument("--out-dir", required=True, help="Output directory root.")
    return parser.parse_args(blender_args)


def require_positive(value, label):
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{label} must be a positive number.")
    return float(value)


def require_wall_opening(opening, wall_width, wall_height, label, bottom):
    width = require_positive(opening["width"], f"{label}.width")
    height = require_positive(opening["height"], f"{label}.height")
    offset = float(opening["horizontalOffset"])
    bottom = float(bottom)
    top = bottom + height
    left = offset - (width / 2.0)
    right = offset + (width / 2.0)

    if bottom < 0 or top > wall_height:
        raise ValueError(f"{label} vertical bounds are outside the wall.")
    if left <= -(wall_width / 2.0) or right >= wall_width / 2.0:
        raise ValueError(f"{label} horizontal bounds are outside the wall.")

    return {
        "id": opening["id"],
        "wall": opening["wall"],
        "left": left,
        "right": right,
        "bottom": bottom,
        "top": top,
        "width": width,
        "height": height,
        "offset": offset,
    }


def validate_config(config):
    building = config["building"]
    roof = config["roof"]
    interior_wall = config["interiorWall"]

    width = require_positive(building["width"], "building.width")
    depth = require_positive(building["depth"], "building.depth")
    wall_height = require_positive(building["wallHeight"], "building.wallHeight")
    wall_thickness = require_positive(building["wallThickness"], "building.wallThickness")
    require_positive(interior_wall["thickness"], "interiorWall.thickness")
    require_positive(interior_wall["height"], "interiorWall.height")
    require_positive(roof["pitchDegrees"], "roof.pitchDegrees")
    require_positive(roof["overhang"], "roof.overhang")

    if wall_thickness >= width / 2.0 or wall_thickness >= depth / 2.0:
        raise ValueError("building.wallThickness is too large for the building footprint.")
    if config["units"] != "meters":
        raise ValueError("units must be meters.")
    if interior_wall["orientation"] != "parallel_to_width":
        raise ValueError("Only an interior wall parallel_to_width is supported.")
    if interior_wall["position"] != "center":
        raise ValueError("Only a centered interior wall is supported.")
    if roof["type"] != "gable":
        raise ValueError("Only a gable roof is supported.")

    openings_by_wall = {"front": [], "back": []}

    door = config["door"]
    if door["wall"] != "front":
        raise ValueError("Only a front door is supported.")
    openings_by_wall["front"].append(require_wall_opening(door, width, wall_height, "door", 0.0))

    for window in config["windows"]:
        wall = window["wall"]
        if wall not in openings_by_wall:
            raise ValueError(f"Unsupported window wall: {wall}")
        sill_height = require_positive(window["sillHeight"], f"window {window['id']}.sillHeight")
        openings_by_wall[wall].append(
            require_wall_opening(window, width, wall_height, f"window {window['id']}", sill_height)
        )

    for wall, openings in openings_by_wall.items():
        sorted_openings = sorted(openings, key=lambda item: item["left"])
        for previous, current in zip(sorted_openings, sorted_openings[1:]):
            if previous["right"] > current["left"]:
                raise ValueError(f"Openings overlap on {wall} wall: {previous['id']} and {current['id']}")

    return {
        "width": width,
        "depth": depth,
        "wall_height": wall_height,
        "wall_thickness": wall_thickness,
        "interior_wall_height": float(interior_wall["height"]),
        "interior_wall_thickness": float(interior_wall["thickness"]),
        "roof_pitch_degrees": float(roof["pitchDegrees"]),
        "roof_overhang": float(roof["overhang"]),
        "openings_by_wall": openings_by_wall,
    }


def clear_scene():
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def make_collection(name):
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection


def make_material(name, color, alpha=1.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.use_nodes = True
    principled = material.node_tree.nodes.get("Principled BSDF")
    if principled is not None:
        principled.inputs["Base Color"].default_value = color
        principled.inputs["Alpha"].default_value = alpha
    if alpha < 1.0:
        material.blend_method = "BLEND"
        if hasattr(material, "use_screen_refraction"):
            material.use_screen_refraction = True
    return material


def link_mesh_object(name, verts, faces, material, collection):
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def add_box(name, center, size, material, collection):
    cx, cy, cz = center
    sx, sy, sz = size
    if sx <= 0 or sy <= 0 or sz <= 0:
        raise ValueError(f"{name} has a non-positive dimension.")

    x0, x1 = cx - sx / 2.0, cx + sx / 2.0
    y0, y1 = cy - sy / 2.0, cy + sy / 2.0
    z0, z1 = cz - sz / 2.0, cz + sz / 2.0
    verts = [
        (x0, y0, z0),
        (x1, y0, z0),
        (x1, y1, z0),
        (x0, y1, z0),
        (x0, y0, z1),
        (x1, y0, z1),
        (x1, y1, z1),
        (x0, y1, z1),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]
    return link_mesh_object(name, verts, faces, material, collection)


def add_floor_plate(dims, material, collection):
    half_width = dims["width"] / 2.0
    half_depth = dims["depth"] / 2.0
    verts = [
        (-half_width, -half_depth, 0.0),
        (half_width, -half_depth, 0.0),
        (half_width, half_depth, 0.0),
        (-half_width, half_depth, 0.0),
    ]
    faces = [(0, 1, 2, 3)]
    return link_mesh_object("floor_plate", verts, faces, material, collection)


def add_panel(name, wall, opening, depth, material, collection):
    y = -(depth / 2.0) if wall == "front" else depth / 2.0
    verts = [
        (opening["left"], y, opening["bottom"]),
        (opening["right"], y, opening["bottom"]),
        (opening["right"], y, opening["top"]),
        (opening["left"], y, opening["top"]),
    ]
    if wall == "back":
        faces = [(0, 3, 2, 1)]
    else:
        faces = [(0, 1, 2, 3)]
    return link_mesh_object(name, verts, faces, material, collection)


def add_wall_segment(name, wall, x0, x1, z0, z1, dims, material, collection):
    width = x1 - x0
    height = z1 - z0
    if width <= 0 or height <= 0:
        return None

    y = -(dims["depth"] / 2.0) + (dims["wall_thickness"] / 2.0)
    if wall == "back":
        y = (dims["depth"] / 2.0) - (dims["wall_thickness"] / 2.0)

    return add_box(
        name,
        ((x0 + x1) / 2.0, y, (z0 + z1) / 2.0),
        (width, dims["wall_thickness"], height),
        material,
        collection,
    )


def add_segmented_wall(wall, dims, material, collection):
    boundaries = {-(dims["width"] / 2.0), dims["width"] / 2.0}
    openings = sorted(dims["openings_by_wall"][wall], key=lambda item: item["left"])
    for opening in openings:
        boundaries.add(opening["left"])
        boundaries.add(opening["right"])

    ordered = sorted(boundaries)
    segment_index = 1
    for x0, x1 in zip(ordered, ordered[1:]):
        span_center = (x0 + x1) / 2.0
        matching = [
            opening for opening in openings if opening["left"] < span_center < opening["right"]
        ]
        solid_ranges = [(0.0, dims["wall_height"])]
        if matching:
            opening = matching[0]
            solid_ranges = []
            if opening["bottom"] > 0.0:
                solid_ranges.append((0.0, opening["bottom"]))
            if opening["top"] < dims["wall_height"]:
                solid_ranges.append((opening["top"], dims["wall_height"]))

        for z0, z1 in solid_ranges:
            add_wall_segment(
                f"{wall}_wall_segment_{segment_index:02d}",
                wall,
                x0,
                x1,
                z0,
                z1,
                dims,
                material,
                collection,
            )
            segment_index += 1


def add_roof(dims, material, collection):
    half_width = (dims["width"] / 2.0) + dims["roof_overhang"]
    half_depth = (dims["depth"] / 2.0) + dims["roof_overhang"]
    eave_z = dims["wall_height"]
    ridge_z = eave_z + (half_width * math.tan(math.radians(dims["roof_pitch_degrees"])))
    verts = [
        (-half_width, -half_depth, eave_z),
        (0.0, -half_depth, ridge_z),
        (half_width, -half_depth, eave_z),
        (-half_width, half_depth, eave_z),
        (0.0, half_depth, ridge_z),
        (half_width, half_depth, eave_z),
    ]
    faces = [
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (0, 1, 2),
        (3, 5, 4),
    ]
    return link_mesh_object("gable_roof", verts, faces, material, collection)


def resolve_child_path(out_root, relative_path, label):
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ValueError(f"{label} must be a non-empty relative path.")
    path = Path(relative_path)
    if path.is_absolute():
        raise ValueError(f"{label} must not be an absolute path.")
    if ".." in path.parts:
        raise ValueError(f"{label} must not contain '..' path segments.")

    resolved_path = (out_root / path).resolve()
    try:
        resolved_path.relative_to(out_root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes the output directory.") from exc
    return resolved_path


def resolve_output_paths(out_dir, output_config):
    out_root = Path(out_dir).resolve()
    blend_path = resolve_child_path(out_root, output_config["blend"], "output.blend")
    glb_path = resolve_child_path(out_root, output_config["glb"], "output.glb")
    render_paths = {
        view: resolve_child_path(out_root, output_config["renders"][view], f"output.renders.{view}")
        for view in ("front", "back", "left", "right")
    }
    validation_path = resolve_child_path(out_root, output_config["validationReport"], "output.validationReport")
    return out_root, blend_path, glb_path, render_paths, validation_path


def path_for_report(out_root, path):
    return path.relative_to(out_root).as_posix()


def validate_output_files(out_root, blend_path, glb_path, render_paths):
    required_outputs = [
        ("house.blend", blend_path),
        ("house.glb", glb_path),
        ("front.png", render_paths["front"]),
        ("back.png", render_paths["back"]),
        ("left.png", render_paths["left"]),
        ("right.png", render_paths["right"]),
    ]
    checks = []

    for label, path in required_outputs:
        exists = path.is_file()
        size_bytes = path.stat().st_size if exists else 0
        passed = exists and size_bytes > 0
        checks.append(
            {
                "label": label,
                "path": path_for_report(out_root, path),
                "exists": exists,
                "sizeBytes": size_bytes,
                "passed": passed,
            }
        )

    return {
        "schemaVersion": 1,
        "status": "passed" if all(check["passed"] for check in checks) else "failed",
        "checks": checks,
    }


def write_validation_report(validation_path, report):
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    with validation_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")

    if report["status"] != "passed":
        failed_labels = ", ".join(check["label"] for check in report["checks"] if not check["passed"])
        raise RuntimeError(f"Outputvalidatie mislukt voor: {failed_labels}")


def look_at(obj, target):
    forward = (Vector(target) - obj.location).normalized()
    world_up = Vector((0.0, 0.0, 1.0))
    right = forward.cross(world_up).normalized()
    up = right.cross(forward).normalized()
    rotation_matrix = Matrix((right, up, -forward)).transposed()
    obj.rotation_euler = rotation_matrix.to_euler()


def move_object_to_collection(obj, collection):
    for source_collection in list(obj.users_collection):
        source_collection.objects.unlink(obj)
    collection.objects.link(obj)


def add_camera(name, location, target, orthographic_scale, collection):
    camera_data = bpy.data.cameras.new(f"{name}_data")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = orthographic_scale
    camera = bpy.data.objects.new(name, camera_data)
    camera.location = location
    collection.objects.link(camera)
    look_at(camera, target)
    return camera


def mesh_objects_from_collections(collection_names):
    mesh_objects = []
    for collection_name in collection_names:
        collection = bpy.data.collections.get(collection_name)
        if collection is None:
            raise ValueError(f"Collection ontbreekt voor camerakadrering: {collection_name}")
        mesh_objects.extend(obj for obj in collection.objects if obj.type == "MESH")

    if not mesh_objects:
        raise ValueError("Geen mesh-objecten gevonden voor camerakadrering.")
    return mesh_objects


def calculate_world_bounds(mesh_objects):
    bpy.context.view_layer.update()
    corners = [
        obj.matrix_world @ Vector(corner)
        for obj in mesh_objects
        for corner in obj.bound_box
    ]

    min_x = min(corner.x for corner in corners)
    max_x = max(corner.x for corner in corners)
    min_y = min(corner.y for corner in corners)
    max_y = max(corner.y for corner in corners)
    min_z = min(corner.z for corner in corners)
    max_z = max(corner.z for corner in corners)

    return {
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "min_z": min_z,
        "max_z": max_z,
        "center": (
            (min_x + max_x) / 2.0,
            (min_y + max_y) / 2.0,
            (min_z + max_z) / 2.0,
        ),
    }


def orthographic_scale(horizontal_extent, vertical_extent):
    aspect = 800.0 / 600.0
    return max(horizontal_extent, vertical_extent * aspect) * 1.20


def add_sun(name, location, target, collection):
    light_data = bpy.data.lights.new(f"{name}_data", "SUN")
    light_data.energy = 2.0
    light = bpy.data.objects.new(name, light_data)
    light.location = location
    collection.objects.link(light)
    look_at(light, target)
    return light


def add_area_light(name, location, target, size, energy, collection):
    light_data = bpy.data.lights.new(f"{name}_data", "AREA")
    light_data.size = size
    light_data.energy = energy
    light = bpy.data.objects.new(name, light_data)
    light.location = location
    collection.objects.link(light)
    look_at(light, target)
    return light


def configure_render_settings():
    try:
        bpy.context.scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
    bpy.context.scene.render.resolution_x = 800
    bpy.context.scene.render.resolution_y = 600
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world.color = (0.88, 0.89, 0.90)


def add_cameras(dims, collection):
    bounds = calculate_world_bounds(mesh_objects_from_collections(("Structure", "Openings", "Roof")))
    target = bounds["center"]
    x_extent = bounds["max_x"] - bounds["min_x"]
    y_extent = bounds["max_y"] - bounds["min_y"]
    z_extent = bounds["max_z"] - bounds["min_z"]
    distance = max(x_extent, y_extent, z_extent) * 2.4
    front_scale = orthographic_scale(x_extent, z_extent)
    back_scale = orthographic_scale(x_extent, z_extent)
    left_scale = orthographic_scale(y_extent, z_extent)
    right_scale = orthographic_scale(y_extent, z_extent)

    return {
        "front": add_camera(
            "camera_front",
            (target[0], bounds["min_y"] - distance, target[2]),
            target,
            front_scale,
            collection,
        ),
        "back": add_camera(
            "camera_back",
            (target[0], bounds["max_y"] + distance, target[2]),
            target,
            back_scale,
            collection,
        ),
        "left": add_camera(
            "camera_left",
            (bounds["min_x"] - distance, target[1], target[2]),
            target,
            left_scale,
            collection,
        ),
        "right": add_camera(
            "camera_right",
            (bounds["max_x"] + distance, target[1], target[2]),
            target,
            right_scale,
            collection,
        ),
    }


def add_lighting(dims, collection):
    roof_span_half = (dims["width"] / 2.0) + dims["roof_overhang"]
    roof_height = roof_span_half * math.tan(math.radians(dims["roof_pitch_degrees"]))
    total_height = dims["wall_height"] + roof_height
    target = (0.0, 0.0, total_height / 2.0)
    radius = max(dims["width"], dims["depth"], total_height)

    add_sun("sun_key", (-radius, -radius, total_height + radius), target, collection)
    light_size = max(dims["width"], dims["depth"])
    light_energy = 280.0
    add_area_light(
        "area_fill_front",
        (0.0, -(dims["depth"] + radius), total_height),
        target,
        light_size,
        light_energy,
        collection,
    )
    add_area_light(
        "area_fill_back",
        (0.0, dims["depth"] + radius, total_height),
        target,
        light_size,
        light_energy,
        collection,
    )
    add_area_light(
        "area_fill_left",
        (-(dims["width"] + radius), 0.0, total_height),
        target,
        light_size,
        light_energy,
        collection,
    )
    add_area_light(
        "area_fill_right",
        (dims["width"] + radius, 0.0, total_height),
        target,
        light_size,
        light_energy,
        collection,
    )


def render_views(cameras, render_paths):
    for view_name, camera in cameras.items():
        render_path = render_paths[view_name]
        render_path.parent.mkdir(parents=True, exist_ok=True)
        bpy.context.scene.camera = camera
        bpy.context.scene.render.filepath = str(render_path)
        bpy.ops.render.render(write_still=True)

        if not render_path.is_file():
            raise RuntimeError(f"Render ontbreekt: {render_path}")
        if render_path.stat().st_size <= 0:
            raise RuntimeError(f"Render is leeg: {render_path}")


def export_glb(glb_path):
    glb_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(glb_path),
        export_format="GLB",
    )

    if not glb_path.is_file():
        raise RuntimeError(f"GLB-export ontbreekt: {glb_path}")
    if glb_path.stat().st_size <= 0:
        raise RuntimeError(f"GLB-export is leeg: {glb_path}")


def build_scene(config, out_dir):
    dims = validate_config(config)
    out_root, blend_path, glb_path, render_paths, validation_path = resolve_output_paths(out_dir, config["output"])

    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.scene.unit_settings.length_unit = "METERS"
    configure_render_settings()

    structure = make_collection("Structure")
    openings = make_collection("Openings")
    roof = make_collection("Roof")
    cameras_collection = make_collection("Cameras")
    lighting_collection = make_collection("Lighting")

    wall_mat = make_material("material_walls_warm_gray", (0.72, 0.70, 0.65, 1.0))
    floor_mat = make_material("material_floor_concrete", (0.45, 0.48, 0.48, 1.0))
    door_mat = make_material("material_door_blue", (0.05, 0.18, 0.36, 1.0))
    glass_mat = make_material("material_window_glass", (0.55, 0.80, 0.95, 0.45), 0.45)
    roof_mat = make_material("material_roof_terracotta", (0.55, 0.14, 0.08, 1.0))

    add_floor_plate(dims, floor_mat, structure)
    add_segmented_wall("front", dims, wall_mat, structure)
    add_segmented_wall("back", dims, wall_mat, structure)
    add_box(
        "left_exterior_wall",
        (-(dims["width"] / 2.0) + (dims["wall_thickness"] / 2.0), 0.0, dims["wall_height"] / 2.0),
        (dims["wall_thickness"], dims["depth"] - (2.0 * dims["wall_thickness"]), dims["wall_height"]),
        wall_mat,
        structure,
    )
    add_box(
        "right_exterior_wall",
        ((dims["width"] / 2.0) - (dims["wall_thickness"] / 2.0), 0.0, dims["wall_height"] / 2.0),
        (dims["wall_thickness"], dims["depth"] - (2.0 * dims["wall_thickness"]), dims["wall_height"]),
        wall_mat,
        structure,
    )
    add_box(
        "center_interior_wall_parallel_to_width",
        (0.0, 0.0, dims["interior_wall_height"] / 2.0),
        (dims["width"] - (2.0 * dims["wall_thickness"]), dims["interior_wall_thickness"], dims["interior_wall_height"]),
        wall_mat,
        structure,
    )

    for opening in dims["openings_by_wall"]["front"]:
        material = door_mat if opening["id"] == config["door"]["id"] else glass_mat
        add_panel(opening["id"], "front", opening, dims["depth"], material, openings)
    for opening in dims["openings_by_wall"]["back"]:
        add_panel(opening["id"], "back", opening, dims["depth"], glass_mat, openings)

    add_roof(dims, roof_mat, roof)
    cameras = add_cameras(dims, cameras_collection)
    add_lighting(dims, lighting_collection)
    render_views(cameras, render_paths)
    export_glb(glb_path)

    blend_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    validation_report = validate_output_files(out_root, blend_path, glb_path, render_paths)
    write_validation_report(validation_path, validation_report)
    print(f"Saved Phase 2 probe blend: {blend_path}")
    print(f"Saved Phase 2 validation report: {validation_path}")


def main():
    args = parse_args(sys.argv)
    config_path = Path(args.config)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    build_scene(config, args.out_dir)


if __name__ == "__main__":
    main()
