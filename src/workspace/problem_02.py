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

    capacity_per_person = participation * days_in_a_quarter  # array([60., 48., 60.])
    capacity_per_skill = np.sum(capacity_per_person * skill_per_person, axis=0)  # array([ 60.,  48., 120.])
    print(f"The total allocable project management number of days: {capacity_per_skill[0]}")
    print(f"The total allocable data modeling number of days: {capacity_per_skill[1]}")
    print(f"The total allocable data science number of days: {capacity_per_skill[2]}")

    capacity_per_person @ np.ones(3)  # 168

    # Model instantiation
    model_1 = pyo.ConcreteModel()

    # Sets
    projects: list[str] = ["P1", "P2", "P3"]
    projects_priority: list[int] = [3, 1, 2]
    model_1.projects = pyo.Set(initialize=projects)

    skills: list[str] = ["project_management", "data_modeling", "data_science"]
    model_1.skills = pyo.Set(initialize=skills)  # Added the 4/4/2023

    collaborators: list[str] = ["John Doe", "Sponge Bob", "Cute Pandas"]
    model_1.collaborators = pyo.Set(initialize=collaborators)

    # Parameters
    skill_per_project_plan_df = pd.DataFrame(data=skill_per_project_plan.T, columns=skills, index=projects)
    skill_per_project_plan_dict = skill_per_project_plan_df.to_dict(orient="dict")
    model_1.project_management = pyo.Param(model_1.projects, initialize=skill_per_project_plan_dict["project_management"])
    model_1.data_modeling = pyo.Param(model_1.projects, initialize=skill_per_project_plan_dict["data_modeling"])
    model_1.data_science = pyo.Param(model_1.projects, initialize=skill_per_project_plan_dict["data_science"])

    skill_per_project_df = pd.DataFrame(data=skill_per_project, columns=skills, index=projects)
    skill_per_person_df = pd.DataFrame(data=skill_per_person, columns=skills, index=collaborators)
    collaborators_per_project_matrices = {}
    for c in collaborators:
        collab = skill_per_person_df.loc[c].to_numpy() * skill_per_project
        collaborators_per_project_matrices[c] = pd.DataFrame(data=collab, columns=skills, index=projects).T

    # todo: check
    # skill_per_person_df = pd.DataFrame(data=skill_per_person.T, columns=skills, index=collaborators)
    # skill_per_person_dict = skill_per_person_df.to_dict(orient="dict")
    # model_1.john = pyo.Param(model_1.collaborators, initialize=skill_per_person_dict["project_management"])
    # model_1.bob = pyo.Param(model_1.collaborators, initialize=skill_per_person_dict["data_modeling"])
    # model_1.cute = pyo.Param(model_1.collaborators, initialize=skill_per_person_dict["data_science"])

    # person_per_project_df = pd.DataFrame(data=skill_per_person, columns=projects, index=collaborators)
    # person_per_project_dict = person_per_project_df.to_dict(orient="dict")
    # model_1.john = pyo.Param(model_1.collaborators, initialize=skill_per_person_dict["project_management"])
    # model_1.bob = pyo.Param(model_1.collaborators, initialize=skill_per_person_dict["data_modeling"])
    # model_1.cute = pyo.Param(model_1.collaborators, initialize=skill_per_person_dict["data_science"])

    model_1.priority = pyo.Param(model_1.projects, initialize=dict(zip(projects, projects_priority)))

    # model_1.priority.display()

    # Decision variable
    model_1.x = pyo.Var(model_1.projects, within=pyo.NonNegativeIntegers)

    # Objective function
    def objective_callback(model: pyo.Model):
        return sum(model.priority[project] * model.x[project] for project in model.projects)

    model_1.objective_func = pyo.Objective(rule=objective_callback, sense=pyo.maximize)

    # Constraints
    def project_management_constraint_callback(model: pyo.Model, i):
        return sum(model.project_management[p] * model.x[p] for p in model.projects) <= capacity_per_skill[0]

    def data_modeling_constraint_callback(model: pyo.Model, i):
        return sum(model.data_modeling[p] * model.x[p] for p in model.projects) <= capacity_per_skill[1]

    def data_science_constraint_callback(model: pyo.Model, i):
        # return sum(model.data_science[project] * model.x[project]) <= capacity_per_skill[2]
        return sum(model.data_science[p] * model.x[p] for p in model.projects) <= capacity_per_skill[2]

    # todo
    def john_doe_constraint_callback(model: pyo.Model, collaborator):
        return sum(model.john[c] for c in model.collaborators) <= capacity_per_person[0]

    def project_outcome_constraint_callback(model: pyo.Model, project):
        return model.x[project] <= 1

    # def p1_outcome_constraint_callback(model: pyo.Model, p):
    #     return model.x["P1"] <= 1
    #
    # def p2_outcome_constraint_callback(model: pyo.Model, p):
    #     return model.x["P2"] <= 1
    #
    # def p3_outcome_constraint_callback(model: pyo.Model, p):
    #     return model.x["P3"] <= 1

    # Skill constraint
    model_1.project_management_constraint = pyo.Constraint(model_1.projects, rule=project_management_constraint_callback)
    model_1.data_modeling_constraint = pyo.Constraint(model_1.projects, rule=data_modeling_constraint_callback)
    model_1.data_science_constraint = pyo.Constraint(model_1.projects, rule=data_science_constraint_callback)

    # Capacity per collaborator constraint
    model_1.john_constraint = pyo.Constraint(model_1.projects, rule=john_doe_constraint_callback)

    # Outcome constraint
    model_1.project_outcome_constraint = pyo.Constraint(model_1.projects, rule=project_outcome_constraint_callback)
    # model_1.p1_outcome_constraint = pyo.Constraint(model_1.projects, rule=p1_outcome_constraint_callback)
    # model_1.p2_outcome_constraint = pyo.Constraint(model_1.projects, rule=p2_outcome_constraint_callback)
    # model_1.p3_outcome_constraint = pyo.Constraint(model_1.projects, rule=p3_outcome_constraint_callback)

    # Solve
    solver = SolverFactory("glpk")
    results = solver.solve(model_1)

    model_1.display()

    print(results)

    print(f"Objective function achieved a score of {model_1.objective_func()}")

    for project in model_1.projects:
        print(f"{project} = {model_1.x[project]()}")

    allocation_per_project = skill_per_project_plan * np.array(list(model_1.x.get_values().values()))
    allocation_per_project_df = pd.DataFrame(data=allocation_per_project, columns=projects, index=skills)

    print("The allocation would be:")
    print(allocation_per_project_df)
    print(allocation_per_project_df.sum(axis=1))

