@echo off
REM Simple batch script to run both 2015 and 2017 experiments
REM Usage: Double-click this file or run from command prompt

echo ========================================================================
echo Running Duernast DSSAT Pipeline for Both Years
echo ========================================================================
echo.

python GENERALIZED_PIPELINE/MASTER_WORKFLOW.py --all

echo.
echo ========================================================================
echo Pipeline completed!
echo ========================================================================
pause
