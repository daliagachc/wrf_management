#!/usr/bin/env bash

mount_dir='/tmp/wrf_management/data_folder'
remote_dir='/wrk/aliagadi/DONOTREMOVE/wrf_management_data'
log_addr='aliagadi@taito-login3.csc.fi'
mkdir -p $mount_dir
umount -f $mount_dir
echo 'cont'
sshfs -oreconnect $log_addr:$remote_dir $mount_dir

mount_dir='/tmp/wrf_management/db_folder'
remote_dir='/homeappl/home/aliagadi/saltena_2018/wrf_management/wrf_management/db_folder'
log_addr='aliagadi@taito-login3.csc.fi'
mkdir -p $mount_dir
umount -f $mount_dir
sshfs -oreconnect $log_addr:$remote_dir $mount_dir

