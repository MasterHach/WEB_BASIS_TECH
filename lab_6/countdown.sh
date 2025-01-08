read -p "Введите число: " number
while [ $number -ge 0 ] 
do
echo $number
number=$((number - 1))
done