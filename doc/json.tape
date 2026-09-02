# VHS documentation
#
# Output:
#   Output <path>.gif               Create a GIF output at the given <path>
#   Output <path>.mp4               Create an MP4 output at the given <path>
#   Output <path>.webm              Create a WebM output at the given <path>

Output json.gif

Require echo

Set Shell "bash"
Set FontSize 14
Set Width 1200
Set Height 800
Set WindowBar Colorful

# Espera un segundo para que la terminal aparezca
Sleep 1s
Type "# This is a video to show how to use 'toomanyfiles_json' command" Sleep 1s Enter
Type "# First, we can create a default configuration file in current directory with --create" Sleep 1s Enter
Type "toomanyfiles_json --create" Sleep 1s Enter
Type "cat TooManyFiles.json" Sleep 1s Enter
Type "# We can simulate the cleanup process without deleting files using --pretend" Sleep 1s Enter
Type "toomanyfiles_json --pretend" Sleep 2s Enter
Type "# We can also list files to process and ignored with --list" Sleep 1s Enter
Type "toomanyfiles_json --list" Sleep 2s Enter
Type "# Finally, execute file removal according to TooManyFiles.json with --remove" Sleep 1s Enter
Type "toomanyfiles_json --remove" Sleep 2s Enter
Sleep 5s
