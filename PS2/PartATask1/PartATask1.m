calib = imread('Calib3.png');
template = imread('Template.png');
fp =  detectCheckerboardPoints(template); % -> moving points - detectcheckerboardpoitns(template)
mp = detectCheckerboardPoints('Calib3.png'); %-> fixed points - detectcheckerboardpoints(distorted)
t = cp2tform(mp, fp, 'projective');
k = imtransform(calib, t) %where I is the new image
%convert to grayscale
img_bw = rgb2gray(k);

K = fspecial('gaussian');

%blur the image
igf = imfilter(img_bw, K);
igf = imfilter(igf, K);
igf = imfilter(igf, K);


%use sobel edge detector
BW1 = edge(img_bw,'canny');

%perform hough transform
[H, T, R] = hough(BW1);

% Get N candidates
N = 10;
P = houghpeaks(H, N);
%Get hough line parameters
lines = houghlines(igf, T, R, P);
%Show lines over original image
figure;
%show original image
subplot(2,1,1);
imshow(k);
title('cool shit');
hold on;

% Overlay detected lines - this code copied from 'doc houghlines'
for k = 1:length(lines)
   xy = [lines(k).point1; lines(k).point2];
   plot(xy(:,1), xy(:,2), 'LineWidth', 2, 'Color', 'blue');

   % Plot beginnings and ends of lines
   plot(xy(1,1), xy(1,2), 'x', 'LineWidth', 2, 'Color', 'yellow');
   plot(xy(2,1), xy(2,2), 'x', 'LineWidth', 2, 'Color', 'red');
end
% Show Hough Space
subplot(2, 1, 2);
imshow(imadjust(mat2gray(H)), 'XData', T, 'YData', R, 'InitialMagnification', 'fit');
title('Hough Line Transform');
xlabel('\theta');
ylabel('\rho');
axis on;
axis normal;
grid on;
hold on;

% Display as colormap
colormap('jet');

%mp -> moving points - detectcheckerboardpoitns(template)
%fp -> fixed points - detectcheckerboardpoints(distorted)
%t = cp2tform(mp, fp, projective)
%k = transform(I, t) where I is the new image
%imshow(k)
