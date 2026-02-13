/**
 * QuPath script to export annotations as GeoJSON for ML pipeline
 * 
 * Usage:
 * 1. Open slide in QuPath
 * 2. Complete annotations
 * 3. Run this script: Automate > Show script editor > Paste > Run
 * 4. Annotations exported to project directory
 */

import qupath.lib.io.GsonTools
import qupath.lib.objects.PathObject
import java.nio.file.Paths

// Get current image and project
def imageData = getCurrentImageData()
def server = imageData.getServer()
def project = getProject()

if (project == null) {
    print("No project open! Please create/open a project first.")
    return
}

// Get slide name
def slideName = server.getMetadata().getName()
slideName = slideName.replaceAll("[^a-zA-Z0-9_-]", "_")

// Get all annotations
def annotations = getAnnotationObjects()

if (annotations.isEmpty()) {
    print("No annotations found in this image!")
    return
}

// Create export directory
def projectPath = project.getPath().getParent()
def exportDir = Paths.get(projectPath.toString(), "annotations", "qupath_exports")
exportDir.toFile().mkdirs()

// Export as GeoJSON
def exportPath = Paths.get(exportDir.toString(), "${slideName}_annotations.geojson")

exportObjectsToGeoJson(annotations, exportPath.toString(), "FEATURE_COLLECTION")

print("✓ Exported ${annotations.size()} annotations to:")
print("  ${exportPath}")
print("")
print("Next steps:")
print("1. Copy GeoJSON to ML pipeline:")
print("   cp ${exportPath} /path/to/pipeline/data/annotations/")
print("2. Run import in pipeline:")
print("   python run/import_qupath_annotations.py --species SPECIES")
