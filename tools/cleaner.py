import os
import re

def remove_comments(code):
    # 1. Supprime les commentaires multi-lignes (''' ou """)
    code = re.sub(r'(""".*?"""|\'\'\'.*?\'\'\')', '', code, flags=re.DOTALL)
    # 2. Supprime les commentaires mono-ligne (#)
    # On fait attention de ne pas supprimer les # à l'intérieur de chaînes de caractères
    code = re.sub(r'#.*', '', code)
    # 3. Nettoie les lignes vides superflues laissées par les commentaires
    code = os.linesep.join([line for line in code.splitlines() if line.strip()])
    return code

def clean_project(directory):
    # Liste des dossiers à ignorer pour ne pas casser le projet ou Git
    ignore_dirs = {'.git', '__pycache__', 'assets', 'data'}
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if file.endswith(".py") and file != "cleaner.py":
                file_path = os.path.join(root, file)
                print(f"Nettoyage de : {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                clean_content = remove_comments(content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(clean_content)

if __name__ == "__main__":
    # On remonte d'un cran pour nettoyer tout le projet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    confirm = input(f"Voulez-vous supprimer TOUS les commentaires dans {project_root} ? (y/n) : ")
    if confirm.lower() == 'y':
        clean_project(project_root)
        print("Terminé !")