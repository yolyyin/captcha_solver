SECONDS=0

cd ~/captcha_solver
source catcha_env/bin/activate
cd ~/captcha_solver/deploy
python classify.py -i ~/captchas -m ~/captcha_solver/models/best.onnx -o ~/captchas_predict -s ~/captcha_solver/symbols.txt
sed -i "1 i\\$(whoami)" ~/captchas_predict/result.csv
RUN_TIME=$SECONDS
echo "-----run time: ${RUN_TIME}s-----"
deactivate