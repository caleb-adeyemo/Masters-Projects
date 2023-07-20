function [res] =  linearRectangularFilterbank(magSpecVec, noChannel)
    i = 1;
    %linspace
    start =1;
    last = 32;
    fbanks = zeros(1,noChannel); 
    for n = 0 : noChannel-1
      fbanks(1,i) = sum(magSpecVec(start:last));
      i = i+ 1;
      start = last;
      last = last + 32;
    end
    res = fbanks;
end