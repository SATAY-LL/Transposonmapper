

#  Allow chrome to run without a sandbox (a manual tweak)

Steps:


1. Run the container in bash mode : 

`docker run --rm -it --net=host -e DISPLAY=:0 -v $(pwd):/data USERNAME/satay bash`

1. Open this document outside the GUI to follow the steps

`xdg-open ../opt/src/allow-open-chrome-in-docker.md`

2. Open the google chrome config file in the nano editor in the terminal of the container

`nano ../usr/bin/google-chrome`

    Steps inside nano:

1. Add `–no-sandbox` at the end of the last line (Line No: 49) of the file.
    - That is from `exec -a "$0" "$HERE/chrome" "$@"` go to `exec -a "$0" "$HERE/chrome" "$@" --no-sandbox`

3. Save and exit 

    - Ctrl-O 
    - Ctrl-X


4. Run the pipeline by writing the following command: 

`bash ../opt/satay/satay.sh` 
