import venv
import subprocess
import os

def create_venv():
    venv.create('venv', with_pip=True)



def setup_env_variables():
    with open('.env', 'w') as f:
        f.write('ANTHROPIC_API_KEY=your_api_key_here\n')

def create_test_data_folder():
    os.makedirs('test_data', exist_ok=True)

def main():
    create_venv()
    setup_env_variables()
    create_test_data_folder()
    print("Local environment setup complete!")

if __name__ == "__main__":
    main()