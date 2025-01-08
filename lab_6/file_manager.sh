DIR_NAME=$1
mkdir "$DIR_NAME"

touch file_1.txt file_2.txt

echo "files were created"

rm file_1.txt file_2.txt

echo "files were deleted"

cd ..