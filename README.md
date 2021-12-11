# FRA502_6261

### Devoloper
Mr.Chanon Khumwilaisak
ID:62340500061
Frab#6

### Video Link
https://drive.google.com/drive/u/1/folders/1M6r7F0O9eg6egpwt3ITbq2k8ZpgL620z

### Require Package
- teleop-twist-keyboard
- ros-control
- Gmapping
- map-server
- amcl
- movebase
- actionlib
- pyaudio
- SpeechRecognition

### Command
1. [new terminal]
- roscore

2. [new terminal]
- source catkin_ws/devel/setup.bash
- roslaunch my_robot run.launch

3. [new terminal]
- source catkin_ws/devel/setup.bash
- roslaunch my_robot navigation.launch

4. [new terminal]
- source catkin_ws/devel/setup.bash
- roslaunch my_robot goal.launch

* รูปแบบคำสั่ง *
เมื่อระบบขึ้นสถานะ "Ready for command"
สามารถพูดได้ 4 อย่าง //ตาม Update ล่าสุด
1. "ไปหยิบน้ำเกลือ"
2. "ไปหยิบสำลี"
3. "ไปหยิบยา"
4. "ไปหยิบแอลกอฮอล์"
