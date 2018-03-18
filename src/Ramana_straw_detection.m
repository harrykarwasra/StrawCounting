clc;
clear all;
close all;

img_rgb = imread('Input\straws0.jpg');
imshow(img_rgb);
title('Original');

img_g = rgb2gray(img_rgb);
figure, imshow(img_g);
title('Gray');

se = strel('square',40);
img_contrast = imadjust(img_g, [0 1], [0 0.75]);%imtophat(img_g, se);
figure, imshow(img_contrast);
title('Contrast');
%{
img_contrast_bw = ~im2bw(img_g);
figure, imshow(img_contrast_bw);
title('Contrast B/W');
%}
img_canny = edge(img_contrast, 'canny');
figure, imshow(img_canny);
title('Canny edge');

pixelCutoffLen = 15;
img_canny_reduced = bwareaopen(img_canny, pixelCutoffLen);
figure, imshow(img_canny_reduced);
title('Canny reduced');

img_bound = bwboundaries(img_canny_reduced);
figure, imshow(img_rgb);
text(10,10,strcat('\color{green}Objects Found:',num2str(length(img_bound))));
hold on;

for k = 1:length(img_bound)
boundary = img_bound{k};
plot(boundary(:,2), boundary(:,1), 'g', 'LineWidth', 0.2)
end

