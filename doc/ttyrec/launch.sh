## ttygif repeat simulation, so you will see twice
## Once gif is generated, close xterm
xterm -hold -bg black -geometry 140x400 -fs 14 -fg white -e "ttyrec -e 'bash demo.sh'; ttygif ttyrecord"