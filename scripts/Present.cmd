@echo off
rem Double-click to open the deck. -ExecutionPolicy Bypass is here because a
rem freshly copied .ps1 is blocked by default on most machines.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0serve-offline.ps1" %*
