#!/bin/sh

DIR_NAME="outwiker-1.4.0-1"

outwiker_dir="$DIR_NAME/usr/share/outwiker/"

if [ -d $outwiker_dir ] ;
then
	rm -r $outwiker_dir
fi

mkdir $outwiker_dir

# Скопируем нужные файлы из исходников
cp -r "../src/outwiker" $outwiker_dir
cp -r "../src/help" $outwiker_dir
cp -r "../src/images" $outwiker_dir
cp -r "../src/locale" $outwiker_dir
cp -r "../src/plugins" $outwiker_dir
cp -r "../src/templates" $outwiker_dir
cp "../src/runoutwiker.py" $outwiker_dir
cp "../copyright" $outwiker_dir
cp "../README" $outwiker_dir
cp "../src/version.txt" $outwiker_dir

# Удалить файлы *.pyc, *.wxg, *.py~, *.wxg~ 
find . -name *.pyc -type f -print | xargs rm 
find . -name *.py~ -type f -print | xargs rm 
find . -name *.wxg -type f -print | xargs rm 
find . -name *.wxg~ -type f -print | xargs rm 
find . -name *.~1~ -type f -print | xargs rm 

# Создание файла с контрольными суммами 
md5deep -r "$DIR_NAME/usr" > "$DIR_NAME/DEBIAN/md5sums"

# Сборка пакета 
fakeroot dpkg-deb --build "$DIR_NAME"

# Установим пакет
sudo dpkg -i "$DIR_NAME.deb"
