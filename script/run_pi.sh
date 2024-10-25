# define parameters
USER='yint'
PI = 'rasp-008.berry.scss.tcd.ie'
JUMPER = 'macneill.scss.tcd.ie'

# run remote classification
ssh -J $USER@$JUMPER $USER@$PI "cd ~/captcha_solver/deploy"
ssh -J $USER@$JUMPER $USER@$PI "./run.sh"