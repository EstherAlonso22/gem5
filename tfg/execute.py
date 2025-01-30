import subprocess

def execute_gem5():
    command = [
        'build/X86/gem5.opt',
        '-re',
        '--outdir=tfg/out/O3boardv1',
        'tfg/configs/configO3board.py'
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Execution successful")
    else:
        print("Execution failed")

if __name__ == "__main__":
    execute_gem5()