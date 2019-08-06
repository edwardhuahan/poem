# Hafez: an Interactive Poetry Generation System

This is the code for the whole pipeline and web interface described in [Hafez: an Interactive Poetry Generation System](http://xingshi.me/data/pdf/ACL2017demo.pdf).

For Rhyme Generation Code, please find it [here](https://github.com/Marjan-GH/Topical_poetry)
For RNN with FSA decoding code, please find it [here](https://github.com/isi-nlp/Zoph_RNN/blob/master/README_XING.md)

## (EDIT) Additional Preparation
I recommend running this on a machine with CUDA and nvidia GPUs such as the deep-learning vm on Google Cloud
Install [git-lfs](https://github.com/git-lfs/git-lfs/wiki/Installation) in order to download the model which is 1GB

Navigate to /exec and run:
```
chmod +x ZOPH_RNN_GPU_EXPAND
```
This makes the RNN executable as a file

## Preparation

0. Unzip the RNN model files in `models`:
Due to the model's large size (more than 1GB), please download here: [lyrics.tl.nn.gz](https://drive.google.com/open?id=0B9mEwe4MVv7XVk9OcUhzWGg2bUU) and [lyrics.tl.topdown.nn.gz](https://drive.google.com/open?id=0B9mEwe4MVv7XbTMyMlBZRDFWcTA)

```
cd models
gunzip lyrics.tl.nn.gz
gunzip lyrics.tl.topdown.nn.gz
```
1. Copy the rhyme generation code into the folder `sonnet-project-for-server/`

```
cd sonnet-project-for-server
git clone https://github.com/Marjan-GH/Topical_poetry
```

2. Follow the [instruction](https://github.com/Marjan-GH/Topical_poetry/blob/master/README.md) to start the server for `Rhyme Generation`.


## Generate a 4-line poem from command line

In this section, we describe how to generate a four line poem from command line.

1. Follow the [instruction](https://github.com/Marjan-GH/Topical_poetry/blob/master/README.md) to generate related files given any topic. Here, we pre-generate all the related files about topic `Mountain`, please check `example/4line/` folder:

* `source.txt` the source file 
* `poem.fsa` the FSA file
* `encourage.txt` the encourange words list
* `rhyme.txt` the rhyme words information. (You don't need this in following steps)

2. Run the script:

```
cd example/4line
bash run_standaline.sh
```
It will print the command it actually call:

```
<ROOT_DIR>/exec/ZOPH_RNN_GPU_EXPAND --adjacent-repeat-penalty -2.0 --repeat-penalty -3.0 -L 60 -b 50 --legacy-model 1 -k 1 <ROOT_DIR>/example/4line/../..//models/lyrics.tl.nn <ROOT_DIR>/example/4line/temp.txt --fsa <ROOT_DIR>/example/4line/poem.fsa --encourage-list <ROOT_DIR>/example/4line/encourage.txt --encourage-weight 1.0 --dec-ratio 0.0 100.0 --decode-main-data-files <ROOT_DIR>/example/4line/source.txt
```

After 1-2 minutes (most time spent on loading the model), it will generate the following 4 line poem and print in STDOUT:

```
as long as you can see that you are grassy !
this land is filled with highest elevation ,
we took a ride across the river valley ,
and now i got to find my own location .
```

