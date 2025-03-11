// Different colored particles use different thresholding
particleColor = getArgument();

// Check for RGB image
if (bitDepth() > 8) {
    // Convert to grayscale
    run("8-bit");
}

// Invert colors - white bg + black ROIs
run("Invert LUTs");

// Subtract background from image
if (particleColor == "Green") {
    run("Subtract Background...", "rolling=10 light");
}

// Generate a binary image from our image
if (particleColor == "Green") {
    setThreshold(55, 255, "raw");
} else {
    setAutoThreshold("MaxEntropy");
}
setOption("BlackBackground", false);
run("Convert to Mask", "background=Light");
run("Fill Holes");
run("Watershed");
saveAs("tif", "sporetraps/images/" + File.getName(getTitle()));

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's redirect=None decimal=3");
run("Analyze Particles...", "circularity=0.00-1.00 show=Overlay exclude include add");
roiManager("Show None");
saveAs("Results", "sporetraps/results/" + File.getNameWithoutExtension(getTitle()) + ".csv");
