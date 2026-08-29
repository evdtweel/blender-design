import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


BLOCKOUT = {
    "wall_thickness": 0.20,
    "floor_thickness": 0.20,
    "roof_thickness": 0.12,
    "wall_top_elevation": 3.60,
    "opening_panel_thickness": 0.04,
}

OUTPUT = {
    "blend": "blender/songkhla_exterior.blend",
    "glb": "exports/songkhla_exterior.glb",
    "validation": "reports/validation.json",
    "renders": {
        "east": "renders/east.png",
        "west": "renders/west.png",
        "north": "renders/north.png",
        "south": "renders/south.png",
        "perspective": "renders/perspective.png",
    },
}


def parse_args(argv):
    blender_args = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser(description="Build the first simple Songkhla exterior model.")
    parser.add_argument("--config", required=True, help="Path to songkhla_exterior.json.")
    parser.add_argument("--out-dir", required=True, help="Output directory root.")
    return parser.parse_args(blender_args)


def require_positive(value, label):
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{label} must be a positive number.")
    return float(value)


def resolve_child_path(out_root, relative_path, label):
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must be a safe relative path.")
    resolved = (out_root / path).resolve()
    resolved.relative_to(out_root)
    return resolved


def make_output_paths(out_dir):
    out_root = Path(out_dir).resolve()
    return {
        "root": out_root,
        "blend": resolve_child_path(out_root, OUTPUT["blend"], "output.blend"),
        "glb": resolve_child_path(out_root, OUTPUT["glb"], "output.glb"),
        "validation": resolve_child_path(out_root, OUTPUT["validation"], "output.validation"),
        "renders": {
            name: resolve_child_path(out_root, rel_path, f"output.renders.{name}")
            for name, rel_path in OUTPUT["renders"].items()
        },
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
        principled.inputs["Roughness"].default_value = 0.55
    if alpha < 1.0:
        material.blend_method = "BLEND"
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
    sx, sy, sz = size
    if sx <= 0 or sy <= 0 or sz <= 0:
        raise ValueError(f"{name} has a non-positive dimension.")
    cx, cy, cz = center
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
    faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return link_mesh_object(name, verts, faces, material, collection)


def get_axis_positions(config):
    x_positions = {axis: float(value) for axis, value in config["buildingGrid"]["axesAToF"]["axisPositions"].items()}
    y_positions = {axis: float(value) for axis, value in config["buildingGrid"]["axes1To4"]["axisPositions"].items()}
    return x_positions, y_positions


def building_dimensions(config):
    x_positions, y_positions = get_axis_positions(config)
    width = x_positions["F"] - x_positions["A"]
    depth = y_positions["4"] - y_positions["1"]
    return width, depth, x_positions, y_positions


def validate_source_config(config):
    if config["units"]["length"] != "m":
        raise ValueError("Config length unit must be m.")
    coords = config["coordinateSystem"]
    if coords["xPositive"] != "east" or coords["yPositive"] != "north" or coords["zPositive"] != "up":
        raise ValueError("Unsupported coordinate system.")
    if coords["frontFacade"] != "east":
        raise ValueError("Front facade must be east.")
    if len(config["exteriorOpenings"]) != 16:
        raise ValueError("Expected exactly 16 configured exterior openings.")

    width, depth, _, _ = building_dimensions(config)
    if not math.isclose(width, 16.0, abs_tol=0.001):
        raise ValueError(f"Expected 16.00 m east-west grid, got {width}.")
    if not math.isclose(depth, 10.5, abs_tol=0.001):
        raise ValueError(f"Expected 10.50 m north-south grid, got {depth}.")

    for value_name, value in BLOCKOUT.items():
        require_positive(value, f"BLOCKOUT.{value_name}")


def opening_type(config, opening):
    type_id = opening["type"]
    if opening["kind"] == "window":
        return config["openingTypes"]["windows"][type_id]
    if opening["kind"] == "door":
        return config["openingTypes"]["doors"][type_id]
    raise ValueError(f"Unsupported opening kind: {opening['kind']}")


def facade_axis_and_normal(opening, width, depth, x_positions, y_positions):
    facade = opening["facade"]
    bay_start, bay_end = opening["bay"].split("-")
    fraction = float(opening["centerFractionWithinBay"])
    if facade == "1":
        y = y_positions[bay_start] + ((y_positions[bay_end] - y_positions[bay_start]) * fraction)
        return (width, y), "east", (1.0, 0.0)
    if facade == "2":
        x = x_positions[bay_start] + ((x_positions[bay_end] - x_positions[bay_start]) * fraction)
        return (x, 0.0), "south", (0.0, -1.0)
    if facade == "3":
        y = y_positions[bay_start] + ((y_positions[bay_end] - y_positions[bay_start]) * fraction)
        return (0.0, y), "west", (-1.0, 0.0)
    if facade == "4":
        x = x_positions[bay_start] + ((x_positions[bay_end] - x_positions[bay_start]) * fraction)
        return (x, depth), "north", (0.0, 1.0)
    raise ValueError(f"Unsupported facade: {facade}")


def opening_bounds(config, opening, width, depth, x_positions, y_positions):
    type_config = opening_type(config, opening)
    opening_width = require_positive(type_config["width"], f"{opening['id']}.width")
    opening_height = require_positive(type_config["height"], f"{opening['id']}.height")
    main_floor = float(config["levels"]["mainFloor"]["elevation"])
    if opening["kind"] == "window":
        bottom = main_floor + require_positive(type_config["sillHeight"], f"{opening['id']}.sillHeight")
    elif opening["type"] == "D4":
        bottom = float(config["levels"]["servicePlatform"]["elevation"])
    else:
        bottom = main_floor
    top = bottom + opening_height
    (center_a, center_b), orientation, normal = facade_axis_and_normal(opening, width, depth, x_positions, y_positions)
    half = opening_width / 2.0

    if orientation in {"east", "west"}:
        low, high = center_b - half, center_b + half
        if low <= 0.0 or high >= depth:
            raise ValueError(f"Opening {opening['id']} is outside facade bounds.")
        span = (low, high)
    else:
        low, high = center_a - half, center_a + half
        if low <= 0.0 or high >= width:
            raise ValueError(f"Opening {opening['id']} is outside facade bounds.")
        span = (low, high)

    if bottom < 0.0 or top > BLOCKOUT["wall_top_elevation"]:
        raise ValueError(f"Opening {opening['id']} is outside blockout wall height.")

    return {
        "id": opening["id"],
        "type": opening["type"],
        "kind": opening["kind"],
        "facade": opening["facade"],
        "orientation": orientation,
        "normal": normal,
        "center": (center_a, center_b),
        "span": span,
        "bottom": bottom,
        "top": top,
        "width": opening_width,
        "height": opening_height,
    }


def make_opening_bounds(config):
    width, depth, x_positions, y_positions = building_dimensions(config)
    bounds = [opening_bounds(config, opening, width, depth, x_positions, y_positions) for opening in config["exteriorOpenings"]]
    by_facade = {"1": [], "2": [], "3": [], "4": []}
    for item in bounds:
        by_facade[item["facade"]].append(item)
    for facade, items in by_facade.items():
        ordered = sorted(items, key=lambda item: item["span"][0])
        for previous, current in zip(ordered, ordered[1:]):
            if previous["span"][1] > current["span"][0]:
                raise ValueError(f"Openings overlap on facade {facade}: {previous['id']} and {current['id']}")
    return bounds, by_facade


def add_floor(config, material, collection):
    width, depth, _, _ = building_dimensions(config)
    floor_top = float(config["levels"]["mainFloor"]["elevation"])
    thickness = BLOCKOUT["floor_thickness"]
    add_box(
        "songkhla_main_floor_blockout",
        (width / 2.0, depth / 2.0, floor_top - (thickness / 2.0)),
        (width, depth, thickness),
        material,
        collection,
    )


def add_wall_segment(name, facade, span0, span1, z0, z1, width, depth, material, collection):
    thickness = BLOCKOUT["wall_thickness"]
    if span1 - span0 <= 0 or z1 - z0 <= 0:
        return
    if facade == "1":
        add_box(name, (width - thickness / 2.0, (span0 + span1) / 2.0, (z0 + z1) / 2.0), (thickness, span1 - span0, z1 - z0), material, collection)
    elif facade == "3":
        add_box(name, (thickness / 2.0, (span0 + span1) / 2.0, (z0 + z1) / 2.0), (thickness, span1 - span0, z1 - z0), material, collection)
    elif facade == "2":
        add_box(name, ((span0 + span1) / 2.0, thickness / 2.0, (z0 + z1) / 2.0), (span1 - span0, thickness, z1 - z0), material, collection)
    elif facade == "4":
        add_box(name, ((span0 + span1) / 2.0, depth - thickness / 2.0, (z0 + z1) / 2.0), (span1 - span0, thickness, z1 - z0), material, collection)


def add_facade_walls(config, openings_by_facade, material, collection):
    width, depth, _, _ = building_dimensions(config)
    wall_bottom = float(config["levels"]["mainFloor"]["elevation"])
    wall_top = BLOCKOUT["wall_top_elevation"]
    facade_lengths = {"1": depth, "3": depth, "2": width, "4": width}
    for facade in ("1", "2", "3", "4"):
        openings = sorted(openings_by_facade[facade], key=lambda item: item["span"][0])
        boundaries = {0.0, facade_lengths[facade]}
        for opening in openings:
            boundaries.add(opening["span"][0])
            boundaries.add(opening["span"][1])
        ordered = sorted(boundaries)
        segment_index = 1
        for span0, span1 in zip(ordered, ordered[1:]):
            center = (span0 + span1) / 2.0
            match = next((opening for opening in openings if opening["span"][0] < center < opening["span"][1]), None)
            z_ranges = [(wall_bottom, wall_top)]
            if match:
                z_ranges = []
                if match["bottom"] > wall_bottom:
                    z_ranges.append((wall_bottom, match["bottom"]))
                if match["top"] < wall_top:
                    z_ranges.append((match["top"], wall_top))
            for z0, z1 in z_ranges:
                add_wall_segment(f"facade_{facade}_wall_segment_{segment_index:02d}", facade, span0, span1, z0, z1, width, depth, material, collection)
                segment_index += 1


def add_opening_panels(bounds, glass_material, door_material, collection):
    panel_t = BLOCKOUT["opening_panel_thickness"]
    for opening in bounds:
        material = door_material if opening["kind"] == "door" else glass_material
        center_z = (opening["bottom"] + opening["top"]) / 2.0
        if opening["orientation"] in {"east", "west"}:
            x = opening["center"][0]
            size = (panel_t, opening["width"], opening["height"])
            center = (x, opening["center"][1], center_z)
        else:
            y = opening["center"][1]
            size = (opening["width"], panel_t, opening["height"])
            center = (opening["center"][0], y, center_z)
        add_box(f"closed_{opening['kind']}_{opening['id']}", center, size, material, collection)


def add_roof(config, material, collection):
    width, depth, _, _ = building_dimensions(config)
    overhang = float(config["roof"]["overhang"]["value"])
    ridge_z = float(config["roof"]["ridgeElevation"]["value"])
    eave_z = BLOCKOUT["wall_top_elevation"]
    thickness = BLOCKOUT["roof_thickness"]
    x0, x1 = -overhang, width + overhang
    y0, y1 = -overhang, depth + overhang
    ridge_x = width / 2.0
    verts = [
        (x0, y0, eave_z),
        (ridge_x, y0, ridge_z),
        (x1, y0, eave_z),
        (x0, y1, eave_z),
        (ridge_x, y1, ridge_z),
        (x1, y1, eave_z),
        (x0, y0, eave_z - thickness),
        (ridge_x, y0, ridge_z - thickness),
        (x1, y0, eave_z - thickness),
        (x0, y1, eave_z - thickness),
        (ridge_x, y1, ridge_z - thickness),
        (x1, y1, eave_z - thickness),
    ]
    faces = [
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (6, 7, 10, 9),
        (7, 8, 11, 10),
        (0, 1, 7, 6),
        (1, 2, 8, 7),
        (3, 9, 10, 4),
        (4, 10, 11, 5),
        (0, 6, 9, 3),
        (2, 5, 11, 8),
    ]
    return link_mesh_object("songkhla_simple_roof_mass_blockout", verts, faces, material, collection)


def look_at(obj, target):
    forward = (Vector(target) - obj.location).normalized()
    world_up = Vector((0.0, 0.0, 1.0))
    right = forward.cross(world_up)
    if right.length == 0:
        right = Vector((1.0, 0.0, 0.0))
    right.normalize()
    up = right.cross(forward).normalized()
    rotation_matrix = Matrix((right, up, -forward)).transposed()
    obj.rotation_euler = rotation_matrix.to_euler()


def add_camera(name, location, target, collection, ortho_scale=None, camera_type="ORTHO", lens=35):
    camera_data = bpy.data.cameras.new(f"{name}_data")
    camera_data.type = camera_type
    if camera_type == "ORTHO":
        camera_data.ortho_scale = ortho_scale
    else:
        camera_data.lens = lens
    camera = bpy.data.objects.new(name, camera_data)
    camera.location = location
    collection.objects.link(camera)
    look_at(camera, target)
    return camera


def configure_render_settings():
    try:
        bpy.context.scene.render.engine = "BLENDER_EEVEE_NEXT"
    except TypeError:
        bpy.context.scene.render.engine = "BLENDER_EEVEE"
    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 900
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world.color = (0.94, 0.95, 0.96)
    bpy.context.scene.view_settings.view_transform = "Standard"
    bpy.context.scene.view_settings.look = "Medium High Contrast"
    bpy.context.scene.view_settings.exposure = 0.35
    bpy.context.scene.view_settings.gamma = 1.0


def add_cameras(config, collection):
    width, depth, _, _ = building_dimensions(config)
    overhang = float(config["roof"]["overhang"]["value"])
    floor_bottom = float(config["levels"]["mainFloor"]["elevation"]) - BLOCKOUT["floor_thickness"]
    ridge_z = float(config["roof"]["ridgeElevation"]["value"])
    target_z = (floor_bottom + ridge_z) / 2.0
    target = (width / 2.0, depth / 2.0, target_z)
    distance = 28.0
    aspect = bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y
    margin_factor = 1.0 / 0.76
    vertical_extent = ridge_z - floor_bottom
    side_horizontal_extent = depth + (2.0 * overhang)
    long_horizontal_extent = width + (2.0 * overhang)
    side_scale = max(side_horizontal_extent, vertical_extent * aspect) * margin_factor
    long_scale = max(long_horizontal_extent, vertical_extent * aspect) * margin_factor
    return {
        "east": add_camera("camera_east_front", (width + distance, depth / 2.0, target_z), target, collection, ortho_scale=side_scale),
        "west": add_camera("camera_west_rear", (-distance, depth / 2.0, target_z), target, collection, ortho_scale=side_scale),
        "north": add_camera("camera_north", (width / 2.0, depth + distance, target_z), target, collection, ortho_scale=long_scale),
        "south": add_camera("camera_south", (width / 2.0, -distance, target_z), target, collection, ortho_scale=long_scale),
        "perspective": add_camera("camera_perspective", (width + 8.667, -9.125, 5.567), (width / 2.0, depth / 2.0, 2.4), collection, camera_type="PERSP", lens=32),
    }


def add_lighting(config, collection):
    width, depth, _, _ = building_dimensions(config)
    target = (width / 2.0, depth / 2.0, 2.7)
    sun_data = bpy.data.lights.new("sun_key_data", "SUN")
    sun_data.energy = 1.0
    sun_data.use_shadow = False
    sun = bpy.data.objects.new("sun_key", sun_data)
    sun.location = (width + 12.0, -12.0, 12.0)
    collection.objects.link(sun)
    look_at(sun, target)

    fill_specs = [
        ("area_fill_east", (width + 8.0, depth / 2.0, 3.0), 16.0, 420.0),
        ("area_fill_west", (-8.0, depth / 2.0, 3.0), 16.0, 420.0),
        ("area_fill_north", (width / 2.0, depth + 8.0, 3.0), 18.0, 420.0),
        ("area_fill_south", (width / 2.0, -8.0, 3.0), 18.0, 420.0),
        ("area_fill_top", (width / 2.0, depth / 2.0, 9.0), 20.0, 180.0),
    ]
    for name, location, size, energy in fill_specs:
        area_data = bpy.data.lights.new(f"{name}_data", "AREA")
        area_data.size = size
        area_data.energy = energy
        area_data.use_shadow = False
        area = bpy.data.objects.new(name, area_data)
        area.location = location
        collection.objects.link(area)
        look_at(area, target)


def render_views(cameras, paths):
    for name, camera in cameras.items():
        path = paths[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        bpy.context.scene.camera = camera
        bpy.context.scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        if not path.is_file() or path.stat().st_size <= 0:
            raise RuntimeError(f"Render failed: {path}")


def export_glb(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(path), export_format="GLB")
    if not path.is_file() or path.stat().st_size <= 0:
        raise RuntimeError(f"GLB export failed: {path}")


def write_validation_report(config, paths, bounds):
    width, depth, _, _ = building_dimensions(config)
    required_files = [
        ("blend", paths["blend"]),
        ("glb", paths["glb"]),
        *[(f"render_{name}", path) for name, path in paths["renders"].items()],
    ]
    output_checks = []
    for label, path in required_files:
        exists = path.is_file()
        size = path.stat().st_size if exists else 0
        output_checks.append({"label": label, "path": path.relative_to(paths["root"]).as_posix(), "exists": exists, "sizeBytes": size, "passed": exists and size > 0})

    checks = [
        {"label": "16_exterior_openings", "expected": 16, "actual": len(bounds), "passed": len(bounds) == 16},
        {"label": "main_width_x_east_west", "expected": 16.0, "actual": width, "passed": math.isclose(width, 16.0, abs_tol=0.001)},
        {"label": "main_depth_y_north_south", "expected": 10.5, "actual": depth, "passed": math.isclose(depth, 10.5, abs_tol=0.001)},
        {"label": "orientation_x_positive_east", "expected": "east", "actual": config["coordinateSystem"]["xPositive"], "passed": config["coordinateSystem"]["xPositive"] == "east"},
        {"label": "orientation_y_positive_north", "expected": "north", "actual": config["coordinateSystem"]["yPositive"], "passed": config["coordinateSystem"]["yPositive"] == "north"},
        {"label": "orientation_z_positive_up", "expected": "up", "actual": config["coordinateSystem"]["zPositive"], "passed": config["coordinateSystem"]["zPositive"] == "up"},
        {"label": "front_facade_east", "expected": "east", "actual": config["coordinateSystem"]["frontFacade"], "passed": config["coordinateSystem"]["frontFacade"] == "east"},
    ]
    checks.extend(output_checks)

    report = {
        "schemaVersion": 1,
        "status": "passed" if all(check["passed"] for check in checks) else "failed",
        "temporaryBlockoutValues": BLOCKOUT,
        "checks": checks,
        "outputs": {key: value.relative_to(paths["root"]).as_posix() for key, value in paths.items() if key in {"blend", "glb", "validation"}},
        "renders": {key: value.relative_to(paths["root"]).as_posix() for key, value in paths["renders"].items()},
    }
    paths["validation"].parent.mkdir(parents=True, exist_ok=True)
    with paths["validation"].open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    exists = paths["validation"].is_file()
    report["checks"].append(
        {
            "label": "validation",
            "path": paths["validation"].relative_to(paths["root"]).as_posix(),
            "exists": exists,
            "passed": exists,
        }
    )
    report["status"] = "passed" if all(check["passed"] for check in report["checks"]) else "failed"
    with paths["validation"].open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    if report["status"] != "passed":
        raise RuntimeError("Validation failed.")
    return report


def build_scene(config, out_dir):
    validate_source_config(config)
    paths = make_output_paths(out_dir)
    bounds, openings_by_facade = make_opening_bounds(config)

    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.scene.unit_settings.length_unit = "METERS"
    configure_render_settings()

    structure = make_collection("Songkhla_Structure")
    openings = make_collection("Songkhla_Closed_Openings")
    roof = make_collection("Songkhla_Roof_Blockout")
    cameras = make_collection("Songkhla_Cameras")
    lighting = make_collection("Songkhla_Lighting")

    wall_mat = make_material("mat_neutral_walls_blockout", (0.74, 0.74, 0.70, 1.0))
    floor_mat = make_material("mat_neutral_floor_blockout", (0.50, 0.52, 0.51, 1.0))
    glass_mat = make_material("mat_closed_window_soft_blue", (0.50, 0.72, 0.84, 0.55), 0.55)
    door_mat = make_material("mat_closed_door_neutral", (0.35, 0.32, 0.28, 1.0))
    roof_mat = make_material("mat_roof_blockout_muted", (0.48, 0.18, 0.12, 1.0))

    add_floor(config, floor_mat, structure)
    add_facade_walls(config, openings_by_facade, wall_mat, structure)
    add_opening_panels(bounds, glass_mat, door_mat, openings)
    add_roof(config, roof_mat, roof)
    camera_map = add_cameras(config, cameras)
    add_lighting(config, lighting)

    render_views(camera_map, paths["renders"])
    export_glb(paths["glb"])

    paths["blend"].parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(paths["blend"]))
    report = write_validation_report(config, paths, bounds)
    print(f"Saved Songkhla exterior blend: {paths['blend']}")
    print(f"Saved Songkhla exterior GLB: {paths['glb']}")
    print(f"Saved Songkhla exterior validation report: {paths['validation']}")
    print(f"Validation status: {report['status']}")


def main():
    args = parse_args(sys.argv)
    with Path(args.config).open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    build_scene(config, args.out_dir)


if __name__ == "__main__":
    main()
