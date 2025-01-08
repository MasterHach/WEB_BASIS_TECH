echo "Before word changing"

while IFS= read -r line || [ -n "$line" ]; do
echo "$line"
done < "$3"

echo "-------------------"
sed -i "s/\b$1\b/$2/g" "$3"

echo "After word changing"

while IFS= read -r line || [ -n "$line" ]; do
echo "$line"
done < "$3"