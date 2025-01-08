if [ ! -d "$1" ]; then
  mkdir -p "$1"
fi

cd "$2"
ls
cd ..

current_date=$(date +%Y-%m-%d)

for file in "$2"/*; do
  if [ -f "$file" ]; then
    filename=$(basename "$file")
    cp "$file" "$1/${filename%.*}_$current_date.${filename##*.}"
  fi
done

cd "$1"
ls