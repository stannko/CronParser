# CRON expression parser.

### Prerequisites
* [conda](https://www.anaconda.com/download/) - Python platform.
* [Python 3](https://www.python.org/) - Programming language.

### Installing
```shell
conda create -n homework python=3.8
cd
git clone https://github.com/stannko/CronParser.git
```
### Running
```shell
source CronParser/script.sh
cron-explain "*/15 0 1,15 * 1-5 /usr/bin/find"
```
