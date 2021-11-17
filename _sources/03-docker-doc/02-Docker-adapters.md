# Creating a custom _adapters.fa_ file

The sequencing company should already trim the adaptes sequence. Therefore , what is usually left to trim is the sequencing primer sequence.

The overrepresented sequences typically dont align very well to the genome , so these sequences are majorly lost during alignment. 

1. Create the adapters.fa in your local data folder 

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
    > Sequencing primer sequence
    >
    ```
    -  Ctrl-O save , Ctrl-X and quit the editor

    ```{note}
    Do not put empty lines in the text file, otherwise BBDuk might yield an error about not finding the adapters.fa file.!
    ```
 
4. Run again the container  and it will automatically look for that file (adapterfile.fa) in the data folder . 
