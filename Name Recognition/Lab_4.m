% Get audio
[x,fs] = audioread("Darcy.wav");

%Get samples
audioLength = length(x);
frameLength = 320;
numframes = floor(audioLength/frameLength);
% Split Audio 
% frameBin = linspace(0, audioLength, numframes);
index = 1;
fbankRes = zeros(259,10); 
% Loop 259 Times
start = 1;
last = 320;
for frame = 1 : numframes -1
    % Section of main Audio
    shortTimeFrame = x(start:last); % Slice of main audio
    % Get Magnitude spec of Slice
    [m, ~]= magAndPhase(shortTimeFrame);
    %FilterBank
    fbankRes(frame,:) = linearRectangularFilterbank(m, 10);
    %Log
    yz = log(fbankRes);
    
    %DCT
    z = dct(yz);
    
    index = index + 1;
    start = last;
    last = last + frameLength;
%     plot(m);
end

%Write .mfc file
    % Open file for writing:
    fid = fopen("Darcy.mfc", 'w', 'ieee-be');
    % Write the header information%
    fwrite(fid, 258, 'int32'); % number of vectors in file (4 byte int)
    fwrite(fid, 200000, 'int32'); % sample period in 100ns units (4 byte int)
    fwrite(fid, 10 * 4, 'int16'); % number of bytes per vector (2 byte int)
    fwrite(fid, 6, 'int16'); % code for the sample kind (2 byte int)
    % Write the data: one coefficient at a time:
    for id = 0: 258
        for j = 1:10
            fwrite(fid, fbankRes(id+1,j), 'float32');
        end
    end




subplot(2,1,1), plot(m)
% subplot(2,1,2), plot(fbank)