# Detección de Comunidades en Redes de Colaboración (CDP)

Este proyecto aborda el **Community Detection Problem (CDP)** aplicado a una red de co-autoría derivada de las publicaciones del congreso NIPS. El objetivo es identificar grupos de autores (comunidades) con una alta densidad de colaboración interna, maximizando la métrica de **Modularidad**.

## Formalización del Problema
El proyecto se desarrolla bajo el marco **PEAS** (Performance, Environment, Actuators, Sensors) y trata el problema como una optimización en un espacio de estados NP-Hard:
* **Entorno:** Grafo $G=(V,E)$ donde los nodos son autores y las aristas representan colaboraciones ponderadas.
* **Función Objetivo:** Maximización de la Modularidad de Newman-Girvan.
* **Codificación:** Representación de soluciones mediante etiquetas de comunidad por nodo.

## Algoritmos Implementados
Se han desarrollado y comparado diversas estrategias de búsqueda para encontrar la partición óptima:

1. **Búsqueda Aleatoria (Random Search):** Establecida como línea base (baseline) de rendimiento.
2. **Algoritmo Constructivo:** Basado en conocimiento del dominio para generar soluciones iniciales de calidad de forma voraz.
3. **Algoritmo Genético (GA):** Enfoque evolutivo con operadores de cruce y mutación adaptados a la estructura de comunidades.
4. **Simulated Annealing (SA):** Algoritmo de optimización metaheurística que permite escapar de óptimos locales mediante una función de probabilidad basada en "temperatura".

## Tecnologías Utilizadas
* **Python:** Lenguaje principal del proyecto.
* **NetworkX:** Para la manipulación y análisis de estructuras de grafos complejas.
* **SQLite:** Gestión de la base de datos de publicaciones NIPS.
* **Pandas & Matplotlib/Seaborn:** Procesamiento de datos y visualización de la evolución del Fitness.

## Estructura del Repositorio
* `CDP_0_SRC.ipynb`, `CDP_1_SRC.ipynb`, `CDP_2_SRC.ipynb`: Notebooks que documentan los Sprints del proyecto, desde la carga de datos hasta la optimización avanzada.
* `downsampling.py`: Script de utilidad para el submuestreo de la base de datos original, permitiendo pruebas ágiles.
* `/docs`: Memoria técnica detallada con el análisis comparativo de resultados y convergencia de los algoritmos.