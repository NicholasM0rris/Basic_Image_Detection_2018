%Read in the templace and calibration images
calib = imread('Calib1.png');
template = imread('Template.png');
%find checkerboard points
fp =  detectCheckerboardPoints(template); % -> moving points - detectcheckerboardpoitns(template)
mp = detectCheckerboardPoints('Calib1.png'); %-> fixed points - detectcheckerboardpoints(distorted)
%Transform the image
t = cp2tform(mp, fp, 'projective');
k = imtransform(calib, t) %where I is the new image
%Show and save the image 
imshow(k)
imwrite(k, 'topdown.png')