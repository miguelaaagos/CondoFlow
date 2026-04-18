# CondoFlow

Plataforma web para la gestion basica de un condominio: unidades, pagos, reservas de areas comunes y anuncios para los residentes. Construida sobre Django 4.2 con vistas basadas en funciones y templates Materialize.

El proyecto parte del CRUD entregado como base en el curso y se adapta a un caso real: administrar un edificio con sus bloques, departamentos, cobros mensuales y las reservas de espacios compartidos.

## Requisitos

- Python 3.9 o superior
- pip
- Opcional: un entorno virtual (recomendado)

## Instalacion local

```bash
# 1. Clonar el repositorio
git clone https://github.com/miguelaaagos/CondoFlow.git
cd CondoFlow

# 2. Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requierements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario (administrador)
python manage.py createsuperuser

# 6. Levantar el servidor de desarrollo
python manage.py runserver
```

La aplicacion queda disponible en `http://127.0.0.1:8000/`.

> Usuario de prueba: **admin** / **admin123** (si se corre la base que viene en el repo).

## Modelo de datos

| Entidad | Que representa |
|---------|----------------|
| `Bloque` | Un edificio o torre del condominio. Tiene nombre y numero de pisos. |
| `Unidad` | Un departamento dentro de un bloque. Se asocia a un propietario y, opcionalmente, a un usuario residente. |
| `Pago` | Un cobro asociado a una unidad. Puede estar `pendiente`, `pagado` o `vencido`. Permite adjuntar comprobante. |
| `Reserva` | Un bloqueo de un area comun (salon, piscina, gimnasio, BBQ) en una fecha y franja horaria. |
| `Anuncio` | Un aviso publicado por la administracion. Puede marcarse como destacado. |

## Roles y permisos

- **Administrador** (`is_staff=True`): ve todo el condominio, crea/edita/elimina unidades, bloques, pagos y anuncios.
- **Residente**: ve solo su unidad, sus pagos y sus reservas; puede crear y editar sus propias reservas.

## Estructura del proyecto

```
CondoFlow/
├── apps/
│   └── movies/              # App principal (nombre heredado del ejemplo)
│       ├── models.py        # Bloque, Unidad, Pago, Reserva, Anuncio
│       ├── views.py         # Vistas basadas en funciones
│       ├── forms.py         # ModelForms por entidad
│       ├── urls.py          # Rutas por recurso
│       └── templates/movies # Templates Materialize
├── crud/                    # Configuracion del proyecto Django
├── manage.py
└── requierements.txt
```

## Notas

- El nombre del app (`apps.movies`) se mantuvo para no romper las migraciones ya generadas. Todo el contenido fue reescrito para CondoFlow.
- La configuracion regional esta pensada para Chile (`es-cl`, `America/Santiago`).
- La base usa SQLite por defecto; para un despliegue real habria que cambiar a PostgreSQL o MySQL via `DATABASES` en `crud/settings.py`.
