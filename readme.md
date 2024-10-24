## steps:
1. In your virtual environment, run pip install -r requirements.txt
2. Generate captcha with your fonts:
   - put your fonts in the train_font folder
   - (optional) put fonts you want to mix(generate in on captcha) in the mix_font folder
   - run on clt: (pls refer to generate.sh)
   ```shell
   python generate.py --font_dir train_font --[max_len(captchas will be 2-max_len length)] --count [font1_generate_number] [font2_generate_number] --output_dir [your_output_data_dir] --symbols symbols.txt --mix_dir mix_font --mix_count [number of mix font generation] --train_ratio [train/val split ratio between 0 and 1]

3. Train yolo model with your generated dataset
   - (optional) you can create a clearml account and run clearml-init in clt to monitor the training in real time,
     Please check https://docs.ultralytics.com/yolov5/tutorials/clearml_logging_integration/#about-clearml
   - run on clt: (pls refer to train.sh)
   ```shell
   python yolo_train.py --model_path yolo11x.pt --data_config_path [your_output_data_dir]/data.yaml --img_size 192 -n [your_train_name] -e [epoch_number] -b [batch_size]
   ```
   - your result will be saved in runs/detect/[your_train_name] folder
   - under the folder, the best performance model will be saved as weights/best.pt
   - when the training is finished, the training loss plot, the confusion matrix, etc. will be saved in the same folder for you to check if the training goes well.

4. Predict the testing captcha images with the trained model, and save the csv file for submitty.
   - run on clt: (pls refer to predict.sh)
   ```shell
   python yolo_predict.py -i [path_to_your_testing_captcha_folder] -m [path_to_your_trained_model] -o [your_output_folder_path] -s symbols.txt -n result.csv --save_plot
   ```
   - add the flag "-save_plot" if you want to save the visualization images of the prediction.
   - your .csv file for submitty will be saved under [your_output_folder_path]
   - remember manually add your shortname to the 1st row of the .csv, and then submit!
   
