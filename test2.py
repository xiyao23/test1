import pypcd
import rospy
from sensor_msgs.msg import PointCloud2


def cb(msg):
    pc = PointCloud2.from_msg(msg)
    pc.save('foo.pcd', compression='binary_compressed')
    # maybe manipulate your pointcloud
    pc.pc_data['x'] *= -1
    outmsg = pc.to_msg()
    # you'll probably need to set the header
    outmsg.header = msg.header
    pub.publish(outmsg)

# ...
sub = rospy.Subscriber('incloud', PointCloud2)
pub = rospy.Publisher('outcloud', PointCloud2, cb)
rospy.init('pypcd_node')
rospy.spin()

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/camera/depth/points', PointCloud2, cb)
    rospy.spin()