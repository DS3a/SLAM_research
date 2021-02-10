This is the workspace in which the simulation for the mine detection bot will be carried out

Changes made in this commit:
    Random placement of 2 mines has been done
    But in order to do that I had to add the /Mine model to /usr/share/gazebo-9/models, it wasn't able to read it from the package file, gotta fix that

    Unable to spawn the bot from chetak_wc_description
