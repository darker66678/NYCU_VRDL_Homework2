import os
from os import walk, getcwd
from PIL import Image
import h5py
import argparse
import random
import pandas as pd

def get_parser():
    parser = argparse.ArgumentParser(description='my description')
    parser.add_argument(
        '--train_folder', default='./yolov5/data/train/')
    parser.add_argument(
        '--test_folder', default='./yolov5/data/test/')
    return parser

def get_img_boxes(mat, idx=0):
    bboxs = mat['digitStruct/bbox']
    meta = {key: [] for key in ['height', 'left', 'top', 'width', 'label']}
    box = mat[bboxs[idx][0]]
    for key in box.keys():
        if box[key].shape[0] == 1:
            meta[key].append(int(box[key][0][0]))
        else:
            for i in range(box[key].shape[0]):
                meta[key].append(int(mat[box[key][i][0]][()].item()))
    return meta

def convert(size, box):
    dw = size[0]
    dh = size[1]
    x = box[0] + (box[1]/2.0)
    y = box[2] + (box[3]/2.0)
    w = box[1]
    h = box[3]
    x = x/dw
    w = w/dw
    y = y/dh
    h = h/dh
    return (x, y, w, h)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    print("start!")
    # build train.txt that include train data
    imgs = []
    for img_file in os.listdir(args.train_folder):
        if img_file.endswith('.png'):
            imgs.append(img_file[0:-4])
    imgs = sorted(imgs, key=lambda x: int(os.path.splitext(x)[0]))

    # sample val_data
    val_num = int(len(imgs)*0.01)
    val_sample = random.sample(imgs, val_num)
    train_imgs = pd.DataFrame(imgs)
    for sample_num in val_sample:
        train_imgs = train_imgs[train_imgs[0] != sample_num]
    train_imgs = sorted(list(train_imgs[0].astype(int)))
    val_sample = sorted(map(int,val_sample))

    file = open("./yolov5/data/cfg/train.txt", "w")
    for i in range(len(train_imgs)):
        file.write("."+args.train_folder+str(train_imgs[i])+'.png\n')
    file.close()
    file = open("./yolov5/data/cfg/val.txt", "w")
    for i in range(len(val_sample)):
        file.write("."+args.train_folder+str(val_sample[i])+'.png\n')
    file.close()

    # build test.txt that include test data
    test_imgs = []
    for img_file in os.listdir(args.test_folder):
        if img_file.endswith('.png'):
            test_imgs.append(img_file[0:-4])
    test_imgs = sorted(test_imgs, key=lambda x: int(os.path.splitext(x)[0]))
    file = open("./yolov5/data/cfg/test.txt", "w")
    for i in range(len(test_imgs)):
        file.write("."+args.test_folder+str(test_imgs[i])+'.png\n')
    file.close()
    
    # get the data in mat file
    mat = h5py.File(
        args.train_folder+'digitStruct.mat', 'r')
    attrs = {}
    for index in range(len(imgs)):
        temp_train = "temp_train/"
        file = open(temp_train+str(index+1)+".txt", "w")
        for key in ['label', 'left', 'top', 'width', 'height']:
            values = get_img_boxes(mat, index)[key]
            attrs[key] = values
        #file.write(str(len(attrs['label'])))
        for j in range(len(attrs['label'])):
            if attrs['label'][j]==10:
                attrs['label'][j]=0
            file.write(str(int(attrs['left'][j])) + " " + str(int(attrs['top'][j])) + " " + str(int(
                attrs['width'][j])) + " " + str(int(attrs['height'][j])) + " " + str(int(attrs['label'][j])) + " ")
            file.write("\n")
        if index % 1000 == 0 and index!=0:
            print(index)
    file.close()

    # transfer to yolo format
    mypath = "./temp_train/"
    outpath = args.train_folder
    txt_name_list = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        txt_name_list.extend(filenames)
        break
    txt_name_list = sorted(txt_name_list,key=lambda x: int(os.path.splitext(x)[0]))
    for txt_name in txt_name_list:
        txt_path = mypath + txt_name
        txt_file = open(txt_path, "r")
        lines = txt_file.read().split('\n')   
        txt_outpath = outpath + txt_name
        txt_outfile = open(txt_outpath, "w")
        
        #Convert the data to YOLO format
        ct = 0
        for line in lines:
            if(len(line) >= 2):
                ct = ct + 1
                elems = line.split(' ')
                xmin = elems[0]
                xmax = elems[2]
                ymin = elems[1]
                ymax = elems[3]
                cls = elems[4]
                path = args.train_folder
                img_path = str(path+'%s.png'%(os.path.splitext(txt_name)[0]))
                im=Image.open(img_path)
                w= int(im.size[0])
                h= int(im.size[1])   
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert((w,h), b)
                txt_outfile.write(str(cls) + " " + " ".join([str(a) for a in bb]) + '\n')  
    print("finish!")      

