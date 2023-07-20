function [predicted_categories] = knn_classifier(k,train_image_feat, train_label, test_image_feat)
%KNN_CLASSIFIER

distances = pdist2(test_image_feat, train_image_feat, "cityblock");

% Working
[~, indices] = sort(distances, 2);
k_nearest_indicies = indices(:,1:k);

% Make the size of the prediction category result
predicted_categories = cell(size(train_image_feat, 1),1);
for i = 1:size(train_image_feat, 1)
    nearest_labels = train_label(k_nearest_indicies(i, :));

    % Use histcounts to count the number of occurrences of each element in the array
    [counts, ~] = histcounts(str2double(nearest_labels));

    % Find the strings that occur more than once
    if any(counts >= 2)
        predicted_categories{i} = char(mode(str2double(nearest_labels)));
    else
        predicted_categories{i} = char(nearest_labels(1));
    end

end

end