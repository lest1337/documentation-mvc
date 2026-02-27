import os
from mkdocs.commands.serve import serve


def main():
    os.chdir("mvc-doc")
    
    # http://localhost:8000
    serve(config_file="mkdocs.yml")
    print ("Documentation MVC is running at http://localhost:8000")


if __name__ == "__main__":
    main()
