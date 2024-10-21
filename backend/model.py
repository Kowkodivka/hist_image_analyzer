import cv2
import numpy as np
from process import process_images


def save_obj(vertices, colors, filename):
    with open(filename, "w") as file:
        for vertex, color in zip(vertices, colors):
            file.write(
                f"v {vertex[0]} {vertex[1]} {vertex[2]} {color[0]} {color[1]} {color[2]}\n"
            )

        num_voxels = len(vertices) // 8

        for i in range(num_voxels):
            start_index = 8 * i + 1
            file.write(
                f"f {start_index} {start_index + 1} {start_index + 2} {start_index + 3}\n"
            )
            file.write(
                f"f {start_index + 4} {start_index + 5} {start_index + 6} {start_index + 7}\n"
            )
            file.write(
                f"f {start_index} {start_index + 1} {start_index + 5} {start_index + 4}\n"
            )
            file.write(
                f"f {start_index + 2} {start_index + 3} {start_index + 7} {start_index + 6}\n"
            )
            file.write(
                f"f {start_index + 1} {start_index + 2} {start_index + 6} {start_index + 5}\n"
            )
            file.write(
                f"f {start_index} {start_index + 3} {start_index + 7} {start_index + 4}\n"
            )


def create_obj_from_images(images, voxel_size, extrude_const, filename):
    vertices = []
    colors = []
    filled_voxels = {}

    for image_idx, img in enumerate(images):
        height, width = img.shape[:2]

        for y in range(height):
            for x in range(width):
                pixel = img[y, x]

                if len(pixel) == 4 and pixel[3] == 0:
                    continue

                for extrusion in range(extrude_const):
                    grid_z = image_idx * extrude_const + extrusion
                    filled_voxels[(x, y, grid_z)] = pixel[:3]

    max_dim = np.max(list(filled_voxels.keys()), axis=0)

    for (x, y, z), color in filled_voxels.items():
        voxel_position = np.array([x, y, z]) * voxel_size

        is_exposed = (
            lambda nx, ny, nz: (nx, ny, nz) not in filled_voxels
            or nx < 0
            or ny < 0
            or nz < 0
            or nx > max_dim[0]
            or ny > max_dim[1]
            or nz > max_dim[2]
        )

        if (
            any(is_exposed(nx, y, z) for nx in [x - 1, x + 1])
            or any(is_exposed(x, ny, z) for ny in [y - 1, y + 1])
            or any(is_exposed(x, y, nz) for nz in [z - 1, z + 1])
        ):

            x0, y0, z0 = voxel_position
            voxel_vertices = [
                (x0, y0, z0),
                (x0 + voxel_size, y0, z0),
                (x0 + voxel_size, y0 + voxel_size, z0),
                (x0, y0 + voxel_size, z0),
                (x0, y0, z0 + voxel_size),
                (x0 + voxel_size, y0, z0 + voxel_size),
                (x0 + voxel_size, y0 + voxel_size, z0 + voxel_size),
                (x0, y0 + voxel_size, z0 + voxel_size),
            ]
            vertices.extend(voxel_vertices)
            color_normalized = np.array(color) / 255.0
            colors.extend([color_normalized] * 8)

    save_obj(vertices, colors, filename)


# images = [
#     cv2.imread(f"./photo/raw/photo_{i}_2024-10-12_17-48-51.jpg", cv2.IMREAD_UNCHANGED)
#     for i in range(1, 10)
# ]
# images = process_images(images)
# create_obj_from_images(images, voxel_size=1, extrude_const=10, filename="output.obj")