% function predicted_categories = boosting(train_image_feats, train_labels, test_image_feats)
% % Split the dataset into training and validation sets
%     train_fraction = 0.7;
%     num_test = size(test_image_feats, 1);
%     categories = unique(train_labels);
%     num_categories = numel(categories);
% 
%     train_idx = [];
%     val_idx = [];
% 
%     for i = 1:num_categories
%         indices = find(strcmp(train_labels, categories(i)));
%         rand_idx = randperm(numel(indices));
%         res = indices(rand_idx(1:floor(numel(indices)*train_fraction)));
%         train_idx = [train_idx; res'];
%         val_idx = [val_idx, setdiff(indices, train_idx)];
%     end
%     train_idx = reshape(train_idx, [], 1);
%     val_idx = reshape(val_idx, [], 1);
% 
%     train_feats = train_image_feats(train_idx, :);
%     train_labels_ = train_labels(train_idx);
%     val_feats = train_image_feats(val_idx, :);
%     val_labels = train_labels(val_idx);
% 
% 
%     % Scores
%     scores = zeros(num_categories, size(val_feats, 1));
% 
%     for i = 1:num_categories
%         y = double(strcmp(train_labels_, categories{i}));
% 
%         % for each lable in the train label
%         for j = 1:size(train_labels_, 1)
%             % check to see if it's a match (1 or 0)
%             if y(j) == 0
%                 % change the 0 to a -1
%                 y(j) = -1;
%             end
%         end
%         
%         
%         % Train a gradient boosting classifier on the training set
%         num_trees = 50; % number of trees in the ensemble
%         classifier = fitensemble(train_feats, y, 'AdaBoostM1', num_trees, 'Tree');
% 
%         scores(i,:) = predict(classifier, val_feats);
% 
%     end
%     
%     
%     
% 
%     % Compute accuracy
%     accuracy = sum(train_idx == val_labels) / numel(val_labels);
%     fprintf('Test accuracy: %.2f%%\n', accuracy * 100);
%     
%     % Evaluate the classifier on the test set
%     predicted_categories = predict(classifier, test_image_feats');
% end

















function predicted_categories = boosting(train_image_feats, train_labels, test_image_feats)
% Split the dataset into training and validation sets
%     train_fraction = 0.7;
%     categories = unique(train_labels);
%     num_categories = numel(categories);
% 
%     train_idx = [];
%     val_idx = [];
% 
%     for i = 1:num_categories
%         indices = find(strcmp(train_labels, categories(i)));
%         rand_idx = randperm(numel(indices));
%         res = indices(rand_idx(1:floor(numel(indices)*train_fraction)));
%         train_idx = [train_idx; res'];
%         val_idx = [val_idx, setdiff(indices, train_idx)];
%     end
%     train_idx = reshape(train_idx, [], 1);
%     val_idx = reshape(val_idx, [], 1);
% 
%     train_feats = train_image_feats(train_idx, :);
%     train_labels_ = train_labels(train_idx);
%     val_feats = train_image_feats(val_idx, :);
%     val_labels = train_labels(val_idx);
% Example data: a 1500x10500 cell array
data = train_image_feats;  % Your data goes here

% Normalize each row
normalized_data = zeros(size(data));
for i = 1:size(data, 1)
    row = data(i, :);
%     row_numeric = cell2mat(row);  % Convert the cell array row to numeric values
    row_normalized = row / sum(row);  % Normalize the row
    normalized_data(i,:) = row_normalized;  % Convert back to cell array format
end 
    % Train a gradient boosting classifier on the training set
    num_trees = 200; % number of trees in the ensemble
    classifier = fitensemble(normalized_data, train_labels, 'Subspace', 5000, 'KNN');

%     res1 = predict(classifier, test_image_feats);
%     
%     
%     
% 
%     % Compute accuracy
%     accuracy = sum(train_idx == val_labels) / numel(val_labels);
%     fprintf('Test accuracy: %.2f%%\n', accuracy * 100);
    
    % Evaluate the classifier on the test set
    predicted_categories = predict(classifier, test_image_feats);
end
