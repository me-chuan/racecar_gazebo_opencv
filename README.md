Racecar Simulator
=================
Simulates an RC car in the MIT tunnel.

1. Run "roslaunch racecar_gazebo racecar.launch" or "roslaunch racecar_gazebo racecar_tunnel.launch"

--- 

*modified by me-chuan(Chen Weihan) for 工科创 ROS 大作业*
*My email address: lemonchuan@sjtu.edu.cn or 3376219114@qq.com*

environment: Ubuntu 20.04, ROS Noetic

prerequisites: 
1. redirect the *python* command to python3
2. install required pip packages
3. also clone mit racecar package alongside this pkg into your workspace(the launch file need this pkg)
4. If you want to run controller.py function, make sure you are using gnome-terminal(the default terminal of Ubuntu), and install wmctrl and tmux correctly.(if you still cannot run this program, please contact me and reflect your problem or give a pullrequest )

**Reminder**: Technically, controller.py is only a python script. It cannot be run by rosrun. You should cd into scripts directory and type:

    python3 controller.py

and a terminal should pop out prompting you to type command.

---

## demo

Here is an example for how to clone this repo and run my program.

build your workspace and clone this repo alongside mit racecar pkg

    mkdir -p demo_ws/src
    cd demo_ws/src
    git clone https://github.com/me-chuan/racecar_gazebo_opencv.git
    git clone https://github.com/mit-racecar/racecar.git
    cd ~/demo_ws
    rosdep install --from-paths src --ignore-src -r -y
    catkin_make

run it!

    source devel/setup.bash
    roslaunch racecar_gazebo racecar_curve.launch
    rosrun racecar_control autoparking.py

or type command below to change into aid-driving mode

    python3 controller.py

If you encounter any errors or bugs, please let me know.

### FAQs:

to be continued...