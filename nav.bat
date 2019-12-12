:: Navigate to a directory from the base folder
FOR /F "tokens=* USEBACKQ" %%g IN (`py param base_dir`) do (SET base_dir=%%g) && cd %base_dir%\%1
