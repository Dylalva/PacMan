<center>
    
# PAC-MAN

</center>

<details>
    <summary><h2>Español</h2></summary>

## Introducción

Este proyecto consiste en la implementación de la lógica de los fantasmas en el juego Pac-Man. Para ello, se hizo uso de diversas herramientas, algoritmos y enfoques de inteligencia artificial, destacando el uso de **A\*** para la búsqueda eficiente de rutas y el algoritmo **Q-Learning** para el aprendizaje y toma de decisiones.

### Herramientas y recursos utilizados:
- **Python**: Lenguaje principal para el desarrollo del proyecto.
- **Pygame**: Librería para el desarrollo de juegos 2D en Python.
- **Numpy**: Librería para arreglos multidimensionales y la realización de operaciones matemáticas de alto rendimiento.
- **Q-Learning**: es una técnica de aprendizaje por refuerzo
- **Algoritmos de búsqueda y aprendizaje**: A\* y Q-Learning.

---

## Algoritmos de Búsqueda

### A* (A-Star)

El algoritmo **A\*** es ampliamente conocido por su eficiencia en la búsqueda de caminos óptimos en comparación con otros algoritmos, como **Dijkstra**, **BFS** o **DFS**. En este proyecto, **A\*** fue adaptado para funcionar dentro de la lógica del movimiento de los fantasmas, en especial para calcular rutas eficientes que les permitan atrapar a Pac-Man o moverse a posiciones específicas del mapa.

El algoritmo utilizado se basa en el siguiente recurso:

- [A\* Search Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/a-search-algorithm-in-python/)

El algoritmo fue modificado y ajustado para cumplir con la estructura y necesidades específicas del proyecto, como la integración con los nodos del mapa de Pac-Man y la evitación de obstáculos.

### Comparación con otros algoritmos

Se eligió **A\*** por su capacidad de encontrar la ruta más corta de manera más eficiente que otros algoritmos:

- **Dijkstra**: Encuentra el camino más corto desde un nodo inicial a todos los otros nodos, pero es menos eficiente que **A\*** cuando se busca un camino específico.
- **BFS (Breadth-First Search)**: Ideal para encontrar la solución más rápida en términos de pasos, pero menos eficiente que **A\*** en gráficos con ponderaciones.
- **DFS (Depth-First Search)**: Menos adecuado para la búsqueda de rutas óptimas en comparación con **A\*** y **BFS**, especialmente en gráficos ponderados.

---

## Q-Learning

El **Q-Learning** es una técnica de aprendizaje por refuerzo que se utilizó en este proyecto para mejorar la toma de decisiones de los fantasmas en determinadas situaciones. Al aplicar **Q-Learning**, los fantasmas pueden aprender estrategias más complejas, como cuándo perseguir a Pac-Man directamente o cuándo buscar un atajo.

Para comprender y aplicar **Q-Learning**, se consultaron los siguientes recursos:

- [Introducción a Q-Learning - EducaOpen](https://www.educaopen.com/digital-lab/blog/inteligencia-artificial/q-learning)
- [Tutorial de Q-Learning - DataCamp](https://www.datacamp.com/es/tutorial/introduction-q-learning-beginner-tutorial)

### Ecuación de Q-Learning

La ecuación de **Q-learning** se utiliza para actualizar el valor Q de un estado y acción específicos, permitiendo al agente aprender el valor esperado de las recompensas futuras al seguir una política óptima. La ecuación es la siguiente:

\[
Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]
\]

donde:

- \( Q(s, a) \): Es el valor Q actual del estado \( s \) y la acción \( a \).
- \( \alpha \): Tasa de aprendizaje, que controla cuánto se ajusta el valor Q actual.
- \( r \): Recompensa recibida después de tomar la acción \( a \) en el estado \( s \).
- \( \gamma \): Factor de descuento, que pondera la importancia de las recompensas futuras.
- \( \max_{a'} Q(s', a') \): Valor Q máximo esperado para el próximo estado \( s' \) al tomar la mejor acción \( a' \) en ese estado.

---
## Numpy

**NumPy** es una biblioteca fundamental en Python para el manejo de arreglos multidimensionales y la realización de operaciones matemáticas de alto rendimiento. En el contexto de este proyecto, **NumPy** permitió implementar cálculos eficientes, como el uso de normas para medir distancias y la manipulación de datos en la tabla Q en el algoritmo de Q-Learning.

### Funcionalidades de NumPy en el proyecto

1. **Creación de Arrays y Manipulación de Datos**:
   - `np.zeros()`: Inicialización de la tabla Q con valores de cero en cada estado, optimizando el almacenamiento de valores para el aprendizaje de los fantasmas.
   - `np.argmax()`: Selección de la acción óptima en la tabla Q, permitiendo que los fantasmas elijan movimientos estratégicos con base en sus experiencias previas.

2. **Cálculo de Distancias**:
   - `np.linalg.norm()`: Cálculo de la distancia entre los fantasmas y Pac-Man, mejorando la precisión de las recompensas en el modelo de Q-Learning al medir la proximidad.

### Documentación y Recursos

Para profundizar en el uso de **NumPy** y explorar ejemplos adicionales, se recomienda la consulta de la documentación oficial:

- [Documentación oficial de NumPy](https://numpy.org/doc/stable/)

NumPy fue esencial para realizar operaciones matemáticas de manera eficiente, lo que permitió optimizar el rendimiento del algoritmo de aprendizaje y los cálculos necesarios en tiempo real para la toma de decisiones de los fantasmas.

---

## Estructura de Datos en Python

El manejo eficiente de las estructuras de datos en Python fue fundamental para implementar los nodos, grafos y otros elementos necesarios para el juego. Python proporciona diversas estructuras de datos útiles para este tipo de proyectos, como listas, diccionarios y sets.

Recursos de Python sobre estructuras de datos:

- [Documentación oficial sobre estructuras de datos en Python](https://docs.python.org/es/dev/tutorial/datastructures.html)

---

## Pygame

**Pygame** fue utilizado como la librería principal para la creación del entorno de Pac-Man, facilitando la implementación de gráficos, manejo de eventos y animaciones. Esta librería permitió la representación gráfica tanto de Pac-Man como de los fantasmas, junto con las interacciones entre ellos.

Para consultar la documentación y aprender a usar **Pygame**, se utilizaron los siguientes recursos:

- [Documentación oficial de Pygame](https://www.pygame.org/docs/)
- [Como usar Pygame para crear Pac-Man](https://pacmancode.com/maze-basics)

---

## Investigación y aprendizaje durante el proyecto

A lo largo del proyecto, se realizaron múltiples búsquedas para entender y adaptar la sintaxis de Python, así como para aplicar buenas prácticas de programación. Durante el desarrollo, se consultaron diferentes fuentes para obtener una comprensión más detallada de las herramientas utilizadas.

### Recursos consultados:

- [Documentación oficial de Python](https://docs.python.org/3/)
- [Modelo de datos en Python](https://docs.python.org/3/reference/datamodel.html#object.__eq__)
- [PEP 8 - Guía de estilo para código Python](https://peps.python.org/pep-0008/#programming-recommendations)
- [Uso de isinstance en Python](https://docs.python.org/3/library/functions.html#isinstance)
- [Funciones lambda en Python - GeeksforGeeks](https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/)
- [Operadores en Python - W3Schools](https://www.w3schools.com/python/python_operators.asp)

---

## Conclusiones

Este proyecto fue un gran ejemplo de cómo diferentes técnicas y herramientas pueden integrarse para crear comportamientos complejos en videojuegos. **A\*** resultó ser un algoritmo de búsqueda eficiente, mientras que el uso de **Q-Learning** permitió a los fantasmas aprender y mejorar sus decisiones. Además, Python y **Pygame** demostraron ser herramientas poderosas para el desarrollo de juegos 2D.
</details>

<details>
    <summary><h2>English</h2></summary>

## Introduction

This project implements the ghost logic in the Pac-Man game. We leveraged various tools, algorithms, and AI approaches—most notably **A\*** for efficient pathfinding and **Q-Learning** for decision-making and learning.

### Tools and Resources Used

- **Python**: Main language for project development.  
- **Pygame**: Library for 2D game development in Python.  
- **NumPy**: Library for high-performance multidimensional array operations.  
- **Q-Learning**: A reinforcement learning technique.  
- **Search & Learning Algorithms**: A\* and Q-Learning.  

---

## Search Algorithms

### A* (A-Star)

The **A\*** algorithm is renowned for efficiently finding optimal paths compared to algorithms like **Dijkstra**, **BFS**, or **DFS**. In this project, we adapted **A\*** to work within the ghosts’ movement logic—especially for computing efficient routes that allow them to catch Pac-Man or move to specific map positions.

We based our implementation on this resource:

- [A* Search Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/a-search-algorithm-in-python/)

We modified and fine-tuned the algorithm to meet the project’s particular needs, such as integrating with Pac-Man’s map nodes and avoiding obstacles.

### Comparison with Other Algorithms

We chose **A\*** because it finds the shortest path more efficiently when you only need a specific route:

- **Dijkstra**: Finds shortest paths from one node to all others, but is less efficient than **A\*** when you only need a single route.  
- **BFS (Breadth-First Search)**: Great for the smallest number of steps in unweighted graphs, but less efficient with weighted graphs.  
- **DFS (Depth-First Search)**: Not ideal for optimal pathfinding, especially in weighted graphs, compared to **A\*** and **BFS**.  

---

## Q-Learning

**Q-Learning** is a reinforcement learning technique we used to improve the ghosts’ decision-making in certain scenarios. By applying Q-Learning, ghosts can learn more complex strategies—like when to directly chase Pac-Man versus when to seek a shortcut.

For background and implementation guidance, we consulted:

- [Introduction to Q-Learning - EducaOpen](https://www.educaopen.com/digital-lab/blog/inteligencia-artificial/q-learning)  
- [Q-Learning Tutorial - DataCamp](https://www.datacamp.com/es/tutorial/introduction-q-learning-beginner-tutorial)  

### The Q-Learning Equation

The **Q-Learning** update rule lets an agent learn the expected future reward of taking action \(a\) in state \(s\). It’s given by:

\[
Q(s, a) \leftarrow Q(s, a) + \alpha \Bigl[\,r + \gamma \max_{a'} Q(s', a') - Q(s, a)\Bigr]
\]

where:

- \( Q(s, a) \): Current Q-value for state \(s\) and action \(a\).  
- \( \alpha \): Learning rate—how much new information overrides old.  
- \( r \): Reward received after taking action \(a\) in state \(s\).  
- \( \gamma \): Discount factor—how much future rewards are valued.  
- \( \max_{a'} Q(s', a') \): Maximum expected Q-value for the next state \(s'\) over all possible actions \(a'\).  

---

## NumPy

**NumPy** is essential in Python for handling multidimensional arrays and high-speed math operations. In this project, NumPy made it possible to implement efficient calculations—like distance norms and Q-table manipulations—in real time.

### NumPy Features Used

1. **Array Creation & Data Handling**  
   - `np.zeros()`: Initialize the Q-table with zeros, giving a clean slate for learning ghost behaviors.  
   - `np.argmax()`: Select the best action from the Q-table, letting ghosts make strategy choices based on prior experience.  

2. **Distance Computations**  
   - `np.linalg.norm()`: Measure the Euclidean distance between ghosts and Pac-Man, improving reward accuracy in the Q-Learning model.  

### Documentation & Resources

For more on NumPy, check out:

- [Official NumPy Documentation](https://numpy.org/doc/stable/)  

NumPy’s efficiency was key to real-time decision-making and learning in our ghost AI.

---

## Data Structures in Python

Efficient data structures were vital for implementing nodes, graphs, and other game elements. Python’s built-in structures—like lists, dictionaries, and sets—made it straightforward to model the Pac-Man maze.

- [Python Data Structures Tutorial](https://docs.python.org/es/dev/tutorial/datastructures.html)  

---

## Pygame

We used **Pygame** to create the Pac-Man environment, handling graphics, events, and animations. It provided an easy way to render Pac-Man, the ghosts, and the maze, as well as detect collisions and user input.

- [Pygame Official Documentation](https://www.pygame.org/docs/)  
- [Using Pygame to Build Pac-Man](https://pacmancode.com/maze-basics)  

---

## Research & Learning During the Project

Throughout development, we researched best practices in Python syntax and coding style. We dove into various resources to deepen our understanding and ensure clean, maintainable code.

### Resources Consulted

- [Python 3 Official Docs](https://docs.python.org/3/)  
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html#object.__eq__)  
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/#programming-recommendations)  
- [Using `isinstance` in Python](https://docs.python.org/3/library/functions.html#isinstance)  
- [Anonymous Functions (lambda) in Python - GeeksforGeeks](https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/)  
- [Operators in Python – W3Schools](https://www.w3schools.com/python/python_operators.asp)  

---

## Conclusions

This project highlights how different techniques and tools can combine to create sophisticated behaviors in video games. **A\*** proved to be an efficient pathfinding algorithm, while **Q-Learning** enabled ghosts to learn and refine their strategies. Moreover, Python and **Pygame** showcased their power for building real-time 2D games.

</details>