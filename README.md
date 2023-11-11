## 1. Prometheus + Node Exporter + Grafana on Ubuntu 22.04 LTS

<details>
  <summary>Explicacion Detallada</summary>
  
  ### Pre Requisitos
  1. Ubuntu with 22.04 Version
  2. Root user account with sudo  privilege.
  3. Prometheus system user and group.
  4. Sufficient storage on your system and good internet connectivity
  5. Ports Required- 9090 (Prometheus), 3000 (Grafana), 9100 (Node Exporter)

### 1: Crear Prometheus System Users and Directory

```
sudo apt update -y
```

crear usuarios y directorios

```
sudo useradd --no-create-home --shell /bin/false prometheus
```

```
sudo mkdir /etc/prometheus
sudo mkdir /var/lib/prometheus
```

```
sudo chown prometheus:prometheus /var/lib/prometheus
```
### 2: Descargar Prometheus Binary File

```
cd /tmp/
```

```
wget https://github.com/prometheus/prometheus/releases/download/v2.46.0/prometheus-2.46.0.linux-amd64.tar.gz
```

Descomprimir usando tar

```
tar -xvf prometheus-2.46.0.linux-amd64.tar.gz
```

```
cd prometheus-2.46.0.linux-amd64

sudo mv console* /etc/prometheus

sudo mv prometheus.yml /etc/prometheus

sudo chown -R prometheus:prometheus /etc/prometheus
```

```
sudo mv prometheus /usr/local/bin/
sudo chown prometheus:prometheus /usr/local/bin/prometheus
```

### 3: Prometheus configuration file

```
sudo nano /etc/prometheus/prometheus.yml
```

### 4: Crear Prometheus Systemd file

```
sudo nano /etc/systemd/system/prometheus.service
```

```
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```

Reload systemd

```
sudo systemctl daemon-reload
```

Start, Enable, Status Prometheus service:

```sudo systemctl start prometheus
sudo systemctl enable prometheus
sudo systemctl status prometheus
```

### 5: Acceder a prometheus en el navegador

```
sudo ufw allow 9090/tcp
```

```
http://server-IP-or-Hostname:9090 || http://192.168.60.3:9090
```

<p aling="center">
    <img src="Readme Images/prometheus.png"/>     
</p>

### 6: Descargar Node Exporter

```
cd /tmp
```

```
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
```

Descomprimir

```
sudo tar xvfz node_exporter-*.*-amd64.tar.gz
```

```
sudo mv node_exporter-*.*-amd64/node_exporter /usr/local/bin/
```

```
sudo useradd -rs /bin/false node_exporter
```

### 7: Crear Node Exporter Systemd service

```
sudo nano /etc/systemd/system/node_exporter.service
```

```
[Unit]

Description=Node Exporter

After=network.target

 

[Service]

User=node_exporter

Group=node_exporter

Type=simple

ExecStart=/usr/local/bin/node_exporter

 

[Install]

WantedBy=multi-user.target
```

Recargar, permitir e iniciar NODE Exporter

```sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
sudo systemctl status node_exporter
```

### 8: Configurar Node Exporter como un Prometheus target

```
sudo nano /etc/prometheus/prometheus.yml
```

```
- job_name: 'Node_Exporter'

    scrape_interval: 5s

    static_configs:

      - targets: ['<Server_IP_of_Node_Exporter_Machine>:9100']
```

Reiniciar

```
sudo systemctl restart prometheus
```

<p aling="center">
    <img src="Readme Images/NodeExporter.png"/>     
</p>

### 9: Instalar Grafana on Ubuntu 22.04 LTS

```
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```

```
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
```

```
sudo apt update
```

```
sudo apt install grafana
```

```
sudo systemctl start grafana-server
```

```
sudo systemctl status grafana-server
sudo systemctl enable grafana-server
```

```
http://your_ip:3000 || http://192.168.60.3:3000 
```

```
Username – admin
Password – admin
```

Home

<p aling="center">
    <img src="Readme Images/graphana home.png"/>     
</p>

DashBoard
<p aling="center">
    <img src="Readme Images/dashboard.png"/>     
</p>

</details>

#### Atajos
Start, Enable, Status Prometheus service:

```sudo systemctl start prometheus
sudo systemctl enable prometheus
sudo systemctl status prometheus
```


Recargar, permitir e iniciar NODE Exporter
```sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
sudo systemctl status node_exporter
```

## 2. API Rest + MySQL on Ubuntu 22.04 LTS

<details>
  <summary>Api Rest configuration</summary>
  
  ### 1: Vagrant Up
 
  ```
  vagrant up
```

### 2: Exportar aplicacion de flask
 
 ir a la ubicacion de la app
 ```
  cd /vagrant
```
Exportar y correr la aplicacion
```
export FLASK_APP=apirest_mysql.py
python3 -m flask run --host=0.0.0.0
```

En caso caso de error intentar:
 ```
pip install Werkzeug==0.16.1
```

 ```
pip install --upgrade Flask Flask-MySQLdb Flask-Cors
```
<p aling="center">
    <img src="Readme Images/script.png"/>     
</p>


### 3: Correr Cliente Rest (se recomienda correrlo en windows)
Dentro de este repositorio se encuentra la carpeta RestClient el cual es un cleinte hecho en Node.js para consumir apis en este caso se recomienda No correrlo en un maquina virtual para evitar conflictos. En cambio se puede correr en windows

Ir a la carpeta RestClient:

Instalar dependencias
 ```
npm i
```

Correr Cliente
 ```
npm start
```
<p aling="center">
    <img src="Readme Images/RestClient.png"/>     
</p>

Ya desde este cliente se pueden consumir las apis del script de la maquina virtual para eso se deben mandar solicitudes http a los siguientes endpoints

Cabe mencionar que el RestClient puede consumir apis de cualquier endpoint con cors

Endpoints:
 ```
http://192.168.60.3:5000/books | http:<MACHINE IP>:<PORT>/books
```
```
http://192.168.60.3:5000/books/:id | http:<MACHINE IP>:<PORT>/books/:id
```

</details>

### Preview

<p aling="center">
    <img src="Readme Images/restClientSimpleTest.gif"/>     
</p>