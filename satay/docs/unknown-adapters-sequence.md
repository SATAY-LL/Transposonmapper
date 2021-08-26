# Identifying the adapters sequence 

To know the adapters sequence , one way is to run the pipeline with the
- [x] Quality checking raw data CHECKED    
- [x] Quality check interrupt CHECKED

Then: 
- When the GUI ask you to continue , say NO and go to your local `/data/fastqc_out/` 
- Open the corresponding html file and go to the "Overrepresented sequences" section
- Copy the sequence that has more than 15% of representation. 


## Create the adapterfile.fa in your local data folder 

1. `cd /data`
2. `nano adapterfile.fa`
3. Edit the file as follows:
    > NAME  
    Paste the copied sequence 
4. Ctrl-O save , Ctrl-X and quit 

 
# Run again the container  


