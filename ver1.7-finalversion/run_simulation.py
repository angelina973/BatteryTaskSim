import pybamm

def run_simulation(model, param, experiments):
    try:
        print("Running Simulation with Experiments:")
        print(experiments)
        experiment_steps = [
            f"Discharge at {power} W for {duration} hours"
            for power, duration in experiments
        ]
        experiment = pybamm.Experiment(experiment_steps)

        sim = pybamm.Simulation(model, experiment=experiment, parameter_values=param)
        solution = sim.solve()

        return solution, sim.parameter_values
    except Exception as e:
        print(f"Simulation failed: {e}")
        return None, None


