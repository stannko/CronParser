cron-explain() {
    if [ $# -ne 1 ] ; then
        echo 'Invalid arguments. Try passing cron expression in ""'
    else
        conda activate ${CONDA_DEFAULT_ENV}
        script=${HOME}/CronParser/main.py
        PYTHONPATH=${HOME}/CronParser \
        python ${script} --expression="$@"
	fi
}
