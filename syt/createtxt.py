from glob import glob

train_img_list = glob('dataset/train/images/*.jpg')
val_img_list = glob('dataset/val/images/*.jpg')

with open('dataset/train.txt', 'w') as f :
    f.write('\n' .join(train_img_list) + '\n')

with open('dataset/val.txt', 'w') as f :
    f.write('\n' .join(val_img_list) + '\n')