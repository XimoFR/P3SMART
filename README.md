# Proyecto 3: SMART

## Descripción y objetivo

Este proyecto tiene como objetivo desarrollar un flujo de trabajo para la ingesta, el procesamiento y el análisis de los datos asociados al proyecto SMART. La finalidad es preparar los datos para obtener resultados útiles y facilitar su visualización.

## Arquitectura

```mermaid
graph LR
    A[Fuente de datos] --> B[Ingesta]
    B --> C[Almacenamiento]
    C --> D[Procesamiento ETL]
    D --> E[Dashboard]
```

## Estructura del repositorio

```text
P3SMART/
├── .gitignore
├── README.md
├── ingesta/
├── etl/
└── dashboard/
```

## Tecnologías

- Python 3.10 o superior.
- Git y GitHub.
- Herramientas de procesamiento y análisis de datos.