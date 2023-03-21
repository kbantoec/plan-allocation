import pyomo.environ as pyo
from pyomo.opt import SolverStatus, TerminationCondition

model = pyo.ConcreteModel()

model.x_1 = pyo.Var(within=pyo.NonNegativeIntegers)
model.x_2 = pyo.Var(within=pyo.NonNegativeIntegers)
model.obj = pyo.Objective(expr=model.x_1 + 2 * model.x_2)
model.con1 = pyo.Constraint(expr=3 * model.x_1 + 4 * model.x_2 >= 1)
model.con2 = pyo.Constraint(expr=2 * model.x_1 + 5 * model.x_2 >= 2)

solver = pyo.SolverFactory("glpk")
res = solver.solve(model, load_solutions=False)

if (res.solver.status == SolverStatus.ok) and (res.solver.termination_condition == TerminationCondition.optimal):
    model.solutions.load_from(res)
else:
    print("Solve failed.")

model.display()
