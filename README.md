# FIX Hisense TVs NTP

## Problema

Algunos modelos de televisores Hisense (o algunas otras marcas que usan componentes Hisense) no pueden conectarse al servidor NTP para sincronizar la fecha y la hora.

Estos televisores no tienen la opción de configurar manualmente la fecha y la hora, por lo que es necesario que se conecten al servidor NTP para obtener la fecha y la hora correcta, de lo contrario, no podrán acceder a ciertas aplicaciones, como por ejemplo YouTube.

## Parche propuesto

La solución es configurar un servidor NTP local en la red local, y configurar el televisor para que se conecte a este servidor NTP local.

Esto involucra tener que redirigir tráfico y/o envenenar los servidores DNS locales para que mientan acerca de las URL que los televisores utilizan para obtener la fecha y la hora. Si bien esto puede ser considerado como un accionar no ético y que afecta la neutralidad de la red, es la única solución que se ha encontrado hasta el momento para que los clientes que compraron esos televisores puedan usar los servicios web. En el momento que el fabricante normalice sus servicios, este parche debería ser desinstalado.

### Configurar un servidor NTP y Web local

#### Aviso en relación al equipo donde se ejecuta esto

> Estos comandos consideran que se está utilizando un sistema operativo basado en Debian, como por ejemplo Ubuntu. Y que el sistema operativo está recién instalado, sin configuraciones adicionales. Si se está utilizando otro sistema operativo, o si ya se han realizado configuraciones adicionales, es posible que estos comandos no funcionen o generen problemas en el sistema operativo.

#### Aviso de seguridad MUY IMPORTANTE

> *El servidor NTP necesita firewall* para que no se acceda desde todo el mundo. Si no se configura un firewall, se puede convertir en un servidor NTP abierto, lo que puede ser utilizado para realizar ataques de denegación de servicio distribuido (DDoS). [Ver este caso](https://www.lacnic.net/innovaportal/file/4016/1/fukuoka-university-public-ntp-service-deployment-use-case.pdf).

#### Paso 1: Instalar Docker

```bash
curl -L get.docker.com | bash
```

#### Paso 2: Crear un contenedor con un servidor NTP

Descargar el archivo `docker-compose.yml`:

```bash
mkdir -p /opt/ayuda.la/fix-tv-ntp/
cd /opt/ayuda.la/fix-tv-ntp/
apt install -y wget && wget https://raw.githubusercontent.com/aweher/fix-tv-ntp/refs/heads/main/docker-compose.yaml
docker compose up --build -d
```

#### Paso 3: Configurar una redirección DNS

Suponiendo que este parche está corriendo en las IP `192.0.2.192` / `2001:db8::192`, se debe redirigir el tráfico DNS de `synctime.hismarttv.com` en el servidor DNS local.

Ejemplo de Unbound

```txt
[...]
 local-zone: "synctime.hismarttv.com" redirect
 local-data: "synctime.hismarttv.com A 192.0.2.192"
 local-data: "synctime.hismarttv.com AAAA 2001:db8::192"
[...]
```

### Actualizar

```bash
git pull
docker compose down
docker compose up --build -d
```

### Desinstalar

```bash
docker compose down -v
```
