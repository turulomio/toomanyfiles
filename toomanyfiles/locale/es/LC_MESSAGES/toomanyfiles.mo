��    ;      �  O   �        )   	     3  �   N     �     �  g   �     c  F   j  #   �  M   �     #     B  ;   _     �     �     �  Q   �  a   4  0   �  c   �  +   +	  Y   W	  S   �	  ,   
     2
  I   D
     �
     �
     �
     �
     �
     �
  ]   �
  0   <     m  G   �  u   �  A   E  ;   �  Q   �  
     a      0   �  9   �     �  %     '   '  B   O  P   �  K   �  v   /     �  #   �  A   �  k   (  8   �     �  7   �  ]    5   e     �  �   �     [     ]  l   j     �  O   �  '   /  F   W  ,   �  (   �  N   �     C  !   b  #   �  ]   �  c     5   j  q   �  /     h   B  b   �  +        :  ]   S     �  '   �  '   �       	          i   -  7   �  "   �  O   �  �   B  T   �  I   !  e   k     �  |   �  >   Z  6   �     �  -   �       =   /  Q   m  V   �  �     %   �  %   �  V     p   b  6   �     
   <                                $      :                                      3      *           /      (       5      '   -   ,   8   &   "       #       	   )                6              ;                       
   !   .   4      2      9   1   7                 +          %   0           'toomanyfiles_examples' directory removed Create example directories Create two directories called 'example' and 'example_directories' in the current working directory and fill it with example files with date and time patterns. D DESCRIPTION Defines a python datetime pattern to search in current directory. The default pattern is '%(default)s'. Delete Deletes files. Be careful, This can't be unmade. Use --pretend before. Developed by Mariano Muñoz 2018-{} Different examples have been created in the directory 'toomanyfiles_examples' Directories status pretending: Directories status removing: Disable log generation. The default value is '%(default)s'. Error passing parameters File status pretending: File status removing: I can't continue, there are different filename roots with date and time patterns: I can't continue, there are files and directories with date and time patterns in the current path I can't remove 'toomanyfiles_examples' directory If we want to save our disk space and we want to keep some of them, we can use TooManyFiles program Makes a simulation and doesn't remove files Makes a simulation selecting which files will be deleted when --remove parameter is used. Maximum number of files to remain in directory. The default value is '%(default)s'. Modifiers to use with --remove and --pretend Not developed yet Number of days to respect from today. The default value is '%(default)s'. O Over max files Over max number of files R Remains Remove example directories' Remove innecesary files or directories with a date and time pattern in the current directory. Remove mode. The default value is '%(default)s'. Removes files permanently Search date and time patterns to delete innecesary files or directories Sets the date and time pattern to search in the current directory filenames. It uses python strftime function format. So, We want to keep the last 5 files because they are too recent. So, {} files have been deleted and {} files have been kept. So, {} files will be deleted and {} will be kept when you use --remove parameter. That's all The number of files too young to delete can't be bigger than the maximum number of files to store This app has the following mandatory parameters: This is a video to show how to use 'toomanyfiles' command Too young to delete Uninstall command only works in Linux We analyze the result with the output.. We are going to create an example directory to learn how to use it We are going to see the 10 last files of directory 'toomanyfiles_examples/files' We can see files with temporal pattern 'YYYYmmdd HHMM' with a day variation We like the result, so we can delete files replacing --pretend by --remove. Selected files will be removed permanently We list the files remaining We make a simulation with --pretend We use to find this kind of files in automatic backups, logs, ... We want to keep the first file of each month from the rest of the files until a max number the files of 15. With --pretend and --remove you can use this parameters: Y {} TooManyFiles in {} detected {} files with pattern {} Project-Id-Version: TooManyFiles
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-08-20 17:44+0200
PO-Revision-Date: 2015-03-22 18:51+0100
Last-Translator: root <turulomio@yahoo.es>
Language-Team: Spanish
Language: es
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
 El directorio 'toomanyfiles_examples' ha sido borrado Crear directorios de ejemplo Crea dos directorios de nombre 'example' y 'example_directories' en el directorio actual y los llena con ficheros de ejemplo que tengan patrónes de fecha y hora. B DESCRIPCIÓN Define un patrón de fecha y hora a buscar en el directorio actual. El patrón por defecto es '%(default)s'. Borrado Borra los ficheros. Ten cuidado, esto no puede deshacerse. Usa antes --pretend. Desarrollado por Mariano Muñoz 2018-{} Se han creado varios ejemplos en el directorio 'toomanyfiles_examples' Estado de los directorios en la simulación: Estado de los directorios en el borrado: Desabilita la generación del registro. El valor por defecto es '%(default)s'. Error al pasar los parámetros Estado de los ficheros simulando: Estado de los ficheros para borrar: No puedo continuar, hay raices de nombres de ficheros distintas con patrones de fecha y hora: No puedo continuar, hay ficheros y directorios con patrones de fecha y hora en el directorio actual No puedo borrar el directorio 'toomanyfiles_examples' Si queremos ahorrar espacio en disco y queremos conservar algunos de ellos, podemos usar el programa TooManyFiles Realiza una simulación y no borra los ficheros Realiza una simulación seleccionando que ficheros serán borrados cuando se use el parámetro --remove. Máximo número de ficheros que quedarán en el directorio. El valor por defecto es '%(default)s'. Parámetros a usar con --remove y --pretend No desarrollado todavía Número de días que se respetan desde hoy sin borrar. El valor por defecto es '%(default)s'. S Supera el número de ficheros a guardar Supera el número de ficheros a guardar P Permanece Borrar directorios de ejemplo Borra ficheros o directorios innecesarios, que tengan un patrón de fecha y hora en el directorio actual. Modo de borrado. El valor por defecto es '%(default)s'. Borra los ficheros permanentemente Busca patrónes de fecha y hora para borrar ficheros o directorios innecesarios Establece el patrón de fecha y hora para buscar en los nombres del directorio actual. Usa el formato de python de la funciónde strftime De esta manera, queremos conservar los 5 últimos ficheros porque son muy recientes. De esta manera, {} ficheros se han borrado y {} ficheros se han guardado. De esta manera, {} ficheros serán borrados y {} serán guardados cuando uses el parámetro --remove. Eso es todo El número de ficheros demasiado recientes para ser borrados no puede ser mayor que el máximo número de ficheros a guardar Esta aplicación tiene los siguientes parámetros obligatorios Este video muestra como usar el comando 'toomanyfiles' Muy joven para borrar El comando 'uninstall' solo funciona en Linux Analizamos el resultado... Vamos a crear un directorio de ejemplo para aprender a usarlo Vamos a ver los 10 últimos ficheros del directorio 'toomanyfiles_examples/files' Podemos ver ficheros con el patrón temporal 'YYYYmmdd HHMM' con un día de variación Estamos de acuerdo con el resultado, por lo que podemos borrar los ficheros sustituyendo --pretend por --remove. Los ficheros seleccionados se borrarán permanentemente Listamos los ficheros que han quedado Hacemos una simulación con --pretend Solemos encontrar este tipo de ficheros en copias de seguridad automáticas, logs, ... Del resto de ficheros, queremos conservar el primer fichero de cada mes hasta un máximo de 15 ficheros en total Con --pretend y --remove puedes usar estos parámetros J {} TooManyFiles en {} detectó {} ficheros con el patrón {} 