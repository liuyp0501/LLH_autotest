LO_TIME=`date +%Y%m%d%H%M`
path0=/data/webserver/tiger-shield/WEB-INF/classes
path1=tiger-shield/WEB-INF/classes
path2=/data/webserver/tiger-shield
path3=tiger-shield

function file_do()
{
a=$file
b=$(echo $a|cut -d '/' -f2)
file_dir=$(dirname $a)
echo $b
case $b in
"com")
     file_deal $file_dir $path0 $path1 $a
;;
"vue")
   file_deal $file_dir $path2 $path3 $a
;;
esac
}

function file_deal()
{
    if [ -d $basepath/$3$1 ];then
            cp -rf $2$4 $basepath/$3$1
        else
            echo $basepath/$3$1 not exit,we new add directory!!
            mkdir -p $basepath/$3$1
            cp -rf $2$4 $basepath/$3$1
        fi
}

basepath=$(cd `dirname $0`; pwd)

if [ ! -f $basepath/file_list.txt ]; then
        echo $basepath the file_list.txt file is not exit!!
        exit
fi

cd $path2/..
cp -rf tiger-shield $path2/../backup/tiger-shield$LO_TIME

for line in `cat $basepath/file_list.txt`
do
        echo $line
        file=$line
        file_do $file
done

cd $basepath
mv tiger-shield tiger-shield$LO_TIME


