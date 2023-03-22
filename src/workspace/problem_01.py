import pyomo.environ as pyo
from pyomo.opt import SolverFactory


if __name__ == "__main__":

    # Model definition
    model = pyo.ConcreteModel(name="Belt manufacturer profit maximization.")

    # Decision variables' definition
    model.x1 = pyo.Var(within=pyo.NonNegativeReals)
    model.x2 = pyo.Var(within=pyo.NonNegativeReals)

    x1 = model.x1
    x2 = model.x2

    # Objective function defition
    model.Obj = pyo.Objective(expr=(4 * x1) + (3 * x2), sense=pyo.maximize)
    
    # Constrains' definition
    model.Constraint_1 = pyo.Constraint(expr=x1 + x2 <= 40)
    model.Constraint_2 = pyo.Constraint(expr=2 * x1 + x2 <= 60)

    optimizer = SolverFactory("glpk")
    results = optimizer.solve(model)

    # Display the results
    print(results)
    print(f"The objective function = {model.Obj()}")
    print(f"x1 = {model.x1()}")
    print(f"x2 = {model.x2()}")
