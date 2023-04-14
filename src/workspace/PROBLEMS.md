# Problem 1

$$\max_{z} = 4 x_1 + 3x_2$$

$$s.t.$$

$$x_1 + x_2 \leq 40$$

$$2x_1 + x_2 \leq 60$$

$$x_1, x_2 \geq 0$$


# Problem 2
A company receives three project demands. The completion of each project requires three types of skilled labor: project management, data modeling, and data science. The amount of each resource needed to achieve each type of project is given in the table below:

| Skill | Project 1 (P1) | Project 2 (P2) | Project 3 (P3) | Total per skill |
| - | - | - | - | - |
| Project management | 18 | 23 | 15 | 56 |
| Data modeling  | 4 | 0 | 20 | 24 |
| Data science | 12 | 30 | 40 | 82 |
| Total per project | 34 | 53 | 75 | 162 |

This matrix is formed by a binary matrix and a quantities' matrix:
```python
skill_per_project = np.array([[1, 1, 1],
                              [1, 0, 1],
                              [1, 1, 1]])
skill_per_project_plan = np.array([[18, 23, 15],
                                    [4, 0, 20],
                                    [12, 30, 100]])

>>> skill_per_project * skill_per_project_plan
array([[ 18,  23,  15],
       [  4,   0,  20],
       [ 12,  30, 100]])
```

Suppose that the timeframe is a quarter. A quarter has 60 business days (5 business days × 4 weeks per month × 3 months) of 8 hours.

The activity rate, or the participation, of each resource pool is:

| Ressource | Participation | Availability in days |
| - | - | - |
| John Doe | 100% | 60 |
| Sponge Bob | 80% | 48 |
| Cute Pandas | 100% | 60 |
| Total | 280% | 168 |

Their skills are: 

| Ressource | Project management  | Data modeling | Data science |
| - | - | - | - |
| John Doe | 1 | 0 | 1 |
| Sponge Bob | 0 | 1 | 0 |
| Cute Pandas | 0 | 0 | 1 |

These tables above can be represented as matrices:
```python
import numpy as np
import pandas as pd
import pyomo.environ as pyo
from pyomo.opt import SolverFactory


if __name__ == "__main__":
    days_in_a_quarter: int = 60

    skill_per_project = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]])

    skill_per_project_plan = np.array([[18, 23, 15],
                                       [4, 0, 20],
                                       [12, 30, 100]])

    skill_per_person = np.array([[1, 0, 1],
                                 [0, 1, 0],
                                 [0, 0, 1]])

    participation = np.array([1, 0.8, 1])

    capacity_per_person = participation * days_in_a_quarter
    # array([60., 48., 60.])

    capacity_per_skill = np.sum(capacity_per_person * skill_per_person, axis=0)
    # array([ 60.,  48., 120.])
```

Project 1 has priority 3 (highest), project 2 has priority 1, and project 3 has priority 2.

## Sets

```python
# Model instantiation
model_1 = pyo.ConcreteModel()

# Sets
projects: list[str] = ["P1", "P2", "P3"]
model_1.projects = pyo.Set(initialize=projects)

skills: list[str] = ["project_management", "data_modeling", "data_science"]
model_1.skills = pyo.Set(initialize=skills)

collaborators: list[str] = ["John Doe", "Sponge Bob", "Cute Pandas"]
model_1.collaborators = pyo.Set(initialize=collaborators)
```

What is the best resource allocation?

We want to maxime the number of projects wrt to their priority and the ressources available.

Our decision variables are: 
* $x_1$ project 1
* $x_2$ project 2
* $x_3$ project 3

The objective function is 
$$\max 3x_1 + 1x_2 + 2x_3$$


$$s.t.$$
$$x_i={0, 1}$$


## Constraints

### The human capacity or capacity per collaborator
When performing the allocation plan, we have to bear in mind that a collaborator cannot exceed their total capacity, $\kappa$. The total capacity for each collaborator is:

| Ressource | Participation | Availability in days |
| - | - | - |
| John Doe | 100% | 60 |
| Sponge Bob | 80% | 48 |
| Cute Pandas | 100% | 60 |

And can be represented as a vector $h=[60, 48, 60]$.

The constraints therefore are:
$$\kappa \cdot x \leq h$$
Where,
* $\kappa$ is the human days allocated to each project, in our case it is a $3 \times 3$ matrix;
* $x$ is the projects' vector of $3 \times 1$.

<!-- We also notice that $\kappa$ is a **decision variable** (i.e., optimisation vairable). It is what we want to calculate. -->

### Total allocable HD per skill
Moreover, we cannot exceed 60HD of project management, 48HD of data modeling, and 120HD of data science. This information is known beforehand. This is why can formulate parameters:
```python
skill_per_project_plan_df = pd.DataFrame(data=skill_per_project_plan.T, columns=skills, index=projects)

#     project_management  data_modeling  data_science
# P1                  18              4            12
# P2                  23              0            30
# P3                  15             20           100

skill_per_project_plan_dict = skill_per_project_plan_df.to_dict(orient="dict")

# {'project_management': {'P1': 18, 'P2': 23, 'P3': 15}, 
#  'data_modeling': {'P1': 4, 'P2': 0, 'P3': 20},
#  'data_science': {'P1': 12, 'P2': 30, 'P3': 100}}

model_1.project_management = pyo.Param(model_1.projects, initialize=skill_per_project_plan_dict["project_management"])

model_1.data_modeling = pyo.Param(model_1.projects, initialize=skill_per_project_plan_dict["data_modeling"])

model_1.data_science = pyo.Param(model_1.projects, initialize=skill_per_project_plan_dict["data_science"])
```

```python
import numpy as np


if __name__ == "__main__":
    skills_matrix = np.array([[1, 0, 1],
                              [0, 1, 0],
                              [0, 0, 1]])
    capacity_per_person = np.array([60, 48, 60])
    capacity_per_skill = np.sum(capacity_per_person * skills_matrix, axis=0)
    print(f"The total allocable project management number of days: {capacity_per_skill[0]}")
    print(f"The total allocable data modeling number of days: {capacity_per_skill[1]}")
    print(f"The total allocable data science number of days: {capacity_per_skill[2]}")
```

Outputs:
```console
The total allocable project management number of days: 60
The total allocable data modeling number of days: 48
The total allocable data science number of days: 120
```

However, as we observe this does not respect the total capacity, which is $168$ days for the quarter. This means that 

$$18x_1 + 23x_2 + 15x_3 \leq 60$$
$$4x_1 + 0x_2 + 20x_3 \leq 48$$
$$12x_1 + 30x_2 + 40x_3 \leq 120$$
$$(18x_1 + 23x_2 + 15x_3) + (4x_1 + 0x_2 + 20x_3) + (12x_1 + 30x_2 + 40x_3) \leq 168 $$

Nonetheless, this way of formulating the problem is not professional.

Let $x$ be the vector of projects, where $x_i$ represents the $i$-th project.

Let $I \in \mathbb{N}$ be the set of projects a business wants to complete. In our case, $I={1, 2, 3}$.

The business wants to maximize the number of projects done with respect to its human resources:

$$\max_x \sum_{i \in I} \pi_i \mathbf{1}_{x_i \gt 0} = \mathbf{\pi}^\top\cdot\mathbf{1}_{\mathbf{x}\gt 0}$$

$$s.t.$$

$$\mathbf{\theta}\cdot\mathbf{1}_{x_i \gt 0} \leq \phi$$
$$\mathbf{\theta}\cdot\mathbf{1}_{x_i \gt 0}\cdot\mathbf{1}^\top \leq 168$$

where, 
* $\pi_i$ is the "profit" coming from the $i$-th project; this implies that $\mathbf{\pi}$ is the vector of profits
* $\mathbf{1}_{x_i \gt 0}$ a binary of having completed project $i$; this yiels a vector like this: $[1, 0, 1]$, where the second value means that the second project has not been completed
* $\mathbf{\theta}$ is the vector of costs of the projects in terms of human days, e.g., $[30, 55, 9]$

If we run the program, we obtain:
```consol
Objective function achieved a score of 6.0
P1 = 1.0
P2 = 1.0
P3 = 1.0
```

The score of 6 means that we completed all the projects with respective priorisation 3 + 1 + 2 = 6.

If we change the data science effort of Project 3 from 40 to 90, we know that we will have to sacrifice a project since we would account 132 human days. And as we know, we can allocate maximum 120 human days of data science. Moreover, in such a case, we would not be able to have a project manager.

In such a casem the program tells us:
```consol
Objective function achieved a score of 5.0
P1 = 1.0
P2 = 0.0
P3 = 1.0
```

We observe that the prioritisation has been respected (otherwise we would have had 4 instead of 5 in the objective function).

Therefore, this quarter we would have allocated:

```shell
The allocation would be:
                      P1   P2     P3
project_management  18.0  0.0   15.0
data_modeling        4.0  0.0   20.0
data_science        12.0  0.0  100.0
```

But we missed something because the following allocation implies that Cute Pandas works 60HD, but John Doe 85HD (= 18 as project manager on P1 + 15 as project manager on P3 + (112 - 60) as data scientist on P3) whilst he should work 60 maximum.
```shell
project_management     33.0
data_modeling          24.0
data_science          112.0
```

Project's matrix
Sponge Bob's matrix
| Skill | Project 1 (P1) | Project 2 (P2) | Project 3 (P3)
| - | - | - | - |
| Project management | 1 | 1 | 1 | 
| Data modeling  | 1 | 0 | 1 | 
| Data science | 1 | 1 | 1 | 

John Doe's matrix
| Skill | Project 1 (P1) | Project 2 (P2) | Project 3 (P3)
| - | - | - | - |
| Project management | 1 | 1 | 1 | 
| Data modeling  | 0 | 0 | 0 | 
| Data science | 1 | 1 | 1 |

Sponge Bob's matrix
| Skill | Project 1 (P1) | Project 2 (P2) | Project 3 (P3)
| - | - | - | - |
| Project management | 0 | 0 | 0 | 
| Data modeling  | 1 | 0 | 1 | 
| Data science | 0 | 0 | 0 | 

Cuta Pandas' matrix
Sponge Bob's matrix
| Skill | Project 1 (P1) | Project 2 (P2) | Project 3 (P3)
| - | - | - | - |
| Project management | 0 | 0 | 0 | 
| Data modeling  | 0 | 0 | 0 | 
| Data science | 1 | 1 | 1 |

Can we map capacity to the persons?

