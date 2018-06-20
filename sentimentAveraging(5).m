
file = fopen('C:\Users\Student\Desktop\Comment_sentiment\sentimentsAndTime.txt');
threeCols = textscan(file,'%f%f%f%f','Delimiter',' :'); %check for empty cells with 'isEmpty'
scores= threeCols{1};
times  = (threeCols{2}.*100)+threeCols{3}; %convert the time into an integer for simplicities sake

scoresWithTime = [scores,times];
sumsAndAmounts = zeros(2,24);
commentAmount = length(scores(:,1));
for i = 1:1:commentAmount
    %add in the comment score to the correct slot
    slot = floor((scoresWithTime(i,2))/100)+1;
    sumsAndAmounts(1,slot) = sumsAndAmounts(1,slot) + scoresWithTime(i,1);
    %tick up its counter
    sumsAndAmounts(2,slot) = sumsAndAmounts(2,slot)+1;
end

averagesPerHour = sumsAndAmounts(1,:)./sumsAndAmounts(2,:);
plot(averagesPerHour);
axis([1 24 0.05 0.15]);

for col=1:1:24
    fprintf('For the %d hour, the avg sentiment is %f \n',col,averagesPerHour(col));
end






