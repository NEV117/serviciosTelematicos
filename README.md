
# Parcial 1 Servicios Telematicos

- Nicolas Escandon
- Santiago Carlosama



## Desarrollo
#### Instalar PAM

```
dnf -y install mod_authnz_pam
```
Ir a `/etc/httpd/conf.modules.d/55-authnz_pam.conf` y descomentar la siguiente línea:
```
nano /etc/httpd/conf.modules.d/55-authnz_pam.conf

# Descomentar la siguiente linea en el archivo
LoadModule authnz_pam_module modules/mod_authnz_pam.so

```
### Parte 1
 -  Configure el archivo de configuración de Apache para el sitio correspondiente y especifique las reglas de  acceso al directorio "/archivos_privados".
- Utilice los módulos PAM adecuados para gestionar la autenticación. Asegúrese de que solo los usuarios del sistema puedan autenticarse exitosamente
- se asume que ya se creo el directo/ virtual hosting de `archivos_privados`


    Ir a `/etc/httpd/conf.d/authnz_pam.conf` y agregar la siguiente configuración para el directorio /archivos_privados:

    ```
    # añadir al final
    <Directory "/var/www/html/auth-pam">
        SSLRequireSSL
        AuthType Basic
        AuthName "PAM Authentication"
        AuthBasicProvider PAM
        AuthPAMService httpd-auth
        Require valid-user
    </Directory>
    ```
    Crear `httpd-auth` o un arhivo equivalente el nombre puede variar segun las necesidades

    Ir a `/etc/pam.d/` y crear por nano o vim:

    ```
    [root@www ~]# nano /etc/pam.d/httpd-auth

    # si el arvhico es nuevo aparecera vacio y se debe escribir la siguiente configuracion
    auth       required     pam_listfile.so item=user sense=deny file=/etc/httpd/conf.d/denyusers onerr=succeed
    auth       include      system-auth
    account    include      system-auth

    ```
-  Cree una lista de `usuarios que deben ser denegados` el acceso al directorio `/archivos_privados` Esta lista 
    debe almacenarse en un archivo separado.

    Ir a `/etc/httpd/conf.d/` y crear el archivo lista `denyusers`

    ```
    [root@www ~]# vi /etc/httpd/conf.d/denyusers
    # Crear Nuevo
    # Lista de Usuarios con autenticacion prohibida
    pamDenied
    ```

    ### Permisos importantes para el funcionamiento
    ```
    chgrp apache /etc/httpd/conf.d/denyusers
    chmod 640 /etc/httpd/conf.d/denyusers

    #!!IMPORTANTE change permission httpd can read shadow
    chgrp apache /etc/shadow
    chmod 440 /etc/shadow
    ```

    ### Reiniciar http service
    ```
    service httpd restart
    ```

- Configure la restricción de acceso para los usuarios de la lista creada en el paso anterior, de modo que  reciban un mensaje de error al intentar acceder al directorio.

    dentro de `/etc/httpd/conf.d/authnz_pam.conf` o en `/etc/httpd/conf/httpd.conf`

    #### En `authnz_pam.conf` 
    agregar la linea `ErrorDocument 401 /error.html` esta puede diriguir a un .html o tener un mensaje de texto
    
    El codigo `401` de estado HTTP 401 indica que la solicitud del cliente no se ha completado porque carece de credenciales de autenticación válidas para el recurso solicitad

    ```
    <Directory "/var/www/html/archivos_privados">
        Require ssl
        AuthType Basic
        AuthName "PAM Authentication"
        AuthBasicProvider PAM
        AuthPAMService httpd-auth
        Require valid-user

        #ErrorDocument 403 "Acceso denegado. No tienes permiso para acceder a este contenido."
        ErrorDocument 401 /error.html
    </Directory>

    ```

    #### En `/etc/httpd/conf/httpd.conf`
    Agregar `ErrorDocument 401 /error.html` o `ErrorDocument 401 "mensaje de texto como cadena"`  al final del archivo


---
### Atajos

#### ruta al conf:
```
nano /etc/httpd/conf/httpd.conf
```
#### ruta a la configuración del virtual host:
```
nano /etc/httpd/conf.d/authnz_pam.conf
```
#### Ruta al log:
```
nano /var/log/secure
```
#### ruta al httpd-auth:
```
cd /etc/pam.d/
nano /etc/pam.d/httpd-auth
```
### Parte 2

- Realice un túnel hacia el servidor web implementado en clase, de manera que los recursos de su servidor web puedan ser visualizados desde cualquier lugar por fuera de su red local. Para efectos de prueba, agregar una página personalizada a su sitio web.
    
    ### Descargar ngrok:
    enlace a [ngrok](https://ngrok.com/download)

    Se debe descomprimir  `ngrok-v3-stable-windows-amd64.zip`  como resultado, obtendrá un archivo .exe en la carpeta donde se haya descomprimido.
    
    Si no se configura la variable de entorno de ngrok, solo funcionará ejecutando el `ngrok.exe` en este caso, la configuración se realiza desde el .exe.

    #### verficar instalación

    ```
    ngrok -v
    ```

    ### Configurar tunel en vagrant

    para esto se debe modificar el `Vagrantfile` agregando la siguiente línea:
    ```
    servidor.vm.network "forwarded_port", guest: 80, host: 8080
    ```

    #### Ejemplo de máquina servidor en CentOS 9:
    ```
    config.vm.define :servidor do |servidor|
    servidor.vm.box = "generic/centos9s"
    servidor.vm.network :private_network, ip: "192.168.50.3"
    servidor.vm.network "forwarded_port", guest: 80, host: 8080
    servidor.vm.hostname = "servidor"
    ```
    ### Reiniciar vagrant y configurar el tunnel con ngrok
     Ejecutar `vagrant reload --provision` para que los cambios anteriores hagan efecto

     ejecutar el archivo `ngrok.exe` y agergar la siguiente línea:

     ```
     ngrok httpd 192.168.50.3:80
     ```

     Si todos los pasos se ejecutaron correctamente, obtendrá lo siguiente:

     <p aling="center">
        <img src="Readme Images/ngrok.png"/>     
     </p>
    



