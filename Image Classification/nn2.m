function [predictions] = nn2(train_image_feats, test_image_feats, batch_size, learning_rate, epoch)
% Train data DataStore
trainData = imageDatastore(train_image_feats);
trainData.Labels = categorical(train_labels_);
% Validate data DataStore
validateData = imageDatastore(val_feats);
validateData.Labels = categorical(val_labels);
% Test data DataStore
testData = imageDatastore(test_image_feats);

numFilters=75;
layers = [
    % image input layer whose input size is 32-32-1. "3" represents one
    % color channel (RGB image)
    imageInputLayer([32 32 3]) 
    % convolutional layer whose filter size is 3 by 3 
    convolution2dLayer(3,numFilters,'Padding','same')
%     % batch normalization layer
%     batchNormalizationLayer
    % activation layer (relu)
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,numFilters*2,'Padding','same')
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,numFilters*4,'Padding','same')
    batchNormalizationLayer
    reluLayer
    fullyConnectedLayer(1000)
    fullyConnectedLayer(500)
    fullyConnectedLayer(100)
    fullyConnectedLayer(15)
    softmaxLayer
    classificationLayer];

% Set up the training options
options = trainingOptions('adam', ...
    'MiniBatchSize',batch_size, ...
    'MaxEpochs',epoch, ...
    'InitialLearnRate',learning_rate, ...
    'Shuffle','every-epoch', ...
    'L2Regularization',0.01, ...
    'Verbose',false, ...
    'Plots','training-progress',...
    'ValidationData',{val_feats, val_labels});


% Train the network
net = trainNetwork(trainData, layers, options);

% Evaluate the trained network
predictions = classify(net, testData);
predictions = cellstr(predictions);
% Compute accuracy
% accuracy = sum(predictions == trainLabels) / numel(trainLabels);
% fprintf('Test accuracy: %.2f%%\n', accuracy * 100);


% % % % ----------- Vary:- Batch size, learing rate, losses

end








