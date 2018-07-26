SLEEP_ECHO=2
SLEEP_COMMAND=4
SLEEP_END=20
echo "# This is a tutorial of toomanyfiles"
sleep $SLEEP_ECHO
echo "# We are going to create an example subdirectory to learn it's use"
sleep $SLEEP_ECHO
echo
echo "toomanyfiles --create_example"
toomanyfiles --create_example
sleep $SLEEP_COMMAND

echo 
echo "# We are going to see the 10 last files, for example"
sleep $SLEEP_ECHO
echo "ls -la example| tail -n 10"
ls -la example| tail -n 10
sleep $SLEEP_COMMAND

echo
echo "# We can see files with the temporal pattern YYYYmmdd HHMM"
sleep $SLEEP_ECHO
echo "# We use to find this files in automatic backups, logs, ..."
sleep $SLEEP_ECHO
echo "# Our hard disk it's almost full, so we want to keep some of them"
sleep $SLEEP_ECHO
echo "# We want to keep the last 5 files because they are too recent"
sleep $SLEEP_ECHO
echo "# We want to keep the first file of each month from the rest of the files until a max number the files of 15."
sleep $SLEEP_ECHO

echo "# We enter in the example directory"
sleep $SLEEP_ECHO
echo "cd example"
cd example
sleep $SLEEP_COMMAND

echo "# We make a simulation"
sleep $SLEEP_ECHO
echo "toomanyfiles --too_young_to_delete 5 --max_files_to_store 15 --pattern '%Y%m%d %H%M' --pretend"
toomanyfiles --too_young_to_delete 5 --max_files_to_store 15 --pattern '%Y%m%d %H%M' --pretend
sleep $SLEEP_COMMAND

echo "# We can analyze the result with the output"
sleep $SLEEP_ECHO
echo "# We like the result, so we can delete the files"
sleep $SLEEP_ECHO

echo "toomanyfiles --too_young_to_delete 5 --max_files_to_store 15 --pattern '%Y%m%d %H%M' --remove"
toomanyfiles --too_young_to_delete 5 --max_files_to_store 15 --pattern '%Y%m%d %H%M' --remove
sleep $SLEEP_COMMAND

echo "# We list the files remaining"
sleep $SLEEP_ECHO
echo "ls -la"
ls -la
sleep $SLEEP_COMMAND

echo "# That's all"
sleep $SLEEP_ECHO

sleep $SLEEP_END