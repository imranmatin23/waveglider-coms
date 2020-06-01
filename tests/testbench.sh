#!/bin/bash
#
# Testbench to execute all tests.
#
# Author: Imran Matin
# Email: imatin@ucsd.edu
#
# Usage:
# in a new terminal
# sh testbench.sh
# 
# Executes all tests in the test directory, and saves the results into a
# timestamped file in the ./results directory.

# create the outfile to store the results using the current time
now=$(date +"%Y-%m-%dT%H:%M:%S")
outfile="results/${now}_test_results.txt"

printf "**************** WaveGlider COMMS Test Results ****************\n" > ${outfile}
printf "Author: Imran Matin\n" >> ${outfile}
printf "Executer: ${USER}\n" >> ${outfile}
printf "Date: $(date +"%Y-%m-%d")\n" >> ${outfile}
printf "Time: $(date +"%H:%M:%S")\n" >> ${outfile}

printf "\n" >> ${outfile}

printf "================ Settings: Camera Settings ===============\n" >> ${outfile}
cat camera_config.py >> ${outfile}

printf "\n" >> ${outfile}

printf "================ Test: test_compression_size.py ===============\n" >> ${outfile}
python test_compression_size.py >> ${outfile}

printf "\n" >> ${outfile}

printf "================ Test: test_event_delay.py ====================\n" >> ${outfile}
python test_event_delay.py >> ${outfile}

printf "\n" >> ${outfile}

printf "================ Test: test_frame_rate.py =====================\n" >> ${outfile}
python test_frame_rate.py >> ${outfile}

printf "\n" >> ${outfile}

printf "================ Test: test_write_speed.py ====================\n" >> ${outfile}
python test_write_speed.py >> ${outfile}