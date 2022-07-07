tit = 'map_100_100';

img = imread(strcat(tit, '.png'));
imggray = rgb2gray(img);
figure
surf(imggray)
set(gca, 'XDir','reverse')

costmap = double(255-imggray);
costmap = ceil(costmap/64);
costmap = floor((10*ones(size(costmap))).^(costmap-1));
figure
surf(costmap)
set(gca, 'XDir','reverse')

writematrix(costmap, strcat(tit, ".txt"))