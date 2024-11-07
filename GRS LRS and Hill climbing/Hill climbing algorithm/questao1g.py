import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def perturb(x, e):
    perturbed_value = np.random.uniform(low=x-e, high=x+e)
    return np.clip(perturbed_value, 0, np.pi,)

def f(x, y):
    return -np.sin(x) * np.sin(x**2 / np.pi)**(2 * 10) - np.sin(y) * np.sin(2 * y**2 / np.pi)**(2 * 10)

fig = plt.figure()
fg = fig.add_subplot(111, projection='3d')

x_values = np.linspace(0, np.pi, 100)
y_values = np.linspace(0, np.pi, 100)
Graphx, graphy = np.meshgrid(x_values, y_values)

fg.plot_surface(Graphx, graphy, f(Graphx, graphy), cmap='viridis', alpha=0.6)

e = 0.1
max_it = 10000
max_viz = 20
num_runs = 100
f_opt_values = []
x_opt_values = []

for run in range(num_runs):
    x_opt = [0, 0]
    f_opt = f(x_opt[0], x_opt[1])
    
    melhoria = True
    i = 0
    while i < max_it and melhoria:
        melhoria = False
        for j in range(max_viz):
            x_cand = [perturb(x_opt[0], e), perturb(x_opt[1], e)]
            f_cand = f(x_cand[0], x_cand[1])
            if f_cand < f_opt:
                x_opt = x_cand
                f_opt = f_cand
                melhoria = True
                break
        i += 1
    
    fg.scatter(x_opt[0], x_opt[1], f_opt, color='r', s = 20)
    f_opt_values.append(round(f_opt, 3))
    x_opt_values.append(x_opt)

modal_f_opt, modal_count = Counter(f_opt_values).most_common(1)[0]

for i in range(len(f_opt_values)):
    if f_opt_values[i] == modal_f_opt:
        modal_x_opt = x_opt_values[i][0]
        modal_y_opt = x_opt_values[i][1]
        break


fg.scatter(modal_x_opt, modal_y_opt, modal_f_opt, color='b', s=60)
fg.set_xlabel('x')
fg.set_ylabel('y')
fg.set_zlabel('z')
fg.set_title(f'Valor modal de f(x,y) = {modal_f_opt} (em azul) (apareceu {modal_count} vezes)')

plt.show()
