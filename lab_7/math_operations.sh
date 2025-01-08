read -p "Введите frist число: " num1

read -p "Введите second число: " num2

read -p "Введите operation: " oper

add() {
  echo "Результат сложения: $(($1 + $2))"
}

subtract() {
  echo "Результат вычитания: $(($1 - $2))"
}

multiply() {
  echo "Результат умножения: $(($1 * $2))"
}

divide() {
    if (($2 != 0)) 
    then
        echo "Результат целочисленного деления: $(($1 / $2))"
    else
        echo "Number $2 is null, cant divide!"
    fi
}

case $oper in
  +)
    add "$num1" "$num2"
    ;;
  -)
    subtract "$num1" "$num2"
    ;;
  '*')
    multiply "$num1" "$num2"
    ;;
  /)
    divide "$num1" "$num2"
    ;;
  *)
    echo "Неверная операция. Пожалуйста, выберите одну из: +, -, *, /"
    ;;
esac