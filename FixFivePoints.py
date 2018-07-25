import os
import os.path as op
import cv2

fivePoints = []

def update(img,x,y):
	cv2.circle(img,(x,y),3,(0,0,255),-1)
	cv2.imshow("img", img)

def onMouse(event, x, y, flags, param):      #标准鼠标交互函数
	if event==cv2.EVENT_LBUTTONDOWN :           #当鼠标移动时
		fivePoints.append(x)
		fivePoints.append(y)
		update(img,x,y)

for root, dirs, files in os.walk(op.join(os.getcwd(),'lfw_point')):
	txts = []
	for file in files:
		if op.splitext(file)[1] == ".txt":
			txts.append(file)
	
	cv2.namedWindow("img")
	cv2.setMouseCallback("img", onMouse)
	i = 0
	skip = 0
	while 1:
		print("[",i,"/",len(txts),"]\t",txts[i])
		imgName_xx = op.splitext(txts[i])[0];
		imgName = imgName_xx[:-5]
		
		imgPath = op.join(os.getcwd(),'lfw',imgName,imgName_xx+'.jpg')
		img = cv2.imread(imgPath);
		txtfile = op.join(os.getcwd(),'lfw_point',txts[i])
		f = open(txtfile, 'r')
		lines = f.readlines()
		f.close()
		for line in lines:
			center = line.split(',')
			cv2.circle(img, (int(float(center[0])), int(float(center[1]))), 3, (0, 255, 0), -1)
		
		#cv2.namedWindow(txts[i])
		#cv2.moveWindow(txts[i],1000,500)
		#cv2.setMouseCallback(txts[i], onMouse)
		#cv2.imshow(txts[i], img)
		cv2.imshow("img", img)
		key = cv2.waitKey()
		#cv2.destroyWindow(txts[i])
		if (key == 97 or key == 100) and len(fivePoints) == 10:
			print(imgName_xx,".txt ","fixed.")
			f = open(txtfile, 'w')
			for point in range(5):
				f.write(str(fivePoints[point*2]) + "," + str(fivePoints[point*2 + 1]) + "\n")
			f.close()
		
		if key == 97 and i > 0:
			i -= 1
		if key == 100 and i < len(txts) - 1:
			i += 1
			
		if key == 106 and i > 99:
			i -= 100
		if key == 108 and i < len(txts) - 100:
			i += 100
		
		if key > 47 and key < 58:
			skip *= 10
			skip += key - 48
		if skip <= len(txts):
			if key == 13 and skip > 0:
				i = skip - 1
				skip = 0
		else:
			skip = 0
		fivePoints = []
		if key == 27:
			break;
