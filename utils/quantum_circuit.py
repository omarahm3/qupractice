from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.result import Result
from qiskit_aer import AerSimulator

def prepare_state(state: str, label: str):
    qc = QuantumCircuit(len(state))

    # prepare information state for Alice
    for i in range(len(state)):
        if state[i] == "1":
            qc.x(i)

    return qc.to_gate(label=label)


def get_state_vector(qc: QuantumCircuit) -> Statevector:
    return Statevector.from_instruction(qc)

def simulate(qc: QuantumCircuit) -> Result:
    backend = AerSimulator()
    qc_aer = transpile(qc, backend)
    return backend.run(qc_aer, shots=8192).result()

def draw_state(state: Statevector, no_amp = True):
    state = state.reverse_qargs()

    if not no_amp:
        return state.draw('latex', max_size=2**5)

    from IPython.display import Latex
    basis_states = []
    for i in range(len(state)):
        if abs(state[i]) > 1e-10:
            basis = format(i, f'0{state.num_qubits}b')
            sign = '+' if state[i].real > 0 else '-'
            basis_states.append(f"{sign}|{basis}\\rangle")
    latex_str = ' '.join(basis_states).replace('+-', '-')
    return Latex(f"${latex_str}$")

def calculate_fidelity(state1: Statevector, state2: Statevector) -> float:
    return float("{:.20f}".format(state_fidelity(state1, state2)))