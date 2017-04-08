# Garnet Auto Check In with Selenium
This script launches a Firefox Browser, logs you into Garnet, and clicks on the attendance button. Used in conjunction with a cronjob, it can help prevent you from forgetting to sign in.

**Click here to see how it works:** https://www.youtube.com/watch?v=6g_GC0GYklw

**A few caveats before continuing:**

•	Using this script is free, and if you choose to use it then you are accepting it as is. If you find a bug and would like to fix it or would like to contribute a new feature, please do so through GitHub.

•	If there are any changes to your General Assembly campus’s IP Address, you will need to reconfigure the script to add the new IP address.

•	If there are any changes to how we sign into Garnet, the script will not work.

•	If your Mac is off or is in sleep mode when the cronjob is supposed to run, then the script will not execute. Make sure your Mac has enough power, and you can adjust the sleep settings under System Preferences > Energy Saver.

•	Closing your laptop will put your Mac to sleep regardless of your sleep settings. Make sure when you get to class to open and sign into your laptop. It is OK if your display goes to sleep, as long as the computer itself is not asleep.

•	You will have to plug in your Github credentials into this script. If you are uncomfortable doing that or have access to private repos then this script may not be for you.

•	When you first configure this script/cronjob you should test it after you have signed into Garnet to confirm that it has been configured correctly. The script will execute the exact same way, but will not click the sign in button because it had already been clicked for that day.

**Prerequisites:**

•	Python 2.7 - https://www.continuum.io/downloads

•	Mozilla Firefox - https://www.mozilla.org

•	Homebrew - https://brew.sh/

**Set Up:**
**Installing Selenium and Geckodriver:**

1.	Go to your terminal and enter ```pip install selenium```.

2.	Enter ```brew install geckodriver``` into the terminal.

**Configuring the Script:**

3.	Download the script from my repo, and place it in a folder.

4.	Open the script with a text editor and enter the appropriate values for the following variables:

```
config_ip = #Your General Assembly Campus's IP Address
config_username = #Your Github Username
config_password = #Your Github Password
config_link_text = #Your course title in Garnet
```

You can get your campuses IP address by going to campus and Googling “my ip address”. Your Garnet course title is located under Cohort Name when you sign into garnet.

![course name](https://brendanbailey.github.io/Blog/GASignin/course_name.png)

**Creating the Cronjob:**

5.	Enter ```env``` and copy the PATH variable.

6.	Enter ``` env EDITOR=nano crontab –e```

7.	Paste the PATH variable into the terminal.

8.	Hit return and enter the cronjob. My cronjob looks like this ```55 8 * * 1-5 cd desktop/programming/github/brendanbailey.github.io/blog/gasignin && python ./garnet_auto_checkin_github.py```. This tells the cronjob to run the script ever weekday at 8:55am. You can copy and paste this into your cronjob directly but make sure that your change directory points to the folder that contains the script that you downloaded. Make sure that your laptop is on and open by 8:55 if you use this setting.

9.	Hit control X and enter Y. This saves the cronjob.
