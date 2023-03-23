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
$$\max z = \sum_{i \in I} \theta_i x_i$$
where, $\theta_i$ is the ROI of the project and $x_i$ a binary of having completed project $i$.
