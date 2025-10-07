# 2 Práctica: Instalación de Ubuntu (sin LUKS, sin LVM) en UEFI/GPT. El disco virtual debe estar en un pool en el escritorio.

video a seguir: https://drive.google.com/file/d/1iVko8_qio1GJt7jcBRAxUaZ0sEWoJO1r/view?usp=sharing

## 2.1 Objetivos

- Instalar Ubuntu en un disco en modo UEFI/GPT.
- Comprender la estructura mínima de particiones en este esquema.
- Tener un sistema sencillo, claro y sin capas adicionales de cifrado o LVM.

## 2.2  Escenario

- Disco duro: 120 GB.
- Sistema: Ubuntu Desktop 24.04 LTS.
- Modo de arranque: UEFI.
- Particionado: manual.
- Deberás crear tu disco virtual (qcow2 en un pool dentro de tu escritorio. Esto es lo único que no aparece en el vídeo en donde resuelvo la práctica. Para saber como hacer esto, ve al punto de teoría anterior donde están todos los tutoriales, deberás ser independiente y buscarlo tú.)

### DESCRIPCIÓN DE INSTALACIÓN DEL POOL.



En primer lugar procederemos a crear una máquina virtual en ubuntu mediante el proceso de instalación de **Virt Manager** y elegiremos como medio de instalación el **Local (Imagen ISO o CDROM)**



![image-20251007175231350](/home/jaime/snap/typora/106/.config/Typora/typora-user-images/image-20251007175231350.png)

A continuación seleccionaremos explorar, escritorio y posteriormente seleccionaremos "Crear nuevo volumen" dentro de escritorio. 

![image-20251007175137519](/home/jaime/snap/typora/106/.config/Typora/typora-user-images/image-20251007175137519.png)

Añadiremos un almacenamiento de 120 GiB en el nuevo volumen y le cambiaremos el nombre si queremos para posteriormente darle a finalizar. 

![image-20251007175036684](/home/jaime/snap/typora/106/.config/Typora/typora-user-images/image-20251007175036684.png)



Posteriormente , añadiremos la imagen ISO de UBUNTU 24.04 y seleccionamos forward para luego añadir los nucleos y el almacenamiento del microprocesador , luego añadiremos el almacenamiento de la maquina virtual y seleccionaremos el almacenamiento personalizado.



![image-20251007175840276](/home/jaime/snap/typora/106/.config/Typora/typora-user-images/image-20251007175840276.png)

Por último seleccionamos el firmware UEFI y le daremos a aplicar para posteriormente iniciar la instalación.

![image-20251007180028327](/home/jaime/snap/typora/106/.config/Typora/typora-user-images/image-20251007180028327.png)



## 2.3 Esquema de particiones

#### 1.EFI System Partition (ESP)

Tamaño: 512 MB
Sistema de archivos: FAT32
Punto de montaje: /boot/efi
Contiene los cargadores (Olvidaos de esto por ahora)

#### 2./boot
Tamaño: 1 GB
Sistema de archivos: ext4
Contiene kernel, initramfs y módulos de GRUB.

#### 3./ (raíz)
Tamaño: 30 GB
Sistema de archivos: ext4
Contiene el sistema operativo y programas.

#### 4./home
Tamaño: 80 GB
Sistema de archivos: ext4
Contiene los datos de usuario.

#### 5.swap
Tamaño: 8 GB (ajustar según la RAM, mirar teoría para saber cuanta)Tipo: área de intercambio.

### ¡La práctica se basa en hacer capturas a pantalla completa del proceso de instalación que hago yo en el video!. En el vídeo que os dejo se ve qué tenéis que hacer, paso a paso. No os olvidéis de
documentar como creais el pool.









