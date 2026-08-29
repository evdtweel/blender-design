import argparse
import json
import math
import sys
from pathlib import Path

import bpy


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


def resolve_output_path(out_dir, relative_blend_path):
    out_root = Path(out_dir).resolve()
    blend_path = (out_root / relative_blend_path).resolve()
    try:
        blend_path.relative_to(out_root)
    except ValueError as exc:
        raise ValueError("Configured blend output path escapes the output directory.") from exc
    return out_root, blend_path


def build_scene(config, out_dir):
    dims = validate_config(config)
    out_root, blend_path = resolve_output_path(out_dir, config["output"]["blend"])

    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.scene.unit_settings.length_unit = "METERS"

    structure = make_collection("Structure")
    openings = make_collection("Openings")
    roof = make_collection("Roof")

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

    blend_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    print(f"Saved Phase 2 probe blend: {blend_path}")


def main():
    args = parse_args(sys.argv)
    config_path = Path(args.config)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    build_scene(config, args.out_dir)


if __name__ == "__main__":
    main()
