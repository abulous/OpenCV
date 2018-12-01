import os
import cv2
import numpy as np
import torch
from torch.autograd import Variable

from net import Net
from option import Options
import utils
from utils import StyleLoader


def run_demo(args, mirror=False):
	style_model = Net(ngf=args.ngf)
	input('style_model =')
	style_model.load_state_dict(torch.load(args.model))
	input('style_model.load')
	style_model.eval()
	if args.cuda:
		style_loader = StyleLoader(args.style_folder, args.style_size)
		style_model.cuda()
	else:
		style_loader = StyleLoader(args.style_folder, args.style_size, False)
	# Define the codec and create VideoWriter object
	height =  480 
	width = 640 
	fps = 24

#	cam = cv2.VideoCapture(0)
#	cam.set(3, width)
#	cam.set(4, height)

	video = cv2.VideoCapture('tvMesh2.mp4')
	video.set(3, width)
	video.set(4, height)
	video.set(5,fps)
#	print(video.get(5))
	
	if args.record:
		fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
		out = cv2.VideoWriter('breakWhiteConv.mov', fourcc, 24, (640, 480), True)

	key = 0
	idx = 0
	counter = 1

	while True:
		# read frame
		idx += 1
		ret_val, frame = video.read()
	#	ret_val, frame = cam.read()
				
		counter += 1
		
		if counter == video.get(7):
			video.set(1, 0)
			counter = 0

		img = np.array(frame).transpose(2, 0, 1)
		# changing style 
		if idx%20 == 1:
			style_v = style_loader.get(int(idx/20))
			style_v = Variable(style_v.data)
			style_model.setTarget(style_v)

		img=torch.from_numpy(img).unsqueeze(0).float()
		if args.cuda:
			img=img.cuda()

		img = Variable(img)
		img = style_model(img)

		if args.cuda:
		#	simg = style_v.cpu().data[0].numpy()
			img = img.cpu().clamp(0, 255).data[0].numpy()
		else:
		#	simg = style_v.data().numpy()
			img = img.clamp(0, 255).data[0].numpy()
		img = img.transpose(1, 2, 0).astype('uint8')

		# display
#		simg = cv2.resize(simg,(swidth, sheight), interpolation = cv2.INTER_CUBIC)
#		cimg[0:sheight,0:swidth,:]=simg
#		fimg = np.concatenate((cimg,img),axis=1)

		if args.record:
			out.write(img)
		
		cv2.imshow('MSG Demo',img)

		#cv2.imwrite('stylized/%i.jpg'%idx,img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cam.release()
	if args.record:
		out.release()
	cv2.destroyAllWindows()

def main():
	# getting things ready
	args = Options().parse()
	if args.subcommand is None:
		raise ValueError("ERROR: specify the experiment type")
	if args.cuda and not torch.cuda.is_available():
		raise ValueError("ERROR: cuda is not available, try running on CPU")

	# run demo
	run_demo(args, mirror=True)

if __name__ == '__main__':
	main()
