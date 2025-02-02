# Rpi_pager
этот проект состоит из нескольких частей. 
1 - Телеграмм бот
2 - raspberry pi (zero w) с e-Paper дисплеем 2.13inch (чернильный)
Работает следующим образом. 
пользователь отправляет сообщение на тг бота, после имя пользователя(который отправил сообщение), сообщение отображается на дисплее 

# install 

python3 -m venv myenv

source myenv/bin/activate

pip install -r requirements.txt (bla-bla-bla)

# how to use

source myenv/bin/activate

python main.py

# Or
 mv bot.service /etc/systemd/system
 
 sudo systemctl daemon-reload
 
 sudo systemctl start bot.service
 
 sudo systemctl enable bot.service
 (add autostart)
