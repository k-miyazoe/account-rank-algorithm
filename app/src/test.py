from simulation import Simulation

def main():
    simulation_instance = Simulation()
    simulation_result = simulation_instance.calculate_msc_purchase()
    simulation_instance.create3dGrapf(simulation_result,"理想状態",'r',"理想状態のグラフ.png")
    
if __name__ == '__main__':
    main()
    