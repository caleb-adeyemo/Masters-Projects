function predicted_categories = libsvm(train_image_feats, train_labels, test_image_feats)

% sort/get the diff categories
categories = unique(train_labels);

% Number of unique categories
num_cat = length(categories);

% Find the number of images we are working with
num_train = size(train_image_feats, 1);

% value for lamda
lambda = 0.000001;

% Scores
scores = zeros(num_cat,num_cat, num_train);

for i = 1:num_cat
    for j = 1:num_cat
        if i ~= j
            % make a binary classifier... cat i vs cat j
            idx = strcmp(categories{i}, train_labels) | strcmp(categories{j}, train_labels);

            % Get the indexes
            res = [];
            for k = 1:num_train
                if idx(k) == 1
                    res = [res, k];
                end
            end

            res = res';
    
            % create new binary labels
            binary_labels = ones(sum(idx),1);
            binary_labels(strcmp(train_labels(idx), categories{j})) = -1;

            ff = train_image_feats(res,:)';
    
            % Train SVM classifier
            [w, b] = vl_svmtrain(ff, binary_labels, lambda);
    
            % get the weights
            scores(i,j,:) =  w'*test_image_feats' + b;
        end
    end
end
% Find the maximum score for each category pair
[~, max_indices] = max(scores, [], 2);

max_idx = mode(max_indices);

% Map the category pair index to the actual category labels
predicted_categories = categories(max_idx);

end