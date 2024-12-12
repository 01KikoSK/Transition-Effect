#!/usr/bin/env python

from gimpfu import *

def transition(image, drawable, duration, transition_type):
    if len(image.layers) < 2:
        pdb.gimp_message("The image needs at least two layers to perform a transition.")
        return

    top_layer = image.layers[0]
    bottom_layer = image.layers[1]

    pdb.gimp_image_undo_group_start(image)

    if transition_type == "Fade":
        for i in range(duration + 1):
            opacity = (i / float(duration)) * 100
            pdb.gimp_layer_set_opacity(top_layer, 100 - opacity)
            pdb.gimp_displays_flush()
            pdb.gimp_progress_update(i / float(duration))

    elif transition_type == "Slide":
        initial_offset = pdb.gimp_drawable_offsets(top_layer)
        for i in range(duration + 1):
            offset = int(initial_offset[0] - (initial_offset[0] * (i / float(duration))))
            pdb.gimp_layer_translate(top_layer, -offset, 0)
            pdb.gimp_displays_flush()
            pdb.gimp_progress_update(i / float(duration))

    elif transition_type == "Wipe":
        for i in range(duration + 1):
            x_offset = int((drawable.width * (i / float(duration))))
            pdb.gimp_image_select_rectangle(image, CHANNEL_OP_SUBTRACT, x_offset, 0, drawable.width - x_offset, drawable.height)
            pdb.gimp_edit_clear(top_layer)
            pdb.gimp_displays_flush()
            pdb.gimp_progress_update(i / float(duration))

    else:
        pdb.gimp_message("Unsupported transition type.")

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_layer_set_opacity(top_layer, 100)

register(
    "python_fu_transition",
    "Transition Effect",
    "Apply various transition effects between layers",
    "Your Name",
    "Your Name",
    "2024",
    "<Image>/Filters/Custom/Transition Effect",
    "RGB*, GRAY*",
    [
        (PF_SPINNER, "duration", "Transition Duration", 10, (1, 100, 1)),
        (PF_RADIO, "transition_type", "Transition Type", "Fade",
         (("Fade", "Fade"), ("Slide", "Slide"), ("Wipe", "Wipe")))
    ],
    [],
    transition)

main()
