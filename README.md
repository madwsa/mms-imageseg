# mms-imageseg
ML project for semantic image segmentation for unmanned spacecraft (Autumn 2021 CS230 final project)

- `notebooks`; model training for milestone and final project submission
- `dataset-generation`: scripts for dataset creation
- `blender-models`: modified versions of 3D models of spacecraft from [NASA](https://nasa3d.arc.nasa.gov/models)

Images of spacecraft photographed from other spacecraft operating in outer space are difficult to come by, especially at a scale typically required for deep learning tasks.  Semantic image segmentation, object detection and localization, and pose estimation are well researched areas with powerful results for many applications, and would be very useful in autonomous satellite operation and rendezvous.  However, Wong et al.~\cite{wong_synthetic_2019} notes that these strong results in broad and common domains may generalize poorly even to specific industrial applications on earth.

To address this, we have generated a prototype synthetic image dataset labelled for semantic segmentation of 2D images of unmanned spacecraft, and are endeavouring to train a performant deep learning image segmentation model using the same, with the ultimate goal of enabling further research in the area of autonomous satellite rendezvous.

