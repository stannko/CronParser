cron-explain() {
    if [ $# -ne 1 ] ; then
        echo 'Invalid arguments. Try passing cron expression in ""'
    else
        conda activate homework
        script=${HOME}/CronParser/main.py
        PYTHONPATH=${HOME}/CronParser \
        python ${script} --expression="$@"
    fi
}
