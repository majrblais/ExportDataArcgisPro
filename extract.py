import arcpy
from arcpy.ia import ExportTrainingDataForDeepLearning
arcpy.env.cellSize = 1
# Check out the ArcGIS Image Analyst extension
arcpy.CheckOutExtension("ImageAnalyst")

# Define input parameters
input_raster = "World Imagery"
additional_input_raster = "LidarProducts/DSM_HS"
output_folder = r"E:\Desktop\roads_m2\complete_data\val_1a"
input_feature_class = "tg"
image_chip_format = "TIFF"
class_value_field = "class"

# Tile and stride sizes
tile_size_x = 2000
tile_size_y = 2000
stride_x = 2000
stride_y = 2000

# Other parameters
metadata_format = "Classified_Tiles"
reference_system = "MAP_SPACE"
output_nofeature_tiles = "ONLY_TILES_WITH_FEATURES"

layer_name = "val_1"
layer_extent = arcpy.Describe(layer_name).extent

# Extract the extent coordinates
extent_left = layer_extent.XMin
extent_bottom = layer_extent.YMin
extent_right = layer_extent.XMax
extent_top = layer_extent.YMax
spatial_ref = layer_extent.spatialReference

spatial_ref = arcpy.SpatialReference(32619)  # WGS 1984 UTM Zone 19N

# Create mask polygons for the extent
mask_polygon = arcpy.management.CreateFeatureclass(
    "in_memory", "mask_polygon", "POLYGON", spatial_reference=spatial_ref
)

with arcpy.da.InsertCursor(mask_polygon, ["SHAPE@"]) as cursor:
    polygon = arcpy.Polygon(
        arcpy.Array([
            arcpy.Point(extent_left, extent_bottom),
            arcpy.Point(extent_left, extent_top),
            arcpy.Point(extent_right, extent_top),
            arcpy.Point(extent_right, extent_bottom),
            arcpy.Point(extent_left, extent_bottom)
        ]),
        spatial_ref
    )
    cursor.insertRow([polygon])

# Run the ExportTrainingDataForDeepLearning tool
ExportTrainingDataForDeepLearning(
    in_raster=input_raster,
    out_folder=output_folder,
    in_class_data=input_feature_class,
    image_chip_format=image_chip_format,
    tile_size_x=tile_size_x,
    tile_size_y=tile_size_y,
    stride_x=stride_x,
    stride_y=stride_y,
    buffer_radius=1,
    output_nofeature_tiles=output_nofeature_tiles,
    metadata_format=metadata_format,
    class_value_field=class_value_field,
    in_mask_polygons=mask_polygon,
    reference_system=reference_system
)

print("Export completed successfully.")
