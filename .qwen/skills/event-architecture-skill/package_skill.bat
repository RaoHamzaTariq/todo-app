@echo off
REM Simple skill packaging script for Windows

echo Creating event-architecture-skill package...

REM Create a zip archive of the skill
powershell Compress-Archive -Path ".\*" -DestinationPath "..\event-architecture-skill.skill" -Force

echo Skill packaged as event-architecture-skill.skill