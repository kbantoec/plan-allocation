import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.lamas = pyo.Var(within=pyo.NonNegativeReals)
model.goats = pyo.Var(within=pyo.NonNegativeReals)

model.maximizeProfit = pyo.Objective(expr=200*model.lamas + 300 * model.goats, sense=pyo.maximize)

# The farmer has only 100 hours
model.LaborConstraint = pyo.Constraint(expr=3*model.lamas + 2*model.goats <= 100)
# The farmer has only 120 bucks for medical services
model.MedicalConstraint = pyo.Constraint(expr=2*model.lamas + 4 * model.goats <= 120)
# Acres: The farmer has only 45 acres
model.LandConstraint = pyo.Constraint(expr=model.lamas + model.goats <= 45)

# Solve the model
optimizer = pyo.SolverFactory("glpk")
optimizer.solve(model)
model.display()
