read -p "Введите число: " number
if (( $number > 0 ))
then
echo "Number $number is positive"

elif (( $number < 0 ))
then
echo "Number $number is negative"

elif (( $number == 0 ))
then
echo "Number $number is null"

else
echo "Number $number is not a number"

fi;