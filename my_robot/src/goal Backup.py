#!/usr/bin/env python

import rospy
import pyaudio
import time
import speech_recognition as sr

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

r = sr.Recognizer()
bot_State = 3

Room_Keyword = {
		 "ห้อง 1" : "room_1",
		 "ห้อง 2" : "room_2",
		 "ห้อง 3" : "room_3",
		 "ห้อง 4" : "room_4",
		}
		
Room_Goal =	{
		 "room_1" : [],
		 "room_2" : [],
		 "room_3" : [],
		 "room_4" : [],
		}

KeyWord = {"ไปหยิบ":"pick",
            "ไปหยิบสำลี":"pick_cotton",
            "ไปหยิบน้ำเกลือ":"pick_saline",
            "ไปหยิบยา ":"pick_medecine",
            "ไปหยิบแอลกอฮอล์":"pick_alcohol",         
            }

Goal = {"pick_alcohol":[5.89,1.31,1.57,0],
        "pick_cotton":[5.89,1.31,1.57,0],
        "pick_medecine":[7.78,1.31,1.57,0],
        "pick_saline":[9.6,1.31,1.57,0],
        
        "Standby_Station":[-6.54,0.55,-1.63,0]}




def movebase_client(map_odom_desire):

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = map_odom_desire[0]
    goal.target_pose.pose.position.y = map_odom_desire[1]

    goal.target_pose.pose.orientation.z = map_odom_desire[2]
    goal.target_pose.pose.orientation.w = map_odom_desire[3]

   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()   

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        
        while 1:
            try:
                rospy.loginfo("Test Microphone : Please Say Something")
                with sr.Microphone() as source:
                    audio = r.listen(source)
                    word = r.recognize_google(audio,language='th')
                    rospy.loginfo("Microphone Status : OK")
                    break

            except:
                rospy.loginfo("Test Microphone : Please Say Something")



        while 1:
            if (bot_State == 0):
               rospy.loginfo("Ready for Command")
               bot_State = 1

            elif (bot_State == 1):  
                try:
                    with sr.Microphone() as source:                
                        audio = r.listen(source)
                        word = r.recognize_google(audio,language='th')
                        try:
                            rospy.loginfo("Going to . . . " + KeyWord[word])
                            result = movebase_client(Goal[KeyWord[word]])
                            if result:
                                rospy.loginfo("Arrive at desired room")
                                bot_State = 2
                        except:
                            rospy.loginfo("Can't decode your voice, pls say again pls")
                            rospy.loginfo("Command Example : ไปหยิบ")
                            pass

                except:
                    pass

            elif (bot_State == 2):  
                rospy.loginfo("Wait for interaction . . .")
                time.sleep(10)
                rospy.loginfo("Back to Standby-Station")
                bot_State = 3
            
            elif (bot_State == 3):
                rospy.loginfo("Going to . . . Standby_Station")
                result = movebase_client(Goal["Standby_Station"])
                if result:
                    rospy.loginfo("Arrive at the Standby-Station")
                    bot_State = 0
            
            elif (bot_State == 4):  
                try:
                    with sr.Microphone() as source:                
                        audio = r.listen(source)
                        word = r.recognize_google(audio,language='th')
                        try:
                            rospy.loginfo("Going to . . . " + Room_KeyWord[word])
                            result = movebase_client(Room_Goal[Room_KeyWord[word]])
                            if result:
                                rospy.loginfo("Arrive at desired room")
                                cafebot_state = 2
                        except:
                            rospy.loginfo("Can't decode your voice, Please say it again")
                            rospy.loginfo("Command Example : ห้อง 1")
                            pass

                except:
                    pass
            




    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
