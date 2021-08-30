# How to use the pipeline in the docker container 

1. Pull the docker image from Docker Hub
```bash
docker pull mwakok/satay:latest
```
2. Build the image and create the docker container locally in your computer

```bash
docker build . -t mwakok/satay:latest
```

## Run the pipeline

- Move to the location where you have the data you would like to mount to the container ,
to use `$(pwd)` in the command bellow (simplest option) , otherwise indicate the absolute path from your computer you would like to be loaded.

```bash
# For Windows (and WSL):
docker run --rm -it -e DISPLAY=host.docker.internal:0 -v /$(pwd):data/ mwakok/satay:latest 
```

```bash
# For macOS
docker run --rm -it -e DISPLAY=docker.for.mac.host.internal:0 -v $(pwd):/data mwakok/satay 
```

```bash
# For Linux
docker run --rm -it --net=host -e DISPLAY=:0 -v $(pwd):/data mwakok/satay

```

## Access the terminal of the docker container 



```bash
# For Windows (and WSL):
docker run --rm -it -e DISPLAY=host.docker.internal:0 -v /$(pwd):data/ mwakok/satay:latest bash
```

```bash
# For macOS
docker run --rm -it -e DISPLAY=docker.for.mac.host.internal:0 -v $(pwd):/data mwakok/satay bash
```

```bash
# For Linux
docker run --rm -it --net=host -e DISPLAY=:0 -v $(pwd):/data mwakok/satay bash

```

- The flag `-e` enables viewing of the GUI outside the container via the Xserver
- The flag `-v` mounts the current directory (pwd) on the host system to the data/ folder inside the container

## Creating a custom adapterfile.fa in your data/ folder 

To know the adapters sequence , one way is to look for the overrepresented sequences in your dataset.
Steps:

1. Run the pipeline with the
    - [x] Quality checking raw data CHECKED    
    - [x] Quality check interrupt CHECKED

2. When the GUI ask you to continue , say NO and go to your local `/data/fastqc_out/` 
    - Open the corresponding html file and go to the "Overrepresented sequences" section
    - Copy the sequence that has more than 15% of representation. 


3. Create the adapterfile.fa in your local data folder 

    - Open a bash terminal and move to the location where you have the data you would like to mount in the pipeline (fastq files)

    ```bash
    cd /data
    ```
    - Create the adapterfile file customized to your dataset. 

    ```bash
    nano adapterfile.fa
    ```
    - Inside the `nano` editor , edit the file as follows: 
    ```bash
    > \> Sequence1
    >
    > Overrepresented sequence 1
    >
    > \> Sequence2
    >
    > Overrepresented sequence 2

    ```
    -  Ctrl-O save , Ctrl-X and quit the editor

    ```{note}
    Note to not put empty lines in the text file, otherwise BBDuk might yield an error about not finding the adapters.fa file.!
    ```

 
4. Run again the container  and it will automatically look for that file (adapterfile.fa) in the data folder . 

## Troubleshooting

- When running the container , mainly for the 1st time , after a reboot of your PC, this may pops up:

``` bash
Gtk-WARNING **: cannot open display: :0
```
There is a solution in Linux is typing the following command in the terminal : `xhost +`
