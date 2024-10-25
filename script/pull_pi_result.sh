# define parameters
USER='yint'
PI = 'rasp-008.berry.scss.tcd.ie'
SRC = '~/captcha_solver/result.csv'
DES = '.'
JUMPER = 'macneill.scss.tcd.ie'

# download file
scp -J $USER@$JUMPER $USER@$PI:$SRC $DST

if [ $? == 0 ]; then
  echo '----download successful----'
else
  echo '----fail to download result file----'
  exit 1
fi