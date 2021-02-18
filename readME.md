This is the workspace in which the simulation for the mine detection bot will be carried out

Changes in latest commit:

Added a depth camera sensor plugin to get posistion of the mine relative to the odom frame.
Posistion of the mine can be obtained using tf and in the camera frame by using
rosrun find_object_2d print_objects_detected node.

The chetak_wc_Camera description urdf mass,torque and inertia values have been reduced by a factor of 10.
Base link had a mass of 600kg before reduction, need to hollow out the bot in cad and change material properties.

Modified minefield.launch in mine_field package to launch all necessary nodes.

Adding markers in 2d costmap at detected coordinates and integration into nav stack yet to be done.

Changes made in previous commit:
    Random placement of 2 mines has been done


The models, and textures in the minefield_sim/models, and the minefield_sim/media don't work unless you copy those folders to /usr/share/gazebo-9/

Do that if you don't want any errors
