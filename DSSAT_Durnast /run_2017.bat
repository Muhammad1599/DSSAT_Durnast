@echo off
REM Simple batch script to run 2017 experiment only
REM Usage: Double-click this file or run from command prompt

echo ========================================================================
echo Running Duernast 2017 DSSAT Pipeline
echo ========================================================================
echo.

python GENERALIZED_PIPELINE/MASTER_WORKFLOW.py 2017

echo.
echo ========================================================================
echo Pipeline completed!
echo ========================================================================
pause
