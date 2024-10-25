SECONDS=0

python classify.py -i ~/captchas -m ~/captcha_solver/models/best.onnx -o ~/captchas_predict -s ~/captcha_solver/symbols.txt

RUN_TIME=$SECONDS
echo "-----run time: ${RUN_TIME}s-----"