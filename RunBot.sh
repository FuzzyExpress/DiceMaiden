rm nohup.out
nohup bundle exec ruby dice_maiden.rb 0 lite &
nohup python3 diceImageDaemon.py &


while : 
do
    sleep 5
done