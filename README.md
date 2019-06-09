系统简介：
    该环境感知系统采用RGB相机（480P）与禾赛20线激光雷达（该版本为订制版本）两种传感器，RGB相机识别图像车牌，激光雷达测量与车牌的距离，并将两种传感器收集到的信息进行融合。该系统开发环境是Ubuntu 16系统中安装的ROS kinect版本。本系统分为图像识别节点、激光雷达节点和融合节点三部分，最后的信息通过融合节点发布在/ganzhixinxi话题上，感知得到的信息为（t，x，y）其中t为识别到物体的种类，x为车牌相对激光雷达的x坐标，y为车牌相对激光雷达的y坐标。
 
 实现原理（图像识别xml文件训练）：
    节点采用python语言编写，python需要安装OpenCV库，以及调用ROS系统中的rospy库，其中图像识别利用OenCV图像的Haar算法，为了保证识别率先将得到图片进行二值化处理，车牌普遍为蓝色，所以提取出图像中蓝色部分，再对抓取图像中车牌图片进行正样本采集。完成后再采集不含有车牌的二值化图像作为负样本。最后将得到正、负样本利用OpenCV进行训练，最后得到xml分类文件。
    
正负样本库图片如下（该库在工程库中的sample文件夹内）：
 ![image](https://github.com/NixG96/Environmental-perception/raw/master/Test-image/正负样本.png)
 
实现原理（图像识别xml调用）：
    训练好xml的文件放到catkin_ws工程文件夹下以便图像识别节点调用（若不在该文件夹下可用绝对地址调用xml文件），该文件夹为ROS系统的工作空间，ROS相关工作文件如node、msg都在该文件下，需要用在Ubuntu命令框内运行＄ roscore指令之后再启动ROS节点。具体ROS教程请参考http://wiki.ros.org/cn 。
   
实现原理（信息融合）：   
   本系统信息融合利用的是tanα值进行信息融合，RGB相机与激光雷达位置图如下，RGB相机的可视角度约为70°，所以先将激光雷达所采集的y<0的点云滤掉，剩下的tan值与角度唯一对应。对应后根据别识别物体的高度匹配较为合理点云点z值，再将该点对应的（x,y）值与物体种类t重新组合为新的信息（t，x，y）
    ![image](https://github.com/NixG96/Environmental-perception/raw/master/Test-image/传感器联合标定.png)

ROS节点及话题测试图如下：
![image](https://github.com/NixG96/Environmental-perception/raw/master/Test-image/ROS节点话题.png)

系统运行效果图如下，其中第一列为识别到的物体种类（1为车牌），第二列是车牌相对激光雷达的x坐标，第三列是车牌相对激光雷达的y坐标：
![image](https://github.com/NixG96/Environmental-perception/raw/master/Test-image/测试效果.png)


本系统后期扩展：
    （1）在ROS系统版本由Python2.7改成3.7后，可以改用谷歌的tensorflow object_detection API进行物体识别。
    （2）匹配算法使用的较为简单，后期可以采用矩阵运算进行信息融合。
    
