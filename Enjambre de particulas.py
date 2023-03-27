import numpy as np
import matplotlib.pyplot as plt

def ackley(x):
    a = 20
    b = 0.2
    c = 2 * np.pi
    d = len(x)
    sum1 = sum([xi**2 for xi in x])
    sum2 = sum([np.cos(c*xi) for xi in x])
    return -a*np.exp(-b*np.sqrt(sum1/d)) - np.exp(sum2/d) + a + np.exp(1)

class Particle:
    def __init__(self, x0):
        self.position = x0
        self.velocity = np.zeros_like(x0)
        self.best_position = x0
        self.best_score = float('inf')

    def update_velocity(self, w, c1, c2, global_best_position):
        r1 = np.random.rand(len(self.position))
        r2 = np.random.rand(len(self.position))
        self.velocity = w*self.velocity + c1*r1*(self.best_position - self.position) + c2*r2*(global_best_position - self.position)

    def update_position(self):
        self.position = self.position + self.velocity

    def evaluate(self, cost_func):
        self.score = cost_func(self.position)
        if self.score < self.best_score:
            self.best_score = self.score
            self.best_position = self.position

class ParticleSwarmOptimizer:
    def __init__(self, cost_func, x0, n_particles, n_iterations, w, c1, c2):
        self.cost_func = cost_func
        self.n_iterations = n_iterations
        self.n_particles = n_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.global_best_score = float('inf')
        self.particles = []
        for i in range(self.n_particles):
            particle = Particle(x0)
            self.particles.append(particle)
            if particle.best_score < self.global_best_score:
                self.global_best_score = particle.best_score
                self.global_best_position = particle.best_position
        self.best_scores = []

    def optimize(self):
        for i in range(self.n_iterations):
            for particle in self.particles:
                particle.evaluate(self.cost_func)
                if particle.best_score < self.global_best_score:
                    self.global_best_score = particle.best_score
                    self.global_best_position = particle.best_position

                self.best_scores.append(self.global_best_score)

            for particle in self.particles:
                particle.update_velocity(self.w, self.c1, self.c2, self.global_best_position)
                particle.update_position()
            self.best_scores.append(self.global_best_score)

        return self.global_best_position, self.global_best_score, self.best_scores


x0 = np.random.uniform(-32.768, 32.768, (2,))
n_particles = 20
n_iterations = 1000
w = 0.5
c1 = 1
c2 = 1

optimizer = ParticleSwarmOptimizer(ackley, x0, n_particles, n_iterations, w, c1, c2)
best_position, best_score, best_scores = optimizer.optimize()

print('Best position:', best_position)
print('Best score:', best_score)
plt.plot(best_scores)
plt.xlabel('Iteration')
plt.ylabel('Best score')
plt.show()

