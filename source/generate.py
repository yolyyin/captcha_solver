#!/usr/bin/env python3

import os
import numpy
import random
import cv2
import argparse
from captcha import image as captcha_image
from source.category import create_category
from train_val_split import split_dataset


def generate_data_config(output_dir,class2cat,name="data.yaml"):
    file_path = os.path.join(output_dir, name)
    with open(file_path,"w") as f:
        f.write(f"path: {output_dir}\ntrain: images/train\nval: images/val\ntest:\n\n")
        f.write("names:\n")
        for c,cat in class2cat.items():
            f.write(f"  {c}: '{cat}'\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--font_dir', help='path of fonts files', type=str)
    parser.add_argument('--width', help='Width of captcha image', type=int,default=192)
    parser.add_argument('--height', help='Height of captcha image', type=int,default=96)
    parser.add_argument('--max_len', help='Length of captchas in characters', type=int)
    parser.add_argument('--count',
                        nargs="+",
                        help='How many captchas to generate',
                        type=int)
    parser.add_argument('--mix_dir',
                        help='path of optional mixed fonts files', type=str)
    parser.add_argument('--mix_count',
                        help='How many mixed font captchas to generate',
                        type=int)
    parser.add_argument('--output_dir', help='Where to store the generated captchas', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    parser.add_argument('--config_name', help='data config file name', type=str,default="data.yaml")
    parser.add_argument('--train_ratio', help='the train/val ratio will be train_ratio:1-train_ratio', type=float)
    args = parser.parse_args()

    if args.font_dir is None:
        print("Please specify the captcha fonts")
        exit(1)

    if args.width is None:
        print("Please specify the captcha image width")
        exit(1)

    if args.height is None:
        print("Please specify the captcha image height")
        exit(1)

    if args.max_len is None:
        print("Please specify the captcha length")
        exit(1)

    if args.count is None:
        print("Please specify the captcha count to generate")
        exit(1)

    if args.output_dir is None:
        print("Please specify the captcha output directory")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    if args.mix_dir is not None:
        if args.mix_count is None:
            print("Please specify the count of mixed font")
            exit(1)

    if args.train_ratio is None:
        print("Please specify the train/val ratio")
        exit(1)
    assert (1 >= args.train_ratio > 0), "train ratio must be 0-1"

    # read all the fonts
    font_names = os.listdir(args.font_dir)
    font_names = sorted(font_names)
    ab_font_paths = []

    # generate number of different fonts
    count_list = args.count

    # check if length of count_list and font_names matches
    if len(font_names) != len(count_list):
        print("font numbers and count numbers must match.")
        exit(1)
    # calculate per_len_count, generate length from 2 to max_len
    per_len_count_list = [count // (args.max_len-1) for count in count_list]

    # read symbol sets
    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()
    print("Generating captchas with symbol set {" + captcha_symbols + "}")
    # by yty, create categories
    cat2class, class2cat = create_category(captcha_symbols)
    print("----cat2class-----")
    print(cat2class)
    print("----class2cat-----")
    for k,v in class2cat.items():
        print(f"  {k}: {v}")

    # generate data.yaml file
    absolute_train_path = os.path.abspath(args.output_dir)
    generate_data_config(absolute_train_path, class2cat, name=args.config_name)
    print(f"data config file generated as {absolute_train_path}/{args.config_name}")

    if not os.path.exists(args.output_dir):
        print("Creating output directory " + args.output_dir)
        os.makedirs(args.output_dir)

    for font_name,per_len_count in zip(font_names, per_len_count_list):
        ab_font_path = os.path.join(args.font_dir, font_name)
        ab_font_paths.append(ab_font_path)

        output_folder = font_name[:font_name.rfind(".")]
        font_raw_name = output_folder
        #print(output_folder)
        out_dir = os.path.join(args.output_dir,output_folder)
        os.makedirs(out_dir,exist_ok=True)
        # define font specif generator
        captcha_generator = captcha_image.ImageCaptcha(width=args.width, height=args.height, fonts=[ab_font_path])

        captcha_generator.character_warp_dx = (0.1, 0.5)
        captcha_generator.character_warp_dy = (0.2, 0.5)
        captcha_generator.character_rotate = (-45,45)
        captcha_generator.word_space_probability = 0.5
        # captcha_generator.word_space_probability = 0.8
        # captcha_generator.word_offset_dx= 0.8

        for length in range(2,args.max_len+1):
            for i in range(per_len_count):
                random_str = ''.join([random.choice(captcha_symbols) for _ in range(length)])
                #image_path = os.path.join(out_dir, random_str+'.png')
                #yty, just use a more normal name
                image_path = os.path.join(out_dir, f'{font_raw_name}_l{length}_{i}.png')
                #if os.path.exists(image_path):
                #    version = 1
                #    while os.path.exists(os.path.join(out_dir, random_str + '_' + str(version) + '.png')):
                #        version += 1
                #    image_path = os.path.join(out_dir, random_str + '_' + str(version) + '.png')
                
                image = numpy.array(captcha_generator.generate_image(image_path,cat2class,random_str))
                cv2.imwrite(image_path, image)

    if args.mix_dir is not None:
        mix_per_len_count = args.mix_count // (args.max_len-1)
        # do some mixed font generation
        out_dir = os.path.join(args.output_dir, "mixed")
        os.makedirs(out_dir, exist_ok=True)
        # read mixed fonts
        font_names = os.listdir(args.mix_dir)
        mix_font_paths = [os.path.join(args.mix_dir,font) for font in font_names]
        # define mixed generator
        mix_generator = captcha_image.ImageCaptcha(width=args.width, height=args.height, fonts=mix_font_paths)

        mix_generator.character_warp_dx = (0.1, 0.5)
        mix_generator.character_warp_dy = (0.2, 0.5)
        mix_generator.character_rotate = (-45, 45)
        mix_generator.word_space_probability = 0.5
        for length in range(2, args.max_len + 1):
            for i in range(mix_per_len_count):
                random_str = ''.join([random.choice(captcha_symbols) for _ in range(length)])
                # yty, just use a more normal name
                image_path = os.path.join(out_dir, f'mix_l{length}_{i}.png')
                image = numpy.array(mix_generator.generate_image(image_path, cat2class, random_str))
                cv2.imwrite(image_path, image)

    # doing train/val split
    split_dataset(args.output_dir, args.train_ratio)


if __name__ == '__main__':
    main()
