{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import scipy as sp\n",
    "import xarray as xr\n",
    "import os\n",
    "import glob\n",
    "import time\n",
    "import subprocess"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "pycharm": {
     "name": "#%%\n"
    }
   },
   "outputs": [
    {
     "ename": "KeyboardInterrupt",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mKeyboardInterrupt\u001b[0m                         Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-27-4ca547665179>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mwhile\u001b[0m \u001b[0;32mTrue\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m     \u001b[0;32mwhile\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0mos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mexists\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mrun_dir\u001b[0m\u001b[0;34m+\u001b[0m\u001b[0;34m'wrf_finished'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 6\u001b[0;31m         \u001b[0mtime\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msleep\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;36m20\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      7\u001b[0m     \u001b[0mos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mremove\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mrun_dir\u001b[0m\u001b[0;34m+\u001b[0m\u001b[0;34m'wrf_finished'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      8\u001b[0m     \u001b[0mlist_of_restarts\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mglob\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mglob\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mrun_dir\u001b[0m\u001b[0;34m+\u001b[0m\u001b[0;34m'wrfrst*'\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;31m# * means all if need specific format then *.csv\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mKeyboardInterrupt\u001b[0m: "
     ]
    }
   ],
   "source": [
    "\n",
    "#path to wrf run directory\n",
    "run_dir='/Users/gbromley/code/wrf_run_configs/scripts/'\n",
    "out_dir=''\n",
    "while True:\n",
    "    #check to see if previous job completed\n",
    "    while not os.path.exists(run_dir+'wrf_finished'):\n",
    "        time.sleep(20)\n",
    "        \n",
    "    #move output to folder\n",
    "    wrf_out_files = glob.glob(run_dir+'wrfout*')\n",
    "    for out_file in wrf_out_files:\n",
    "        subprocess.run('mv '+out_file+' '+out_dir+out_file, shell=True)\n",
    "        \n",
    "    \n",
    "    #remove job finshed file\n",
    "    os.remove(run_dir+'wrf_finished')\n",
    "    #remove rsl files\n",
    "    rsl_files = glob.glob(run_dir+'rsl.*')\n",
    "    for rsl in rsl_files:\n",
    "        os.remove(f)\n",
    "    #find most recent restart file\n",
    "    list_of_restarts = glob.glob(run_dir+'wrfrst*') # * means all if need specific format then *.csv\n",
    "    latest_restart = max(list_of_restarts, key=os.path.getctime)\n",
    "    #get start date for next run\n",
    "    year_start = latest_restart.split('/')[6][11:15]\n",
    "    month_start = latest_restart.split('/')[6][16:18]\n",
    "    day_start = latest_restart.split('/')[6][19:21]\n",
    "\n",
    "    #read data from most recent restart file\n",
    "\n",
    "    #add start dates to namelist\n",
    "    with open('/Users/gbromley/code/wrf_run_configs/wrf/4km_NGP/test_namelist.input', 'r') as nl_template:\n",
    "        file_data = nl_template.read()\n",
    "        new_namelist = file_data.replace('<year_start>',year_start)\n",
    "        new_namelist = new_namelist.replace('<month_start>',month_start)\n",
    "        new_namelist = new_namelist.replace('<day_start>', day_start)\n",
    "        new_namelist = new_namelist.replace('<rst>', '.true.')\n",
    "    with open(run_dir+'namelist.input', 'w+') as file:\n",
    "        file.write(new_namelist)\n",
    "    #submit new job\n",
    "    subprocess.run('qsub runwrf.csh', shell=True)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  },
  "pycharm": {
   "stem_cell": {
    "cell_type": "raw",
    "source": [],
    "metadata": {
     "collapsed": false
    }
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}