# FIX Hisense TVs NTP

## Problema

Algunos modelos de televisores Hisense (o algunas otras marcas que usan componentes Hisense) no pueden conectarse al servidor API de la marca para sincronizar la fecha y la hora.

Estos televisores no tienen la opción de configurar manualmente la fecha y la hora, por lo que es necesario que se conecten al servidor API para obtener la fecha y la hora correcta, de lo contrario, no podrán acceder a ciertas aplicaciones, como por ejemplo YouTube.

## Parche propuesto

La solución es simular un servidor API en la red local, y configurar algún truco en la red para que el televisor se conecte a este servidor local en vez de utilizar el real del fabricante.

Esto involucra tener que redirigir tráfico y/o envenenar los servidores DNS locales para que mientan acerca de las URL que los televisores utilizan para obtener la fecha y la hora. Si bien esto puede ser considerado como un accionar no ético y que afecta la neutralidad de la red, es la única solución que se ha encontrado hasta el momento para que los clientes que compraron esos televisores puedan usar los servicios web. En el momento que el fabricante normalice sus servicios, este parche debería ser desinstalado.

### Configurar Web local

#### Aviso en relación al equipo donde se ejecuta esto

> Estos comandos consideran que se está utilizando un sistema operativo basado en Debian, como por ejemplo Ubuntu. Y que el sistema operativo está recién instalado, sin configuraciones adicionales. Si se está utilizando otro sistema operativo, o si ya se han realizado configuraciones adicionales, es posible que estos comandos no funcionen o generen problemas en el sistema operativo.
> El puerto 80 debe estar disponible en el sistema operativo.

#### Paso 1: Instalar Docker

```bash
curl -L get.docker.com | bash
```

#### Paso 2: Crear un contenedor con un servidor NTP

Descargar el archivo `docker-compose.yml`:

```bash
mkdir -p /opt/ayuda.la
cd /opt/ayuda.la
git clone https://github.com/aweher/fix-tv-ntp.git
cd fix-tv-ntp
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

### ¿Cómo actualizar?

```bash
cd /opt/ayuda.la/fix-tv-ntp

git stash #solo si se hicieron cambios manuales en algun archivo

git pull
docker compose down
docker compose up --build -d
```

### ¿Cómo desinstalar?

```bash
cd /opt/ayuda.la/fix-tv-ntp
docker compose down -v
```
