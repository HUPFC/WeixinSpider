#!/bin/bash
#----------------------------------
#
#  Crontab统一入口，自动进行进程检测，防止相同进程多次出现;
#
#----------------------------------

echo "---- Start Crontab_DB Shell V1.0 ----"
#PHP执行路径
PHPCMD=php
#PHP执行入口脚本
PHPDIR=yii
#PHP执行日志
CRONLOGDIR=/logs/
CRONLOG=$CRONLOGDIR$1$(date +%Y_%m_%d)".log"

#判断日志目录是否存在
if [ ! -d "$CRONLOGDIR" ];then
        mkdir $CRONLOGDIR
fi

#判断是否有执行的脚本，如果没有执行，进行执行操作
RunProcess=`ps -ef |grep "$1"|grep -v "grep"|grep -v "Shell"|grep -v "tail"`
echo $RunProcess
if [  -z "$RunProcess" ] ; then
        nohup  $PHPCMD  $PHPDIR $1 >> $CRONLOG 2>&1 &
else
        echo "$1 process is running & exit."
fi

echo "---- End Crontab_DB Shell V1.0 ----"
exit
