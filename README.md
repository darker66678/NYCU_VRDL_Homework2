# NYCU_VRDL_Homework2
This is a Homework in VRDL class at NYCU , building a object detector of SVHN dataset with deep learning

NYCU_VRDL_Homework2

| -```yolo_v5``` This is a reference project from [yolov5](https://github.com/ultralytics/yolov5)

....|-```data```It includes all the config.files

....|-```models``` It includes all the model configs

....|-```train.py``` It is main program of training

....|-```val.py``` (inference.py) It is main program of testing

| -```requirements.txt``` need to install these librarys

| -```yolo_format.py``` using this code translates ```.mat``` to yolo format (Data preprocessing)

| -```yolov5_train.sh``` this is shell script for training

| -```yolov5_test.sh``` this is shell script for testing

| -```train``` training data

| -```test``` testing data
## Requirements
To install requirements: ```pip install -r requirements.txt```
My Python version==3.8.12
## Data preprocessing
Download SVHN dataset and put them in ```./train``` and ```./test```

Because the ground truth info is the ```.mat``` file, we need to do preprocessing, align the yolo format.

```python yolo_format.py --train_folder ./train/ --test_folder ./test/ ```

The program will randomly split 0.01 of training data as validation data
## Training
```sh yolov5_train.sh``` quickly train

you can alter info of yolov5_train.sh

1.```--img```  img resolution 

2.```--batch``` batch size

3.```--epochs``` training epochs

4.```--data```  yaml path

5.```--weights``` version of yolov5

## Evaluation
[Download my yolov5 model](https://drive.google.com/file/d/1G2jE57AjQs4ChBBVvnlMX4bPitxJw74z/view?usp=sharing)

put it in ```./yolo_v5/runs```

In ```./yolo_v5/data/svhn.yaml ```, change ```val.txt``` into ```test.txt```

```sh yolov5_test.sh``` quickly train and produce json file

you can alter info of yolov5_test.sh

1.```--data```  yaml path

2.```--weights``` your model file



Finally find the ```yolov5m6_512_predictions.json``` file  in ```./yolo_v5/runs/exp/```
## Pre-trained model
I choose pre-trained model of [yolov5](https://github.com/ultralytics/yolov5),
it will download in your training

just indicated ```--weights xxx.pt```

[Click here see all the pre-trained model](https://github.com/ultralytics/yolov5#pretrained-checkpoints)

[Download my yolov5 model](https://drive.google.com/file/d/1G2jE57AjQs4ChBBVvnlMX4bPitxJw74z/view?usp=sharing)

## Results
my model's map:
|model name|Map|Inference time per image|
|---|--|-----|
|Yolov5_m6 (512*512)|0.428469|0.0651833|
|Yolov5_l (256*256)|0.372573|--|

## Colab deploy
[Colab](https://colab.research.google.com/drive/1uMu3PLxIXXeicIaqqKhetJcgyiZmB1N2?usp=sharing)

![Colab time](https://github.com/darker66678/NYCU_VRDL_Homework2/blob/main/colab_time.png)

