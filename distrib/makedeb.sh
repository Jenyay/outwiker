#!/bin/sh

DIR_NAME="outwiker-0.99.3-1"

outwiker_dir="$DIR_NAME/opt/outwiker/"

if [ -d $outwiker_dir ] ;
then
	rm -r $outwiker_dir
fi

mkdir $outwiker_dir

# Скопируем нужные файлы из исходников
cp -r "../src/core" $outwiker_dir
cp -r "../src/gui" $outwiker_dir
cp -r "../src/help" $outwiker_dir
cp -r "../src/images" $outwiker_dir
cp -r "../src/libs" $outwiker_dir
cp -r "../src/pages" $outwiker_dir
cp "../src/outwiker.py" $outwiker_dir
cp "../src/copyright" $outwiker_dir
cp "../src/README" $outwiker_dir

# Удалить файлы *.pyc, *.wxg, *.py~, *.wxg~ 
find . -name *.pyc -type f -print | xargs rm 
find . -name *.py~ -type f -print | xargs rm 
find . -name *.wxg -type f -print | xargs rm 
find . -name *.wxg~ -type f -print | xargs rm 

# Создание файла с контрольными суммами 
md5deep -r "$DIR_NAME/opt" > "$DIR_NAME/DEBIAN/md5sums"
md5deep -r "$DIR_NAME/usr" >> "$DIR_NAME/DEBIAN/md5sums"

# Сборка пакета 
fakeroot dpkg-deb --build "$DIR_NAME"
