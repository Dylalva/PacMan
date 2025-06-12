import random
import numpy as np
"""
La clase implementa el modelo de Q-learning, un método de aprendizaje por refuerzo que permite a un agente aprender
una política óptima a través de la exploración y la explotación de recompensas acumuladas.

Q-learning utiliza una tabla Q (matriz de valores) que almacena el valor esperado de cada acción en cada estado.
El agente aprende iterativamente actualizando estos valores Q en función de la recompensa inmediata y el valor futuro
estimado, lo cual ayuda al agente a elegir las mejores acciones.

Problemas y Limitaciones del Modelo:
- Requiere de mucho almacenamiento: Cada estado y acción posibles deben almacenarse, lo cual puede ser muy
  costoso en problemas con grandes espacios de estado y acción.
- Exploración vs. Explotación: El modelo utiliza técnicas como epsilon-greedy para balancear la exploración de
  nuevas acciones con la explotación de acciones conocidas.
  
Librerías utilizadas:
- Numpy: Para manejar eficientemente los cálculos de matrices y probabilidades.
- Random: Para la implementación de la exploración aleatoria.

Recursos utilizados para la implementación de este modo de entrenamiento:
https://www.geeksforgeeks.org/epsilon-greedy-algorithm-in-reinforcement-learning/
https://www.geeksforgeeks.org/q-learning-in-python/
"""

class QLearning:
    def __init__(self, state_size, action_size, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = {}

    def initialize_state(self, state):
        """Inicializar las acciones para un estado si aún no está en q_table"""
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_size)


    def choose_action(self, state):
        """Metodo epsilon-greedy para elegir una acción: explorar o explotar
           Este metodo se realizo en base a: https://www.geeksforgeeks.org/epsilon-greedy-algorithm-in-reinforcement-learning/"""
        self.initialize_state(state)  # Asegurar que el estado esté en la tabla
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.action_size - 1)  # Explorar
        else:
            return np.argmax(self.q_table[state])  # Explotar

    def update_q_table(self, state, action, reward, next_state):
        """Actualiza la tabla Q usando la ecuación de Q-Learning"""
        self.initialize_state(state)       # Asegurar que el estado actual exista
        self.initialize_state(next_state)  # Asegurar que el siguiente estado exista
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

    def get_q_table(self):
        return self.q_table
