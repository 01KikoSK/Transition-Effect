#!/usr/bin/env python

from gimpfu import *

def transition(image, drawable, duration):
    # Ensure the image has at least two layers
    if len(image.layers) < 2:
        pdb.gimp_message("The image needs at least two layers to perform a transition.")
        return

    # Get the top two layers
    top_layer = image.layers[0]
    bottom_layer = image.layers[1]

    # Create a new layer for the transition effect
    transition_layer = pdb.gimp_layer_new_from_visible(image, image, "Transition Layer")
    pdb.gimp_image_insert_layer(image, transition_layer, None, 0)

    # Apply the transition effect
    for i in range(duration + 1):
        opacity = (i / float(duration)) * 100
        pdb.gimp_layer_set_opacity(top_layer, 100 - opacity)
        pdb.gimp_displays_flush()
        pdb.gimp_progress_update(i / float(duration))

    pdb.gimp_layer_set_opacity(top_layer, 100)
    pdb.gimp_image_remove_layer(image, transition_layer)

register(
    "python_fu_transition",
    "Transition Effect",
    "Apply a simple transition effect between two layers",
    "Your Name",
    "Your Name",
    "2024",
    "<Image>/Filters/Custom/Transition Effect",
    "RGB*, GRAY*",
    [
        (PF_SPINNER, "duration", "Transition Duration", 10, (1, 100, 1))
    ],
    [],
    transition)

main()
