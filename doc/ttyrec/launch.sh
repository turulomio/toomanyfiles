## ttygif repeat simulation, so you will see twice
## Once gif is generated, close xterm

#xterm -hold -bg black -geometry 140x400  -fa monaco -fs 18 -fg white -e "ttyrec -e 'bash demo.sh'; ttygif ttyrecord"
xterm -hold -bg black -geometry 140x400  -fa monaco -fs 18 -fg white -e "ttyrec -e 'python3 demo.py'; ttygif ttyrecord"
