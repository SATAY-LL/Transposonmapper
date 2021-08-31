# Creating a custom _adapters.fa_ file

To know the adapters sequence, one way is to look for the overrepresented sequences in your dataset.
Steps:

1. Run the pipeline with the
    - [x] Quality checking raw data CHECKED    
    - [x] Quality check interrupt CHECKED

2. When the GUI ask you to continue, say NO and go to your local `/data/fastqc_out/` 
    - Open the corresponding html file and go to the "Overrepresented sequences" section
    - Copy the sequence that has more than 15% of representation. 

3. Create the adapters.fa in your local data folder 

    - Open a bash terminal and move to the location where you have the data you would like to mount in the pipeline (fastq files)

    ```bash
    cd /data
    ```
    - Create the adapters.fa file customized to your dataset. 

    ```bash
    nano adapters.fa
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
    Do not put empty lines in the text file, otherwise BBDuk might yield an error about not finding the adapters.fa file.!
    ```
 
4. Run again the container  and it will automatically look for that file (adapterfile.fa) in the data folder . 
