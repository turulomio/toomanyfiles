# VHS documentation
#
# Output:
#   Output <path>.gif               Create a GIF output at the given <path>
#   Output <path>.mp4               Create an MP4 output at the given <path>
#   Output <path>.webm              Create a WebM output at the given <path>

Output tree.gif

Require echo

Set Shell "bash"
Set FontSize 14
Set Width 1200
Set Height 800
Set WindowBar Colorful

# Espera un segundo para que la terminal aparezca
Sleep 1s
Type "# This is a video to show how to use 'toomanyfiles_tree' command" Sleep 1s Enter
Type "# It recursively searches and executes all TooManyFiles.json configuration files in the directory tree" Sleep 1s Enter
Type "# By default, output is hidden and only a progress bar is shown" Sleep 1s Enter
Type "toomanyfiles_tree --remove" Sleep 2s Enter
Type "# We can use --show_output to display detailed output for each configuration" Sleep 1s Enter
Type "toomanyfiles_tree --remove --show_output" Sleep 2s Enter
Sleep 5s
