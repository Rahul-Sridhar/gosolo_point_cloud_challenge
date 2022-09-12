import numpy as np
from plyfile import PlyData, PlyElement


def open_ply(file_path):
    rdata = PlyData.read(file_path)
    points = []
    for i in range(len(rdata.elements[0].data)):
        point = rdata.elements[0].data[i]
        a = np.array(list(point))
        points.append(a)
    data = np.array(points)
    return data


def write_ply(name, data):
    tuples = []
    for point_i in range(data.shape[0]):
        tuples.append(tuple(data[point_i, :9]))

    described_data = np.array(
        tuples,
        dtype=[
            ("x", "double"),
            ("y", "double"),
            ("z", "double"),
            ("nx", "double"),
            ("ny", "double"),
            ("nz", "double"),
            ("red", "u1"),
            ("green", "u1"),
            ("blue", "u1"),
        ],
    )
    element = PlyElement.describe(described_data, "vertex")
    PlyData([element], text=False).write(name)


def main():
    points = open_ply("data/PointCloud.ply")
    # Your code goes here
    
    unique_color_to_points = dict()
    for point in points:
        color_combo = str(point[6]) + "," + str(point[7]) + "," + str(point[8])
        if color_combo not in unique_color_to_points:
            unique_color_to_points[color_combo] = []
        unique_color_to_points[color_combo].append(point)
        
    
    unique_color_to_means = dict()
    unique_color_to_stds = dict()
    for unique_color, color_points in unique_color_to_points.items():
        color_points = np.array(color_points)
        means = []
        stds = []
        for i in range(9):
            mean = color_points[:,i].mean()
            std = color_points[:,i].std()
            means.append(mean)
            stds.append(std)
        unique_color_to_means[unique_color] = np.array(means)
        unique_color_to_stds[unique_color] = np.array(stds)
        
    for unique_color, color_points in unique_color_to_points.items():
    means = unique_color_to_means[unique_color]
    mean_z = means[2]
    mean_nx = means[3]
    mean_ny = means[4]
    mean_nz = means[5]
    stds = unique_color_to_stds[unique_color]
    std_z = stds[2]
    std_nx = stds[3]
    std_ny = stds[4]
    std_nz = stds[5]
    for idx, color_point in enumerate(color_points):
        color_point_z = color_point[2]
        color_point_nx = color_point[3]
        color_point_ny = color_point[4]
        color_point_nz = color_point[5]
        if(color_point_z > mean_z + 2 * std_z or color_point_z < mean_z - 2 * std_z or 
           color_point_nx > mean_nx + 2 * std_nx or color_point_nx < mean_nx - 2 * std_nx or 
           color_point_ny > mean_ny + 2 * std_ny or color_point_ny < mean_ny - 2 * std_ny or 
           color_point_nz > mean_nz + 2 * std_nz or color_point_nz < mean_nz - 2 * std_nz):
            color_points[idx][6] = color_points[idx][7] = color_points[idx][8] = 0.0
            
    new_points = []
    for unique_color, color_points in unique_color_to_points.items():
        new_points.append(color_points)
    new_points = np.concatenate(new_points)
    
    write_ply("data/Result.ply", points)
    return 0


if __name__ == "__main__":
    main()
