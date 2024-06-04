##### Raul Mansurov C2 SERVER #########

### Description of project

The project is contains Command and control server and client project supports command execution,system enumartion,downloading file from client,upload file to server,screenshot taking,running services on the client.These helps us to automate tasks above the client.Project useally is for windows O.S but support MacOS,and Linux,also project contains exe file for windows.My project can bypass specified detection systems(Windows Defender,Antivirus,EDR etc)

### Dependencies

- Python 3.x
- colorama library
- pyautogui library
- requests library
- psutil library
- pyuac library
- pyfiglet
- termcolor
- cryptography

If you want to utilize this library, you can install the required libraries with using pip command:
pip install requests colorama pyautogui pyuac psutil pyfiglet termcolor crytography

### Instructions for running the script

If you want to run exe file you can do it with double click in Windows,If you want to watch my decryption algoritm you can see decrypt.py --> c2_decrypt.py,My project contains 4 file command_control_server.py,command_control_client.py,exe file for windows os,c2_decrypt.py,README.md and finally requirements.txt
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
You must run before server for receive the connection

You can run my python script:
    python <server.py>
    python <client.py>

