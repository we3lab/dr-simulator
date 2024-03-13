import marimo

__generated_with = "0.1.58"
app = marimo.App()


@app.cell
def __():
    import marimo as mo

    from dr_simulator.dr_events import DemandResponseEvents as dr_eve
    return dr_eve, mo


@app.cell
def __(mo):
    mo.md(
        f"""
    ### Welcome to Demand Response Events Simulator

    Incentive based Demand Response programs are voluntary programs offered to residential, commercial, and industrial customer. The participants are offered financial incentives if they voluntarily reduce loads during stressful times for the grid, which are notified as DR events. There are different flavors of these DR programs across the country, with different rules that constitute when the events are called, how often they are called, the duration of these calls and much more. The DR Simulator tool uses various program and simulation parameters to model these incentive-based demand response programs across the country. This enables the user to configure any DR programs from any ISOs and simulate DR events once they provide the simulation parameters based on historical distribution or based on a custom distribution.

    Use this package to simulate any incentive based demand response events for a custom distribution or distribution learned from historic demand response events.

    Essentially you need to set two types of parameters

    1. Program Parameters
    2. Simulation Parameters
        
        """
    )
    return


if __name__ == "__main__":
    app.run()
