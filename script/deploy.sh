# define parameters
USER='yint'
PI = 'rasp-008.berry.scss.tcd.ie'
SRC = 'captcha_solver'
DES = '~/captcha_solver'
MODEL = 'models'
JUMPER = 'macneill.scss.tcd.ie'

# run deployment
# make a new folder for everythin
rm -r $SRC
mkdir -p $SRC
cp -r deploy $SRC
cp -r models $SRC
cp symbols.txt $SRC

# push the folder to remote
#clean
ssh -J $USER@$JUMPER $USER@$PI "rm -r $DST"
#scp
scp -rp -J $USER@$JUMPER $SRC $USER@$PI:$DST

if [ $? == 0 ]; then
  echo '----deployment successful----'
else
  echo '----fail to upload files----'
  exit 1
fi