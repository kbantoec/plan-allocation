# Problem 1

$$\max_{z} = 4 x_1 + 3x_2$$

$$s.t.$$

$$x_1 + x_2 \leq 40$$

$$2x_1 + x_2 \leq 60$$

$$x_1, x_2 \geq 0$$


# Problem 2
A company receives three project demands. The completion of each project requires three types of skilled labor: project management, data modeling, and data science. The amount of each resource needed to achieve each type of project is given in the table below:

| Resource | Project 1 (P1) | Project 2 (P2) | Project 3 (P3) |
| - | - | - | - |
| Project management | 8 | | |




Let $x$ be the vector of projects, where $x_i$ represents the $i$-th project.

Let $I \in \mathbb{N}$ be the set of projects a business wants to complete. 

The business wants to maximize the number of projects done with respect to its human resources:

$$\max z = \sum_{i \in I} \pi_i \mathbf{1}_{x_i \gt 0} = \mathbf{\pi}^\top\cdot\mathbf{1}_{\mathbf{x}\gt 0}$$

$$s.t.$$

$$\mathbf{\theta}\cdot\mathbf{x}$$

where, 
* $\pi_i$ is the "profit" coming from the $i$-th project; this implies that $\mathbf{\pi}$ is the vector of profits
* $\mathbf{1}_{x_i \gt 0}$ a binary of having completed project $i$; this yiels a vector like this: $[1, 0, 1]$, where the second value means that the second project has not been completed
* $\mathbf{\theta}$ is the vector of costs of the projects in terms of human days, e.g., $[30, 55, 9]$
