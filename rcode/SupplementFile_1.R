#libraries to install:

#install.packages("tidyverse")
#install.packages("ggplot2")
#install.packages("plyr")
#install.packages("BiocManager")
#library(BiocManager)

#BiocManager::install("Rsamtools")
#BiocManager::install("Rbowtie2")
#BiocManager::install("ShortRead")
#BiocManager::install("BSgenome.Scerevisiae.UCSC.sacCer3", version = "3.8") #We'll use v3.8 throughout for future compatibility


#load libraries
library(ggplot2)
library(tidyverse)
library(tcltk)
library(plyr)
library(Rsamtools)
library(Rbowtie2)
library(ShortRead)
library("BSgenome.Scerevisiae.UCSC.sacCer3")


###################Variables to declare #########################################
#
samplename<-"foobar"                        #This can be anything. It will be used to name the output files
#
#
genomepath<- "C:/Users/myuser/yeastgenome/"  #points to the folder where the genome and the genome annotation files are stored
workpath<- "C:/Users/myuser/results/"        #points to the folder in which the results will be saved
#
#
tmpfolder<- "C:/Users/myuser/tmp/"        #points to a temporary folder where intermediate data will be temporarily stored.
dir.create(tmpfolder)
#
#
#
fastqFolder <- "C:/Users/myuser/myFastqFolder/" #points to the folder where the fastq Files are saved
#
##################################################################################

#The variables below are generated automatically
trimmed<-paste0(tmpfolder,"/trimmed.fq")
samfile<-paste0(tmpfolder,"/aligned.sam")
setwd(workpath)
bamfile<-paste0(workpath,"/",samplename)

yeastGFF<-paste0(genomepath,"/saccharomyces_cerevisiae_R64-2-1_20150113.gff")
yeastgenome<-paste0(genomepath,"/yeastgenome.fa")

fastqfilesNlaIII<-list.files(fastqFolder,"NlaIII.*[.]fastq[.]gz", ignore.case=T, recursive = T)
fastqfilesDpnII<-list.files(fastqFolder,"DpnII.*[.]fastq[.]gz", ignore.case=T, recursive = T)


#preprocess NLAIII Fastq file and remove adaptors
NlaIII="CATG"
file.remove(trimmed)
for (i in fastqfilesNlaIII){
  stream <- open(FastqStreamer(paste0(fastqFolder,"/",i),100000))
  repeat{
    fq<-yield(stream)
    if (length(fq) == 0)
      +             break
    
    ########Trimming of adaptors
    vmatchPattern(NlaIII,fq@sread)->matchingReads
    lapply(matchingReads@ends, function(l) l[[1]])->matchingReads
    matchingReads[unlist(lapply(matchingReads, is.null))]<-NA
    unlist(matchingReads)->matchingReads
    narrow(fq, end = matchingReads)->fq
    
    
    #######trimming based on quality:
    ##the phred score (here 13) relates to the CLC quality score limit like this:
    ##clcscore=10^(phredscore/-10). for a clcscore of 0.05, phredscore = 13 but 13 won't work
    phredscore="4"
    
    fq <- trimTailw(fq, 2, phredscore, 2)
    writeFastq(fq, trimmed, "a", compress=FALSE)
  }
  close(stream)
}


#preprocess DpnII Fastq file and remove adaptors

DpnII="GATC"
#file.remove(trimmedDpnII)
for (i in fastqfilesDpnII){
  stream <- open(FastqStreamer(paste0(fastqFolder,"/",i),100000))
  repeat{
    fq<-yield(stream)
    if (length(fq) == 0)
      +             break
    
    ########Trimming of adaptors
    vmatchPattern(DpnII,fq@sread)->matchingReads
    lapply(matchingReads@ends, function(l) l[[1]])->matchingReads
    matchingReads[unlist(lapply(matchingReads, is.null))]<-NA
    unlist(matchingReads)->matchingReads
    narrow(fq, end = matchingReads)->fq
    
    #######trimming based on quality:
    fq <- trimTailw(fq, 2, phredscore, 2)
    writeFastq(fq, trimmed, "a", compress=FALSE)
  }
  close(stream)
}


genome <- BSgenome.Scerevisiae.UCSC.sacCer3
infoseq<-genome@seqinfo
writeBSgenomeToFasta(genome, yeastgenome)
dir.create(paste0(dirname(yeastgenome), "/bowtie2/"))
indexedgenome<-paste0(dirname(yeastgenome), "/bowtie2/indexedgenome")
bowtie2_build(yeastgenome, indexedgenome, overwrite = TRUE)


indexedgenome<-paste0(dirname(yeastgenome), "/bowtie2/indexedgenome")
bowtie2(indexedgenome,
        samfile,
        trimmed,
        "--local --threads 6",
        overwrite=TRUE
)


asBam(samfile,destination = bamfile)
file.remove(samfile)
file.remove(trimmed)

qual<-5
parameters<-ScanBamParam(what=c("rname", "strand", "pos", "qwidth"), mapqFilter= qual)
bamdata<-scanBam(paste0(bamfile,".bam"), param = parameters)

bamdata[[1]]$strand->orientation
bamdata[[1]]$pos->position
bamdata[[1]]$qwidth->size
bamdata[[1]]$rname->chr

remove(bamdata)






posplus<-as.array(position[(orientation == "+")])
chrplus<-as.factor(chr[(orientation == "+")])
oriplus<-as.factor(orientation[(orientation == "+")])

posminus<-as.array(position[(orientation == "-")])
sizeminus<-as.array(size[(orientation == "-")])
chrminus<-as.factor(chr[(orientation == "-")])
oriminus<-as.factor(orientation[(orientation == "-")])




corrpositionminus<-posminus+sizeminus



readcoordinates<-data.frame(
  chrom = fct_c(chrplus,chrminus), 
  coord = c(posplus,corrpositionminus), 
  strand = fct_c(oriplus, oriminus)
)


readcoordinates<-readcoordinates[
  order(readcoordinates$chrom, readcoordinates$coord),
]

len_chr = c(230218,  813184, 316620, 1531933,  576874,
            270161, 1090940, 562643,  439888,  745751, 
            666816, 1078177, 924431,  784333, 1091291,
            948066,   85799)
chr_name = c("chrI",   "chrII",  "chrIII",  "chrIV",  "chrV",
             "chrVI",  "chrVII", "chrVIII", "chrIX",  "chrX",
             "chrXI",  "chrXII", "chrXIII", "chrXIV", "chrXV", 
             "chrXVI", "chrmt")

outofbounds<-integer()  
for (i in 1:length(len_chr)) {
  outofbounds<-c(outofbounds, which(readcoordinates$chrom == chr_name[i] & readcoordinates$coord > len_chr[i]))
}

readcoordinates<-readcoordinates[-outofbounds,]


rm(tncoordinates)
tncoordinates<-list()
lvlchrom<-levels(readcoordinates$chrom)


pb<-txtProgressBar(min=0, max = length(readcoordinates$chrom))
#process first read
readcounter<-1
tnnumber<-1
readnumb<-1
tncounter<-1
coord<-readcoordinates$coord[readcounter]
strand<-readcoordinates$strand[readcounter]
readnumb<-1
tncoordinates$chrom[tncounter]<-readcoordinates$chrom[readcounter]
tncoordinates$pos[tncounter]<-readcoordinates$pos[readcounter]
tncoordinates$strand[tncounter]<-readcoordinates$strand[readcounter]


#process further reads
for (readcounter in 2:length(readcoordinates$chrom)) {
  if (abs(readcoordinates$coord[readcounter]-coord)<3 & readcoordinates$strand[readcounter]==strand) {
    readnumb<-readnumb+1
  } else {
    tncoordinates$chrom[tncounter]<-readcoordinates$chrom[readcounter-1]
    tncoordinates$coord[tncounter]<-as.integer(mean(readcoordinates$coord[(readcounter-readnumb):(readcounter-1)]))
    tncoordinates$strand[tncounter]<-readcoordinates$strand[readcounter-1]
    tncoordinates$readnumb[tncounter]<-readnumb
    
    readnumb<-1
    tncounter<-tncounter+1
    coord<-readcoordinates$coord[readcounter]
    strand<-readcoordinates$strand[readcounter]
  }
  setTxtProgressBar(pb,readcounter)
  
}





rm(pb)
rm(parameters)
rm(chr)
rm(chrminus)
rm(chrplus)
rm(coord)
rm(corrpositionminus)
rm(fastqFilesDpnII)
rm(fastqFilesNlaIII)
rm(trimmed)
rm(orientation)
rm(oriminus)
rm(oriplus)
rm(position)
rm(posminus)
rm(posplus)
rm(qual)
rm(readcounter)
rm(readnumb)
rm(samfile)
rm(size)
rm(sizeminus)
rm(strand)
rm(tncounter)
rm(tnnumber)
rm(outofbounds)


#read GFF 

gffdata<-import.gff(yeastGFF)
GFF<-list()
GFF$type<-gffdata@elementMetadata@listData$type
GFF$name<-gffdata@elementMetadata@listData$Name
GFF$gene<-gffdata@elementMetadata@listData$gene
GFF$start<-gffdata@ranges@start
GFF$end<-gffdata@ranges@start+gffdata@ranges@width




read.delim(yeastGFF, header=F, comment.char="#", skip = 18, nrows = 23058) -> tmpgff
gff<-plyr::rename(tmpgff, c("V1" = "chrom", "V2"="source", "V3"="type","V4"="start","V5"="end","V7"="strand"))
gff$chrom<-as.character(gff$chrom)
gff$chrom<-factor(gff$chrom, levels = lvlchrom)

GFF$chrom<-gff$chrom
GFF$strand<-gff$strand

GFF<-data.frame(GFF)

GFF[GFF$type=="gene",]->gene
knowngene<-which(gene$gene!="NA")
gene$name<-as.character(gene$name)
gene$name[knowngene]<-as.character(gene$gene[knowngene])



GFF[GFF$type=="centromere",]->centromere




centromereplot<-list()
centromereplot$chrom<-(1:16)
centromereplot$coord<-(centromere$start+centromere$end)/2

ggplot()+
  geom_histogram(data=data.frame(tncoordinates), aes(x=coord), binwidth=20000)+
  geom_point(data = data.frame(centromereplot), aes(x=coord, y=1000),color="red")+
  facet_wrap(~ chrom, nrow = 5)

tnpergene<-numeric()
readpergene<-numeric()
readpergenecrude<-numeric()
pb<-txtProgressBar(min=0, max = length(gene$chrom))

for (i in 1:length(gene$start)) {
  tnindex<-which((tncoordinates$coord > gene$start[i]) &
                   (tncoordinates$coord < gene$end[i]) & 
                   (tncoordinates$chrom == as.numeric(gene$chrom[i])))
  
  tnpergene[i]<-length(tnindex)
  
  if (length(tnindex)>0) {
    readpergene[i]<-sum(tncoordinates$readnumb[tnindex])-max(tncoordinates$readnumb[tnindex])
  } else {
    readpergene[i]<-0
  }
  
  readpergenecrude[i]<-sum(tncoordinates$readnumb[tnindex])
  
  setTxtProgressBar(pb,i)
}


hist(tnpergene, breaks=seq(min(tnpergene),max(tnpergene)),xlim=c(0,200),ylim=c(0,100))
hist(readpergene, breaks=seq(min(readpergene),max(readpergene)),xlim=c(0,200), ylim=c(0,100))
# ggplot()+
#   geom_point(mapping=aes(x=tnpergene, y=readpergene, color=gene$chrom))+
#   xlim(0,500)+
#   ylim(0,5000)


bedfile<-paste0(bamfile,".bed")
headerline<-paste0("track name=\"",basename(bamfile),"\" useScore=1")



bed<-list()
bed$chrom<-plyr::mapvalues(tncoordinates$chrom, as.character(1:17), lvlchrom)
bed$start<-format(tncoordinates$coord, scientific = FALSE)
bed$end<-format((tncoordinates$coord+1), scientific = FALSE)
bed$desc<-paste(replicate(length(bed$start),"."))
bed$score<-tncoordinates$readnumb*10+100
bed<-data.frame(bed)



writeLines(headerline, con = bedfile)
write.table(bed,bedfile, quote =FALSE, row.names = FALSE, col.names =FALSE, append=TRUE)

readLines(bedfile, n=10)

wigfile<-paste0(bamfile,".wig")
headerline<-paste0("track type=wiggle_0 maxHeightPixels=60 name=\"",basename(bamfile),"\"")


wig<-list()
wig$chrom<-plyr::mapvalues(tncoordinates$chrom, as.character(1:17), lvlchrom)
wig$coord<-format(tncoordinates$coord, scientific = FALSE)
wig$score<-tncoordinates$readnumb
wig<-data.frame(wig)

wigdup<-which(duplicated(wig[,1:2]))
wig[(wigdup-1),3]<-wig[(wigdup-1),3]+wig[(wigdup),3]
wig<-wig[-wigdup,]
wigchrom<-wig$chrom
wig$chrom<-NULL

writeLines(headerline, con = wigfile)
for (i in lvlchrom) {
  
  write(paste0("variableStep chrom=",i), file = wigfile, append=TRUE)
  write.table(wig[
    wigchrom == i
    ,],
    wigfile, quote =FALSE, row.names = FALSE, col.names =FALSE, append=TRUE)
}

readLines(wigfile, n=10)


pergenefile<-paste0(bamfile,"_pergene.txt")
headerline<-paste("gene_name", "number_of_transposon_per_gene","number_of_read_per_gene")

pergene<-list()
pergene$name<-gene$name
pergene$tn<-tnpergene
pergene$read<-readpergene
pergene<-data.frame(pergene)

writeLines(headerline, con = pergenefile)
write.table(pergene,pergenefile, quote =FALSE, row.names = FALSE, col.names =FALSE, append=TRUE)


readLines(pergenefile, n=10)

