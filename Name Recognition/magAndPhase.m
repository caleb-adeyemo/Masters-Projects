function [shortTimeMag, shortTimePhase] = magAndPhase(speechFrame)
speechFrameSize = size(speechFrame);

    w = hamming(speechFrameSize(1));
    v = w .* speechFrame;
    y = fft(v);
    shortTimeMag = abs(y);
    shortTimePhase = angle(y);
end 