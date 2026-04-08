@echo off
REM Use XAMPP PHP to run Composer (when `composer` is not in PATH)
set PHP_EXE=C:\xampp\php\php.exe
if not exist "%PHP_EXE%" set PHP_EXE=php
"%PHP_EXE%" "%~dp0composer.phar" %*
